<template>
  <div class="space-y-6">
    <!-- View Header -->
    <div class="bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          <h2 class="text-lg font-bold text-white tracking-wide">Multi-Exam Overlap & Topic Synergy</h2>
          <span class="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full">
            {{ selectedExamIds.length }} Exams Compared
          </span>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Instant pairwise overlap percentages and shared topic analysis across all your selected Grade A cadres.
        </p>
      </div>

      <!-- Quick Metrics -->
      <div class="flex items-center space-x-3 text-xs bg-slate-850 border border-slate-800 rounded-xl px-4 py-2">
        <div>
          <span class="text-slate-400 block text-[10px] uppercase font-semibold">Total Union Topics</span>
          <span class="text-white font-mono font-bold text-sm">{{ totalUnionTopicsCount }}</span>
        </div>
        <div class="w-px h-6 bg-slate-700"></div>
        <div>
          <span class="text-slate-400 block text-[10px] uppercase font-semibold">Universal Topics</span>
          <span class="text-emerald-400 font-mono font-bold text-sm">{{ universalTopicsCount }}</span>
        </div>
      </div>
    </div>

    <!-- Pairwise Overlap Heatmap Grid -->
    <div class="bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-lg space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <span>Pairwise Overlap Matrix</span>
          <span class="text-xs font-normal text-slate-400 lowercase">(click any cell to inspect common topics)</span>
        </h3>
        <span class="text-xs text-slate-400">Higher % = More shared syllabus</span>
      </div>

      <!-- Responsive Matrix Table -->
      <div class="overflow-x-auto rounded-xl border border-slate-800">
        <table class="w-full text-xs text-left border-collapse">
          <thead>
            <tr class="bg-slate-850 border-b border-slate-800">
              <th class="p-3 font-semibold text-slate-400 sticky left-0 bg-slate-850 z-10">Exam</th>
              <th
                v-for="eid in selectedExamIds"
                :key="eid"
                class="p-3 font-mono font-bold text-center text-slate-200 border-l border-slate-800"
              >
                {{ getExamCode(eid) }}
                <div class="text-[10px] font-normal text-slate-400">{{ getExamTopicCount(eid) }} topics</div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="rowEid in selectedExamIds"
              :key="rowEid"
              class="border-b border-slate-800/60 hover:bg-slate-800/30 transition-colors"
            >
              <td class="p-3 font-semibold text-white sticky left-0 bg-slate-900 z-10 flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: getExamColor(rowEid) }"></span>
                <span class="font-mono font-bold">{{ getExamCode(rowEid) }}</span>
                <span class="text-[11px] text-slate-400 truncate max-w-[130px] hidden sm:inline">{{ getExamTitle(rowEid) }}</span>
              </td>

              <td
                v-for="colEid in selectedExamIds"
                :key="colEid"
                @click="onSelectPair(rowEid, colEid)"
                class="p-3 text-center border-l border-slate-800 cursor-pointer transition-all"
                :class="getCellBg(rowEid, colEid)"
              >
                <div v-if="rowEid === colEid" class="font-mono text-slate-500 font-bold">100%</div>
                <div v-else>
                  <div class="font-mono font-bold" :class="getPercentColor(getOverlapPct(rowEid, colEid))">
                    {{ getOverlapPct(rowEid, colEid) }}%
                  </div>
                  <div class="text-[10px] text-slate-400">
                    {{ getSharedCount(rowEid, colEid) }} shared
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Active Pairwise or Universal Shared Topics Inspection -->
    <div class="bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-lg space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div>
          <div class="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
            {{ activeInspectionTitle }}
          </div>
          <h3 class="text-base font-bold text-white mt-0.5">
            {{ activeTopicsList.length }} Common Audited Topics
          </h3>
        </div>

        <!-- Filter / Search within common topics -->
        <div class="flex items-center space-x-2">
          <input
            v-model="topicSearch"
            type="text"
            placeholder="Filter common topics..."
            class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 w-48 sm:w-60"
          />
          <button
            v-if="activePair"
            @click="activePair = null"
            class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors"
            title="Reset to all selected exams"
          >
            Show All
          </button>
        </div>
      </div>

      <!-- Topics Grid -->
      <div v-if="displayedTopics.length === 0" class="py-8 text-center text-slate-400 text-xs">
        No topics match your current filter.
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div
          v-for="topic in displayedTopics"
          :key="topic.topic_id"
          class="p-3 rounded-xl bg-slate-850 border border-slate-800 hover:border-slate-700 transition-colors flex flex-col justify-between space-y-2"
        >
          <div class="space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span class="px-2 py-0.5 rounded font-medium bg-slate-800 text-slate-300 border border-slate-700">
                {{ topic.domain }}
              </span>
              <span class="text-slate-400 font-mono text-[10px]">{{ topic.topic_id }}</span>
            </div>
            <h4 class="text-xs font-bold text-white leading-snug">{{ topic.topic_title }}</h4>
            <p v-if="topic.description" class="text-[11px] text-slate-400 line-clamp-2">{{ topic.description }}</p>
          </div>

          <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
            <span>Sub-domain: <strong class="text-slate-300">{{ topic.sub_domain }}</strong></span>
            <span class="text-emerald-400 font-medium">Audited in {{ getTopicExamDegree(topic.topic_id) }} of {{ selectedExamIds.length }} exams</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useSyllabusVisualizationStore, CLUSTER_COLORS } from '@/stores/useSyllabusVisualizationStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import type { TopicRecord } from '@/types/syllabus';

const vizStore = useSyllabusVisualizationStore();
const examStore = useExamMasterStore();

const topicSearch = ref('');
const activePair = ref<[string, string] | null>(null);

const selectedExamIds = computed(() => vizStore.selectedExamIds);

function getExamCode(examId: string): string {
  return examStore.examsMap[examId]?.short_code || examId.replace(/^(UPSC_|PSU_)/, '');
}

function getExamTitle(examId: string): string {
  return examStore.examsMap[examId]?.title || examId;
}

function getExamColor(examId: string): string {
  const cat = examStore.examsMap[examId]?.category;
  return CLUSTER_COLORS[cat || 'Central-Civil'] || '#10B981';
}

function getExamTopicCount(examId: string): number {
  return vizStore.examTopicMap[examId]?.size || 0;
}

// Pairwise shared topics
function getSharedTopicIds(examA: string, examB: string): string[] {
  const setA = vizStore.examTopicMap[examA];
  const setB = vizStore.examTopicMap[examB];
  if (!setA || !setB) return [];

  const shared: string[] = [];
  for (const tid of setA) {
    if (setB.has(tid)) {
      shared.push(tid);
    }
  }
  return shared;
}

function getSharedCount(examA: string, examB: string): number {
  return getSharedTopicIds(examA, examB).length;
}

function getOverlapPct(examA: string, examB: string): number {
  const count = getSharedCount(examA, examB);
  const sizeA = getExamTopicCount(examA);
  const sizeB = getExamTopicCount(examB);
  const minSize = Math.min(sizeA, sizeB);
  if (minSize === 0) return 0;
  return Math.round((count / minSize) * 100);
}

function getCellBg(examA: string, examB: string): string {
  if (activePair.value && ((activePair.value[0] === examA && activePair.value[1] === examB) || (activePair.value[0] === examB && activePair.value[1] === examA))) {
    return 'bg-emerald-500/20 ring-1 ring-emerald-500/50';
  }
  if (examA === examB) return 'bg-slate-850/50';
  const pct = getOverlapPct(examA, examB);
  if (pct >= 60) return 'bg-emerald-500/15 hover:bg-emerald-500/25';
  if (pct >= 35) return 'bg-sky-500/10 hover:bg-sky-500/20';
  if (pct > 0) return 'bg-slate-800/40 hover:bg-slate-800/70';
  return 'hover:bg-slate-800/40';
}

function getPercentColor(pct: number): string {
  if (pct >= 60) return 'text-emerald-400';
  if (pct >= 35) return 'text-sky-400';
  if (pct > 0) return 'text-amber-400';
  return 'text-slate-500';
}

function onSelectPair(examA: string, examB: string) {
  if (examA === examB) {
    activePair.value = null;
  } else {
    activePair.value = [examA, examB];
  }
}

// Overall Union & Universal
const totalUnionTopicsCount = computed(() => {
  const union = new Set<string>();
  for (const eid of selectedExamIds.value) {
    const set = vizStore.examTopicMap[eid];
    if (set) {
      for (const t of set) union.add(t);
    }
  }
  return union.size;
});

const universalTopicsCount = computed(() => {
  if (selectedExamIds.value.length === 0) return 0;
  let intersection: Set<string> | null = null;
  for (const eid of selectedExamIds.value) {
    const set = vizStore.examTopicMap[eid];
    if (!set) return 0;
    if (intersection === null) {
      intersection = new Set(set);
    } else {
      for (const t of intersection) {
        if (!set.has(t)) intersection.delete(t);
      }
    }
  }
  return intersection ? intersection.size : 0;
});

// Active Topics List
const activeInspectionTitle = computed(() => {
  if (activePair.value) {
    return `${getExamCode(activePair.value[0])} ⟷ ${getExamCode(activePair.value[1])} Common Syllabus`;
  }
  return `Core Topics Shared Across All Selected Examinations`;
});

const activeTopicsList = computed<TopicRecord[]>(() => {
  let ids: string[] = [];
  if (activePair.value) {
    ids = getSharedTopicIds(activePair.value[0], activePair.value[1]);
  } else {
    // Show topics shared by at least 2 exams
    const counts: Record<string, number> = {};
    for (const eid of selectedExamIds.value) {
      const set = vizStore.examTopicMap[eid];
      if (set) {
        for (const tid of set) {
          counts[tid] = (counts[tid] || 0) + 1;
        }
      }
    }
    ids = Object.keys(counts).filter((tid) => counts[tid] >= 2);
    // Sort by frequency
    ids.sort((a, b) => (counts[b] || 0) - (counts[a] || 0));
  }

  return ids.map((id) => vizStore.topicsMap[id]).filter(Boolean);
});

function getTopicExamDegree(topicId: string): number {
  let count = 0;
  for (const eid of selectedExamIds.value) {
    if (vizStore.examTopicMap[eid]?.has(topicId)) count++;
  }
  return count;
}

const displayedTopics = computed(() => {
  let list = activeTopicsList.value;
  if (vizStore.selectedDomain !== 'ALL') {
    list = list.filter((t) => t.domain === vizStore.selectedDomain);
  }
  if (topicSearch.value.trim()) {
    const q = topicSearch.value.toLowerCase().trim();
    list = list.filter(
      (t) =>
        t.topic_title.toLowerCase().includes(q) ||
        t.topic_id.toLowerCase().includes(q) ||
        t.sub_domain.toLowerCase().includes(q) ||
        (t.description && t.description.toLowerCase().includes(q))
    );
  }
  return list;
});
</script>