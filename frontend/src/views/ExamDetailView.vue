<template>
  <div class="space-y-6 pb-16">
    <!-- Back Navigation & Breadcrumb -->
    <div class="flex items-center justify-between">
      <router-link
        to="/exams"
        class="inline-flex items-center space-x-2 text-sm text-slate-400 hover:text-white transition-colors"
      >
        <span class="text-base">←</span>
        <span>Back to Exam Catalog</span>
      </router-link>

      <div class="flex items-center space-x-3">
        <button
          @click="openInSyllabusExplorer"
          class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 transition-all shadow-sm"
        >
          <span>🔀 Compare in Syllabus Overlap</span>
        </button>
        <a
          v-if="exam?.latest_official_notification_url"
          :href="exam.latest_official_notification_url"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition-colors"
        >
          <span>Official Notification ↗</span>
        </a>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="py-16 text-center text-slate-400">
      Loading audited examination details...
    </div>

    <!-- Not Found State -->
    <div v-else-if="!exam" class="p-12 text-center bg-slate-900 rounded-2xl border border-slate-800 space-y-4">
      <h2 class="text-xl font-bold text-white">Examination Not Found</h2>
      <p class="text-sm text-slate-400">We couldn't find an audited record for ID: {{ examId }}</p>
      <router-link to="/exams" class="inline-block px-4 py-2 rounded-lg bg-emerald-500 text-white font-semibold text-xs">
        Return to Catalog
      </router-link>
    </div>

    <!-- Exam Content -->
    <div v-else class="space-y-6">
      <!-- Exam Hero Card -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 sm:p-8 shadow-xl space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center space-x-2.5">
            <span class="px-2.5 py-1 rounded-md text-xs font-bold font-mono tracking-wider bg-slate-800 text-emerald-400 border border-slate-700">
              {{ exam.short_code }}
            </span>
            <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
              {{ exam.category }}
            </span>
            <span class="text-xs text-slate-500 hidden sm:inline">•</span>
            <span class="text-xs text-slate-400 hidden sm:inline">{{ exam.administering_body }}</span>
          </div>

          <!-- Live Eligibility Status Pill -->
          <div v-if="verdict" class="flex items-center space-x-2">
            <span
              class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border flex items-center space-x-1.5"
              :class="getStatusBadgeClass(verdict.status)"
            >
              <span>{{ getStatusIcon(verdict.status) }}</span>
              <span>{{ formatStatus(verdict.status) }}</span>
            </span>
          </div>
        </div>

        <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
          {{ exam.title }}
        </h1>
        <p class="text-sm sm:text-base text-slate-300 leading-relaxed max-w-4xl">
          {{ exam.description }}
        </p>

        <!-- Meta Details Row -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-slate-800 text-xs">
          <div>
            <span class="text-slate-500 block text-[11px]">Administering Authority</span>
            <span class="text-white font-medium">{{ exam.administering_body }}</span>
          </div>
          <div>
            <span class="text-slate-500 block text-[11px]">Examination Frequency</span>
            <span class="text-white font-medium">{{ exam.frequency || 'Annual' }}</span>
          </div>
          <div v-if="exam.latest_gazette_ref">
            <span class="text-slate-500 block text-[11px]">Statutory Gazette Clause</span>
            <span class="text-slate-300 font-mono text-[11px] truncate block">{{ exam.latest_gazette_ref }}</span>
          </div>
        </div>
      </div>

      <!-- Personalized Eligibility Audit Banner -->
      <div
        v-if="verdict"
        class="rounded-2xl border p-5 shadow-lg space-y-3"
        :class="getVerdictContainerClass(verdict.status)"
      >
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-center space-x-2.5">
            <span class="text-xl">{{ getStatusIcon(verdict.status) }}</span>
            <div>
              <h3 class="text-base font-bold text-white">
                Personalized Eligibility: {{ formatStatus(verdict.status) }}
              </h3>
              <p class="text-xs text-slate-300">
                Audited against your saved candidate profile for the 2027 cycle.
              </p>
            </div>
          </div>

          <router-link
            to="/profile"
            class="self-start sm:self-auto px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors"
          >
            Edit Profile →
          </router-link>
        </div>

        <!-- Skipped Requirements Alert (Needs Info) -->
        <div
          v-if="verdict.status === 'NEEDS_INFO' && verdict.skipped_requirements?.length"
          class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs text-amber-200 space-y-2"
        >
          <div class="font-bold flex items-center space-x-1.5 text-amber-400">
            <span>⚠️</span>
            <span>You skipped criteria required for this specific examination:</span>
          </div>
          <ul class="list-disc list-inside space-y-1 text-slate-200">
            <li v-for="req in verdict.skipped_requirements" :key="req">
              {{ req }}
            </li>
          </ul>
          <div class="pt-1">
            <router-link
              to="/profile"
              class="inline-block text-xs font-bold text-amber-400 hover:text-amber-300 underline"
            >
              Update your profile with these details to verify eligibility →
            </router-link>
          </div>
        </div>

        <!-- Statutory Evaluation Reasons -->
        <div class="space-y-1 text-xs">
          <div
            v-for="(r, idx) in verdict.reasons"
            :key="idx"
            class="flex items-start space-x-2 text-slate-300"
          >
            <span class="text-slate-500">•</span>
            <span>{{ r }}</span>
          </div>
        </div>

        <!-- Relaxations Applied -->
        <div v-if="verdict.relaxations_applied?.length" class="pt-2 border-t border-slate-800 flex flex-wrap gap-2 text-[11px]">
          <span class="text-slate-400 font-semibold">Relaxations Applied:</span>
          <span
            v-for="rel in verdict.relaxations_applied"
            :key="rel"
            class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium"
          >
            {{ rel }}
          </span>
        </div>
      </div>

      <!-- Two-Column Layout: 2027 Timeline & Statutory Rules -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Card 1: 2027 Key Dates & Timeline -->
        <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-4">
          <div class="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <span class="text-lg">📅</span>
            <h3 class="text-base font-bold text-white tracking-wide">2027 Examination Schedule & Dates</h3>
          </div>

          <div v-if="!timelineEntries.length" class="text-xs text-slate-400 py-4">
            Tentative schedule for 2027 cycle pending official gazette release.
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="item in timelineEntries"
              :key="item.label"
              class="flex items-center justify-between p-3 rounded-xl bg-slate-850 border border-slate-800/80"
            >
              <span class="text-xs font-medium text-slate-300">{{ item.label }}</span>
              <span class="text-xs font-bold font-mono text-emerald-400">{{ item.value }}</span>
            </div>
          </div>
        </div>

        <!-- Card 2: Official Statutory Rules Summary -->
        <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-4">
          <div class="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <span class="text-lg">⚖️</span>
            <h3 class="text-base font-bold text-white tracking-wide">Official Eligibility Requirements</h3>
          </div>

          <div class="space-y-2.5 text-xs text-slate-300">
            <div class="flex justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Reference Cutoff Rule:</span>
              <span class="font-medium text-white">{{ examRule?.cutoff_rule || 'Exam Year Cycle' }}</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">General Age Bracket:</span>
              <span class="font-bold text-white">{{ examRule?.min_age_gen || 21 }} – {{ examRule?.max_age_gen || 32 }} years</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Minimum Degree:</span>
              <span class="font-medium text-white">{{ examRule?.min_education || 'Bachelor Degree' }}</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Accepted Disciplines:</span>
              <span class="font-medium text-emerald-400 truncate max-w-[240px]">
                {{ examRule?.accepted_disciplines?.join(', ') || 'Any Discipline' }}
              </span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Final Year Students Allowed:</span>
              <span class="font-semibold" :class="examRule?.allows_final_year ? 'text-emerald-400' : 'text-rose-400'">
                {{ examRule?.allows_final_year ? 'Yes (Provisional)' : 'No (Strict passing proof required)' }}
              </span>
            </div>
            <div v-if="examRule?.physical_standards" class="py-1.5 border-b border-slate-800 space-y-1">
              <span class="text-slate-400 block">Physical Standards:</span>
              <div class="text-[11px] text-slate-300 space-y-0.5">
                <div v-if="examRule.physical_standards.min_height_male_cm">
                  Height: Min {{ examRule.physical_standards.min_height_male_cm }} cm (Male) / {{ examRule.physical_standards.min_height_female_cm || 152 }} cm (Female)
                </div>
                <div v-if="examRule.physical_standards.min_chest_male_cm">
                  Chest: Min {{ examRule.physical_standards.min_chest_male_cm }} cm (Expansion 5 cm)
                </div>
              </div>
            </div>
            <div class="py-1.5 text-slate-400 text-[11px]">
              <strong class="text-slate-300">Gazette Citation:</strong>
              <div class="font-mono text-slate-400 mt-0.5">{{ examRule?.citation || exam.latest_gazette_ref || 'Official Notification' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Audited Syllabus Breakdown -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
          <div>
            <h3 class="text-base font-bold text-white tracking-wide flex items-center space-x-2">
              <span>📚 Audited Syllabus & Mapped Topics</span>
              <span class="px-2 py-0.5 rounded-full bg-slate-800 text-emerald-400 font-mono text-xs">
                {{ examTopics.length }} Topics
              </span>
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">
              Curated topics mapped to official notifications with depth levels.
            </p>
          </div>

          <button
            @click="openInSyllabusExplorer"
            class="px-3.5 py-2 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-600 text-white shadow transition-colors flex items-center space-x-1.5"
          >
            <span>Compare in Overlap Explorer →</span>
          </button>
        </div>

        <div v-if="examTopics.length === 0" class="py-8 text-center text-slate-400 text-xs">
          Loading audited syllabus topics...
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="item in examTopics"
            :key="item.topic_id"
            class="p-3.5 rounded-xl bg-slate-850 border border-slate-800 space-y-1.5"
          >
            <div class="flex items-center justify-between text-[11px]">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-medium">
                {{ item.domain }}
              </span>
              <span class="px-2 py-0.5 rounded font-mono text-[10px] bg-slate-800/80 text-sky-400">
                {{ item.depth || 'Foundation' }}
              </span>
            </div>
            <h4 class="text-xs font-bold text-white">{{ item.topic_title }}</h4>
            <div class="text-[10px] text-slate-400">Sub-domain: {{ item.sub_domain }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import { AUTHORITATIVE_EXAM_RULES } from '@/services/eligibilityEngine';
import type { EligibilityVerdict } from '@/types/profile';

const route = useRoute();
const router = useRouter();

const examStore = useExamMasterStore();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const vizStore = useSyllabusVisualizationStore();

const examId = computed(() => route.params.id as string);
const exam = computed(() => examStore.examsMap[examId.value]);
const examRule = computed(() => AUTHORITATIVE_EXAM_RULES[examId.value]);
const isLoading = computed(() => examStore.isLoading);

onMounted(async () => {
  await examStore.loadExams();
  await profileStore.loadInitialProfile();
  await vizStore.loadSyllabusData();
  await eligibilityStore.evaluateAllExams(profileStore.profile);
});

const verdict = computed<EligibilityVerdict | undefined>(() => {
  return eligibilityStore.verdicts[examId.value];
});

const timelineEntries = computed(() => {
  const t = exam.value?.tentative_timeline_2027;
  if (!t) return [];
  const entries: { label: string; value: string }[] = [];
  
  if (t.notification_month) entries.push({ label: 'Notification Window', value: t.notification_month });
  if (t.application_window) entries.push({ label: 'Application Window', value: t.application_window });
  if (t.prelims_stage_1 || t.prelims_date) entries.push({ label: 'Prelims / Phase 1 Exam', value: t.prelims_stage_1 || t.prelims_date });
  if (t.mains_stage_2 || t.mains_date) entries.push({ label: 'Mains / Phase 2 Exam', value: t.mains_stage_2 || t.mains_date });
  if (t.interview_window) entries.push({ label: 'Interview & Personality Test', value: t.interview_window });
  if (t.final_result) entries.push({ label: 'Final Result Declaration', value: t.final_result });

  return entries;
});

const examTopics = computed(() => {
  const mappings = vizStore.allMappings.filter((m) => m.exam_id === examId.value);
  return mappings.map((m) => {
    const topic = vizStore.topicsMap[m.topic_id];
    return {
      topic_id: m.topic_id,
      topic_title: topic?.topic_title || m.topic_id,
      domain: topic?.domain || 'General',
      sub_domain: topic?.sub_domain || 'General',
      depth: m.depth_level,
    };
  });
});

function formatStatus(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'Eligible';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'Conditionally Eligible';
    case 'NEEDS_INFO':
      return 'Needs More Info';
    case 'INELIGIBLE':
      return 'Ineligible';
    default:
      return status;
  }
}

function getStatusIcon(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return '✅';
    case 'CONDITIONALLY_ELIGIBLE':
      return '🔷';
    case 'NEEDS_INFO':
      return '⚠️';
    case 'INELIGIBLE':
      return '❌';
    default:
      return 'ℹ️';
  }
}

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
    case 'NEEDS_INFO':
      return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    case 'INELIGIBLE':
      return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    default:
      return 'bg-slate-800 text-slate-300 border-slate-700';
  }
}

function getVerdictContainerClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-950/20 border-emerald-500/30';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'bg-blue-950/20 border-blue-500/30';
    case 'NEEDS_INFO':
      return 'bg-amber-950/20 border-amber-500/30';
    case 'INELIGIBLE':
      return 'bg-rose-950/20 border-rose-500/30';
    default:
      return 'bg-slate-900 border-slate-800';
  }
}

function openInSyllabusExplorer() {
  if (!vizStore.selectedExamIds.includes(examId.value)) {
    vizStore.toggleExamSelection(examId.value);
  }
  router.push('/syllabus');
}
</script>