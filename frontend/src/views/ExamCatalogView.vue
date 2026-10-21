<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Audited Grade A Examinations</h1>
        <p class="text-sm text-slate-400">Verified official notifications, statutory clauses, and 2027 cycles across 36 premier cadres.</p>
      </div>

      <!-- Search Input -->
      <div class="w-full md:w-72">
        <input
          v-model="examStore.searchQuery"
          type="text"
          placeholder="Search by title, code or body..."
          class="w-full px-3.5 py-2 rounded-lg bg-slate-800 border border-slate-700 text-sm text-white focus:outline-none focus:border-emerald-500"
        />
      </div>
    </div>

    <!-- Cluster Pill Filter -->
    <div class="flex flex-wrap gap-2">
      <button
        v-for="f in clusterFilters"
        :key="f.value"
        @click="examStore.selectedCluster = f.value"
        class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
        :class="examStore.selectedCluster === f.value ? 'bg-emerald-500 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="examStore.isLoading" class="py-12 text-center text-slate-400">
      Loading audited examinations...
    </div>

    <!-- Exam Cards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="exam in examStore.filteredExams"
        :key="exam.exam_id"
        class="p-5 rounded-xl bg-slate-850 border border-slate-800 hover:border-slate-700 transition-colors flex flex-col justify-between"
      >
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs px-2.5 py-0.5 rounded font-medium bg-slate-800 text-slate-300 border border-slate-700">
              {{ exam.category }}
            </span>
            <span class="text-xs text-slate-400 font-mono">{{ exam.short_code }}</span>
          </div>

          <h2 class="text-lg font-bold text-white leading-snug">{{ exam.title }}</h2>
          <p class="text-xs text-slate-400 line-clamp-2">{{ exam.description }}</p>

          <div class="text-xs text-slate-300 space-y-1 pt-2 border-t border-slate-800">
            <div><span class="text-slate-500">Administered by:</span> {{ exam.administering_body }}</div>
            <div v-if="exam.tentative_timeline_2027">
              <span class="text-slate-500">2027 Prelims/Phase 1:</span>
              <span class="text-emerald-400 ml-1">
                {{ formatTimeline(exam.tentative_timeline_2027) }}
              </span>
            </div>
          </div>
        </div>

        <div class="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs">
          <a
            :href="exam.latest_official_notification_url"
            target="_blank"
            rel="noopener noreferrer"
            class="text-emerald-400 hover:text-emerald-300 underline font-medium"
          >
            Official Notification ↗
          </a>
          <router-link
            to="/quiz"
            class="text-slate-400 hover:text-white"
          >
            Check Eligibility →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useExamMasterStore } from '@/stores/useExamMasterStore';

const examStore = useExamMasterStore();

const clusterFilters = [
  { label: 'All Exams (36)', value: 'ALL' },
  { label: 'Central Civil', value: 'Central-Civil' },
  { label: 'Regulatory', value: 'Regulatory' },
  { label: 'Defense', value: 'Defense' },
  { label: 'State PSC', value: 'State-PSC' },
  { label: 'PSU', value: 'PSU' },
];

onMounted(async () => {
  await examStore.loadExams();
});

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
</script>
