import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExamsList } from '../services/apiWorkerClient';
import type { ExamRecord } from '../types/profile';
import rawExamsJson from '../data/grade_a_exams.json';

const RAW_BUNDLED_EXAMS: ExamRecord[] = (rawExamsJson.exams || (rawExamsJson as any).default?.exams || rawExamsJson) as ExamRecord[];

// 11 PSU recruitments consolidated into Posts
export const CONSOLIDATED_PSU_EXAM_IDS = new Set<string>([
  'PSU_IOCL_ET',
  'PSU_ONGC_GT',
  'PSU_NTPC_EET',
  'PSU_PGCIL_ET',
  'PSU_BPCL_MT',
  'PSU_HPCL_OFFICER',
  'PSU_SAIL_MTT',
  'PSU_GAIL_ET',
  'PSU_COAL_INDIA_MT',
  'PSU_BHEL_ET',
  'PSU_BARC_NPCIL_ET'
]);

// Authoritative GATE Exam Record established as primary technical exam
export const GATE_EXAM_RECORD: ExamRecord = {
  exam_id: 'GATE',
  title: 'Graduate Aptitude Test in Engineering',
  short_code: 'GATE',
  category: 'Central-Civil',
  administering_body: 'IIT / IISc Consortium',
  frequency: 'Annual',
  official_website: 'https://gate2026.iitg.ac.in',
  latest_official_notification_url: 'https://gate2026.iitg.ac.in/documents/information-brochure.pdf',
  latest_gazette_ref: 'Statutory National Engineering Benchmark for Postgraduate Admissions and Grade A PSU Cadres',
  tentative_timeline_2027: {
    notification_month: 'August 2026',
    application_window: 'August – September 2026',
    prelims_stage_1: 'February 2027 (CBT)',
    final_result: 'March 2027',
  },
  description: 'Premier national technical examination testing comprehensive understanding of undergraduate engineering and science disciplines, serving as mandatory qualifying examination for Grade A PSU recruitment (IOCL, ONGC, NTPC, PowerGrid, BPCL, HPCL, SAIL, GAIL, Coal India, BHEL, BARC/NPCIL) and master\'s admissions.',
  eligibility: {
    min_age_gen: 18,
    max_age_gen: 65,
    cutoff_reference_date_rule: 'No statutory age restriction',
    min_education_level: 'Bachelor Degree or Final/Pre-Final Year Appearing',
    accepted_disciplines: ['Engineering', 'Technology', 'Architecture', 'Science', 'Commerce', 'Arts', 'ANY'],
    allows_final_year: true,
    relaxations: {},
  }
};

// Construct primary examinations: non-PSU + GATE (15 total)
function buildInitialPrimaryExams(): ExamRecord[] {
  const filtered = RAW_BUNDLED_EXAMS.filter((e) => !CONSOLIDATED_PSU_EXAM_IDS.has(e.exam_id));
  return [GATE_EXAM_RECORD, ...filtered];
}

export const useExamMasterStore = defineStore('examMaster', () => {
  // Pre-seed with the primary examinations (15 total)
  const exams = ref<ExamRecord[]>(buildInitialPrimaryExams());
  // Store all audited exams including PSUs for direct lookup and backward compatibility
  const allAuditedRecords = ref<ExamRecord[]>([GATE_EXAM_RECORD, ...RAW_BUNDLED_EXAMS]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const selectedCluster = ref<string>('ALL');
  const searchQuery = ref<string>('');

  async function loadExams() {
    // Already populated synchronously from bundled assets
    if (exams.value.length >= 15) return;
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExamsList();
      if (data && data.length > 0) {
        allAuditedRecords.value = [GATE_EXAM_RECORD, ...data];
        exams.value = [
          GATE_EXAM_RECORD,
          ...data.filter((e) => !CONSOLIDATED_PSU_EXAM_IDS.has(e.exam_id))
        ];
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to load exams.';
    } finally {
      isLoading.value = false;
    }
  }

  // Lookup map containing ALL records (primary + PSUs) so no routes 404
  const examsMap = computed<Record<string, ExamRecord>>(() => {
    const map: Record<string, ExamRecord> = {};
    for (const exam of allAuditedRecords.value) {
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

  function getClusterCount(category: string): number {
    return exams.value.filter((e) => e.category === category).length;
  }

  function isPsuRecruitment(examId: string): boolean {
    return CONSOLIDATED_PSU_EXAM_IDS.has(examId);
  }

  return {
    exams,
    allAuditedRecords,
    isLoading,
    error,
    selectedCluster,
    searchQuery,
    examsMap,
    loadExams,
    filteredExams,
    totalExamsCount,
    getClusterCount,
    isPsuRecruitment,
  };
});
