import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExamsList } from '../services/apiWorkerClient';
import type { ExamRecord } from '../types/profile';
import rawExamsJson from '../data/grade_a_exams.json';

const BUNDLED_EXAMS: ExamRecord[] = (rawExamsJson.exams || (rawExamsJson as any).default?.exams || rawExamsJson) as ExamRecord[];

export const useExamMasterStore = defineStore('examMaster', () => {
  // Pre-seed synchronously so exams are immediately available on 1st tick
  const exams = ref<ExamRecord[]>(Array.isArray(BUNDLED_EXAMS) ? [...BUNDLED_EXAMS] : []);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const selectedCluster = ref<string>('ALL');
  const searchQuery = ref<string>('');

  async function loadExams() {
    if (exams.value.length >= 36) return;
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExamsList();
      if (data && data.length > 0) {
        exams.value = data;
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to load exams.';
    } finally {
      isLoading.value = false;
    }
  }

  const examsMap = computed<Record<string, ExamRecord>>(() => {
    const map: Record<string, ExamRecord> = {};
    for (const exam of exams.value) {
      map[exam.exam_id] = exam;
    }
    return map;
  });

  const filteredExams = computed(() => {
    let result = exams.value;
    if (selectedCluster.value !== 'ALL') {
      result = result.filter((e) => e.category === selectedCluster.value);
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      result = result.filter(
        (e) =>
          e.title.toLowerCase().includes(q) ||
          e.short_code.toLowerCase().includes(q) ||
          e.administering_body.toLowerCase().includes(q)
      );
    }
    return result;
  });

  const totalExamsCount = computed(() => exams.value.length);

  return {
    exams,
    isLoading,
    error,
    selectedCluster,
    searchQuery,
    examsMap,
    loadExams,
    filteredExams,
    totalExamsCount,
  };
});
