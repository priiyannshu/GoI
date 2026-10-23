import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useAuthStore } from './useAuthStore';
import { syncProfileToEdge } from '../services/apiWorkerClient';

const STORAGE_KEY_EXAMS = 'goi_hidden_exams';
const STORAGE_KEY_POSTS = 'goi_hidden_posts';

export const useHiddenStore = defineStore('hiddenItems', () => {
  const hiddenExamIds = ref<string[]>([]);
  const hiddenPostIds = ref<string[]>([]);
  const isLoaded = ref<boolean>(false);
  const isSyncing = ref<boolean>(false);

  const authStore = useAuthStore();

  function loadHiddenItems() {
    if (typeof window === 'undefined') return;
    try {
      const storedExams = localStorage.getItem(STORAGE_KEY_EXAMS);
      if (storedExams) {
        hiddenExamIds.value = JSON.parse(storedExams);
      }
      const storedPosts = localStorage.getItem(STORAGE_KEY_POSTS);
      if (storedPosts) {
        hiddenPostIds.value = JSON.parse(storedPosts);
      }
    } catch (e) {
      console.warn('Failed to parse hidden items from localStorage', e);
    }
    isLoaded.value = true;
  }

  function persistExams() {
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY_EXAMS, JSON.stringify(hiddenExamIds.value));
    }
    triggerCloudSync();
  }

  function persistPosts() {
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY_POSTS, JSON.stringify(hiddenPostIds.value));
    }
    triggerCloudSync();
  }

  // Trigger sync of hidden items to cloud profile if logged in
  let cloudSyncTimer: any = null;
  function triggerCloudSync() {
    if (!authStore.candidateId) return;
    if (cloudSyncTimer) clearTimeout(cloudSyncTimer);
    cloudSyncTimer = setTimeout(async () => {
      if (typeof navigator !== 'undefined' && !navigator.onLine) return;
      try {
        isSyncing.value = true;
        // Import useProfileStore dynamically or read profile payload
        const { useProfileStore } = await import('./useProfileStore');
        const profileStore = useProfileStore();
        if (profileStore.isProfileCompleteForD1) {
          const payload = profileStore.getD1Payload();
          await syncProfileToEdge(payload);
        }
      } catch (err) {
        console.warn('Failed to sync hidden items to cloud:', err);
      } finally {
        isSyncing.value = false;
      }
    }, 400);
  }

  /**
   * Set hidden items directly from cloud profile (e.g. after login or profile load)
   */
  function setHiddenItemsFromRemote(exams?: string[], posts?: string[]) {
    if (Array.isArray(exams)) {
      hiddenExamIds.value = [...new Set(exams)];
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY_EXAMS, JSON.stringify(hiddenExamIds.value));
      }
    }
    if (Array.isArray(posts)) {
      hiddenPostIds.value = [...new Set(posts)];
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY_POSTS, JSON.stringify(hiddenPostIds.value));
      }
    }
    isLoaded.value = true;
  }

  function clearHiddenItemsLocal() {
    hiddenExamIds.value = [];
    hiddenPostIds.value = [];
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY_EXAMS);
      localStorage.removeItem(STORAGE_KEY_POSTS);
    }
  }

  function hideExam(examId: string) {
    if (!hiddenExamIds.value.includes(examId)) {
      hiddenExamIds.value.push(examId);
      persistExams();
    }
  }

  function unhideExam(examId: string) {
    const idx = hiddenExamIds.value.indexOf(examId);
    if (idx >= 0) {
      hiddenExamIds.value.splice(idx, 1);
      persistExams();
    }
  }

  function isExamHidden(examId: string): boolean {
    return hiddenExamIds.value.includes(examId);
  }

  function toggleExamHidden(examId: string) {
    if (isExamHidden(examId)) {
      unhideExam(examId);
    } else {
      hideExam(examId);
    }
  }

  function hidePost(postId: string) {
    if (!hiddenPostIds.value.includes(postId)) {
      hiddenPostIds.value.push(postId);
      persistPosts();
    }
  }

  function unhidePost(postId: string) {
    const idx = hiddenPostIds.value.indexOf(postId);
    if (idx >= 0) {
      hiddenPostIds.value.splice(idx, 1);
      persistPosts();
    }
  }

  function isPostHidden(postId: string): boolean {
    return hiddenPostIds.value.includes(postId);
  }

  function togglePostHidden(postId: string) {
    if (isPostHidden(postId)) {
      unhidePost(postId);
    } else {
      hidePost(postId);
    }
  }

  function unhideAllExams() {
    hiddenExamIds.value = [];
    persistExams();
  }

  function unhideAllPosts() {
    hiddenPostIds.value = [];
    persistPosts();
  }

  function unhideAll() {
    unhideAllExams();
    unhideAllPosts();
  }

  const totalHiddenCount = computed(() => hiddenExamIds.value.length + hiddenPostIds.value.length);
  const hiddenExamsCount = computed(() => hiddenExamIds.value.length);
  const hiddenPostsCount = computed(() => hiddenPostIds.value.length);

  return {
    hiddenExamIds,
    hiddenPostIds,
    isLoaded,
    isSyncing,
    loadHiddenItems,
    triggerCloudSync,
    setHiddenItemsFromRemote,
    clearHiddenItemsLocal,
    hideExam,
    unhideExam,
    isExamHidden,
    toggleExamHidden,
    hidePost,
    unhidePost,
    isPostHidden,
    togglePostHidden,
    unhideAllExams,
    unhideAllPosts,
    unhideAll,
    totalHiddenCount,
    hiddenExamsCount,
    hiddenPostsCount,
  };
});
