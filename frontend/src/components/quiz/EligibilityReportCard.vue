<template>
  <div class="w-full max-w-6xl mx-auto px-4 py-8 space-y-8">
    <!-- Header Hero & Metric Overview -->
    <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
      <div class="absolute -right-16 -top-16 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
        <div>
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold mb-3">
            <span>2027 Official Examination Intelligence Cycle</span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Statutory Eligibility Report Card
          </h1>
          <p class="text-sm text-slate-400 mt-2 max-w-2xl">
            Multi-dimensional evaluation across all 36 Indian Grade A civil, regulatory, defense, state PSC, and PSU examinations audited against gazette notification clauses.
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-3 self-start md:self-center">
          <button
            @click="$emit('edit-profile')"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 transition flex items-center"
          >
            <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Edit Profile
          </button>
          <button
            @click="printReport"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 transition shadow-lg shadow-emerald-600/30 flex items-center"
          >
            <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
            </svg>
            Print Dossier
          </button>
        </div>
      </div>

      <!-- High-Level Metric Tiles -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-6 border-t border-slate-800">
        <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-4 text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-white">{{ totalCount }}</span>
          <span class="text-xs font-medium text-slate-400 uppercase tracking-wider mt-1 block">Total Audited</span>
        </div>
        <div class="bg-emerald-950/30 border border-emerald-800/40 rounded-2xl p-4 text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-emerald-400">{{ eligibleCount }}</span>
          <span class="text-xs font-medium text-emerald-300 uppercase tracking-wider mt-1 block">Fully Eligible</span>
        </div>
        <div class="bg-amber-950/30 border border-amber-800/40 rounded-2xl p-4 text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-amber-400">{{ conditionallyEligibleCount }}</span>
          <span class="text-xs font-medium text-amber-300 uppercase tracking-wider mt-1 block">Conditionally Eligible</span>
        </div>
        <div class="bg-rose-950/30 border border-rose-800/40 rounded-2xl p-4 text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-rose-400">{{ ineligibleCount }}</span>
          <span class="text-xs font-medium text-rose-300 uppercase tracking-wider mt-1 block">Ineligible</span>
        </div>
      </div>
    </div>

    <!-- Filter & Search Controls Bar -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-lg">
      <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <!-- Search Input -->
        <div class="relative flex-1">
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by exam title, short code (CSE, RBI, GATE), or administering body..."
            class="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
          />
        </div>

        <!-- Status Filter Tabs -->
        <div class="flex items-center bg-slate-800 p-1 rounded-xl border border-slate-700 overflow-x-auto">
          <button
            v-for="st in statusFilters"
            :key="st.id"
            @click="eligibilityStore.setFilterStatus(st.id)"
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap"
            :class="filterStatus === st.id ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'"
          >
            {{ st.label }}
          </button>
        </div>
      </div>

      <!-- Cluster Filter Pills -->
      <div class="flex items-center space-x-2 overflow-x-auto pb-1 pt-1 border-t border-slate-800/80">
        <span class="text-xs text-slate-400 font-medium whitespace-nowrap mr-1">Cluster:</span>
        <button
          v-for="cl in clusterFilters"
          :key="cl.id"
          @click="eligibilityStore.setFilterCluster(cl.id)"
          class="px-3 py-1 rounded-lg text-xs font-medium transition whitespace-nowrap border"
          :class="filterCluster === cl.id 
            ? 'bg-slate-800 text-white border-emerald-500/60' 
            : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-300'"
        >
          {{ cl.label }} ({{ getClusterCount(cl.id) }})
        </button>
      </div>
    </div>

    <!-- Tabulated Exam Verdict Cards -->
    <div v-if="displayedVerdicts.length > 0" class="space-y-4">
      <div
        v-for="verdict in displayedVerdicts"
        :key="verdict.exam_id"
        class="bg-slate-900 border rounded-2xl p-5 sm:p-6 transition hover:border-slate-700 shadow-md"
        :class="[
          verdict.status === 'ELIGIBLE' ? 'border-emerald-900/60 bg-gradient-to-r from-emerald-950/10 to-transparent' :
          verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'border-amber-900/60 bg-gradient-to-r from-amber-950/10 to-transparent' :
          'border-slate-800'
        ]"
      >
        <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <!-- Exam Title & Conducting Authority -->
          <div class="flex items-start space-x-3">
            <span 
              class="w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm flex-shrink-0"
              :class="[
                verdict.status === 'ELIGIBLE' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                'bg-slate-800 text-slate-400 border border-slate-700'
              ]"
            >
              {{ getExamShortCode(verdict.exam_id) }}
            </span>
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <h3 class="text-base sm:text-lg font-bold text-white">{{ getExamTitle(verdict.exam_id) }}</h3>
                <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                  {{ getExamCategory(verdict.exam_id) }}
                </span>
                <span class="text-xs text-slate-500">
                  by {{ getExamAdminBody(verdict.exam_id) }}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-1 line-clamp-2">
                {{ getExamDescription(verdict.exam_id) }}
              </p>
            </div>
          </div>

          <!-- Status Badge -->
          <div class="self-start sm:self-auto flex-shrink-0">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"
              :class="[
                verdict.status === 'ELIGIBLE' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                'bg-rose-500/20 text-rose-400 border border-rose-500/30'
              ]"
            >
              <span class="w-1.5 h-1.5 rounded-full mr-1.5"
                :class="[
                  verdict.status === 'ELIGIBLE' ? 'bg-emerald-400' :
                  verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'bg-amber-400' :
                  'bg-rose-400'
                ]"
              ></span>
              {{ formatStatus(verdict.status) }}
            </span>
          </div>
        </div>

        <!-- Applied Relaxations Badges -->
        <div v-if="verdict.relaxations_applied && verdict.relaxations_applied.length > 0" class="mt-3 flex flex-wrap gap-1.5">
          <span 
            v-for="(rel, idx) in verdict.relaxations_applied" 
            :key="idx"
            class="text-[11px] px-2.5 py-0.5 rounded-md bg-emerald-950/40 text-emerald-300 border border-emerald-800/40 font-medium"
          >
            ✓ {{ rel }}
          </span>
        </div>

        <!-- Statutory Evaluation Reasons -->
        <div class="mt-4 pt-3 border-t border-slate-800/80">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-1.5">Evaluation Verdict Details:</span>
          <ul class="space-y-1">
            <li
              v-for="(reason, idx) in verdict.reasons"
              :key="idx"
              class="text-xs flex items-start"
              :class="verdict.status === 'INELIGIBLE' ? 'text-rose-300' : verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'text-amber-300' : 'text-slate-300'"
            >
              <span class="mr-2 flex-shrink-0">
                {{ verdict.status === 'ELIGIBLE' ? '✓' : verdict.status === 'CONDITIONALLY_ELIGIBLE' ? 'ℹ️' : '✗' }}
              </span>
              <span>{{ reason }}</span>
            </li>
          </ul>
        </div>

        <!-- Collapsible Official Gazette Citation & Quick Syllabus Action -->
        <div class="mt-4 pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <details class="text-slate-400 group">
            <summary class="cursor-pointer font-medium hover:text-emerald-400 transition flex items-center space-x-1">
              <span>View Official Gazette Citation</span>
              <span class="group-open:rotate-180 transition text-[10px]">▼</span>
            </summary>
            <div class="mt-2 p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-[11px] text-slate-300 space-y-1 font-mono">
              <div><strong class="text-slate-400">Statutory Citation:</strong> {{ verdict.statutory_citation }}</div>
              <div v-if="getExamGazette(verdict.exam_id)"><strong class="text-slate-400">Gazette Ref:</strong> {{ getExamGazette(verdict.exam_id) }}</div>
              <div v-if="getExamTimeline(verdict.exam_id)" class="text-emerald-400 font-sans mt-1">
                📅 2027 Tentative Timeline: {{ getExamTimeline(verdict.exam_id) }}
              </div>
            </div>
          </details>

          <div class="flex items-center space-x-2">
            <router-link
              :to="{ path: '/syllabus', query: { exam: verdict.exam_id } }"
              class="px-3 py-1.5 rounded-lg bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 border border-emerald-500/40 transition flex items-center font-medium"
            >
              <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              Inspect Syllabus Overlap
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center">
      <svg class="mx-auto h-12 w-12 text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <h3 class="text-base font-semibold text-white">No examinations match active filters</h3>
      <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
        Try broadening your search query, or switch cluster and status filter pills.
      </p>
      <button
        @click="resetFilters"
        class="mt-4 px-4 py-2 rounded-xl text-xs font-medium text-emerald-400 bg-emerald-950/40 border border-emerald-800 hover:bg-emerald-900/50 transition"
      >
        Reset All Filters
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import type { ExamRecord } from '@/types/profile';

const props = defineProps<{
  examsMap?: Record<string, ExamRecord>;
}>();

defineEmits(['edit-profile']);

const eligibilityStore = useEligibilityStore();

const totalCount = computed(() => eligibilityStore.totalCount);
const eligibleCount = computed(() => eligibilityStore.eligibleCount);
const conditionallyEligibleCount = computed(() => eligibilityStore.conditionallyEligibleCount);
const ineligibleCount = computed(() => eligibilityStore.ineligibleCount);

const filterCluster = computed(() => eligibilityStore.filterCluster);
const filterStatus = computed(() => eligibilityStore.filterStatus);
const searchQuery = computed({
  get: () => eligibilityStore.searchQuery,
  set: (val: string) => eligibilityStore.setSearchQuery(val),
});

const statusFilters = [
  { id: 'ALL', label: 'All Verdicts' },
  { id: 'ELIGIBLE', label: 'Eligible' },
  { id: 'CONDITIONALLY_ELIGIBLE', label: 'Conditionally Eligible' },
  { id: 'INELIGIBLE', label: 'Ineligible' },
];

const clusterFilters = [
  { id: 'ALL', label: 'All 36 Exams' },
  { id: 'Central-Civil', label: 'Central Civil' },
  { id: 'Regulatory', label: 'Regulatory & Finance' },
  { id: 'Defense', label: 'Defense' },
  { id: 'State-PSC', label: 'State PSCs' },
  { id: 'PSU', label: 'PSUs (GATE)' },
];

const displayedVerdicts = computed(() => {
  return eligibilityStore.filteredVerdicts(props.examsMap || {});
});

function getClusterCount(clusterId: string): number {
  if (clusterId === 'ALL') return totalCount.value;
  if (!props.examsMap) return 0;
  return Object.values(eligibilityStore.verdicts).filter((v) => {
    const exam = props.examsMap?.[v.exam_id];
    return exam && exam.category === clusterId;
  }).length;
}

function formatStatus(status: string): string {
  switch (status) {
    case 'ELIGIBLE': return 'Eligible';
    case 'CONDITIONALLY_ELIGIBLE': return 'Conditionally Eligible';
    case 'INELIGIBLE': return 'Ineligible';
    default: return status;
  }
}

function getExamShortCode(examId: string): string {
  return props.examsMap?.[examId]?.short_code || examId.split('_').slice(-1)[0];
}

function getExamTitle(examId: string): string {
  return props.examsMap?.[examId]?.title || examId;
}

function getExamCategory(examId: string): string {
  const cat = props.examsMap?.[examId]?.category || 'Grade A';
  return cat.replace(/-/g, ' ');
}

function getExamAdminBody(examId: string): string {
  return props.examsMap?.[examId]?.administering_body || 'Government Commission';
}

function getExamDescription(examId: string): string {
  return props.examsMap?.[examId]?.description || '';
}

function getExamGazette(examId: string): string | undefined {
  return props.examsMap?.[examId]?.latest_gazette_ref;
}

function getExamNotificationUrl(examId: string): string {
  return props.examsMap?.[examId]?.latest_official_notification_url || 'https://upsc.gov.in';
}

function getExamTimeline(examId: string): string {
  const timeline = props.examsMap?.[examId]?.tentative_timeline_2027;
  if (!timeline) return '2027 Annual Cycle';
  if (typeof timeline === 'string') {
    try {
      const parsed = JSON.parse(timeline);
      return (
        parsed.prelims_date ||
        parsed.written_exam_date ||
        parsed.exam_date ||
        parsed.notification_month ||
        '2027 Cycle'
      );
    } catch {
      return timeline;
    }
  }
  return (
    timeline.prelims_date ||
    timeline.written_exam_date ||
    timeline.exam_date ||
    timeline.notification_month ||
    '2027 Cycle'
  );
}

function resetFilters() {
  eligibilityStore.setFilterCluster('ALL');
  eligibilityStore.setFilterStatus('ALL');
  eligibilityStore.setSearchQuery('');
}

function printReport() {
  if (typeof window !== 'undefined') {
    window.print();
  }
}
</script>
