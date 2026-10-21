import type { ExamRecord } from '../types/profile';
import type { AuthResponse } from '../types/auth';
import { indexedDbStorage } from './indexedDbStorage';
import rawExamsJson from '../data/grade_a_exams.json';
import rawTaxonomyJson from '../data/syllabus_taxonomy.json';

const API_BASE = '/api/v1';

// Static bundled catalog for instantaneous 0ms loading
const STATIC_EXAMS: ExamRecord[] = (rawExamsJson.exams || (rawExamsJson as any).default?.exams || rawExamsJson) as ExamRecord[];

export async function fetchExamsList(): Promise<ExamRecord[]> {
  // If we already have the bundled list, return it immediately while refreshing cache
  if (Array.isArray(STATIC_EXAMS) && STATIC_EXAMS.length >= 31) {
    // Cache in IndexedDB for offline resilience in background
    indexedDbStorage.cacheExams(STATIC_EXAMS).catch(() => {});
    
    // Background revalidate if online (non-blocking)
    if (typeof navigator !== 'undefined' && navigator.onLine) {
      revalidateExams().catch(() => {});
    }
    return STATIC_EXAMS;
  }

  // Fallback to IndexedDB cache
  try {
    const cached = await indexedDbStorage.getCachedExams();
    if (cached && cached.length >= 31) {
      return cached;
    }
  } catch {
    // Ignore
  }

  return STATIC_EXAMS || [];
}

async function revalidateExams(): Promise<void> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2000);
    const res = await fetch(`${API_BASE}/exams`, { signal: controller.signal });
    clearTimeout(timeout);
    if (res.ok) {
      const json = await res.json();
      const list: ExamRecord[] = json.data || json.exams || json;
      if (Array.isArray(list) && list.length > 0) {
        await indexedDbStorage.cacheExams(list);
      }
    }
  } catch {
    // Ignore background revalidation errors
  }
}

export async function fetchSyllabusTaxonomy(): Promise<any> {
  // Return static bundled taxonomy immediately
  if (rawTaxonomyJson) {
    return rawTaxonomyJson;
  }
  return { domains: [], total_topics: 0 };
}

export async function loginCandidate(
  candidateName: string,
  pin: string,
  uniqueId?: string
): Promise<AuthResponse> {
  const payload: any = { candidate_name: candidateName, pin };
  if (uniqueId) {
    payload.unique_id = uniqueId;
  }
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok && res.status !== 300) {
    throw new Error(data.message || data.error || `Login failed: HTTP ${res.status}`);
  }
  return data;
}

export async function registerCandidate(
  candidateName: string,
  pin: string
): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ candidate_name: candidateName, pin }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.message || data.error || `Registration failed: HTTP ${res.status}`);
  }
  return data;
}

export async function fetchCandidateProfile(userId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/profile/${encodeURIComponent(userId)}`);
  if (!res.ok) {
    throw new Error(`Failed to load profile for ${userId}: HTTP ${res.status}`);
  }
  return await res.json();
}

export async function syncProfileToEdge(profileData: any): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/profile/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileData),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || data.error || `Profile sync failed: HTTP ${res.status}`);
    }
    return data;
  } catch (error) {
    console.warn('Edge sync failed, queuing in IndexedDB outbox:', error);
    await indexedDbStorage.enqueueSync(profileData, 'sync_profile');
    throw error;
  }
}
