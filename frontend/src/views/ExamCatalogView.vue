<template>
  <div class="space-y-6 pb-12 max-w-full overflow-hidden">
    <!-- Catalog Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Official Examinations</h1>
      </div>

      <!-- Search Input -->
      <div class="w-full md:w-80">
        <input
          v-model="examStore.searchQuery"
          type="text"
          placeholder="Search by title, code or authority..."
          class="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500 shadow-xs"
        />
      </div>
    </div>

    <!-- Hidden Exams Banner if any are hidden -->
    <div
      v-if="hiddenStore.hiddenExamsCount > 0"
      class="p-3.5 rounded-xl bg-slate-100 dark:bg-slate-850 border border-slate-200 dark:border-slate-700/80 text-xs flex items-center justify-between"
    >
      <div class="flex items-center space-x-2 text-slate-600 dark:text-slate-300">
        <span>👁️‍🗨️</span>
        <span>
          <strong>{{ hiddenStore.hiddenExamsCount }}</strong> examination(s) hidden from active catalog.
        </span>
      </div>
      <router-link
        to="/hidden"
        class="text-xs font-bold text-emerald-600 dark:text-emerald-400 hover:underline"
      >
        View Hidden Examinations →
      </router-link>
    </div>

    <!-- Dual Filter Controls: Cluster & Eligibility Status -->
    <div class="space-y-3">
      <!-- Cluster Pill Filter -->
      <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
        <button
          v-for="f in clusterFilters"
          :key="f.value"
          @click="examStore.selectedCluster = f.value"
          class="px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-xs"
          :class="
            examStore.selectedCluster === f.value
              ? 'bg-emerald-500 text-white'
              : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-750 border border-slate-200 dark:border-slate-700'
          "
        >
          {{ f.label }}
        </button>
      </div>

      <!-- Eligibility Filter Pills (No Conditional Tier) -->
      <div class="flex flex-wrap items-center gap-1.5 text-xs">
        <span class="text-slate-500 text-[11px] font-semibold uppercase mr-1">Eligibility:</span>
        <button
          @click="statusFilter = 'ALL'"
          class="px-2.5 py-1 rounded-lg font-medium transition-colors border"
          :class="
            statusFilter === 'ALL'
              ? 'bg-slate-700 text-white border-slate-600'
              : 'bg-slate-100 dark:bg-slate-850 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:text-slate-900 dark:hover:text-white'
          "
        >
          All ({{ displayedExams.length }})
        </button>
        <button
          @click="statusFilter = 'ELIGIBLE'"
          class="px-2.5 py-1 rounded-lg font-medium transition-colors border"
          :class="
            statusFilter === 'ELIGIBLE'
              ? 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 border-emerald-500/50'
              : 'bg-slate-100 dark:bg-slate-850 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:text-emerald-600 dark:hover:text-emerald-400'
          "
        >
          Eligible ({{ eligibilityStore.eligibleCount }})
        </button>
        <button
          @click="statusFilter = 'NEEDS_INFO'"
          class="px-2.5 py-1 rounded-lg font-medium transition-colors border"
          :class="
            statusFilter === 'NEEDS_INFO'
              ? 'bg-amber-500/20 text-amber-700 dark:text-amber-300 border-amber-500/50'
              : 'bg-slate-100 dark:bg-slate-850 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:text-amber-600 dark:hover:text-amber-400'
          "
        >
          Missing Info ({{ eligibilityStore.needsInfoCount }})
        </button>
        <button
          @click="statusFilter = 'INELIGIBLE'"
          class="px-2.5 py-1 rounded-lg font-medium transition-colors border"
          :class="
            statusFilter === 'INELIGIBLE'
              ? 'bg-rose-500/20 text-rose-700 dark:text-rose-300 border-rose-500/50'
              : 'bg-slate-100 dark:bg-slate-850 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:text-rose-600 dark:hover:text-rose-400'
          "
        >
          Ineligible ({{ eligibilityStore.ineligibleCount }})
        </button>
      </div>
    </div>

    <!-- Exam Cards Grid -->
    <div v-if="displayedExams.length === 0" class="py-16 text-center text-slate-400 text-sm">
      No examinations match your current filters.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="exam in displayedExams"
        :key="exam.exam_id"
        @click="goToExam(exam.exam_id)"
        class="p-5 rounded-2xl bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-slate-400 dark:hover:border-slate-700 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between shadow-xs group"
      >
        <div class="space-y-3">
          <!-- Top Row: Cluster Pill, Live Eligibility Pill & Hide Button -->
          <div class="flex items-center justify-between gap-2">
            <span class="text-[11px] px-2.5 py-0.5 rounded-md font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
              {{ formatCategory(exam.category) }}
            </span>

            <div class="flex items-center space-x-2">
              <div v-if="getVerdict(exam.exam_id)" class="flex items-center">
                <span
                  class="px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider border flex items-center space-x-1"
                  :class="getStatusBadgeClass(getVerdict(exam.exam_id)!.status)"
                >
                  <span>{{ getStatusIcon(getVerdict(exam.exam_id)!.status) }}</span>
                  <span>{{ formatStatus(getVerdict(exam.exam_id)!.status) }}</span>
                </span>
              </div>

              <!-- Quick Hide Button -->
              <button
                @click.stop="hiddenStore.hideExam(exam.exam_id)"
                class="p-1 rounded-md text-slate-400 hover:text-rose-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                title="Hide this exam"
              >
                🚫
              </button>
            </div>
          </div>

          <!-- Exam Title & Short Code -->
          <div>
            <div class="text-xs text-slate-500 dark:text-slate-400 font-mono font-bold">{{ exam.short_code }}</div>
            <h2 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors leading-snug mt-0.5 break-words">
              {{ exam.title }}
            </h2>
          </div>

          <!-- Description -->
          <p class="text-xs text-slate-600 dark:text-slate-400 line-clamp-2 leading-relaxed break-words">
            {{ exam.description }}
          </p>

          <!-- Missing Requirements Alert on Card -->
          <div
            v-if="getVerdict(exam.exam_id)?.status === 'NEEDS_INFO' && getVerdict(exam.exam_id)?.skipped_requirements?.length"
            class="p-2.5 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-[11px] text-amber-800 dark:text-amber-300 space-y-1"
          >
            <div class="font-bold flex items-center space-x-1 text-amber-700 dark:text-amber-400">
              <span>⚠️</span>
              <span>Missing Profile Input:</span>
            </div>
            <div class="text-amber-800 dark:text-amber-200 truncate">
              {{ getVerdict(exam.exam_id)!.skipped_requirements![0] }}
            </div>
          </div>

          <!-- 2027 Key Date & Authority Info -->
          <div class="text-xs text-slate-700 dark:text-slate-300 space-y-1 pt-2.5 border-t border-slate-100 dark:border-slate-800/80">
            <div class="flex justify-between items-center gap-1">
              <span class="text-slate-500 text-[11px]">Authority:</span>
              <span class="text-slate-800 dark:text-slate-300 font-medium truncate">{{ exam.administering_body }}</span>
            </div>
            <div v-if="exam.tentative_timeline_2027" class="flex justify-between items-center gap-1">
              <span class="text-slate-500 text-[11px]">2027 Prelims Date:</span>
              <span class="text-emerald-600 dark:text-emerald-400 font-mono font-bold text-[11px] truncate">
                {{ formatTimeline(exam.tentative_timeline_2027) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Card Footer -->
        <div class="pt-3.5 mt-3.5 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
          <span class="text-emerald-600 dark:text-emerald-400 group-hover:text-emerald-700 dark:group-hover:text-emerald-300 font-semibold flex items-center space-x-1">
            <span>View Statutory Rules & Syllabus</span>
            <span class="group-hover:translate-x-1 transition-transform">→</span>
          </span>
          <span class="text-slate-400 text-[11px] font-mono">
            Inspect
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useHiddenStore } from '@/stores/useHiddenStore';
import type { EligibilityVerdict, ExamRecord } from '@/types/profile';

const router = useRouter();
const examStore = useExamMasterStore();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const hiddenStore = useHiddenStore();

const statusFilter = ref<string>('ALL');

const clusterFilters = [
  { label: 'All Exams (36)', value: 'ALL' },
  { label: 'Central Civil', value: 'Central-Civil' },
  { label: 'Regulatory', value: 'Regulatory' },
  { label: 'Defense', value: 'Defense' },
  { label: 'State PSC', value: 'State-PSC' },
  { label: 'PSU', value: 'PSU' },
];

onMounted(async () => {
  hiddenStore.loadHiddenItems();
  await examStore.loadExams();
  await profileStore.loadInitialProfile();
  await eligibilityStore.evaluateAllExams(profileStore.profile);
});

function getVerdict(examId: string): EligibilityVerdict | undefined {
  return eligibilityStore.verdicts[examId];
}

const displayedExams = computed<ExamRecord[]>(() => {
  let list = examStore.filteredExams;

  // Filter out hidden exams
  list = list.filter((exam) => !hiddenStore.isExamHidden(exam.exam_id));

  if (statusFilter.value !== 'ALL') {
    list = list.filter((exam) => {
      const v = getVerdict(exam.exam_id);
      return v && v.status === statusFilter.value;
    });
  }
  return list;
});

function goToExam(examId: string) {
  router.push(`/exams/${examId}`);
}

function formatTimeline(timeline: any): string {
  if (!timeline) return 'Tentative 2027';
  if (typeof timeline === 'string') {
    try {
      const parsed = JSON.parse(timeline);
      return parsed.prelims_stage_1 || parsed.prelims_date || parsed.prelims_or_interview || parsed.notification_month || 'Tentative 2027';
    } catch {
      return timeline;
    }
  }
  return timeline.prelims_stage_1 || timeline.prelims_date || timeline.prelims_or_interview || timeline.notification_month || 'Tentative 2027';
}

function formatCategory(category?: string): string {
  return category ? category.replace(/-/g, ' ') : '';
}

function formatStatus(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'Eligible';
    case 'NEEDS_INFO':
      return 'Missing Info';
    case 'INELIGIBLE':
      return 'Ineligible';
    default:
      return status;
  }
}

function getStatusIcon(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return '●';
    case 'NEEDS_INFO':
      return '▲';
    case 'INELIGIBLE':
      return '✕';
    default:
      return '○';
  }
}

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/40';
    case 'NEEDS_INFO':
      return 'bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/40';
    case 'INELIGIBLE':
      return 'bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/40';
    default:
      return 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700';
  }
}
</script>
