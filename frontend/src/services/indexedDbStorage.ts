/**
 * Offline Persistence Service using browser-native IndexedDB.
 * Database: grade_a_offline_db
 * Stores: user_profile, exam_catalog, eligibility_verdicts, sync_queue, profiles
 * Automatically falls back to localStorage when IndexedDB is blocked or unavailable.
 */

import { openDB, type IDBPDatabase } from 'idb';
import type { UserProfileInput, EligibilityVerdict, ExamRecord } from '../types/profile';

const DB_NAME = 'grade_a_offline_db';
const DB_VERSION = 2;

export class IndexedDbStorage {
  private dbPromise: Promise<IDBPDatabase<any>> | null = null;

  constructor() {
    if (typeof window !== 'undefined' && 'indexedDB' in window) {
      this.initDB();
      this.setupNetworkListeners();
    }
  }

  private initDB(): Promise<IDBPDatabase<any>> {
    if (!this.dbPromise) {
      this.dbPromise = openDB(DB_NAME, DB_VERSION, {
        upgrade(db, oldVersion) {
          // Store 1: user_profile
          if (!db.objectStoreNames.contains('user_profile')) {
            db.createObjectStore('user_profile', { keyPath: 'id' });
          }
          // Store 2: profiles (for Explorer 1 / legacy compatibility)
          if (!db.objectStoreNames.contains('profiles')) {
            db.createObjectStore('profiles');
          }
          // Store 3: exam_catalog
          if (!db.objectStoreNames.contains('exam_catalog')) {
            db.createObjectStore('exam_catalog', { keyPath: 'exam_id' });
          }
          // Store 4: eligibility_verdicts
          if (!db.objectStoreNames.contains('eligibility_verdicts')) {
            db.createObjectStore('eligibility_verdicts', { keyPath: 'exam_id' });
          }
          // Store 5: sync_queue
          if (!db.objectStoreNames.contains('sync_queue')) {
            db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
          }
        },
      });
    }
    return this.dbPromise;
  }

  // --- Profile Operations ---

  async saveProfile(profile: UserProfileInput | any): Promise<void> {
    try {
      const db = await this.initDB();
      const record = { id: 'current_profile', ...profile, updated_at: new Date().toISOString() };
      const tx = db.transaction(['user_profile', 'profiles'], 'readwrite');
      await Promise.all([
        tx.objectStore('user_profile').put(record),
        tx.objectStore('profiles').put(profile, 'current_user'),
        tx.done,
      ]);
    } catch {
      // Fallback to localStorage
      if (typeof window !== 'undefined') {
        try {
          localStorage.setItem('grade_a_current_profile', JSON.stringify(profile));
        } catch (e) {
          console.warn('[IndexedDB] Fallback localStorage save profile failed:', e);
        }
      }
    }
  }

  async loadProfile(): Promise<UserProfileInput | null> {
    try {
      const db = await this.initDB();
      const result = await db.get('user_profile', 'current_profile');
      if (result) {
        const { id, updated_at, ...profileData } = result;
        return profileData as UserProfileInput;
      }
      const legacyResult = await db.get('profiles', 'current_user');
      if (legacyResult) {
        return legacyResult as UserProfileInput;
      }
      return this.loadProfileFromLocalStorage();
    } catch {
      return this.loadProfileFromLocalStorage();
    }
  }

  private loadProfileFromLocalStorage(): UserProfileInput | null {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem('grade_a_current_profile');
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  async clearProfile(): Promise<void> {
    try {
      const db = await this.initDB();
      const tx = db.transaction(['user_profile', 'profiles'], 'readwrite');
      await Promise.all([
        tx.objectStore('user_profile').delete('current_profile'),
        tx.objectStore('profiles').delete('current_user'),
        tx.done,
      ]);
    } catch {
      // ignore
    }
    if (typeof window !== 'undefined') {
      localStorage.removeItem('grade_a_current_profile');
    }
  }

  // --- Exam Catalog Caching ---

  async cacheExams(exams: ExamRecord[]): Promise<void> {
    try {
      const db = await this.initDB();
      const tx = db.transaction('exam_catalog', 'readwrite');
      const store = tx.objectStore('exam_catalog');
      await Promise.all(exams.map((exam) => store.put(exam)));
      await tx.done;
    } catch {
      if (typeof window !== 'undefined') {
        try {
          localStorage.setItem('grade_a_cached_exams', JSON.stringify(exams));
        } catch (e) {
          console.warn('[IndexedDB] Fallback localStorage cache exams failed:', e);
        }
      }
    }
  }

  async getCachedExams(): Promise<ExamRecord[] | null> {
    try {
      const db = await this.initDB();
      const list = await db.getAll('exam_catalog');
      if (list && list.length > 0) return list as ExamRecord[];
      return this.getCachedExamsFromLocalStorage();
    } catch {
      return this.getCachedExamsFromLocalStorage();
    }
  }

  private getCachedExamsFromLocalStorage(): ExamRecord[] | null {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem('grade_a_cached_exams');
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  // --- Verdicts Caching ---

  async saveVerdicts(verdicts: Record<string, EligibilityVerdict>): Promise<void> {
    try {
      const db = await this.initDB();
      const tx = db.transaction('eligibility_verdicts', 'readwrite');
      const store = tx.objectStore('eligibility_verdicts');
      await Promise.all(Object.values(verdicts).map((verdict) => store.put(verdict)));
      await tx.done;
    } catch {
      if (typeof window !== 'undefined') {
        try {
          localStorage.setItem('grade_a_cached_verdicts', JSON.stringify(verdicts));
        } catch (e) {
          console.warn('[IndexedDB] Fallback localStorage save verdicts failed:', e);
        }
      }
    }
  }

  async loadVerdicts(): Promise<Record<string, EligibilityVerdict> | null> {
    try {
      const db = await this.initDB();
      const list = await db.getAll('eligibility_verdicts');
      if (list && list.length > 0) {
        const map: Record<string, EligibilityVerdict> = {};
        for (const item of list) {
          map[item.exam_id] = item;
        }
        return map;
      }
      return this.loadVerdictsFromLocalStorage();
    } catch {
      return this.loadVerdictsFromLocalStorage();
    }
  }

  private loadVerdictsFromLocalStorage(): Record<string, EligibilityVerdict> | null {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem('grade_a_cached_verdicts');
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  // --- Offline Sync Outbox Queue ---

  async enqueueSync(payload: any, action: string = 'sync_profile'): Promise<void> {
    try {
      const db = await this.initDB();
      await db.add('sync_queue', {
        action,
        payload,
        queued_at: new Date().toISOString(),
      });
    } catch {
      // ignore
    }
  }

  private setupNetworkListeners(): void {
    if (typeof window === 'undefined') return;
    window.addEventListener('online', () => {
      console.log('[IndexedDB] Network restored. Triggering offline sync...');
      this.flushSyncQueue();
    });
  }

  async flushSyncQueue(): Promise<void> {
    if (typeof navigator !== 'undefined' && !navigator.onLine) return;
    try {
      const db = await this.initDB();
      const items = await db.getAll('sync_queue');
      if (!items || items.length === 0) return;

      for (const item of items) {
        try {
          const res = await fetch('/api/v1/profile/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item.payload),
          });
          if (res.ok) {
            await db.delete('sync_queue', item.id);
          } else if (res.status >= 500 || res.status === 429) {
            // Server error or rate-limited; stop queue processing and retry later
            console.warn(`[IndexedDB] Server returned ${res.status}, deferring queue flush.`);
            break;
          } else if (res.status === 400 || res.status === 422) {
            // Unrecoverable payload validation error; drop item to prevent permanent blocking
            console.error(`[IndexedDB] Dropping invalid sync queue item #${item.id}: HTTP ${res.status}`);
            await db.delete('sync_queue', item.id);
          }
        } catch (e) {
          console.warn('[IndexedDB] Sync item deferred, will retry later:', e);
          break;
        }
      }
    } catch (e) {
      console.warn('[IndexedDB] Flush sync queue error:', e);
    }
  }
}

export const indexedDbStorage = new IndexedDbStorage();

// Convenience and backwards compatibility exports
export const saveLocalProfile = (profile: any) => indexedDbStorage.saveProfile(profile);
export const getLocalProfile = () => indexedDbStorage.loadProfile();
export const queueOfflineSync = (action: string, payload: any) => indexedDbStorage.enqueueSync(payload, action);
