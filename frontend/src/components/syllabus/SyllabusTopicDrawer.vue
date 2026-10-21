<template>
  <Teleport to="body">
    <transition name="drawer-fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex justify-end"
        @keydown.escape="handleClose"
      >
        <!-- Backdrop Overlay -->
        <div
          class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity"
          @click="handleClose"
        ></div>

        <!-- Slide-over Drawer Panel -->
        <div
          class="relative w-full max-w-xl h-full bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 shadow-2xl flex flex-col justify-between z-10 overflow-hidden transform transition-transform duration-300"
        >
          <!-- Drawer Header -->
          <div class="p-6 border-b border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-850/50 flex items-start justify-between gap-4">
            <div class="space-y-1.5 min-w-0">
              <div class="flex flex-wrap items-center gap-2 text-xs">
                <span
                  v-if="stageName"
                  class="px-2.5 py-0.5 rounded-md font-semibold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                >
                  {{ stageName }}
                </span>
                <span
                  v-if="paperName"
                  class="px-2.5 py-0.5 rounded-md font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20"
                >
                  {{ paperName }}
                </span>
              </div>
              <h2 class="text-lg sm:text-xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-snug break-words">
                {{ topic?.title }}
              </h2>
            </div>

            <!-- Close Button -->
            <button
              @click="handleClose"
              class="p-2 rounded-xl text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors shrink-0"
              aria-label="Close topic drawer"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Drawer Scrollable Body -->
          <div class="flex-1 overflow-y-auto p-6 space-y-6 text-sm">
            <!-- Checklist Action Card -->
            <div
              class="p-4 rounded-2xl border transition-all flex items-center justify-between gap-4 cursor-pointer select-none"
              :class="
                isCompleted
                  ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/30'
                  : 'bg-slate-50 dark:bg-slate-850 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
              "
              @click="$emit('toggle-completed')"
            >
              <div class="flex items-center space-x-3 min-w-0">
                <div
                  class="w-6 h-6 rounded-lg border flex items-center justify-center transition-all shrink-0"
                  :class="
                    isCompleted
                      ? 'bg-emerald-500 border-emerald-600 text-white shadow-xs'
                      : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800'
                  "
                >
                  <svg v-if="isCompleted" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <div class="font-bold text-slate-900 dark:text-white text-xs sm:text-sm">
                    {{ isCompleted ? 'Preparation Status: Mastered' : 'Preparation Status: Pending' }}
                  </div>
                  <div class="text-[11px] text-slate-500 dark:text-slate-400">
                    {{ isCompleted ? 'Marked complete in your candidate preparation tracker' : 'Click to toggle mastery status' }}
                  </div>
                </div>
              </div>

              <span
                class="px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0"
                :class="
                  isCompleted
                    ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                    : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                "
              >
                {{ isCompleted ? '✓ Done' : '+ Mark Done' }}
              </span>
            </div>

            <!-- Detailed Description -->
            <div class="space-y-2">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Official Curriculum Scope
              </h3>
              <p class="text-slate-700 dark:text-slate-300 leading-relaxed text-sm whitespace-pre-line">
                {{ topic?.description }}
              </p>
            </div>

            <!-- Sub-Points / Curriculum Items -->
            <div v-if="topic?.sub_points?.length" class="space-y-2.5">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Key Focus Areas & Sub-Topics
              </h3>
              <div class="space-y-2">
                <div
                  v-for="(pt, idx) in topic.sub_points"
                  :key="idx"
                  class="flex items-start space-x-2.5 p-3 rounded-xl bg-slate-50 dark:bg-slate-850/80 border border-slate-200 dark:border-slate-800/80 text-xs text-slate-700 dark:text-slate-300"
                >
                  <span class="text-emerald-500 mt-0.5">•</span>
                  <span class="leading-relaxed">{{ pt }}</span>
                </div>
              </div>
            </div>

            <!-- Weightage Estimation -->
            <div v-if="topic?.weightage_estimate" class="p-3.5 rounded-xl bg-sky-50 dark:bg-sky-950/20 border border-sky-200 dark:border-sky-800/40 space-y-1">
              <div class="text-xs font-bold text-sky-800 dark:text-sky-300 flex items-center space-x-1.5">
                <span>📊</span>
                <span>Expected Weightage / Examination Impact</span>
              </div>
              <p class="text-xs text-sky-900 dark:text-sky-200">
                {{ topic.weightage_estimate }}
              </p>
            </div>

            <!-- Official Curriculum Reference -->
            <div class="space-y-2 pt-2 border-t border-slate-200 dark:border-slate-800">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Official Curriculum Authority
              </h3>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-2">
                <div class="text-xs text-slate-600 dark:text-slate-300 space-y-1">
                  <div>
                    <span class="text-slate-400">Source Clause:</span>
                    <span class="font-mono font-medium text-slate-800 dark:text-slate-200 ml-1">
                      {{ topic?.source_clause || 'Official Examination Notification Syllabus Clause' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Drawer Footer -->
          <div class="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-850/50 flex items-center justify-between">
            <button
              @click="$emit('toggle-completed')"
              class="px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-xs"
              :class="
                isCompleted
                  ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20 hover:bg-rose-500/20'
                  : 'bg-emerald-500 text-white hover:bg-emerald-600'
              "
            >
              {{ isCompleted ? 'Mark as Incomplete' : '✓ Mark as Mastered' }}
            </button>

            <button
              @click="handleClose"
              class="px-4 py-2 rounded-xl text-xs font-semibold bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-750 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import type { SyllabusTopic } from '@/types/curriculum';

const props = defineProps<{
  isOpen: boolean;
  topic: SyllabusTopic | null;
  paperName?: string;
  stageName?: string;
  isCompleted: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'toggle-completed'): void;
}>();

function handleClose() {
  emit('close');
}
</script>

<style scoped>
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.25s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
</style>
