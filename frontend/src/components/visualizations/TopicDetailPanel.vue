<template>
  <transition name="slide-panel">
    <div
      v-if="detail"
      class="bg-slate-850 rounded-2xl border border-slate-700 p-5 shadow-2xl space-y-4 text-xs text-slate-200"
    >
      <!-- Header -->
      <div class="flex items-start justify-between gap-3 border-b border-slate-750 pb-3">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span
              class="px-2.5 py-0.5 rounded-md text-[10px] font-bold text-slate-900"
              :style="{ backgroundColor: getDomainColor(detail.topic.domain) }"
            >
              {{ detail.topic.domain }}
            </span>
            <span class="text-[11px] text-slate-400 font-mono">{{ detail.topic.sub_domain }}</span>
            <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono text-slate-400 border border-slate-700">
              {{ detail.topic.topic_id }}
            </span>
          </div>
          <h3 class="text-base font-extrabold text-white leading-snug">
            {{ detail.topic.topic_title }}
          </h3>
        </div>
        <button
          @click="closePanel"
          class="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          title="Close Details Panel"
        >
          ✕
        </button>
      </div>

      <!-- Description -->
      <p class="text-slate-300 leading-relaxed text-xs">
        {{ detail.topic.description }}
      </p>

      <!-- Carry-Over Synergy Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div>
          <span class="text-[10px] text-slate-400 block uppercase tracking-wider">In Active Selection</span>
          <span class="text-sm font-bold font-mono text-emerald-400">
            {{ detail.degreeInSelection }} / {{ store.selectedExamIds.length }} Exams
          </span>
        </div>
        <div>
          <span class="text-[10px] text-slate-400 block uppercase tracking-wider">Universal Prevalence</span>
          <span class="text-sm font-bold font-mono text-sky-400">
            {{ detail.totalExamsRequiring }} Grade A Posts
          </span>
        </div>
        <div class="col-span-2 sm:col-span-1">
          <span class="text-[10px] text-slate-400 block uppercase tracking-wider">Synergy Readiness</span>
          <span class="text-sm font-bold font-mono text-purple-400">
            {{ Math.round((detail.degreeInSelection / store.selectedExamIds.length) * 100) }}% Coverage
          </span>
        </div>
      </div>

      <!-- Statutory Stage Mappings in Active Selection -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">
          Audited Stages & Cognitive Depth Requirements
        </h4>
        <div class="space-y-2 max-h-60 overflow-y-auto pr-1">
          <div
            v-for="m in detail.mappings"
            :key="`${m.exam_id}-${m.stage_name}`"
            class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5"
          >
            <div class="flex items-center justify-between gap-2">
              <span class="font-bold text-white font-mono">{{ getExamLabel(m.exam_id) }}</span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold font-mono text-white"
                :class="getDepthBadgeClass(m.depth_level)"
              >
                {{ m.depth_level }}
              </span>
            </div>
            <div class="text-[11px] text-slate-300 font-medium">
              Stage: {{ m.stage_name }}
              <span v-if="m.weightage_pct_estimate" class="text-emerald-400 font-mono ml-1">
                (~{{ m.weightage_pct_estimate }}% weightage)
              </span>
            </div>
            <div class="text-[10px] text-slate-400 flex items-start space-x-1">
              <span class="text-slate-500 font-semibold">Statutory Clause:</span>
              <span class="italic text-slate-400">{{ m.source_clause_ref }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  useSyllabusVisualizationStore,
  DOMAIN_COLORS,
} from '@/stores/useSyllabusVisualizationStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import type { DepthLevel } from '@/types/syllabus';

const store = useSyllabusVisualizationStore();
const examMaster = useExamMasterStore();

const detail = computed(() => store.activeTopicDetail);

function getExamLabel(examId: string): string {
  const exam = examMaster.examsMap[examId];
  return exam?.short_code || examId.replace(/^(UPSC_|PSU_|IAF_)/, '').replace(/_/g, ' ');
}

function getDomainColor(domain?: string): string {
  if (!domain) return '#38BDF8';
  return DOMAIN_COLORS[domain] || '#38BDF8';
}

function getDepthBadgeClass(depth: DepthLevel): string {
  switch (depth) {
    case 'Analytical':
      return 'bg-pink-500/20 text-pink-300 border border-pink-500/40';
    case 'Advanced':
      return 'bg-amber-500/20 text-amber-300 border border-amber-500/40';
    case 'Intermediate':
      return 'bg-sky-500/20 text-sky-300 border border-sky-500/40';
    case 'Foundation':
    default:
      return 'bg-slate-700 text-slate-300 border border-slate-600';
  }
}

function closePanel() {
  store.setSelectedTopic(null);
  store.setHoveredTopic(null);
}
</script>

<style scoped>
.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: all 0.2s ease-out;
}
.slide-panel-enter-from,
.slide-panel-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
