import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type {
  ExaminationScheme,
  SchemeStage,
  SchemePaper,
  ProgressMetric,
  CurriculumDataset
} from '../types/curriculum';
import rawCurriculumData from '../data/exam_curriculum_data.json';

const CURRICULUM_DATA = rawCurriculumData as unknown as CurriculumDataset;
const STORAGE_KEY = 'goi_syllabus_tracker_v2';

export const useSyllabusTrackerStore = defineStore('syllabusTracker', () => {
  // Map of examId -> array of completed topicIds
  const completedMap = ref<Record<string, string[]>>({});
  // Map of examId -> selected stream/discipline code (e.g. GATE -> 'ME')
  const selectedDisciplines = ref<Record<string, string>>({});
  // Search query state per exam
  const searchQueries = ref<Record<string, string>>({});

  // Initialize from LocalStorage
  function loadFromStorage() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const stored = window.localStorage.getItem(STORAGE_KEY);
        if (stored) {
          const parsed = JSON.parse(stored);
          if (parsed && typeof parsed === 'object') {
            completedMap.value = parsed.completed || parsed;
            if (parsed.disciplines) {
              selectedDisciplines.value = parsed.disciplines;
            }
          }
        }
      }
    } catch (e) {
      console.warn('Failed to load syllabus tracking data from localStorage', e);
    }
  }

  function saveToStorage() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const payload = {
          completed: completedMap.value,
          disciplines: selectedDisciplines.value,
          updated_at: new Date().toISOString()
        };
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
      }
    } catch (e) {
      console.warn('Failed to save syllabus tracking data to localStorage', e);
    }
  }

  // Load immediately on instantiation
  loadFromStorage();

  // Helper getters
  function getCompletedTopicIds(examId: string): string[] {
    return completedMap.value[examId] || [];
  }

  function isTopicCompleted(examId: string, topicId: string): boolean {
    const list = completedMap.value[examId];
    if (!list) return false;
    return list.includes(topicId);
  }

  function toggleTopic(examId: string, topicId: string): boolean {
    if (!completedMap.value[examId]) {
      completedMap.value[examId] = [];
    }
    const currentList = completedMap.value[examId];
    const index = currentList.indexOf(topicId);
    let nowCompleted = false;

    if (index >= 0) {
      currentList.splice(index, 1);
      nowCompleted = false;
    } else {
      currentList.push(topicId);
      nowCompleted = true;
    }

    saveToStorage();
    return nowCompleted;
  }

  function markPaperDone(examId: string, paper: SchemePaper) {
    if (!completedMap.value[examId]) {
      completedMap.value[examId] = [];
    }
    const set = new Set(completedMap.value[examId]);
    for (const topic of paper.topics) {
      set.add(topic.topic_id);
    }
    completedMap.value[examId] = Array.from(set);
    saveToStorage();
  }

  function resetPaper(examId: string, paper: SchemePaper) {
    if (!completedMap.value[examId]) return;
    const paperTopicIds = new Set(paper.topics.map((t) => t.topic_id));
    completedMap.value[examId] = completedMap.value[examId].filter((id) => !paperTopicIds.has(id));
    saveToStorage();
  }

  function resetExam(examId: string) {
    completedMap.value[examId] = [];
    saveToStorage();
  }

  function getActiveDiscipline(examId: string, scheme?: ExaminationScheme): string {
    if (selectedDisciplines.value[examId]) {
      return selectedDisciplines.value[examId];
    }
    if (scheme && scheme.disciplines && scheme.disciplines.length > 0) {
      return scheme.disciplines[0].code;
    }
    return '';
  }

  function setActiveDiscipline(examId: string, code: string) {
    selectedDisciplines.value[examId] = code;
    saveToStorage();
  }

  // Progress Calculations
  function getPaperProgress(examId: string, paper: SchemePaper): ProgressMetric {
    const total = paper.topics.length;
    if (total === 0) return { completed: 0, total: 0, pct: 0 };
    const completedList = completedMap.value[examId] || [];
    let done = 0;
    for (const t of paper.topics) {
      if (completedList.includes(t.topic_id)) {
        done++;
      }
    }
    return {
      completed: done,
      total,
      pct: Math.round((done / total) * 100)
    };
  }

  function getStageProgress(
    examId: string,
    stage: SchemeStage,
    activeStreamId?: string
  ): ProgressMetric {
    let done = 0;
    let total = 0;
    const completedList = completedMap.value[examId] || [];

    for (const paper of stage.papers) {
      // If paper has stream_id and doesn't match active stream, skip from calculation
      if (paper.stream_id && activeStreamId && paper.stream_id !== activeStreamId) {
        continue;
      }
      for (const t of paper.topics) {
        total++;
        if (completedList.includes(t.topic_id)) {
          done++;
        }
      }
    }

    return {
      completed: done,
      total,
      pct: total > 0 ? Math.round((done / total) * 100) : 0
    };
  }

  function getExamProgress(
    examId: string,
    scheme: ExaminationScheme,
    activeStreamId?: string
  ): ProgressMetric {
    let done = 0;
    let total = 0;
    const completedList = completedMap.value[examId] || [];

    for (const stage of scheme.stages) {
      for (const paper of stage.papers) {
        if (paper.stream_id && activeStreamId && paper.stream_id !== activeStreamId) {
          continue;
        }
        for (const t of paper.topics) {
          total++;
          if (completedList.includes(t.topic_id)) {
            done++;
          }
        }
      }
    }

    return {
      completed: done,
      total,
      pct: total > 0 ? Math.round((done / total) * 100) : 0
    };
  }

  function getScheme(examId: string): ExaminationScheme | undefined {
    return CURRICULUM_DATA.schemes[examId];
  }

  const allSchemes = computed(() => CURRICULUM_DATA.schemes);

  return {
    completedMap,
    selectedDisciplines,
    searchQueries,
    allSchemes,
    getScheme,
    getCompletedTopicIds,
    isTopicCompleted,
    toggleTopic,
    markPaperDone,
    resetPaper,
    resetExam,
    getActiveDiscipline,
    setActiveDiscipline,
    getPaperProgress,
    getStageProgress,
    getExamProgress,
    loadFromStorage,
    saveToStorage
  };
});
