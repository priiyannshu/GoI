import type { ExamRecord } from '../types/profile';
import { indexedDbStorage } from './indexedDbStorage';

const API_BASE = '/api/v1';

export async function fetchExamsList(): Promise<ExamRecord[]> {
  // 1. Try local IndexedDB cache first
  try {
    const cached = await indexedDbStorage.getCachedExams();
    if (cached && cached.length >= 36) {
      // Background revalidate if online
      if (typeof navigator !== 'undefined' && navigator.onLine) {
        revalidateExams().catch(() => {});
      }
      return cached;
    }
  } catch {
    // Continue to network
  }

  // 2. Network fetch
  try {
    const res = await fetch(`${API_BASE}/exams`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const json = await res.json();
    const list: ExamRecord[] = json.data || json.exams || json;
    if (Array.isArray(list) && list.length > 0) {
      await indexedDbStorage.cacheExams(list);
      return list;
    }
  } catch (error) {
    console.warn('Network request failed, falling back to local static catalog:', error);
  }

  // 3. Fallback to imported static JSON
  try {
    const local = await import('../../../data/grade_a_exams.json');
    const exams = (local.exams || (local as any).default?.exams || []) as ExamRecord[];
    if (exams.length > 0) {
      await indexedDbStorage.cacheExams(exams);
      return exams;
    }
  } catch (e) {
    console.warn('Failed to load static JSON catalog fallback:', e);
  }

  return [];
}

async function revalidateExams(): Promise<void> {
  const res = await fetch(`${API_BASE}/exams`);
  if (res.ok) {
    const json = await res.json();
    const list: ExamRecord[] = json.data || json.exams || json;
    if (Array.isArray(list) && list.length > 0) {
      await indexedDbStorage.cacheExams(list);
    }
  }
}

export async function fetchSyllabusTaxonomy(): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/syllabus/taxonomy`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Network request failed, falling back to local static taxonomy:', error);
    try {
      const local = await import('../../../data/syllabus_taxonomy.json');
      return (local as any).default || local;
    } catch (e) {
      console.warn('Static taxonomy import failed:', e);
      return { domains: [], total_topics: 0 };
    }
  }
}

export async function syncProfileToEdge(profileData: any): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/profile/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileData),
    });
    if (!res.ok) throw new Error(`Profile sync failed: HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn('Edge sync failed, queuing in IndexedDB outbox:', error);
    await indexedDbStorage.enqueueSync(profileData, 'sync_profile');
    throw error;
  }
}
