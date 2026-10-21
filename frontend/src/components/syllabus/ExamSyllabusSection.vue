<template>
  <div class="space-y-6">
    <!-- Redesigned Aspirant-First Syllabus Container -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-xl overflow-hidden">
      
      <!-- 1. Scheme Summary Top Bar / Collapsible Header -->
      <button
        type="button"
        @click="isSectionOpen = !isSectionOpen"
        class="w-full p-6 sm:p-8 flex flex-col lg:flex-row lg:items-center justify-between gap-4 text-left hover:bg-slate-50/60 dark:hover:bg-slate-850/40 transition-colors select-none cursor-pointer"
        :class="isSectionOpen ? 'border-b border-slate-200 dark:border-slate-800' : ''"
      >
        <div class="flex items-center space-x-2">
          <span class="text-xl">📚</span>
          <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Examination Syllabus & Pattern
          </h2>
        </div>

        <div class="flex items-center justify-between lg:justify-end gap-3 w-full lg:w-auto">
          <!-- Pattern High-Level Metric Badges -->
          <div class="flex flex-wrap items-center gap-2 text-xs">
            <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 font-medium">
              <span class="text-slate-400 font-normal">Total Marks:</span>
              <strong class="text-slate-900 dark:text-white font-mono">{{ scheme.total_marks }}</strong>
            </div>
            <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 font-medium">
              <span class="text-slate-400 font-normal">Stages:</span>
              <strong class="text-slate-900 dark:text-white">{{ scheme.stages.length }}</strong>
            </div>
            <div class="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 font-medium">
              <span class="text-slate-400 font-normal">Penalty:</span>
              <strong class="text-rose-600 dark:text-rose-400">{{ scheme.negative_marking_rule || 'Standard Rule' }}</strong>
            </div>
          </div>

          <!-- Section Expand/Collapse Chevron -->
          <svg
            class="w-5 h-5 text-slate-500 transform transition-transform duration-200 shrink-0 ml-1"
            :class="isSectionOpen ? 'rotate-180' : ''"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      <!-- Collapsible Body Content -->
      <div v-show="isSectionOpen" class="p-6 sm:p-8 space-y-6">
      <!-- 2. Overall Preparation Progress Bar -->
      <div class="p-4 sm:p-5 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800/80 space-y-2.5">
        <div class="flex items-center justify-between text-xs sm:text-sm">
          <div class="flex items-center space-x-2">
            <span class="font-bold text-slate-900 dark:text-white">Your Preparation Progress</span>
            <span class="text-slate-400">•</span>
            <span class="text-slate-600 dark:text-slate-400 text-xs">
              {{ overallProgress.completed }} of {{ overallProgress.total }} topics mastered
            </span>
          </div>
          <div class="font-mono font-extrabold text-emerald-600 dark:text-emerald-400 text-sm">
            {{ overallProgress.pct }}%
          </div>
        </div>

        <div class="w-full bg-slate-200 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden">
          <div
            class="bg-emerald-500 h-full transition-all duration-500 ease-out rounded-full"
            :style="{ width: `${overallProgress.pct}%` }"
          ></div>
        </div>

        <!-- Small Reset Progress Link Under Preparation Bar -->
        <div class="flex items-center justify-end pt-0.5">
          <button
            @click="confirmReset"
            class="text-[11px] text-slate-400 hover:text-rose-500 dark:hover:text-rose-400 underline transition-colors cursor-pointer"
            title="Reset checked topics for this examination"
          >
            Reset Progress
          </button>
        </div>
      </div>

      <!-- 3. Utility Toolbar: Search Filter -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1">
        <!-- Live Topic Search -->
        <div class="w-full sm:w-80 relative">
          <input
            v-model="searchFilter"
            type="text"
            placeholder="Search topic or keywords..."
            class="w-full pl-9 pr-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition-colors"
          />
          <span class="absolute left-3 top-2.5 text-slate-400 text-xs">🔍</span>
          <button
            v-if="searchFilter"
            @click="searchFilter = ''"
            class="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600 dark:hover:text-white text-xs p-0.5"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- 4. Stage Selector Tabs -->
      <div class="flex border-b border-slate-200 dark:border-slate-800 gap-1 overflow-x-auto pb-px">
        <button
          v-for="stg in scheme.stages"
          :key="stg.stage_id"
          @click="activeStageId = stg.stage_id"
          class="px-4 py-3 text-xs sm:text-sm font-bold border-b-2 transition-all flex items-center space-x-2 whitespace-nowrap"
          :class="
            activeStageId === stg.stage_id
              ? 'border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-50/30 dark:bg-emerald-950/10'
              : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:border-slate-300 dark:hover:border-slate-700'
          "
        >
          <span>{{ stg.stage_name }}</span>
          <span
            class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold"
            :class="
              activeStageId === stg.stage_id
                ? 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-300'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-500'
            "
          >
            {{ trackerStore.getStageProgress(scheme.exam_id, stg, activeDiscipline).completed }} /
            {{ trackerStore.getStageProgress(scheme.exam_id, stg, activeDiscipline).total }}
          </span>
        </button>
      </div>

      <!-- 5. Discipline Selector (Only shown if multi-stream / GATE / PSU) -->
      <div v-if="scheme.disciplines && scheme.disciplines.length > 0" class="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold text-slate-700 dark:text-slate-300 flex items-center space-x-1.5">
            <span>⚙️</span>
            <span>Select Engineering Stream / Discipline:</span>
          </span>
          <span class="text-slate-500 text-[11px]">
            Curriculum dynamically switches to selected branch
          </span>
        </div>

        <div class="flex flex-wrap items-center gap-1.5 pt-1">
          <button
            v-for="disc in scheme.disciplines"
            :key="disc.code"
            @click="trackerStore.setActiveDiscipline(scheme.exam_id, disc.code)"
            class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all"
            :class="
              activeDiscipline === disc.code
                ? 'bg-emerald-500 text-white shadow-xs font-bold'
                : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-slate-700'
            "
          >
            {{ disc.name }} ({{ disc.code }})
          </button>
        </div>
      </div>


      <!-- 7. Active Stage Content: Collapsible Paper Cards -->
      <div v-if="activeStage" class="space-y-4">
        <!-- Stage Subtitle/Description -->
        <div v-if="activeStage.description" class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          <strong>Stage Format:</strong> {{ activeStage.description }}
        </div>

        <!-- Papers List -->
        <div
          v-for="paper in displayedPapers"
          :key="paper.paper_id"
          class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden shadow-xs transition-all"
          :class="isPaperExpanded(paper.paper_id) ? 'shadow-md border-slate-300 dark:border-slate-700' : ''"
        >
          <!-- Collapsible Paper Card Header -->
          <div
            class="p-4 sm:p-5 flex flex-col lg:flex-row lg:items-center justify-between gap-3 cursor-pointer select-none bg-slate-50/50 dark:bg-slate-850/30 hover:bg-slate-100/60 dark:hover:bg-slate-800/40 transition-colors"
            @click="togglePaper(paper.paper_id)"
          >
            <div class="space-y-2 min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <h3 class="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white tracking-tight">
                  {{ paper.paper_name }}
                </h3>
                <span
                  class="px-2 py-0.5 rounded-md text-[11px] font-bold border"
                  :class="
                    paper.is_qualifying
                      ? 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/30'
                      : 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/30'
                  "
                >
                  {{ paper.merit_status }}
                </span>
              </div>

              <!-- Paper Scheme Specification Metrics -->
              <div class="flex flex-wrap items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
                <span class="flex items-center space-x-1">
                  <span class="text-slate-400">Marks:</span>
                  <strong class="text-slate-900 dark:text-white font-mono">{{ paper.marks }}</strong>
                </span>
                <span>•</span>
                <span class="flex items-center space-x-1">
                  <span class="text-slate-400">Duration:</span>
                  <strong class="text-slate-900 dark:text-white">{{ paper.duration_hours }}h</strong>
                </span>
                <span>•</span>
                <span class="flex items-center space-x-1">
                  <span class="text-slate-400">Format:</span>
                  <strong class="text-slate-900 dark:text-white">{{ paper.question_type }}</strong>
                </span>
                <span>•</span>
                <span class="flex items-center space-x-1">
                  <span class="text-slate-400">Negative Penalty:</span>
                  <strong class="text-rose-600 dark:text-rose-400">{{ paper.negative_marking }}</strong>
                </span>
              </div>
            </div>

            <!-- Paper Progress & Chevron Action -->
            <div class="flex items-center space-x-3 self-end lg:self-auto shrink-0 pt-2 lg:pt-0">
              <div class="text-right">
                <div class="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">
                  {{ trackerStore.getPaperProgress(scheme.exam_id, paper).completed }} /
                  {{ trackerStore.getPaperProgress(scheme.exam_id, paper).total }} Topics
                </div>
                <div class="w-24 bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden mt-1">
                  <div
                    class="bg-emerald-500 h-full rounded-full transition-all duration-300"
                    :style="{ width: `${trackerStore.getPaperProgress(scheme.exam_id, paper).pct}%` }"
                  ></div>
                </div>
              </div>

              <button
                type="button"
                class="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
                aria-label="Toggle paper"
              >
                <svg
                  class="w-4 h-4 transform transition-transform duration-200"
                  :class="isPaperExpanded(paper.paper_id) ? 'rotate-180' : ''"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Paper Topics Checklist Grid (Shown when expanded) -->
          <div v-if="isPaperExpanded(paper.paper_id)" class="p-5 border-t border-slate-200 dark:border-slate-800 space-y-4">
            <div class="text-xs text-slate-500 text-[11px] pb-1 border-b border-slate-100 dark:border-slate-800/60">
              Check topics as you prepare. Progress persists automatically offline.
            </div>

            <!-- Topics Grid -->
            <div v-if="getFilteredTopicsForPaper(paper).length === 0" class="py-6 text-center text-slate-400 text-xs">
              No topics in this paper match your search "{{ searchFilter }}".
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="topic in getFilteredTopicsForPaper(paper)"
                :key="topic.topic_id"
                class="p-3.5 rounded-xl border transition-all flex items-start space-x-3 group relative cursor-pointer select-none"
                :class="
                  trackerStore.isTopicCompleted(scheme.exam_id, topic.topic_id)
                    ? 'bg-emerald-50/40 dark:bg-emerald-950/15 border-emerald-300/80 dark:border-emerald-500/30'
                    : 'bg-slate-50 dark:bg-slate-850/80 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                "
                @click="trackerStore.toggleTopic(scheme.exam_id, topic.topic_id)"
              >
                <!-- Checkbox -->
                <div
                  class="mt-0.5 w-5 h-5 rounded-md border flex items-center justify-center transition-all shrink-0"
                  :class="
                    trackerStore.isTopicCompleted(scheme.exam_id, topic.topic_id)
                      ? 'bg-emerald-500 border-emerald-600 text-white'
                      : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 group-hover:border-slate-400'
                  "
                >
                  <svg
                    v-if="trackerStore.isTopicCompleted(scheme.exam_id, topic.topic_id)"
                    class="w-3.5 h-3.5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>

                <!-- Topic Info & Summary -->
                <div class="flex-1 min-w-0 pr-8">
                  <h4
                    class="text-xs sm:text-sm font-bold tracking-tight break-words leading-snug"
                    :class="
                      trackerStore.isTopicCompleted(scheme.exam_id, topic.topic_id)
                        ? 'text-slate-900 dark:text-white line-through decoration-emerald-500/60'
                        : 'text-slate-900 dark:text-white'
                    "
                  >
                    {{ topic.title }}
                  </h4>

                  <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                    {{ topic.description }}
                  </p>

                  <div v-if="topic.sub_points?.length" class="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono mt-1">
                    • {{ topic.sub_points.length }} sub-points covered
                  </div>
                </div>

                <!-- Details Trigger Button (Opens Topic Drawer) -->
                <button
                  type="button"
                  @click.stop="openTopicDrawer(topic, paper, activeStage)"
                  class="absolute right-3 top-3 p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-white dark:hover:bg-slate-800 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 transition-all text-xs"
                  title="Inspect detailed official syllabus scope"
                >
                  <span>ⓘ</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- 8. Slide-Over Topic Detail Drawer -->
    <SyllabusTopicDrawer
      :is-open="isDrawerOpen"
      :topic="selectedDrawerTopic"
      :paper-name="selectedDrawerPaper?.paper_name"
      :stage-name="selectedDrawerStage?.stage_name"
      :is-completed="selectedDrawerTopic ? trackerStore.isTopicCompleted(scheme.exam_id, selectedDrawerTopic.topic_id) : false"
      @close="isDrawerOpen = false"
      @toggle-completed="handleDrawerToggle"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import type {
  ExaminationScheme,
  SchemeStage,
  SchemePaper,
  SyllabusTopic
} from '@/types/curriculum';
import { useSyllabusTrackerStore } from '@/stores/useSyllabusTrackerStore';
import SyllabusTopicDrawer from '@/components/syllabus/SyllabusTopicDrawer.vue';

const props = defineProps<{
  scheme: ExaminationScheme;
}>();

const trackerStore = useSyllabusTrackerStore();

// Stage & Discipline Selection
const activeStageId = ref<string>(props.scheme.stages[0]?.stage_id || 'prelims');
const activeDiscipline = computed(() => {
  return trackerStore.getActiveDiscipline(props.scheme.exam_id, props.scheme);
});

// Search Filter
const searchFilter = ref<string>('');

// Section Collapsible State (starts collapsed)
const isSectionOpen = ref(false);

// Paper Expansion State (starts collapsed, no cards expanded on their own)
const expandedPaperIds = ref<Set<string>>(new Set());

const activeStage = computed<SchemeStage | undefined>(() => {
  return props.scheme.stages.find((s) => s.stage_id === activeStageId.value);
});

const displayedPapers = computed<SchemePaper[]>(() => {
  if (!activeStage.value) return [];
  return activeStage.value.papers.filter((paper) => {
    // If paper has stream_id and doesn't match active discipline, filter it out
    if (paper.stream_id && activeDiscipline.value && paper.stream_id !== activeDiscipline.value) {
      return false;
    }
    return true;
  });
});

function isPaperExpanded(paperId: string): boolean {
  return expandedPaperIds.value.has(paperId);
}

function togglePaper(paperId: string) {
  if (expandedPaperIds.value.has(paperId)) {
    expandedPaperIds.value.delete(paperId);
  } else {
    expandedPaperIds.value.add(paperId);
  }
}

function getFilteredTopicsForPaper(paper: SchemePaper): SyllabusTopic[] {
  if (!searchFilter.value.trim()) {
    return paper.topics;
  }
  const q = searchFilter.value.toLowerCase().trim();
  return paper.topics.filter(
    (t) =>
      t.title.toLowerCase().includes(q) ||
      t.description.toLowerCase().includes(q) ||
      (t.sub_points && t.sub_points.some((p) => p.toLowerCase().includes(q)))
  );
}

const overallProgress = computed(() => {
  return trackerStore.getExamProgress(props.scheme.exam_id, props.scheme, activeDiscipline.value);
});

function confirmReset() {
  if (window.confirm(`Reset all checklist progress for ${props.scheme.exam_title}?`)) {
    trackerStore.resetExam(props.scheme.exam_id);
  }
}

// Drawer State
const isDrawerOpen = ref(false);
const selectedDrawerTopic = ref<SyllabusTopic | null>(null);
const selectedDrawerPaper = ref<SchemePaper | null>(null);
const selectedDrawerStage = ref<SchemeStage | null>(null);

function openTopicDrawer(topic: SyllabusTopic, paper: SchemePaper, stage?: SchemeStage) {
  selectedDrawerTopic.value = topic;
  selectedDrawerPaper.value = paper;
  selectedDrawerStage.value = stage || activeStage.value || null;
  isDrawerOpen.value = true;
}

function handleDrawerToggle() {
  if (selectedDrawerTopic.value) {
    trackerStore.toggleTopic(props.scheme.exam_id, selectedDrawerTopic.value.topic_id);
  }
}
</script>

<style scoped>
@media print {
  button, input {
    display: none !important;
  }
}
</style>
