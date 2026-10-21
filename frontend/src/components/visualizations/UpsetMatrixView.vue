<template>
  <div class="upset-matrix-container w-full bg-slate-900 rounded-xl border border-slate-800 p-4 sm:p-6 space-y-5">
    <!-- View Header and Toolbar -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800">
      <div>
        <div class="flex items-center space-x-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          <h2 class="text-lg font-bold text-white tracking-wide">UpSet Overlap Matrix View</h2>
          <span class="px-2 py-0.5 text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded">
            Disjoint Combinations
          </span>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Decomposes all overlapping syllabi into mutually exclusive disjoint subsets. Columns represent exclusive exam intersections.
        </p>
      </div>

      <!-- Controls: Sort Mode & Capping Indicator -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- Sort Control -->
        <div class="flex items-center space-x-1.5 bg-slate-850 px-2.5 py-1.5 rounded-lg border border-slate-800 text-xs">
          <span class="text-slate-400">Sort:</span>
          <select
            v-model="sortMode"
            class="bg-slate-800 text-white border-0 text-xs rounded px-2 py-1 focus:ring-1 focus:ring-emerald-500 outline-none cursor-pointer"
          >
            <option value="cardinality_desc">Cardinality (High to Low)</option>
            <option value="degree_desc">Degree (Most Exams First)</option>
            <option value="degree_asc">Degree (Least Exams First)</option>
          </select>
        </div>

        <!-- Metric Badges -->
        <div class="flex items-center space-x-2 text-xs">
          <span class="px-2.5 py-1.5 rounded-lg bg-slate-850 border border-slate-800 text-slate-300 font-mono">
            <strong class="text-emerald-400">{{ activeCombinations.length }}</strong> Combinations
          </span>
          <span class="px-2.5 py-1.5 rounded-lg bg-slate-850 border border-slate-800 text-slate-300 font-mono">
            <strong class="text-emerald-400">{{ totalUniqueTopics }}</strong> Topics in Union
          </span>
        </div>
      </div>
    </div>

    <!-- Boundary Notification / Information Banners -->
    <div v-if="selectedExamIds.length === 0" class="p-8 text-center bg-slate-850 rounded-xl border border-slate-800 space-y-2">
      <div class="w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto text-base">⚠️</div>
      <h3 class="text-sm font-semibold text-white">No Examinations Selected</h3>
      <p class="text-xs text-slate-400 max-w-sm mx-auto">
        Please select at least one examination from the exam catalog or top toolbar to generate the UpSet intersection matrix.
      </p>
    </div>

    <div v-else-if="selectedExamIds.length === 1" class="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg text-xs text-blue-300 flex items-center justify-between">
      <span>
        Single exam selection boundary active: showing all <strong>{{ totalUniqueTopics }}</strong> topics for <strong>{{ selectedExamIds[0] }}</strong>. Add more exams to analyze multi-way syllabus overlaps.
      </span>
      <span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-200 font-mono text-[10px]">Degree 1</span>
    </div>

    <div v-else-if="totalCombinationsCount > 50" class="p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-300 flex items-center justify-between">
      <span>
        Large set selection: <strong>{{ totalCombinationsCount }}</strong> disjoint intersections generated. Displaying top <strong>50</strong> combinations capped for visualization clarity.
      </span>
      <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-200 font-mono text-[10px]">Capped at 50</span>
    </div>

    <!-- Main SVG Visualization Canvas -->
    <div
      v-if="selectedExamIds.length > 0 && activeCombinations.length > 0"
      class="upset-svg-viewport relative overflow-x-auto overflow-y-hidden rounded-xl bg-slate-950 border border-slate-800"
      ref="containerRef"
    >
      <svg
        :width="svgWidth"
        :height="svgHeight"
        class="block font-sans select-none"
      >
        <defs>
          <linearGradient id="upsetBarGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#34D399" />
            <stop offset="100%" stop-color="#10B981" />
          </linearGradient>
          <linearGradient id="upsetBarGradientHover" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#38BDF8" />
            <stop offset="100%" stop-color="#0284C7" />
          </linearGradient>
          <linearGradient id="leftBarGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#475569" />
            <stop offset="100%" stop-color="#64748B" />
          </linearGradient>
        </defs>

        <!-- TOP BAR CHART: Cardinality of Disjoint Intersections -->
        <g class="top-bar-chart">
          <!-- Background Chart Grid Lines -->
          <line
            v-for="tick in topTicks"
            :key="'grid-' + tick"
            :x1="layout.leftMargin"
            :y1="yScaleTop(tick)"
            :x2="svgWidth - 20"
            :y2="yScaleTop(tick)"
            stroke="#1E293B"
            stroke-dasharray="3 3"
            stroke-width="1"
          />
          <text
            v-for="tick in topTicks"
            :key="'tick-label-' + tick"
            :x="layout.leftMargin - 8"
            :y="yScaleTop(tick) + 3"
            text-anchor="end"
            fill="#64748B"
            font-size="9"
            font-family="monospace"
          >
            {{ tick }}
          </text>

          <!-- Top Intersection Bars -->
          <g
            v-for="(comb, colIdx) in activeCombinations"
            :key="'bar-' + comb.key"
            class="transition-opacity duration-150"
            :opacity="hoveredCombKey && hoveredCombKey !== comb.key ? 0.4 : 1"
          >
            <rect
              :x="colX(colIdx) - layout.colWidth * 0.35"
              :y="yScaleTop(comb.cardinality)"
              :width="layout.colWidth * 0.7"
              :height="Math.max(2, layout.topHeight - 20 - yScaleTop(comb.cardinality))"
              :fill="isCombActive(comb.key) ? 'url(#upsetBarGradientHover)' : 'url(#upsetBarGradient)'"
              rx="3"
              class="transition-colors duration-150"
            />
            <!-- Number on top of bar -->
            <text
              :x="colX(colIdx)"
              :y="yScaleTop(comb.cardinality) - 5"
              text-anchor="middle"
              :fill="isCombActive(comb.key) ? '#38BDF8' : '#F1F5F9'"
              font-size="10"
              font-weight="bold"
              font-family="monospace"
            >
              {{ comb.cardinality }}
            </text>
          </g>

          <!-- Top Axis Baseline -->
          <line
            :x1="layout.leftMargin"
            :y1="layout.topHeight - 20"
            :x2="svgWidth - 20"
            :y2="layout.topHeight - 20"
            stroke="#334155"
            stroke-width="1.5"
          />
          <!-- Top Chart Axis Label -->
          <text
            :x="layout.leftMargin - 8"
            :y="16"
            text-anchor="end"
            fill="#94A3B8"
            font-size="10"
            font-weight="bold"
          >
            Intersection Size
          </text>
        </g>

        <!-- LEFT BAR CHART & MATRIX ROWS -->
        <g class="matrix-rows">
          <!-- Zebra Row Backgrounds -->
          <rect
            v-for="(examId, rowIdx) in selectedExamIds"
            :key="'row-bg-' + examId"
            :x="10"
            :y="rowY(rowIdx) - layout.rowHeight / 2"
            :width="svgWidth - 30"
            :height="layout.rowHeight"
            :fill="rowIdx % 2 === 0 ? '#151F32' : 'transparent'"
            rx="4"
          />

          <!-- Exam Row Labels and Total Set Sizes -->
          <g
            v-for="(examId, rowIdx) in selectedExamIds"
            :key="'exam-row-' + examId"
          >
            <!-- Exam Short Code / Title -->
            <text
              :x="layout.leftLabelWidth"
              :y="rowY(rowIdx) + 4"
              text-anchor="end"
              fill="#E2E8F0"
              font-size="11"
              font-weight="600"
              class="cursor-default"
            >
              {{ getExamShortCode(examId) }}
            </text>

            <!-- Exam Set Size Horizontal Bar -->
            <rect
              :x="layout.leftLabelWidth + 12"
              :y="rowY(rowIdx) - 6"
              :width="examBarWidth(examId)"
              :height="12"
              fill="url(#leftBarGradient)"
              rx="2"
            />
            <!-- Set Size Number Label -->
            <text
              :x="layout.leftLabelWidth + 16 + examBarWidth(examId)"
              :y="rowY(rowIdx) + 3"
              fill="#94A3B8"
              font-size="9"
              font-family="monospace"
              font-weight="bold"
            >
              {{ examSetSizes[examId] || 0 }}
            </text>
          </g>

          <!-- Left Chart Header Label -->
          <text
            :x="layout.leftLabelWidth"
            :y="layout.topHeight - 8"
            text-anchor="end"
            fill="#94A3B8"
            font-size="10"
            font-weight="bold"
          >
            Total Topics per Exam
          </text>
        </g>

        <!-- CENTRAL COMBINATION MATRIX (Circles & Connectors) -->
        <g class="combination-matrix">
          <!-- Column Connectors (Degree >= 2) -->
          <line
            v-for="(comb, colIdx) in activeCombinations"
            v-show="comb.degree >= 2"
            :key="'conn-' + comb.key"
            :x1="colX(colIdx)"
            :y1="connectorYMin(comb)"
            :x2="colX(colIdx)"
            :y2="connectorYMax(comb)"
            :stroke="isCombActive(comb.key) ? '#38BDF8' : '#10B981'"
            stroke-width="3"
            stroke-linecap="round"
          />

          <!-- Matrix Dot Glyphs (Filled = Active, Unfilled = Inactive) -->
          <template v-for="(comb, colIdx) in activeCombinations" :key="'matrix-col-' + comb.key">
            <circle
              v-for="(examId, rowIdx) in selectedExamIds"
              :key="'dot-' + comb.key + '-' + examId"
              :cx="colX(colIdx)"
              :cy="rowY(rowIdx)"
              :r="isExamInComb(comb, examId) ? 7 : 4.5"
              :fill="isExamInComb(comb, examId) ? (isCombActive(comb.key) ? '#38BDF8' : '#10B981') : '#0F172A'"
              :stroke="isExamInComb(comb, examId) ? (isCombActive(comb.key) ? '#0284C7' : '#047857') : '#334155'"
              :stroke-width="isExamInComb(comb, examId) ? 2 : 1.5"
              class="transition-all duration-150"
            />
          </template>

          <!-- Interactive Column Hit Areas (Hover & Click) -->
          <rect
            v-for="(comb, colIdx) in activeCombinations"
            :key="'hit-' + comb.key"
            :x="colX(colIdx) - layout.colWidth / 2"
            :y="0"
            :width="layout.colWidth"
            :height="svgHeight"
            fill="transparent"
            class="cursor-pointer"
            @mouseenter="onHoverCombination(comb, $event)"
            @mousemove="onMoveTooltip($event)"
            @mouseleave="onLeaveCombination"
            @click="onClickCombination(comb)"
          />

          <!-- Active Column Highlight Halo -->
          <rect
            v-if="hoveredCombKey || vizStore.pinnedCombinationKey"
            :x="colX(activeColIndex) - layout.colWidth / 2"
            :y="0"
            :width="layout.colWidth"
            :height="svgHeight"
            fill="#38BDF8"
            fill-opacity="0.08"
            stroke="#38BDF8"
            stroke-width="1.5"
            stroke-opacity="0.4"
            rx="4"
            pointer-events="none"
          />
        </g>
      </svg>

      <!-- Floating Interactive Tooltip -->
      <div
        v-if="tooltip.visible"
        class="fixed z-50 pointer-events-none px-3 py-2.5 rounded-lg bg-slate-900/95 border border-slate-700 shadow-2xl backdrop-blur-md text-xs space-y-1.5 max-w-xs transition-opacity duration-150"
        :style="{ left: tooltip.x + 14 + 'px', top: tooltip.y + 14 + 'px' }"
      >
        <div class="flex items-center justify-between gap-3">
          <span class="font-bold text-white">{{ tooltip.title }}</span>
          <span class="px-1.5 py-0.5 rounded font-mono font-bold text-[10px] bg-emerald-500/20 text-emerald-300">
            {{ tooltip.cardinality }} Topics
          </span>
        </div>
        <div class="text-[11px] text-slate-300">
          <span class="text-slate-400">Participating Exams:</span>
          <div class="flex flex-wrap gap-1 mt-1">
            <span
              v-for="e in tooltip.exams"
              :key="e"
              class="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-200 text-[10px]"
            >
              {{ getExamShortCode(e) }}
            </span>
          </div>
        </div>
        <div v-if="tooltip.sampleTopics.length > 0" class="pt-1 border-t border-slate-800 text-[10px] text-slate-400">
          <span class="text-slate-500">Sample topics:</span>
          <ul class="list-disc list-inside mt-0.5 space-y-0.5 text-slate-300">
            <li v-for="t in tooltip.sampleTopics" :key="t" class="truncate">{{ t }}</li>
          </ul>
        </div>
        <div class="pt-1 text-[9px] text-emerald-400 font-medium">
          Click column to lock & explore in syllabus drawer
        </div>
      </div>
    </div>

    <!-- Active Intersection Detail Drawer / Topic Inspector -->
    <div
      v-if="pinnedCombination"
      class="mt-4 p-4 rounded-xl bg-slate-850 border border-slate-700 space-y-3"
    >
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-800">
        <div>
          <div class="flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <h3 class="text-sm font-bold text-white">
              Selected Intersection: {{ pinnedCombination.key }}
            </h3>
            <span class="px-2 py-0.5 rounded font-mono font-bold text-xs bg-sky-500/20 text-sky-300 border border-sky-500/30">
              {{ pinnedCombination.cardinality }} Exclusive Topics
            </span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5">
            These topics are exclusively required by precisely this group of examinations and zero other selected exams.
          </p>
        </div>
        <button
          @click="clearActiveIntersection"
          class="self-start sm:self-auto px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs border border-slate-700 transition-colors"
        >
          Clear Selection
        </button>
      </div>

      <!-- Topic Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-64 overflow-y-auto pr-1">
        <div
          v-for="topic in pinnedCombination.topics"
          :key="topic.topic_id"
          class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-emerald-500/40 transition-colors space-y-1"
          @mouseenter="vizStore.setHoveredTopic(topic.topic_id)"
          @mouseleave="vizStore.setHoveredTopic(null)"
        >
          <div class="flex items-center justify-between gap-1">
            <span class="text-[10px] font-mono text-emerald-400 truncate">{{ topic.domain }}</span>
            <span class="text-[9px] font-mono text-slate-500 truncate">{{ topic.sub_domain }}</span>
          </div>
          <div class="text-xs font-semibold text-slate-200 line-clamp-1" :title="topic.topic_title">
            {{ topic.topic_title }}
          </div>
          <p class="text-[10px] text-slate-400 line-clamp-2">{{ topic.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import * as d3 from 'd3';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import {
  loadTaxonomyData,
  getFilteredExamTopicMap,
  calculateUpSetCombinations,
} from '@/services/syllabusDataService';
import type { UpSetCombination, TopicTaxonomyDetail, TopicRecord } from '@/types/syllabus';

const vizStore = useSyllabusVisualizationStore();
const examStore = useExamMasterStore();

// Reactive State
const sortMode = ref<'cardinality_desc' | 'degree_desc' | 'degree_asc'>('cardinality_desc');
const hoveredCombKey = ref<string | null>(null);
const containerRef = ref<HTMLElement | null>(null);

const rawTaxonomy = ref<Record<string, TopicTaxonomyDetail>>({});
const isLoading = ref<boolean>(true);

// Layout Constants
const layout = {
  leftLabelWidth: 140,
  leftChartWidth: 90,
  leftMargin: 250, // leftLabelWidth + leftChartWidth + padding
  topHeight: 140,
  colWidth: 36,
  rowHeight: 34,
};

// Tooltip State
const tooltip = ref<{
  visible: boolean;
  x: number;
  y: number;
  title: string;
  exams: string[];
  cardinality: number;
  sampleTopics: string[];
}>({
  visible: false,
  x: 0,
  y: 0,
  title: '',
  exams: [],
  cardinality: 0,
  sampleTopics: [],
});

// Load taxonomy data on mount
onMounted(async () => {
  try {
    const data = await loadTaxonomyData();
    rawTaxonomy.value = data.lookup;
  } finally {
    isLoading.value = false;
  }
});

const selectedExamIds = computed(() => vizStore.selectedExamIds);

// Filtered Exam-Topic Map
const filteredData = computed(() => {
  return getFilteredExamTopicMap(
    selectedExamIds.value,
    rawTaxonomy.value,
    vizStore.selectedDomain,
    vizStore.minDepthLevel
  );
});

// Exam Set Sizes (Left Chart)
const examSetSizes = computed<Record<string, number>>(() => {
  const sizes: Record<string, number> = {};
  for (const id of selectedExamIds.value) {
    sizes[id] = filteredData.value.examTopicMap[id]?.size || 0;
  }
  return sizes;
});

const maxSetSize = computed(() => {
  const values = Object.values(examSetSizes.value);
  return values.length > 0 ? Math.max(...values, 1) : 1;
});

function examBarWidth(examId: string): number {
  const size = examSetSizes.value[examId] || 0;
  return (size / maxSetSize.value) * layout.leftChartWidth;
}

// UpSet Combinations Computation
const calculatedUpSet = computed(() => {
  return calculateUpSetCombinations(
    filteredData.value.examTopicMap,
    filteredData.value.topicLookup,
    50
  );
});

const totalUniqueTopics = computed(() => calculatedUpSet.value.totalUniqueTopics);
const totalCombinationsCount = computed(() => calculatedUpSet.value.totalCombinationsCount);

// Sorted Active Combinations
const activeCombinations = computed<UpSetCombination[]>(() => {
  const list = [...calculatedUpSet.value.combinations];
  if (sortMode.value === 'cardinality_desc') {
    list.sort((a, b) => b.cardinality - a.cardinality || b.degree - a.degree);
  } else if (sortMode.value === 'degree_desc') {
    list.sort((a, b) => b.degree - a.degree || b.cardinality - a.cardinality);
  } else if (sortMode.value === 'degree_asc') {
    list.sort((a, b) => a.degree - b.degree || b.cardinality - a.cardinality);
  }
  return list;
});

// Pinned Combination Details
const pinnedCombination = computed<UpSetCombination | null>(() => {
  if (!vizStore.pinnedCombinationKey) return null;
  return (
    activeCombinations.value.find((c) => c.key === vizStore.pinnedCombinationKey) || null
  );
});

// Coordinate Calculations
const svgWidth = computed(() => {
  const cols = activeCombinations.value.length;
  return Math.max(760, layout.leftMargin + cols * layout.colWidth + 40);
});

const svgHeight = computed(() => {
  const rows = selectedExamIds.value.length;
  return layout.topHeight + rows * layout.rowHeight + 30;
});

const maxCardinality = computed(() => {
  if (activeCombinations.value.length === 0) return 10;
  return Math.max(...activeCombinations.value.map((c) => c.cardinality), 1);
});

const topTicks = computed(() => {
  const max = maxCardinality.value;
  return [Math.round(max * 0.25), Math.round(max * 0.5), Math.round(max * 0.75), max].filter(
    (v, i, arr) => arr.indexOf(v) === i && v > 0
  );
});

function colX(colIdx: number): number {
  return layout.leftMargin + colIdx * layout.colWidth + layout.colWidth / 2;
}

function rowY(rowIdx: number): number {
  return layout.topHeight + rowIdx * layout.rowHeight + layout.rowHeight / 2;
}

function yScaleTop(cardinality: number): number {
  const scale = d3
    .scaleLinear()
    .domain([0, maxCardinality.value])
    .range([layout.topHeight - 20, 25]);
  return scale(cardinality);
}

function isExamInComb(comb: UpSetCombination, examId: string): boolean {
  return comb.examIds.includes(examId);
}

function connectorYMin(comb: UpSetCombination): number {
  const indices = comb.examIds
    .map((eid) => selectedExamIds.value.indexOf(eid))
    .filter((idx) => idx >= 0);
  if (indices.length === 0) return 0;
  return rowY(Math.min(...indices));
}

function connectorYMax(comb: UpSetCombination): number {
  const indices = comb.examIds
    .map((eid) => selectedExamIds.value.indexOf(eid))
    .filter((idx) => idx >= 0);
  if (indices.length === 0) return 0;
  return rowY(Math.max(...indices));
}

function isCombActive(combKey: string): boolean {
  return hoveredCombKey.value === combKey || vizStore.pinnedCombinationKey === combKey;
}

const activeColIndex = computed(() => {
  const key = hoveredCombKey.value || vizStore.pinnedCombinationKey;
  if (!key) return -1;
  return activeCombinations.value.findIndex((c) => c.key === key);
});

function getExamShortCode(examId: string): string {
  const exam = examStore.examsMap[examId];
  if (exam && exam.short_code) return exam.short_code;
  return examId.replace(/^(UPSC_|PSU_)/, '');
}

// Interaction Handlers
function onHoverCombination(comb: UpSetCombination, event: MouseEvent) {
  hoveredCombKey.value = comb.key;
  tooltip.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    title: comb.degree === 1 ? 'Single Exam Module' : `${comb.degree}-Exam Intersection`,
    exams: comb.examIds,
    cardinality: comb.cardinality,
    sampleTopics: comb.topics.slice(0, 4).map((t) => t.topic_title),
  };
}

function onMoveTooltip(event: MouseEvent) {
  tooltip.value.x = event.clientX;
  tooltip.value.y = event.clientY;
}

function onLeaveCombination() {
  hoveredCombKey.value = null;
  tooltip.value.visible = false;
}

function onClickCombination(comb: UpSetCombination) {
  if (vizStore.pinnedCombinationKey === comb.key) {
    vizStore.setActiveIntersection([]);
  } else {
    vizStore.setActiveIntersection(comb.topicIds, comb.key);
  }
}

function clearActiveIntersection() {
  vizStore.setActiveIntersection([]);
}
</script>

<style scoped>
.upset-matrix-container {
  font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
}
</style>
