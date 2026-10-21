<template>
  <div class="bg-slate-850 rounded-2xl border border-slate-800 p-4 sm:p-5 shadow-xl space-y-4">
    <!-- Row 1: Active Exam Selector & Quick Presets -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <!-- Active Exam Pills -->
      <div class="space-y-1.5 flex-1">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center space-x-2">
            <span class="text-slate-400 font-semibold uppercase tracking-wider text-[11px]">Selected Examinations</span>
            <span
              class="px-2 py-0.5 rounded-full font-mono font-medium text-[10px]"
              :class="store.selectedExamIds.length === 4 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-slate-800 text-slate-300 border border-slate-700'"
            >
              {{ store.selectedExamIds.length }} / 4 Max
            </span>
          </div>
          <span class="text-slate-500 text-[11px] hidden sm:inline">Min 2, Max 4 for cross-set topology</span>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <!-- Exam Pills -->
          <div
            v-for="exam in store.selectedExamRecords"
            :key="exam.exam_id"
            class="group inline-flex items-center space-x-2 px-3 py-1.5 rounded-xl border transition-all shadow-sm"
            :class="getExamPillClass(exam.category)"
          >
            <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: getClusterColor(exam.category) }"></span>
            <span class="font-bold font-mono text-xs text-white">{{ exam.short_code }}</span>
            <span class="text-[11px] text-slate-300 hidden md:inline truncate max-w-[140px]">{{ exam.title }}</span>
            <button
              v-if="store.selectedExamIds.length > 2"
              @click="store.toggleExamSelection(exam.exam_id)"
              class="text-slate-400 hover:text-rose-400 p-0.5 rounded transition-colors text-xs ml-1"
              title="Remove Exam (Min 2 required)"
            >
              ✕
            </button>
            <span v-else class="text-slate-600 text-xs cursor-not-allowed ml-1" title="Minimum 2 exams required for set comparison">
              •
            </span>
          </div>

          <!-- Add Exam Dropdown / Trigger -->
          <div class="relative inline-block" ref="dropdownRef">
            <button
              @click="isExamDropdownOpen = !isExamDropdownOpen"
              :disabled="store.selectedExamIds.length >= 4"
              class="px-3 py-1.5 rounded-xl border text-xs font-semibold flex items-center space-x-1.5 transition-all shadow-sm"
              :class="
                store.selectedExamIds.length >= 4
                  ? 'bg-slate-800/40 border-slate-800 text-slate-600 cursor-not-allowed'
                  : 'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30 text-emerald-400 hover:text-emerald-300'
              "
            >
              <span>+ Add Exam</span>
              <span class="text-[10px]">▾</span>
            </button>

            <!-- Exam Picker Popover -->
            <transition name="popover">
              <div
                v-if="isExamDropdownOpen"
                class="absolute left-0 mt-2 w-72 sm:w-80 max-h-80 overflow-y-auto bg-slate-900 border border-slate-700 rounded-xl shadow-2xl p-2 z-50 space-y-1"
              >
                <div class="px-2 py-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">
                  Select Grade A Examination
                </div>
                <div
                  v-for="cand in availableExams"
                  :key="cand.exam_id"
                  @click="selectExamCandidate(cand.exam_id)"
                  class="p-2 rounded-lg hover:bg-slate-800 cursor-pointer flex items-center justify-between text-xs transition-colors"
                >
                  <div class="flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: getClusterColor(cand.category) }"></span>
                    <span class="font-bold font-mono text-white">{{ cand.short_code }}</span>
                    <span class="text-slate-300 text-[11px] truncate max-w-[150px]">{{ cand.title }}</span>
                  </div>
                  <span class="text-[10px] text-slate-500">{{ cand.category }}</span>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Quick Preset Buttons -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs">
          <span class="text-slate-400 font-semibold uppercase tracking-wider text-[11px]">Curated Presets</span>
          <button
            @click="store.resetToDefaults()"
            class="text-[11px] text-slate-400 hover:text-emerald-400 transition-colors flex items-center space-x-1"
            title="Reset to default exams and filters"
          >
            <span>↺ Reset Defaults</span>
          </button>
        </div>
        <div class="flex flex-wrap items-center gap-1.5">
          <button
            v-for="preset in PRESET_OPTIONS"
            :key="preset.id"
            @click="store.setPreset(preset.id)"
            class="px-2.5 py-1 rounded-lg text-[11px] font-medium border transition-colors"
            :class="
              isPresetActive(preset.examIds)
                ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300'
                : 'bg-slate-800 hover:bg-slate-750 border-slate-700 text-slate-400 hover:text-slate-200'
            "
            :title="preset.description"
          >
            {{ preset.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Active Intersection Banner (Cross-View Synchronization Indicator) -->
    <div
      v-if="store.activeIntersectionTopics.length > 0"
      class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 px-3.5 py-2 rounded-xl bg-indigo-950/50 border border-indigo-500/40 text-xs text-indigo-200"
    >
      <div class="flex items-center space-x-2">
        <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
        <span class="font-bold text-indigo-300">Active Topology Filter:</span>
        <span class="font-mono text-white">{{ store.pinnedCombinationKey || 'Selected Intersection' }}</span>
        <span class="px-2 py-0.5 rounded-full bg-indigo-500/20 border border-indigo-500/40 font-mono text-[10px] text-indigo-300">
          {{ store.activeIntersectionTopics.length }} topics isolated
        </span>
      </div>
      <button
        @click="store.clearActiveIntersection()"
        class="self-start sm:self-auto px-2.5 py-1 rounded-lg bg-indigo-900/60 hover:bg-indigo-800 text-indigo-300 hover:text-white border border-indigo-700/60 transition-colors flex items-center space-x-1 text-[11px]"
        title="Clear Intersection Filter"
      >
        <span>Clear Filter ✕</span>
      </button>
    </div>

    <!-- Row 2: Synchronized Filters & View Switcher -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3 pt-3 border-t border-slate-800 items-center">
      <!-- Domain Filter (4 cols) -->
      <div class="lg:col-span-4 flex items-center space-x-2">
        <label class="text-slate-400 text-xs font-medium whitespace-nowrap">Domain:</label>
        <select
          :value="store.selectedDomain"
          @change="(e) => store.setDomain((e.target as HTMLSelectElement).value)"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
        >
          <option value="ALL">All Domains (192 Topics)</option>
          <option value="General Studies">General Studies</option>
          <option value="Quantitative Aptitude">Quantitative Aptitude</option>
          <option value="Reasoning">Reasoning & Mental Ability</option>
          <option value="English">English Language & Comprehension</option>
          <option value="Economics & Finance">Economics & Financial Systems</option>
          <option value="Technical">Technical & Engineering Specializations</option>
        </select>
      </div>

      <!-- Cognitive Depth Filter (3 cols) -->
      <div class="lg:col-span-3 flex items-center space-x-2">
        <label class="text-slate-400 text-xs font-medium whitespace-nowrap">Min Depth:</label>
        <select
          :value="store.minDepthLevel"
          @change="(e) => store.setMinDepth((e.target as HTMLSelectElement).value as any)"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 font-mono"
        >
          <option value="Foundation">Foundation+ (1.5px)</option>
          <option value="Intermediate">Intermediate+ (2.5px)</option>
          <option value="Advanced">Advanced+ (3.5px)</option>
          <option value="Analytical">Analytical Only (5.0px)</option>
        </select>
      </div>

      <!-- Topic Search Input (2 cols) -->
      <div class="lg:col-span-2 relative">
        <input
          type="text"
          :value="store.searchQuery"
          @input="(e) => store.setSearchQuery((e.target as HTMLInputElement).value)"
          placeholder="Filter topics..."
          class="w-full bg-slate-800 border border-slate-700 rounded-xl pl-3 pr-7 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
        />
        <button
          v-if="store.searchQuery"
          @click="store.setSearchQuery('')"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white text-xs"
        >
          ✕
        </button>
      </div>

      <!-- View Switcher Tabs (3 cols) -->
      <div class="lg:col-span-3 flex rounded-xl bg-slate-800 p-1 border border-slate-700/80">
        <button
          @click="store.activeTab = 'upset'"
          class="flex-1 py-1 rounded-lg text-xs font-semibold transition-colors text-center"
          :class="store.activeTab === 'upset' ? 'bg-emerald-500 text-white shadow' : 'text-slate-400 hover:text-slate-200'"
        >
          UpSet Matrix
        </button>
        <button
          @click="store.activeTab = 'venn'"
          class="flex-1 py-1 rounded-lg text-xs font-semibold transition-colors text-center"
          :class="store.activeTab === 'venn' ? 'bg-emerald-500 text-white shadow' : 'text-slate-400 hover:text-slate-200'"
        >
          Venn (2–4)
        </button>
        <button
          @click="store.activeTab = 'bipartite'"
          class="flex-1 py-1 rounded-lg text-xs font-semibold transition-colors text-center"
          :class="store.activeTab === 'bipartite' ? 'bg-emerald-500 text-white shadow' : 'text-slate-400 hover:text-slate-200'"
        >
          Network
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import {
  useSyllabusVisualizationStore,
  PRESET_OPTIONS,
  CLUSTER_COLORS,
} from '@/stores/useSyllabusVisualizationStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';

const store = useSyllabusVisualizationStore();
const examMaster = useExamMasterStore();

const isExamDropdownOpen = ref<boolean>(false);
const dropdownRef = ref<HTMLDivElement | null>(null);

function getClusterColor(category?: string): string {
  if (!category) return '#3B82F6';
  return CLUSTER_COLORS[category] || '#3B82F6';
}

function getExamPillClass(category?: string): string {
  switch (category) {
    case 'Regulatory':
      return 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300';
    case 'Defense':
      return 'bg-amber-500/10 border-amber-500/30 text-amber-300';
    case 'State-PSC':
      return 'bg-purple-500/10 border-purple-500/30 text-purple-300';
    case 'PSU':
      return 'bg-pink-500/10 border-pink-500/30 text-pink-300';
    case 'Central-Civil':
    default:
      return 'bg-blue-500/10 border-blue-500/30 text-blue-300';
  }
}

const availableExams = computed(() => {
  const selected = new Set(store.selectedExamIds);
  return examMaster.exams.filter((e) => !selected.has(e.exam_id));
});

function selectExamCandidate(examId: string) {
  store.toggleExamSelection(examId);
  isExamDropdownOpen.value = false;
}

function isPresetActive(examIds: string[]): boolean {
  if (examIds.length !== store.selectedExamIds.length) return false;
  const s = new Set(store.selectedExamIds);
  return examIds.every((id) => s.has(id));
}

function handleOutsideClick(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isExamDropdownOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick);
});

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick);
});
</script>

<style scoped>
.popover-enter-active,
.popover-leave-active {
  transition: all 0.15s ease-out;
}
.popover-enter-from,
.popover-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
