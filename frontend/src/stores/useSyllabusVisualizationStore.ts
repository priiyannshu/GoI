import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { DepthLevel, TopicRecord, ExamSyllabusMapping, BipartiteGraphData, BipartiteGraphNode, BipartiteGraphLink } from '@/types/syllabus';
import type { ExamRecord } from '@/types/profile';
import { useExamMasterStore } from './useExamMasterStore';
import rawTaxonomyJson from '../data/syllabus_taxonomy.json';
import rawMapSeedData from '../data/exam_syllabus_map_seed.json';

const BUNDLED_TOPICS: TopicRecord[] = (rawTaxonomyJson as any).topics_flat || [];
const BUNDLED_MAPPINGS: ExamSyllabusMapping[] = (rawMapSeedData as any).default || rawMapSeedData || [];

const INITIAL_TOPICS_MAP: Record<string, TopicRecord> = {};
for (const t of BUNDLED_TOPICS) {
  INITIAL_TOPICS_MAP[t.topic_id] = t;
}

export const DEPTH_WEIGHTS: Record<DepthLevel, number> = {
  Foundation: 1,
  Intermediate: 2,
  Advanced: 3,
  Analytical: 4,
};

export const DEPTH_STROKE_WIDTHS: Record<DepthLevel, number> = {
  Foundation: 1.5,
  Intermediate: 2.5,
  Advanced: 3.5,
  Analytical: 5.0,
};

export const DOMAIN_COLORS: Record<string, string> = {
  'General Studies': '#38BDF8',       // Sky 400
  'Quantitative Aptitude': '#F43F5E', // Rose 500
  'Reasoning': '#A855F7',             // Purple 500
  'English': '#34D399',               // Emerald 400
  'Economics & Finance': '#F59E0B',   // Amber 500
  'Technical': '#06B6D4',             // Cyan 500
};

export const CLUSTER_COLORS: Record<string, string> = {
  'Central-Civil': '#3B82F6',         // Blue 500
  'Regulatory': '#10B981',            // Emerald 500
  'Defense': '#F59E0B',               // Amber 500
  'State-PSC': '#8B5CF6',             // Purple 500
  'PSU': '#EC4899',                   // Pink 500
};

export interface QuickPreset {
  id: string;
  label: string;
  description: string;
  examIds: string[];
}

export const PRESET_OPTIONS: QuickPreset[] = [
  {
    id: 'upsc_trio',
    label: 'UPSC All-India Trio',
    description: 'Civil Services, Forest Service & Engineering Services',
    examIds: ['UPSC_CSE', 'UPSC_IFOS', 'UPSC_ESE'],
  },
  {
    id: 'regulatory_trio',
    label: 'Regulatory Financial Trio',
    description: 'Premier regulators: RBI Grade B, NABARD Grade A & SIDBI Grade A',
    examIds: ['RBI_GRADE_B', 'NABARD_GRADE_A', 'SIDBI_GRADE_A'],
  },
  {
    id: 'defense_trifecta',
    label: 'Uniformed Defense Trifecta',
    description: 'Combined Defence Services, AFCAT & Central Armed Police Forces',
    examIds: ['UPSC_CDS', 'IAF_AFCAT', 'UPSC_CAPF_AC'],
  },
  {
    id: 'state_psc_triangle',
    label: 'State PSC Administrative',
    description: 'Largest state commissions: UPPSC PCS, BPSC CCE & MPPSC SSE',
    examIds: ['UPPSC_PCS', 'BPSC_CCE', 'MPPSC_SSE'],
  },
  {
    id: 'civil_finance_duo',
    label: 'Civil-Finance Dual Aspirant',
    description: 'High-synergy overlap between UPSC CSE and RBI Grade B',
    examIds: ['UPSC_CSE', 'RBI_GRADE_B'],
  },
];

export const useSyllabusVisualizationStore = defineStore('syllabusViz', () => {
  // Master Selected Exams (Enforced bounds: min 2, max 4)
  const defaultSelectedExams = ['UPSC_CSE', 'RBI_GRADE_B', 'UPPSC_PCS'];
  const selectedExamIds = ref<string[]>([...defaultSelectedExams]);

  // Interactive Highlighting & Selection
  const hoveredTopicId = ref<string | null>(null);
  const hoveredExamId = ref<string | null>(null);
  const selectedTopicId = ref<string | null>(null);
  const activeIntersectionTopics = ref<string[]>([]);
  const pinnedCombinationKey = ref<string | null>(null);

  // Global Filters & View Routing
  const selectedDomain = ref<string>('ALL');
  const minDepthLevel = ref<DepthLevel>('Foundation');
  const searchQuery = ref<string>('');
  const activeTab = ref<'matrix' | 'upset'>('matrix');

  // Loading & Cache State
  const isLoading = ref<boolean>(false);
  const isDataLoaded = ref<boolean>(BUNDLED_TOPICS.length > 0);
  const error = ref<string | null>(null);

  // Raw Data Buffers (Pre-seeded synchronously for instant display)
  const allTopics = ref<TopicRecord[]>([...BUNDLED_TOPICS]);
  const topicsMap = ref<Record<string, TopicRecord>>({ ...INITIAL_TOPICS_MAP });
  const allMappings = ref<ExamSyllabusMapping[]>([...BUNDLED_MAPPINGS]);
  const domainsList = ref<string[]>([
    'General Studies',
    'Quantitative Aptitude',
    'Reasoning',
    'English',
    'Economics & Finance',
    'Technical',
  ]);

  // -------------------------------------------------------------
  // Data Loader Action
  // -------------------------------------------------------------
  async function loadSyllabusData(): Promise<void> {
    if (isDataLoaded.value && allTopics.value.length > 0) return;
    isLoading.value = true;
    error.value = null;

    try {
      // 1. Ensure master exam catalog is loaded
      const examStore = useExamMasterStore();
      if (examStore.exams.length === 0) {
        await examStore.loadExams();
      }

      // 2. Load Taxonomy Topics
      let taxonomyPayload: any = null;
      try {
        const res = await fetch('/api/v1/syllabus/taxonomy');
        if (res.ok) {
          taxonomyPayload = await res.json();
        }
      } catch {
        // Fall back to static import
      }

      if (!taxonomyPayload || !taxonomyPayload.topics_flat) {
        const localTax = await import('../../../data/syllabus_taxonomy.json');
        taxonomyPayload = (localTax as any).default || localTax;
      }

      const rawTopics: TopicRecord[] = taxonomyPayload.topics_flat || [];
      allTopics.value = rawTopics;

      const tMap: Record<string, TopicRecord> = {};
      for (const t of rawTopics) {
        tMap[t.topic_id] = t;
      }
      topicsMap.value = tMap;

      // 3. Load Exam Syllabus Mappings
      let mappingsPayload: ExamSyllabusMapping[] = [];
      try {
        const res = await fetch('/api/v1/syllabus/matrix');
        if (res.ok) {
          const json = await res.json();
          mappingsPayload = json.data || json.mappings || [];
        }
      } catch {
        // Fall back to static import
      }

      if (!mappingsPayload || mappingsPayload.length === 0) {
        const localMap = await import('../../../data/exam_syllabus_map_seed.json');
        mappingsPayload = (localMap as any).default || localMap;
      }

      allMappings.value = mappingsPayload || [];
      isDataLoaded.value = true;
    } catch (err: any) {
      console.error('Failed to load syllabus visualization datasets:', err);
      error.value = err.message || 'Failed to initialize syllabus datasets.';
    } finally {
      isLoading.value = false;
    }
  }

  // -------------------------------------------------------------
  // Filtered Mappings & Topics
  // -------------------------------------------------------------
  const minDepthWeight = computed<number>(() => DEPTH_WEIGHTS[minDepthLevel.value] || 1);

  // Mappings filtered by selected exams and minimum cognitive depth
  const activeExamMappings = computed<ExamSyllabusMapping[]>(() => {
    const selectedSet = new Set(selectedExamIds.value);
    const minWeight = minDepthWeight.value;

    return allMappings.value.filter((m) => {
      if (!selectedSet.has(m.exam_id)) return false;
      const weight = DEPTH_WEIGHTS[m.depth_level] || 1;
      return weight >= minWeight;
    });
  });

  // Map of exam_id -> Set of valid topic_ids (matching minDepth)
  const examTopicMap = computed<Record<string, Set<string>>>(() => {
    const map: Record<string, Set<string>> = {};
    for (const eid of selectedExamIds.value) {
      map[eid] = new Set<string>();
    }
    for (const m of activeExamMappings.value) {
      if (map[m.exam_id]) {
        map[m.exam_id].add(m.topic_id);
      }
    }
    return map;
  });

  // Filtered Topics based on domain, search query, and active exam presence
  const filteredTopics = computed<TopicRecord[]>(() => {
    const q = searchQuery.value.trim().toLowerCase();
    const dom = selectedDomain.value;
    const activeExamTopicSet = new Set<string>();

    for (const m of activeExamMappings.value) {
      activeExamTopicSet.add(m.topic_id);
    }

    return allTopics.value.filter((topic) => {
      // Must be present in at least one selected exam at required depth
      if (!activeExamTopicSet.has(topic.topic_id)) return false;

      // Domain filter
      if (dom !== 'ALL' && topic.domain !== dom) return false;

      // Search filter
      if (q) {
        const matchesTitle = topic.topic_title.toLowerCase().includes(q);
        const matchesId = topic.topic_id.toLowerCase().includes(q);
        const matchesDesc = topic.description.toLowerCase().includes(q);
        const matchesSubDomain = topic.sub_domain.toLowerCase().includes(q);
        if (!matchesTitle && !matchesId && !matchesDesc && !matchesSubDomain) {
          return false;
        }
      }

      return true;
    });
  });

  // Topic Degree Map (degree = number of selected exams offering this topic)
  const topicDegreeMap = computed<Record<string, number>>(() => {
    const deg: Record<string, number> = {};
    const eMap = examTopicMap.value;

    for (const topic of filteredTopics.value) {
      let count = 0;
      for (const eid of selectedExamIds.value) {
        if (eMap[eid]?.has(topic.topic_id)) {
          count++;
        }
      }
      deg[topic.topic_id] = count;
    }
    return deg;
  });

  // Selected Exam Records from ExamMasterStore
  const examMasterStore = useExamMasterStore();
  const selectedExamRecords = computed<ExamRecord[]>(() => {
    return selectedExamIds.value.map((eid) => {
      return (
        examMasterStore.examsMap[eid] || {
          exam_id: eid,
          title: eid.replace(/_/g, ' '),
          short_code: eid.split('_')[1] || eid,
          category: 'Central-Civil',
          administering_body: 'Government of India',
          frequency: 'Annual',
          official_website: 'https://upsc.gov.in',
          latest_official_notification_url: 'https://upsc.gov.in',
          tentative_timeline_2027: {},
        }
      );
    });
  });

  // -------------------------------------------------------------
  // Bipartite Graph Dataset Generation
  // -------------------------------------------------------------
  const bipartiteGraphData = computed<BipartiteGraphData>(() => {
    const nodes: BipartiteGraphNode[] = [];
    const links: BipartiteGraphLink[] = [];

    const activeTopics = filteredTopics.value;
    const activeTopicIds = new Set(activeTopics.map((t) => t.topic_id));
    const degrees = topicDegreeMap.value;
    const eMap = examTopicMap.value;

    // 1. Add Exam Nodes (Outer Radial Ring)
    for (const exam of selectedExamRecords.value) {
      const topicCount = eMap[exam.exam_id]?.size || 0;
      nodes.push({
        id: exam.exam_id,
        name: exam.title,
        short_code: exam.short_code,
        category: exam.category,
        cluster: exam.category,
        type: 'exam',
        r: 32, // Prescribed exam radius (test_f20_bipartite_graph_two_node_classes)
        degree: topicCount,
        color: CLUSTER_COLORS[exam.category] || '#3B82F6',
        description: exam.administering_body,
      });
    }

    // 2. Add Topic Nodes (Inner Radial Zone)
    for (const topic of activeTopics) {
      const deg = degrees[topic.topic_id] || 0;
      // Radius scales with square root of degree: r = 12 + sqrt(degree) * 3
      const radius = 12 + Math.sqrt(deg) * 3;

      nodes.push({
        id: topic.topic_id,
        name: topic.topic_title,
        type: 'topic',
        r: radius,
        degree: deg,
        domain: topic.domain,
        sub_domain: topic.sub_domain,
        color: DOMAIN_COLORS[topic.domain] || '#38BDF8',
        description: topic.description,
      });
    }

    // 3. Add Bipartite Links (Exam -> Topic)
    const selectedSet = new Set(selectedExamIds.value);
    const minWeight = minDepthWeight.value;

    for (const m of allMappings.value) {
      if (!selectedSet.has(m.exam_id)) continue;
      if (!activeTopicIds.has(m.topic_id)) continue;

      const weight = DEPTH_WEIGHTS[m.depth_level] || 1;
      if (weight < minWeight) continue;

      const strokeWidth = DEPTH_STROKE_WIDTHS[m.depth_level] || 2.5;

      links.push({
        source: m.exam_id,
        target: m.topic_id,
        stage_name: m.stage_name,
        depth_level: m.depth_level,
        weight: weight,
        stroke_width: strokeWidth,
        is_optional: m.is_optional || false,
        weightage_pct_estimate: m.weightage_pct_estimate,
        source_clause_ref: m.source_clause_ref,
      });
    }

    return { nodes, links };
  });

  // Active Detail for Selected or Hovered Topic
  const activeTopicDetail = computed(() => {
    const tid = selectedTopicId.value || hoveredTopicId.value;
    if (!tid) return null;

    const topic = topicsMap.value[tid];
    if (!topic) return null;

    // Find all mappings across selected exams
    const relevantMappings = allMappings.value.filter(
      (m) => m.topic_id === tid && selectedExamIds.value.includes(m.exam_id)
    );

    // Also find any other Grade A exams that test this topic
    const otherExamMappings = allMappings.value.filter(
      (m) => m.topic_id === tid && !selectedExamIds.value.includes(m.exam_id)
    );

    return {
      topic,
      mappings: relevantMappings,
      otherMappingsCount: otherExamMappings.length,
      degreeInSelection: relevantMappings.length,
      totalExamsRequiring: relevantMappings.length + otherExamMappings.length,
    };
  });

  // -------------------------------------------------------------
  // Interaction & Mutation Actions
  // -------------------------------------------------------------
  function setHoveredTopic(topicId: string | null) {
    hoveredTopicId.value = topicId;
  }

  function setHoveredExam(examId: string | null) {
    hoveredExamId.value = examId;
  }

  function setSelectedTopic(topicId: string | null) {
    selectedTopicId.value = topicId;
  }

  function setActiveIntersection(topicIds: string[], combinationKey?: string) {
    activeIntersectionTopics.value = topicIds;
    pinnedCombinationKey.value = combinationKey || null;
  }

  function clearActiveIntersection() {
    activeIntersectionTopics.value = [];
    pinnedCombinationKey.value = null;
  }

  function toggleExamSelection(examId: string): boolean {
    const idx = selectedExamIds.value.indexOf(examId);
    if (idx >= 0) {
      // Prevent deselection below minimum bound of 2
      if (selectedExamIds.value.length > 2) {
        selectedExamIds.value.splice(idx, 1);
        return true;
      }
      return false;
    } else {
      // Allow selecting up to 10 exams
      if (selectedExamIds.value.length < 10) {
        selectedExamIds.value.push(examId);
        return true;
      }
      return false;
    }
  }

  function setExamSelection(examIds: string[]) {
    // Clamp to 2..10 items
    const valid = Array.from(new Set(examIds)).slice(0, 10);
    if (valid.length >= 2) {
      selectedExamIds.value = valid;
    }
  }

  function setPreset(presetId: string) {
    const preset = PRESET_OPTIONS.find((p) => p.id === presetId);
    if (preset) {
      setExamSelection(preset.examIds);
    }
  }

  function setDomain(domain: string) {
    selectedDomain.value = domain;
  }

  function setMinDepth(depth: DepthLevel) {
    minDepthLevel.value = depth;
  }

  function setSearchQuery(q: string) {
    searchQuery.value = q;
  }

  function resetToDefaults() {
    selectedExamIds.value = [...defaultSelectedExams];
    hoveredTopicId.value = null;
    hoveredExamId.value = null;
    selectedTopicId.value = null;
    activeIntersectionTopics.value = [];
    pinnedCombinationKey.value = null;
    selectedDomain.value = 'ALL';
    minDepthLevel.value = 'Foundation';
    searchQuery.value = '';
  }

  return {
    // State
    selectedExamIds,
    hoveredTopicId,
    hoveredExamId,
    selectedTopicId,
    activeIntersectionTopics,
    pinnedCombinationKey,
    selectedDomain,
    minDepthLevel,
    searchQuery,
    activeTab,
    isLoading,
    isDataLoaded,
    error,
    allTopics,
    topicsMap,
    allMappings,
    domainsList,

    // Computed Getters
    filteredTopics,
    activeExamMappings,
    examTopicMap,
    topicDegreeMap,
    selectedExamRecords,
    bipartiteGraphData,
    activeTopicDetail,

    // Actions
    loadSyllabusData,
    setHoveredTopic,
    setHoveredExam,
    setSelectedTopic,
    setActiveIntersection,
    clearActiveIntersection,
    toggleExamSelection,
    setExamSelection,
    setPreset,
    setDomain,
    setMinDepth,
    setSearchQuery,
    resetToDefaults,
  };
});
