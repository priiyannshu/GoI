import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const STORAGE_KEY_EXAMS = 'goi_hidden_exams';
const STORAGE_KEY_POSTS = 'goi_hidden_posts';

export const useHiddenStore = defineStore('hiddenItems', () => {
  const hiddenExamIds = ref<string[]>([]);
  const hiddenPostIds = ref<string[]>([]);
  const isLoaded = ref<boolean>(false);

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
  }

  function persistPosts() {
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY_POSTS, JSON.stringify(hiddenPostIds.value));
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
    loadHiddenItems,
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
