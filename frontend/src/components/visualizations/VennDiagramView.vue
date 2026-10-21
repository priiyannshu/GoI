<template>
  <div class="venn-diagram-container w-full bg-slate-900 rounded-xl border border-slate-800 p-4 sm:p-6 space-y-5">
    <!-- View Header and Toolbar -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800">
      <div>
        <div class="flex items-center space-x-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-sky-400"></span>
          <h2 class="text-lg font-bold text-white tracking-wide">Dynamic Venn Diagram View</h2>
          <span class="px-2 py-0.5 text-[11px] font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/30 rounded">
            {{ activeVennSetCount }}-Set Diagram ({{ activeRegionsCount }} Disjoint Regions)
          </span>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Interactive 2-set, 3-set, and 4-set Venn diagram with Edwards-Venn rotated ellipses. Click any region badge to inspect exclusive topics.
        </p>
      </div>

      <!-- Quick Exam Switcher / Selector Pills -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="text-xs text-slate-400 mr-1">Active Sets:</div>
        <div
          v-for="(examId, idx) in activeExamIds"
          :key="examId"
          class="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-slate-850 border text-xs font-medium"
          :style="{ borderColor: SET_COLORS[idx] + '60', color: SET_COLORS[idx] }"
        >
          <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: SET_COLORS[idx] }"></span>
          <span>{{ getExamShortCode(examId) }}</span>
          <span class="text-[10px] opacity-75 font-mono font-bold">({{ examSetSizes[examId] || 0 }})</span>
        </div>
      </div>
    </div>

    <!-- Boundary Notification / Empty States -->
    <!-- Case 1: Less than 2 exams selected -->
    <div
      v-if="selectedExamIds.length < 2"
      class="p-8 text-center bg-slate-850 rounded-xl border border-slate-800 space-y-3"
    >
      <div class="w-12 h-12 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 flex items-center justify-center mx-auto text-xl">
        ⭕
      </div>
      <h3 class="text-sm font-bold text-white">Minimum 2 Examinations Required</h3>
      <p class="text-xs text-slate-400 max-w-md mx-auto">
        Venn diagrams calculate intersecting regions among 2, 3, or 4 examinations. Please select at least two exams from the catalog to generate the diagram.
      </p>
      <div class="flex justify-center gap-2 pt-2">
        <button
          @click="addPresetDuo"
          class="px-3 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold shadow transition-colors"
        >
          Load UPSC CSE + RBI Grade B
        </button>
      </div>
    </div>

    <!-- Case 2: More than 4 exams selected (Cap Enforcement) -->
    <div
      v-else-if="selectedExamIds.length > 4"
      class="p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-xs text-amber-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
    >
      <div class="flex items-center space-x-2">
        <span class="text-amber-400 font-bold">⚠️ Venn Diagram Capped at 4 Exams:</span>
        <span>
          Planar Venn diagrams are geometrically capped at 4 sets (15 disjoint regions). Currently showing the first 4 exams.
        </span>
      </div>
      <button
        @click="vizStore.activeTab = 'upset'"
        class="self-start sm:self-auto px-3 py-1 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 font-semibold transition-colors"
      >
        Switch to UpSet Matrix (Unlimited)
      </button>
    </div>

    <!-- Venn Visualization Canvas (for 2, 3, or 4 exams) -->
    <div
      v-if="activeExamIds.length >= 2 && activeExamIds.length <= 4"
      class="venn-viewport relative overflow-x-auto rounded-xl bg-slate-950 border border-slate-800 p-2 sm:p-4"
    >
      <div class="flex justify-center">
        <!-- SVG Canvas -->
        <svg
          :width="currentLayout.width"
          :height="currentLayout.height"
          :viewBox="`0 0 ${currentLayout.width} ${currentLayout.height}`"
          class="block max-w-full font-sans select-none"
        >
          <defs>
            <!-- Radial glow filter for active region badges -->
            <filter id="badgeGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#38BDF8" flood-opacity="0.6" />
            </filter>
            <filter id="coreGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#10B981" flood-opacity="0.8" />
            </filter>
          </defs>

          <!-- 2-SET VENN GEOMETRY -->
          <g v-if="activeVennSetCount === 2" class="venn-2-set">
            <!-- Set A Circle -->
            <circle
              :cx="layout2Set.circleA.cx"
              :cy="layout2Set.circleA.cy"
              :r="layout2Set.circleA.r"
              fill="#10B981"
              fill-opacity="0.18"
              stroke="#10B981"
              stroke-width="2.5"
            />
            <!-- Set B Circle -->
            <circle
              :cx="layout2Set.circleB.cx"
              :cy="layout2Set.circleB.cy"
              :r="layout2Set.circleB.r"
              fill="#38BDF8"
              fill-opacity="0.18"
              stroke="#38BDF8"
              stroke-width="2.5"
            />

            <!-- Set Header Labels -->
            <text
              :x="layout2Set.circleA.cx - 60"
              :y="layout2Set.circleA.cy - layout2Set.circleA.r - 12"
              text-anchor="middle"
              fill="#10B981"
              font-size="13"
              font-weight="bold"
            >
              {{ getExamShortCode(activeExamIds[0]) }} ({{ examSetSizes[activeExamIds[0]] || 0 }})
            </text>
            <text
              :x="layout2Set.circleB.cx + 60"
              :y="layout2Set.circleB.cy - layout2Set.circleB.r - 12"
              text-anchor="middle"
              fill="#38BDF8"
              font-size="13"
              font-weight="bold"
            >
              {{ getExamShortCode(activeExamIds[1]) }} ({{ examSetSizes[activeExamIds[1]] || 0 }})
            </text>
          </g>

          <!-- 3-SET VENN GEOMETRY -->
          <g v-else-if="activeVennSetCount === 3" class="venn-3-set">
            <!-- Circle A (Top) -->
            <circle
              :cx="layout3Set.circleA.cx"
              :cy="layout3Set.circleA.cy"
              :r="layout3Set.radius"
              fill="#10B981"
              fill-opacity="0.16"
              stroke="#10B981"
              stroke-width="2.5"
            />
            <!-- Circle B (Bottom-Left) -->
            <circle
              :cx="layout3Set.circleB.cx"
              :cy="layout3Set.circleB.cy"
              :r="layout3Set.radius"
              fill="#38BDF8"
              fill-opacity="0.16"
              stroke="#38BDF8"
              stroke-width="2.5"
            />
            <!-- Circle C (Bottom-Right) -->
            <circle
              :cx="layout3Set.circleC.cx"
              :cy="layout3Set.circleC.cy"
              :r="layout3Set.radius"
              fill="#A855F7"
              fill-opacity="0.16"
              stroke="#A855F7"
              stroke-width="2.5"
            />

            <!-- Set Labels -->
            <text
              :x="layout3Set.circleA.cx"
              :y="layout3Set.circleA.cy - layout3Set.radius - 12"
              text-anchor="middle"
              fill="#10B981"
              font-size="13"
              font-weight="bold"
            >
              {{ getExamShortCode(activeExamIds[0]) }} ({{ examSetSizes[activeExamIds[0]] || 0 }})
            </text>
            <text
              :x="layout3Set.circleB.cx - 60"
              :y="layout3Set.circleB.cy + layout3Set.radius + 20"
              text-anchor="middle"
              fill="#38BDF8"
              font-size="13"
              font-weight="bold"
            >
              {{ getExamShortCode(activeExamIds[1]) }} ({{ examSetSizes[activeExamIds[1]] || 0 }})
            </text>
            <text
              :x="layout3Set.circleC.cx + 60"
              :y="layout3Set.circleC.cy + layout3Set.radius + 20"
              text-anchor="middle"
              fill="#A855F7"
              font-size="13"
              font-weight="bold"
            >
              {{ getExamShortCode(activeExamIds[2]) }} ({{ examSetSizes[activeExamIds[2]] || 0 }})
            </text>
          </g>

          <!-- 4-SET VENN GEOMETRY (Edwards-Venn / 4 Rotated Congruent Ellipses) -->
          <g v-else-if="activeVennSetCount === 4" class="venn-4-set">
            <!-- Ellipse A: Center (320, 280), Rot -45deg -->
            <g transform="translate(320, 280) rotate(-45)">
              <ellipse
                cx="0"
                cy="0"
                :rx="layout4Set.rx"
                :ry="layout4Set.ry"
                fill="#10B981"
                fill-opacity="0.14"
                stroke="#10B981"
                stroke-width="2"
              />
            </g>
            <!-- Ellipse B: Center (380, 280), Rot -45deg -->
            <g transform="translate(380, 280) rotate(-45)">
              <ellipse
                cx="0"
                cy="0"
                :rx="layout4Set.rx"
                :ry="layout4Set.ry"
                fill="#38BDF8"
                fill-opacity="0.14"
                stroke="#38BDF8"
                stroke-width="2"
              />
            </g>
            <!-- Ellipse C: Center (380, 280), Rot +45deg -->
            <g transform="translate(380, 280) rotate(45)">
              <ellipse
                cx="0"
                cy="0"
                :rx="layout4Set.rx"
                :ry="layout4Set.ry"
                fill="#A855F7"
                fill-opacity="0.14"
                stroke="#A855F7"
                stroke-width="2"
              />
            </g>
            <!-- Ellipse D: Center (440, 280), Rot +45deg -->
            <g transform="translate(440, 280) rotate(45)">
              <ellipse
                cx="0"
                cy="0"
                :rx="layout4Set.rx"
                :ry="layout4Set.ry"
                fill="#F59E0B"
                fill-opacity="0.14"
                stroke="#F59E0B"
                stroke-width="2"
              />
            </g>

            <!-- 4 Set Labels -->
            <text x="170" y="80" fill="#10B981" font-size="12" font-weight="bold">
              ● {{ getExamShortCode(activeExamIds[0]) }} ({{ examSetSizes[activeExamIds[0]] || 0 }})
            </text>
            <text x="500" y="80" fill="#38BDF8" font-size="12" font-weight="bold">
              ● {{ getExamShortCode(activeExamIds[1]) }} ({{ examSetSizes[activeExamIds[1]] || 0 }})
            </text>
            <text x="170" y="520" fill="#A855F7" font-size="12" font-weight="bold">
              ● {{ getExamShortCode(activeExamIds[2]) }} ({{ examSetSizes[activeExamIds[2]] || 0 }})
            </text>
            <text x="500" y="520" fill="#F59E0B" font-size="12" font-weight="bold">
              ● {{ getExamShortCode(activeExamIds[3]) }} ({{ examSetSizes[activeExamIds[3]] || 0 }})
            </text>
          </g>

          <!-- DISJOINT REGION BADGES (Interactive Hit Targets) -->
          <g class="region-badges">
            <g
              v-for="region in calculatedRegions"
              :key="'region-' + region.mask"
              :transform="`translate(${region.centroid.x}, ${region.centroid.y})`"
              class="cursor-pointer transition-transform duration-150"
              :class="{
                'scale-115': isRegionActive(region),
              }"
              @mouseenter="onHoverRegion(region, $event)"
              @mousemove="onMoveTooltip($event)"
              @mouseleave="onLeaveRegion"
              @click="onClickRegion(region)"
            >
              <!-- Badge Outer Glow Circle / Halo -->
              <circle
                :r="isRegionActive(region) ? 22 : 17"
                :fill="getRegionBadgeBg(region)"
                :stroke="isRegionActive(region) ? '#38BDF8' : getRegionBadgeStroke(region)"
                :stroke-width="isRegionActive(region) ? 2.5 : 1.5"
                :filter="region.degree === activeVennSetCount && region.cardinality > 0 ? 'url(#coreGlow)' : (isRegionActive(region) ? 'url(#badgeGlow)' : undefined)"
              />

              <!-- Number on Badge -->
              <text
                x="0"
                y="4"
                text-anchor="middle"
                :fill="region.cardinality > 0 ? '#FFFFFF' : '#64748B'"
                :font-size="region.cardinality >= 100 ? 9 : 11"
                font-weight="bold"
                font-family="monospace"
              >
                {{ region.cardinality }}
              </text>
            </g>
          </g>
        </svg>
      </div>

      <!-- Floating Interactive Tooltip -->
      <div
        v-if="tooltip.visible"
        class="fixed z-50 pointer-events-none px-3.5 py-2.5 rounded-lg bg-slate-900/95 border border-slate-700 shadow-2xl backdrop-blur-md text-xs space-y-1.5 max-w-xs transition-opacity duration-150"
        :style="{ left: tooltip.x + 14 + 'px', top: tooltip.y + 14 + 'px' }"
      >
        <div class="flex items-center justify-between gap-3">
          <span class="font-bold text-white">{{ tooltip.title }}</span>
          <span class="px-1.5 py-0.5 rounded font-mono font-bold text-[10px] bg-sky-500/20 text-sky-300">
            {{ tooltip.cardinality }} Topics
          </span>
        </div>
        <div class="text-[11px] text-slate-300">
          <span class="text-slate-400">Exams in Region:</span>
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
          <span class="text-slate-500">Topics in this region:</span>
          <ul class="list-disc list-inside mt-0.5 space-y-0.5 text-slate-300">
            <li v-for="t in tooltip.sampleTopics" :key="t" class="truncate">{{ t }}</li>
          </ul>
        </div>
        <div class="pt-1 text-[9px] text-sky-400 font-medium">
          Click region to lock & inspect topic list below
        </div>
      </div>
    </div>

    <!-- Pairwise Overlap & Synergy Metrics (For 2 to 4 exams) -->
    <div
      v-if="pairwiseMetrics.length > 0"
      class="p-4 rounded-xl bg-slate-850 border border-slate-800 space-y-3"
    >
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">
          Pairwise Jaccard & Szymkiewicz-Simpson Synergy Metrics
        </h3>
        <span class="text-[11px] text-slate-400">
          {{ pairwiseMetrics.length }} Pairwise Comparison{{ pairwiseMetrics.length > 1 ? 's' : '' }}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        <div
          v-for="metric in pairwiseMetrics"
          :key="metric.examA + '-' + metric.examB"
          class="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs space-y-2"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-1 font-bold text-white">
              <span>{{ getExamShortCode(metric.examA) }}</span>
              <span class="text-slate-500">↔</span>
              <span>{{ getExamShortCode(metric.examB) }}</span>
            </div>
            <span
              v-if="metric.jaccardSimilarity === 1.0"
              class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
            >
              100% Identical
            </span>
            <span
              v-else-if="metric.overlapCoefficient === 1.0"
              class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30"
            >
              Complete Subset
            </span>
            <span
              v-else-if="metric.overlapCoefficient === 0.0"
              class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30"
            >
              Disjoint Sets
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-800 font-mono text-[11px]">
            <div>
              <span class="text-slate-400 text-[10px] block">Jaccard Index</span>
              <strong class="text-emerald-400">{{ (metric.jaccardSimilarity * 100).toFixed(1) }}%</strong>
            </div>
            <div>
              <span class="text-slate-400 text-[10px] block">Overlap Coeff</span>
              <strong class="text-sky-400">{{ (metric.overlapCoefficient * 100).toFixed(1) }}%</strong>
            </div>
          </div>

          <div class="flex items-center justify-between text-[10px] text-slate-400 pt-1">
            <span>Shared: <strong class="text-slate-200">{{ metric.intersectionCount }}</strong></span>
            <span>Unique A: <strong class="text-slate-200">{{ metric.uniqueToA }}</strong></span>
            <span>Unique B: <strong class="text-slate-200">{{ metric.uniqueToB }}</strong></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Region Topic Inspector -->
    <div
      v-if="pinnedRegion"
      class="mt-4 p-4 rounded-xl bg-slate-850 border border-slate-700 space-y-3"
    >
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-800">
        <div>
          <div class="flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <h3 class="text-sm font-bold text-white">
              Selected Region: {{ pinnedRegion.label }}
            </h3>
            <span class="px-2 py-0.5 rounded font-mono font-bold text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              {{ pinnedRegion.cardinality }} Topics
            </span>
          </div>
          <p class="text-[11px] text-slate-400 mt-0.5">
            Topics in this exclusive region are required by precisely these examinations under current filters.
          </p>
        </div>
        <button
          @click="clearActiveRegion"
          class="self-start sm:self-auto px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs border border-slate-700 transition-colors"
        >
          Clear Selection
        </button>
      </div>

      <!-- Topic Grid -->
      <div
        v-if="pinnedRegion.topics.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-64 overflow-y-auto pr-1"
      >
        <div
          v-for="topic in pinnedRegion.topics"
          :key="topic.topic_id"
          class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-sky-500/40 transition-colors space-y-1"
          @mouseenter="vizStore.setHoveredTopic(topic.topic_id)"
          @mouseleave="vizStore.setHoveredTopic(null)"
        >
          <div class="flex items-center justify-between gap-1">
            <span class="text-[10px] font-mono text-sky-400 truncate">{{ topic.domain }}</span>
            <span class="text-[9px] font-mono text-slate-500 truncate">{{ topic.sub_domain }}</span>
          </div>
          <div class="text-xs font-semibold text-slate-200 line-clamp-1" :title="topic.topic_title">
            {{ topic.topic_title }}
          </div>
          <p class="text-[10px] text-slate-400 line-clamp-2">{{ topic.description }}</p>
        </div>
      </div>
      <div v-else class="text-xs text-slate-500 italic p-3 text-center">
        Zero topics exclusively in this region under current domain and cognitive depth filters.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import {
  loadTaxonomyData,
  getFilteredExamTopicMap,
  calculateVennRegions,
  calculateAllPairwiseMetrics,
} from '@/services/syllabusDataService';
import type { VennRegion, TopicTaxonomyDetail, PairwiseMetric } from '@/types/syllabus';

const vizStore = useSyllabusVisualizationStore();
const examStore = useExamMasterStore();

// Set Colors
const SET_COLORS = ['#10B981', '#38BDF8', '#A855F7', '#F59E0B'];

const rawTaxonomy = ref<Record<string, TopicTaxonomyDetail>>({});
const hoveredRegionMask = ref<number | null>(null);

// Layout Specifications
const layout2Set = {
  width: 680,
  height: 440,
  circleA: { cx: 260, cy: 220, r: 145 },
  circleB: { cx: 420, cy: 220, r: 145 },
};

const layout3Set = {
  width: 700,
  height: 520,
  radius: 140,
  circleA: { cx: 350, cy: 195 },
  circleB: { cx: 285, cy: 307.5 },
  circleC: { cx: 415, cy: 307.5 },
};

const layout4Set = {
  width: 760,
  height: 580,
  rx: 185,
  ry: 95,
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

onMounted(async () => {
  const data = await loadTaxonomyData();
  rawTaxonomy.value = data.lookup;
});

const selectedExamIds = computed(() => vizStore.selectedExamIds);

// Active exams capped at 4 for Venn diagram
const activeExamIds = computed(() => {
  return selectedExamIds.value.slice(0, 4);
});

const activeVennSetCount = computed(() => activeExamIds.value.length);

const currentLayout = computed(() => {
  if (activeVennSetCount.value === 2) return layout2Set;
  if (activeVennSetCount.value === 3) return layout3Set;
  return layout4Set;
});

// Filtered Exam-Topic Map
const filteredData = computed(() => {
  return getFilteredExamTopicMap(
    activeExamIds.value,
    rawTaxonomy.value,
    vizStore.selectedDomain,
    vizStore.minDepthLevel
  );
});

// Set sizes for each active exam
const examSetSizes = computed<Record<string, number>>(() => {
  const sizes: Record<string, number> = {};
  for (const id of activeExamIds.value) {
    sizes[id] = filteredData.value.examTopicMap[id]?.size || 0;
  }
  return sizes;
});

// Exam short code lookup
const examShortCodes = computed<Record<string, string>>(() => {
  const map: Record<string, string> = {};
  for (const id of activeExamIds.value) {
    const ex = examStore.examsMap[id];
    map[id] = ex?.short_code || id.replace(/^(UPSC_|PSU_)/, '');
  }
  return map;
});

// Calculated Venn Disjoint Regions
const calculatedRegions = computed<VennRegion[]>(() => {
  if (activeExamIds.value.length < 2 || activeExamIds.value.length > 4) {
    return [];
  }
  const result = calculateVennRegions(
    activeExamIds.value,
    filteredData.value.examTopicMap,
    filteredData.value.topicLookup,
    examShortCodes.value
  );
  return result.regions;
});

const activeRegionsCount = computed(() => calculatedRegions.value.length);

// Pairwise Metrics
const pairwiseMetrics = computed<PairwiseMetric[]>(() => {
  if (activeExamIds.value.length < 2) return [];
  return calculateAllPairwiseMetrics(
    activeExamIds.value,
    filteredData.value.examTopicMap
  );
});

// Pinned Region
const pinnedRegion = computed<VennRegion | null>(() => {
  if (!vizStore.pinnedCombinationKey) return null;
  return (
    calculatedRegions.value.find((r) => r.label === vizStore.pinnedCombinationKey) || null
  );
});

function isRegionActive(region: VennRegion): boolean {
  return (
    hoveredRegionMask.value === region.mask ||
    vizStore.pinnedCombinationKey === region.label
  );
}

function getRegionBadgeBg(region: VennRegion): string {
  if (isRegionActive(region)) return '#0284C7'; // Sky-600
  if (region.degree === activeVennSetCount.value && region.cardinality > 0) {
    return '#059669'; // Emerald-600 for core intersection
  }
  if (region.cardinality === 0) return '#0F172A';
  return '#1E293B';
}

function getRegionBadgeStroke(region: VennRegion): string {
  if (region.degree === activeVennSetCount.value && region.cardinality > 0) {
    return '#10B981';
  }
  if (region.cardinality === 0) return '#334155';
  return '#475569';
}

function getExamShortCode(examId: string): string {
  return examShortCodes.value[examId] || examId;
}

// Interaction Handlers
function onHoverRegion(region: VennRegion, event: MouseEvent) {
  hoveredRegionMask.value = region.mask;
  tooltip.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    title: region.label,
    exams: region.participatingExamIds,
    cardinality: region.cardinality,
    sampleTopics: region.topics.slice(0, 4).map((t) => t.topic_title),
  };
}

function onMoveTooltip(event: MouseEvent) {
  tooltip.value.x = event.clientX;
  tooltip.value.y = event.clientY;
}

function onLeaveRegion() {
  hoveredRegionMask.value = null;
  tooltip.value.visible = false;
}

function onClickRegion(region: VennRegion) {
  if (vizStore.pinnedCombinationKey === region.label) {
    vizStore.setActiveIntersection([]);
  } else {
    vizStore.setActiveIntersection(region.topicIds, region.label);
  }
}

function clearActiveRegion() {
  vizStore.setActiveIntersection([]);
}

function addPresetDuo() {
  vizStore.selectedExamIds = ['UPSC_CSE', 'RBI_GRADE_B'];
}
</script>

<style scoped>
.venn-diagram-container {
  font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
}
.scale-115 {
  transform: scale(1.15);
}
</style>
