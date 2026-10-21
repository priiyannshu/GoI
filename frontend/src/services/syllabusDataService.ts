import type {
  DepthLevel,
  TopicRecord,
  TopicTaxonomyDetail,
  UpSetCombination,
  VennRegion,
  PairwiseMetric,
} from '../types/syllabus';
import { fetchSyllabusTaxonomy } from './apiWorkerClient';

export const DEPTH_RANK: Record<DepthLevel, number> = {
  Foundation: 1,
  Intermediate: 2,
  Advanced: 3,
  Analytical: 4,
};

let cachedTaxonomyLookup: Record<string, TopicTaxonomyDetail> | null = null;
let cachedTopicsFlat: TopicRecord[] | null = null;

export async function loadTaxonomyData(): Promise<{
  lookup: Record<string, TopicTaxonomyDetail>;
  topics: TopicRecord[];
}> {
  if (cachedTaxonomyLookup && cachedTopicsFlat) {
    return { lookup: cachedTaxonomyLookup, topics: cachedTopicsFlat };
  }

  try {
    const rawData = await fetchSyllabusTaxonomy();
    if (rawData && rawData.lookup_by_id) {
      cachedTaxonomyLookup = rawData.lookup_by_id;
      cachedTopicsFlat = rawData.topics_flat || Object.values(rawData.lookup_by_id);
      return { lookup: cachedTaxonomyLookup!, topics: cachedTopicsFlat! };
    }
  } catch (err) {
    console.warn('Failed to load taxonomy via client, importing local JSON:', err);
  }

  // Fallback to static JSON import
  try {
    const local = await import('../../../data/syllabus_taxonomy.json');
    const data = (local as any).default || local;
    cachedTaxonomyLookup = data.lookup_by_id || {};
    cachedTopicsFlat = data.topics_flat || Object.values(cachedTaxonomyLookup!);
    return { lookup: cachedTaxonomyLookup!, topics: cachedTopicsFlat! };
  } catch (err) {
    console.error('Fatal: Cannot load syllabus taxonomy data:', err);
    return { lookup: {}, topics: [] };
  }
}

/**
 * Filters syllabus topics by domain and cognitive depth for each selected exam.
 */
export function getFilteredExamTopicMap(
  selectedExamIds: string[],
  taxonomyLookup: Record<string, TopicTaxonomyDetail>,
  domain: string = 'ALL',
  minDepth: DepthLevel = 'Foundation'
): {
  examTopicMap: Record<string, Set<string>>;
  topicLookup: Record<string, TopicRecord>;
} {
  const minRank = DEPTH_RANK[minDepth] ?? 1;
  const examTopicMap: Record<string, Set<string>> = {};
  const topicLookup: Record<string, TopicRecord> = {};

  for (const examId of selectedExamIds) {
    examTopicMap[examId] = new Set<string>();
  }

  for (const [topicId, topic] of Object.entries(taxonomyLookup)) {
    // Apply domain filter
    if (domain !== 'ALL' && topic.domain !== domain) {
      continue;
    }

    topicLookup[topicId] = {
      topic_id: topic.topic_id,
      domain: topic.domain,
      sub_domain: topic.sub_domain,
      topic_title: topic.topic_title,
      description: topic.description,
    };

    if (!Array.isArray(topic.mapped_exams)) continue;

    for (const mapping of topic.mapped_exams) {
      if (selectedExamIds.includes(mapping.exam_id)) {
        const rank = DEPTH_RANK[mapping.depth_level] ?? 1;
        if (rank >= minRank) {
          examTopicMap[mapping.exam_id].add(topicId);
        }
      }
    }
  }

  return { examTopicMap, topicLookup };
}

/**
 * Computes exclusive disjoint intersections for UpSet Overlap Matrix.
 * Satisfies Alexander Lex UpSet specification and oracle.py calculate_upset_intersections.
 */
export function calculateUpSetCombinations(
  examTopicMap: Record<string, Set<string>>,
  topicLookup: Record<string, TopicRecord>,
  maxCombinationsCap: number = 50
): {
  combinations: UpSetCombination[];
  totalUniqueTopics: number;
  totalCombinationsCount: number;
} {
  const examIds = Object.keys(examTopicMap).sort();
  const allTopicIds = new Set<string>();
  for (const topics of Object.values(examTopicMap)) {
    for (const t of topics) {
      allTopicIds.add(t);
    }
  }

  const combinationGroups = new Map<string, { examIds: string[]; topicIds: string[] }>();

  // For each topic in the union, compute its exact exclusive membership mask
  for (const topicId of allTopicIds) {
    const activeExams = examIds.filter((e) => examTopicMap[e].has(topicId));
    if (activeExams.length > 0) {
      const key = activeExams.join(' & ');
      let group = combinationGroups.get(key);
      if (!group) {
        group = { examIds: activeExams, topicIds: [] };
        combinationGroups.set(key, group);
      }
      group.topicIds.push(topicId);
    }
  }

  // Convert to UpSetCombination array
  const combinations: UpSetCombination[] = [];
  for (const [key, group] of combinationGroups.entries()) {
    combinations.push({
      key,
      examIds: group.examIds,
      topicIds: group.topicIds,
      topics: group.topicIds.map((tid) => topicLookup[tid] || { topic_id: tid, topic_title: tid, domain: '', sub_domain: '', description: '' }),
      cardinality: group.topicIds.length,
      degree: group.examIds.length,
    });
  }

  // Sort descending by cardinality (as per test specification)
  combinations.sort((a, b) => {
    if (b.cardinality !== a.cardinality) {
      return b.cardinality - a.cardinality;
    }
    return b.degree - a.degree;
  });

  const totalCombinationsCount = combinations.length;
  const cappedCombinations = combinations.slice(0, maxCombinationsCap);

  return {
    combinations: cappedCombinations,
    totalUniqueTopics: allTopicIds.size,
    totalCombinationsCount,
  };
}

/**
 * Calculates Jaccard similarity = |A ∩ B| / |A ∪ B|.
 */
export function calculateJaccardSimilarity(setA: Set<string>, setB: Set<string>): number {
  if (setA.size === 0 && setB.size === 0) return 1.0;
  let intersectionCount = 0;
  for (const item of setA) {
    if (setB.has(item)) intersectionCount++;
  }
  const unionSize = setA.size + setB.size - intersectionCount;
  if (unionSize === 0) return 0.0;
  return intersectionCount / unionSize;
}

/**
 * Calculates Szymkiewicz-Simpson Overlap Coefficient = |A ∩ B| / min(|A|, |B|).
 */
export function calculateOverlapCoefficient(setA: Set<string>, setB: Set<string>): number {
  const minLen = Math.min(setA.size, setB.size);
  if (minLen === 0) return 0.0;
  let intersectionCount = 0;
  for (const item of setA) {
    if (setB.has(item)) intersectionCount++;
  }
  return intersectionCount / minLen;
}

/**
 * Computes pairwise metrics between all selected exams.
 */
export function calculateAllPairwiseMetrics(
  selectedExamIds: string[],
  examTopicMap: Record<string, Set<string>>
): PairwiseMetric[] {
  const metrics: PairwiseMetric[] = [];
  for (let i = 0; i < selectedExamIds.length; i++) {
    for (let j = i + 1; j < selectedExamIds.length; j++) {
      const a = selectedExamIds[i];
      const b = selectedExamIds[j];
      const setA = examTopicMap[a] || new Set();
      const setB = examTopicMap[b] || new Set();

      let shared = 0;
      for (const t of setA) {
        if (setB.has(t)) shared++;
      }
      const uniqueA = setA.size - shared;
      const uniqueB = setB.size - shared;

      metrics.push({
        examA: a,
        examB: b,
        intersectionCount: shared,
        jaccardSimilarity: calculateJaccardSimilarity(setA, setB),
        overlapCoefficient: calculateOverlapCoefficient(setA, setB),
        uniqueToA: uniqueA,
        uniqueToB: uniqueB,
      });
    }
  }
  return metrics;
}

/**
 * Geometric centroid specifications for Venn diagram regions.
 * Scaled for responsive SVG coordinate systems.
 */
export const VENN_CENTROIDS_2_SET: Record<number, { x: number; y: number }> = {
  1: { x: 195, y: 220 }, // A only
  2: { x: 425, y: 220 }, // B only
  3: { x: 310, y: 220 }, // A & B
};

export const VENN_CENTROIDS_3_SET: Record<number, { x: number; y: number }> = {
  1: { x: 320, y: 120 }, // A only (Top)
  2: { x: 205, y: 325 }, // B only (Bottom-Left)
  4: { x: 435, y: 325 }, // C only (Bottom-Right)
  3: { x: 242, y: 210 }, // A & B (Top-Left)
  5: { x: 398, y: 210 }, // A & C (Top-Right)
  6: { x: 320, y: 345 }, // B & C (Bottom-Center)
  7: { x: 320, y: 250 }, // A & B & C (Center)
};

export const VENN_CENTROIDS_4_SET: Record<number, { x: number; y: number }> = {
  1: { x: 200, y: 350 }, // A only
  2: { x: 430, y: 265 }, // B only
  3: { x: 270, y: 375 }, // A & B
  4: { x: 325, y: 265 }, // C only
  5: { x: 260, y: 220 }, // A & C
  6: { x: 375, y: 395 }, // B & C
  7: { x: 305, y: 315 }, // A & B & C
  8: { x: 550, y: 350 }, // D only
  9: { x: 375, y: 140 }, // A & D
  10: { x: 490, y: 220 }, // B & D
  11: { x: 430, y: 175 }, // A & B & D
  12: { x: 480, y: 375 }, // C & D
  13: { x: 320, y: 175 }, // A & C & D
  14: { x: 445, y: 315 }, // B & C & D
  15: { x: 375, y: 250 }, // A & B & C & D (All 4)
};

/**
 * Calculates disjoint regions for dynamic Venn diagram (2, 3, or 4 sets).
 */
export function calculateVennRegions(
  selectedExamIds: string[],
  examTopicMap: Record<string, Set<string>>,
  topicLookup: Record<string, TopicRecord>,
  examShortCodes: Record<string, string> = {}
): {
  regions: VennRegion[];
  k: number;
} {
  const k = selectedExamIds.length;
  if (k < 2 || k > 4) {
    return { regions: [], k };
  }

  const numRegions = (1 << k) - 1; // 3 for 2 sets, 7 for 3 sets, 15 for 4 sets
  const regionTopicsMap = new Map<number, string[]>();
  for (let m = 1; m <= numRegions; m++) {
    regionTopicsMap.set(m, []);
  }

  // Find all unique topics across selected exams
  const allTopicIds = new Set<string>();
  for (const id of selectedExamIds) {
    const s = examTopicMap[id];
    if (s) {
      for (const t of s) allTopicIds.add(t);
    }
  }

  // Assign each topic to its exact bitmask
  for (const topicId of allTopicIds) {
    let mask = 0;
    for (let i = 0; i < k; i++) {
      const examId = selectedExamIds[i];
      if (examTopicMap[examId]?.has(topicId)) {
        mask |= (1 << i);
      }
    }
    if (mask > 0 && mask <= numRegions) {
      regionTopicsMap.get(mask)!.push(topicId);
    }
  }

  // Get centroid coordinate map based on k
  const centroidMap =
    k === 2
      ? VENN_CENTROIDS_2_SET
      : k === 3
      ? VENN_CENTROIDS_3_SET
      : VENN_CENTROIDS_4_SET;

  const regions: VennRegion[] = [];
  for (let m = 1; m <= numRegions; m++) {
    const topicIds = regionTopicsMap.get(m) || [];
    const participatingExamIds: string[] = [];
    const participatingShortCodes: string[] = [];

    for (let i = 0; i < k; i++) {
      if ((m & (1 << i)) !== 0) {
        const eid = selectedExamIds[i];
        participatingExamIds.push(eid);
        participatingShortCodes.push(examShortCodes[eid] || eid);
      }
    }

    let label = '';
    if (participatingExamIds.length === 1) {
      label = `${participatingShortCodes[0]} Only`;
    } else if (participatingExamIds.length === k) {
      label = `Core Common (${participatingShortCodes.join(' ∩ ')})`;
    } else {
      label = participatingShortCodes.join(' ∩ ');
    }

    const defaultCentroid = { x: 300, y: 250 };
    const centroid = centroidMap[m] || defaultCentroid;

    regions.push({
      mask: m,
      participatingExamIds,
      topicIds,
      topics: topicIds.map((tid) => topicLookup[tid] || { topic_id: tid, topic_title: tid, domain: '', sub_domain: '', description: '' }),
      cardinality: topicIds.length,
      degree: participatingExamIds.length,
      centroid,
      label,
    });
  }

  return { regions, k };
}
