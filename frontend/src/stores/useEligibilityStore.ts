import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { EligibilityVerdict, UserProfileInput, ExamRecord } from '../types/profile';
import { evaluateAllExams as runEligibilityEvaluation, AUTHORITATIVE_EXAM_RULES } from '../services/eligibilityEngine';
import { indexedDbStorage } from '../services/indexedDbStorage';

export const useEligibilityStore = defineStore('eligibilityReport', () => {
  // State
  const verdicts = ref<Record<string, EligibilityVerdict>>({});
  const isEvaluating = ref<boolean>(false);
  const lastEvaluatedAt = ref<string | null>(null);

  // Filters & Search
  const filterCluster = ref<string>('ALL');
  const filterStatus = ref<string>('ALL');
  const searchQuery = ref<string>('');
  const sortBy = ref<'STATUS' | 'NAME' | 'TIMELINE'>('STATUS');

  // Selected Exam for Modal Citation View
  const selectedVerdict = ref<EligibilityVerdict | null>(null);

  // --- Getters ---

  const verdictList = computed<EligibilityVerdict[]>(() => Object.values(verdicts.value));

  const eligibleCount = computed(
    () => verdictList.value.filter((v) => v.status === 'ELIGIBLE').length
  );
  const conditionallyEligibleCount = computed(() => 0);
  const needsInfoCount = computed(
    () => verdictList.value.filter((v) => v.status === 'NEEDS_INFO').length
  );
  const ineligibleCount = computed(
    () => verdictList.value.filter((v) => v.status === 'INELIGIBLE').length
  );
  const totalCount = computed(() => verdictList.value.length);

  const filteredVerdicts = computed(() => {
    return (examsMap?: Record<string, ExamRecord>) => {
      const map = examsMap || {};
      let result = verdictList.value;

      // Status Filter
      if (filterStatus.value !== 'ALL') {
        result = result.filter((v) => v.status === filterStatus.value);
      }

      // Cluster Filter
      if (filterCluster.value !== 'ALL') {
        result = result.filter((v) => {
          const exam = map[v.exam_id];
          return exam && exam.category === filterCluster.value;
        });
      }

      // Search Query
      if (searchQuery.value.trim()) {
        const q = searchQuery.value.toLowerCase().trim();
        result = result.filter((v) => {
          const exam = map[v.exam_id];
          const title = exam?.title?.toLowerCase() || '';
          const code = exam?.short_code?.toLowerCase() || '';
          const id = v.exam_id.toLowerCase();
          return title.includes(q) || code.includes(q) || id.includes(q);
        });
      }

      // Sorting
      return [...result].sort((a, b) => {
        if (sortBy.value === 'STATUS') {
          const weight: Record<string, number> = { ELIGIBLE: 1, CONDITIONALLY_ELIGIBLE: 2, NEEDS_INFO: 3, INELIGIBLE: 4 };
          return (weight[a.status] || 99) - (weight[b.status] || 99);
        }
        if (sortBy.value === 'NAME') {
          const titleA = map[a.exam_id]?.title || a.exam_id;
          const titleB = map[b.exam_id]?.title || b.exam_id;
          return titleA.localeCompare(titleB);
        }
        return 0;
      });
    };
  });

  // --- Actions ---

  async function evaluateAllExams(profile: UserProfileInput, rules?: any) {
    isEvaluating.value = true;
    try {
      // Use built-in AUTHORITATIVE_EXAM_RULES by default
      const examRules = rules && Object.keys(rules).length > 0 ? rules : AUTHORITATIVE_EXAM_RULES;
      const results = runEligibilityEvaluation(profile, examRules, 2027);

      verdicts.value = results;
      lastEvaluatedAt.value = new Date().toISOString();

      // Cache offline in IndexedDB
      await indexedDbStorage.saveVerdicts(results);
    } finally {
      isEvaluating.value = false;
    }
  }

  async function loadCachedVerdicts() {
    const cached = await indexedDbStorage.loadVerdicts();
    if (cached && Object.keys(cached).length > 0) {
      verdicts.value = cached;
    }
  }

  function setFilterCluster(cluster: string) {
    filterCluster.value = cluster;
  }

  function setFilterStatus(status: string) {
    filterStatus.value = status;
  }

  function setSearchQuery(q: string) {
    searchQuery.value = q;
  }

  function selectVerdict(verdict: EligibilityVerdict | null) {
    selectedVerdict.value = verdict;
  }

  return {
    verdicts,
    isEvaluating,
    lastEvaluatedAt,
    filterCluster,
    filterStatus,
    searchQuery,
    sortBy,
    selectedVerdict,
    verdictList,
    eligibleCount,
    conditionallyEligibleCount,
    needsInfoCount,
    ineligibleCount,
    totalCount,
    filteredVerdicts,
    evaluateAllExams,
    loadCachedVerdicts,
    setFilterCluster,
    setFilterStatus,
    setSearchQuery,
    selectVerdict,
  };
});
