<template>
  <div class="space-y-6 pb-16 max-w-full overflow-hidden">
    <!-- Back Navigation & Action Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <router-link
        to="/exams"
        class="inline-flex items-center space-x-2 text-sm text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
      >
        <span class="text-base">←</span>
        <span>Back to All Examinations</span>
      </router-link>

      <div class="flex items-center space-x-2.5">
        <!-- Hide / Disable Exam Button -->
        <button
          @click="hiddenStore.toggleExamHidden(examId)"
          class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors border"
          :class="
            hiddenStore.isExamHidden(examId)
              ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30 hover:bg-rose-500/20'
              : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-750'
          "
        >
          <span>{{ hiddenStore.isExamHidden(examId) ? '👁️ Unhide Examination' : '🚫 Hide Examination' }}</span>
        </button>
      </div>
    </div>

    <!-- Hidden Exam Banner if Hidden -->
    <div
      v-if="hiddenStore.isExamHidden(examId)"
      class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-300 dark:border-rose-500/30 text-xs text-rose-800 dark:text-rose-300 flex items-center justify-between"
    >
      <span>⚠️ You have hidden this examination. It will not appear in the active catalog.</span>
      <button
        @click="hiddenStore.unhideExam(examId)"
        class="font-bold underline hover:text-rose-600"
      >
        Restore Visibility
      </button>
    </div>

    <!-- Not Found State -->
    <div v-if="!exam" class="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-4">
      <h2 class="text-xl font-bold text-slate-900 dark:text-white">Examination Not Found</h2>
      <p class="text-sm text-slate-500 dark:text-slate-400">We couldn't find an audited record for ID: {{ examId }}</p>
      <router-link to="/exams" class="inline-block px-4 py-2 rounded-lg bg-emerald-500 text-white font-semibold text-xs">
        Return to Catalog
      </router-link>
    </div>

    <!-- Exam Content (Renders Instantly) -->
    <div v-else class="space-y-6">
      <!-- Exam Hero Card -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-sm dark:shadow-xl space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center space-x-2.5">
            <span class="px-2.5 py-1 rounded-md text-xs font-bold font-mono tracking-wider bg-slate-100 dark:bg-slate-800 text-emerald-600 dark:text-emerald-400 border border-slate-300 dark:border-slate-700">
              {{ exam.short_code }}
            </span>
            <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-300 dark:border-slate-700">
              {{ formatCategory(exam.category) }}
            </span>
            <span class="text-xs text-slate-400 hidden sm:inline">•</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 hidden sm:inline">{{ exam.administering_body }}</span>
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

        <h1 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight break-words">
          {{ exam.title }}
        </h1>
        <p class="text-sm sm:text-base text-slate-600 dark:text-slate-300 leading-relaxed max-w-4xl break-words">
          {{ exam.description }}
        </p>

        <!-- Meta Details Row -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-slate-200 dark:border-slate-800 text-xs">
          <div>
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Administering Authority</span>
            <span class="text-slate-900 dark:text-white font-medium">{{ exam.administering_body }}</span>
          </div>
          <div>
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Examination Frequency</span>
            <span class="text-slate-900 dark:text-white font-medium">{{ exam.frequency || 'Annual' }}</span>
          </div>
          <div v-if="exam.latest_gazette_ref">
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Statutory Gazette Clause</span>
            <span class="text-slate-700 dark:text-slate-300 font-mono text-[11px] break-words block">{{ exam.latest_gazette_ref }}</span>
          </div>
        </div>
      </div>

      <!-- Personalized Eligibility Audit Banner -->
      <div
        v-if="verdict"
        class="rounded-2xl border p-5 shadow-sm dark:shadow-lg space-y-3"
        :class="getVerdictContainerClass(verdict.status)"
      >
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-center space-x-2.5">
            <span class="text-xl">{{ getStatusIcon(verdict.status) }}</span>
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white">
                Personalized Eligibility: {{ formatStatus(verdict.status) }}
              </h3>
              <p class="text-xs text-slate-600 dark:text-slate-300">
                Audited against your candidate profile for the 2027 cycle.
              </p>
            </div>
          </div>

          <router-link
            to="/profile"
            class="self-start sm:self-auto px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-700 transition-colors"
          >
            Edit Profile →
          </router-link>
        </div>

        <!-- Missing Info Alert (Needs Info) -->
        <div
          v-if="verdict.status === 'NEEDS_INFO' && verdict.skipped_requirements?.length"
          class="p-4 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-xs text-amber-900 dark:text-amber-200 space-y-2"
        >
          <div class="font-bold flex items-center space-x-1.5 text-amber-800 dark:text-amber-400">
            <span>⚠️</span>
            <span>Required profile information missing for this examination:</span>
          </div>
          <ul class="list-disc list-inside space-y-1 text-slate-700 dark:text-slate-200">
            <li v-for="req in verdict.skipped_requirements" :key="req" class="break-words">
              {{ req }}
            </li>
          </ul>
          <div class="pt-1">
            <router-link
              to="/profile"
              class="inline-block text-xs font-bold text-amber-700 dark:text-amber-400 hover:underline"
            >
              Complete your profile with these details to verify eligibility →
            </router-link>
          </div>
        </div>

        <!-- Statutory Evaluation Reasons -->
        <div class="space-y-1 text-xs">
          <div
            v-for="(r, idx) in verdict.reasons"
            :key="idx"
            class="flex items-start space-x-2 text-slate-700 dark:text-slate-300"
          >
            <span class="text-slate-400">•</span>
            <span class="break-words min-w-0">{{ r }}</span>
          </div>
        </div>

        <!-- Relaxations Applied -->
        <div v-if="verdict.relaxations_applied?.length" class="pt-2 border-t border-slate-200 dark:border-slate-800 flex flex-wrap gap-2 text-[11px]">
          <span class="text-slate-500 dark:text-slate-400 font-semibold">Relaxations Applied:</span>
          <span
            v-for="rel in verdict.relaxations_applied"
            :key="rel"
            class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-medium"
          >
            {{ rel }}
          </span>
        </div>
      </div>

      <!-- Two-Column Layout: 2027 Timeline & Statutory Rules -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Card 1: 2027 Key Dates & Timeline -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-4">
          <div class="flex items-center space-x-2 pb-3 border-b border-slate-200 dark:border-slate-800">
            <span class="text-lg">📅</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-wide">2027 Examination Schedule & Dates</h3>
          </div>

          <div v-if="!timelineEntries.length" class="text-xs text-slate-500 dark:text-slate-400 py-4">
            Tentative schedule for 2027 cycle pending official gazette release.
          </div>

          <div v-else class="space-y-2.5">
            <div
              v-for="item in timelineEntries"
              :key="item.label"
              class="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800/80 gap-1"
            >
              <span class="text-xs font-medium text-slate-600 dark:text-slate-300">{{ item.label }}</span>
              <span class="text-xs font-bold font-mono text-emerald-600 dark:text-emerald-400 break-words">{{ item.value }}</span>
            </div>
          </div>
        </div>

        <!-- Card 2: Official Statutory Rules Summary -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-4 min-w-0">
          <div class="flex items-center space-x-2 pb-3 border-b border-slate-200 dark:border-slate-800">
            <span class="text-lg">⚖️</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-wide">Official Statutory Requirements</h3>
          </div>

          <div class="space-y-2 text-xs text-slate-700 dark:text-slate-300">
            <div class="flex flex-col sm:flex-row sm:justify-between py-1.5 border-b border-slate-200 dark:border-slate-800 gap-1">
              <span class="text-slate-500 dark:text-slate-400 shrink-0">Reference Cutoff Rule:</span>
              <span class="font-medium text-slate-900 dark:text-white break-words sm:text-right">{{ examRule?.cutoff_rule || 'Exam Year Cycle' }}</span>
            </div>
            <div class="flex flex-col sm:flex-row sm:justify-between py-1.5 border-b border-slate-200 dark:border-slate-800 gap-1">
              <span class="text-slate-500 dark:text-slate-400 shrink-0">General Age Bracket:</span>
              <span class="font-bold text-slate-900 dark:text-white sm:text-right">{{ examRule?.min_age_gen || 21 }} – {{ examRule?.max_age_gen || 32 }} years</span>
            </div>
            <div class="flex flex-col sm:flex-row sm:justify-between py-1.5 border-b border-slate-200 dark:border-slate-800 gap-1">
              <span class="text-slate-500 dark:text-slate-400 shrink-0">Minimum Degree:</span>
              <span class="font-medium text-slate-900 dark:text-white break-words sm:text-right">{{ examRule?.min_education || 'Bachelor Degree' }}</span>
            </div>
            <div class="flex flex-col sm:flex-row sm:justify-between py-1.5 border-b border-slate-200 dark:border-slate-800 gap-1">
              <span class="text-slate-500 dark:text-slate-400 shrink-0">Accepted Disciplines:</span>
              <span class="font-medium text-emerald-600 dark:text-emerald-400 break-words sm:text-right">
                {{ examRule?.accepted_disciplines?.join(', ') || 'Any Discipline' }}
              </span>
            </div>
            <div class="flex flex-col sm:flex-row sm:justify-between py-1.5 border-b border-slate-200 dark:border-slate-800 gap-1">
              <span class="text-slate-500 dark:text-slate-400 shrink-0">Final Year Students Allowed:</span>
              <span class="font-semibold sm:text-right" :class="examRule?.allows_final_year ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
                {{ examRule?.allows_final_year ? 'Yes (Provisional proof required before Mains)' : 'No (Degree proof required on cutoff)' }}
              </span>
            </div>
            <div v-if="examRule?.physical_standards" class="py-2 border-b border-slate-200 dark:border-slate-800 space-y-2">
              <span class="text-slate-500 dark:text-slate-400 block font-semibold text-xs">Statutory Physical Standards:</span>
              <div class="text-[11px] text-slate-700 dark:text-slate-300 space-y-2">
                <!-- Cockpit Anthropometrics for Flying Branches (AFCAT / CDS AFA) -->
                <div v-if="examRule.physical_standards.flying_branch_standards" class="p-2.5 rounded-xl bg-sky-50 dark:bg-sky-950/30 border border-sky-200 dark:border-sky-800/40 space-y-1">
                  <div class="font-bold text-sky-800 dark:text-sky-300 flex items-center space-x-1">
                    <span>✈️ Flying Branch (Cockpit Anthropometrics)</span>
                  </div>
                  <div class="text-slate-600 dark:text-slate-300 space-y-0.5 pl-1">
                    <div>• Standing Height: <strong class="text-slate-800 dark:text-slate-100">Min {{ examRule.physical_standards.flying_branch_standards.min_height_cm }} cm</strong> (Male & Female, no concessions)</div>
                    <div>• Sitting Height: <strong class="text-slate-800 dark:text-slate-100">{{ examRule.physical_standards.flying_branch_standards.sitting_height_min_cm }} – {{ examRule.physical_standards.flying_branch_standards.sitting_height_max_cm }} cm</strong></div>
                    <div>• Leg Length: <strong class="text-slate-800 dark:text-slate-100">{{ examRule.physical_standards.flying_branch_standards.leg_length_min_cm }} – {{ examRule.physical_standards.flying_branch_standards.leg_length_max_cm }} cm</strong></div>
                    <div>• Thigh Length: <strong class="text-slate-800 dark:text-slate-100">Max {{ examRule.physical_standards.flying_branch_standards.thigh_length_max_cm }} cm</strong></div>
                  </div>
                </div>

                <!-- Ground Duty & Standard Standing Biometrics -->
                <div v-if="examRule.physical_standards.min_height_male_cm" class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 space-y-1">
                  <div class="font-bold text-slate-800 dark:text-slate-200">
                    {{ examRule.physical_standards.flying_branch_standards ? '🎖️ Ground Duty / General Cadres' : '📏 Statutory Biometrics' }}
                  </div>
                  <div class="text-slate-600 dark:text-slate-300 space-y-0.5 pl-1">
                    <div>Height: Min {{ examRule.physical_standards.min_height_male_cm }} cm (Male) / {{ examRule.physical_standards.min_height_female_cm || 152 }} cm (Female)</div>
                    <div v-if="examRule.physical_standards.min_chest_male_cm">
                      Chest: Min {{ examRule.physical_standards.min_chest_male_cm }} cm (Expansion 5 cm)
                    </div>
                    <div v-if="examRule.physical_standards.min_weight_male_kg">
                      Weight: Min {{ examRule.physical_standards.min_weight_male_kg }} kg (Male) / {{ examRule.physical_standards.min_weight_female_kg || 46 }} kg (Female)
                    </div>
                  </div>
                </div>

                <!-- State Police Cadres (DSP / RPS) -->
                <div v-if="examRule.physical_standards.DSP_Male || examRule.physical_standards.RPS_Male" class="p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 space-y-1">
                  <div class="font-bold text-amber-800 dark:text-amber-300">🚓 Police Service Cadres (DSP / RPS)</div>
                  <div class="text-slate-600 dark:text-slate-300 space-y-0.5 pl-1">
                    <div v-if="examRule.physical_standards.DSP_Male">
                      Male Height: Min {{ examRule.physical_standards.DSP_Male.min_height_cm }} cm
                      <span v-if="examRule.physical_standards.DSP_Male.min_chest_cm"> | Chest: {{ examRule.physical_standards.DSP_Male.min_chest_cm }} cm (+5cm)</span>
                    </div>
                    <div v-if="examRule.physical_standards.RPS_Male">
                      Male Height: Min {{ examRule.physical_standards.RPS_Male.min_height_cm }} cm | Chest: {{ examRule.physical_standards.RPS_Male.min_chest_cm }} cm (+5cm)
                    </div>
                    <div class="text-[10px] text-slate-500 dark:text-slate-400 mt-1 italic">
                      *Administrative cadres (SDM, Accounts, Revenue) enforce zero height/chest requirements.
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="py-1.5 text-slate-500 dark:text-slate-400 text-[11px] break-words">
              <strong class="text-slate-700 dark:text-slate-300">Gazette Citation:</strong>
              <div class="font-mono text-slate-600 dark:text-slate-400 mt-0.5 break-words">{{ examRule?.citation || exam.latest_gazette_ref || 'Official Notification' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- DIRECT COMPLETE SYLLABUS SECTION -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-sm dark:shadow-lg space-y-5">
        <!-- Syllabus Header with Stats -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div>
            <h3 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white tracking-wide flex items-center space-x-2">
              <span>📚 Examination Syllabus & Mapped Curriculum</span>
              <span class="px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-emerald-600 dark:text-emerald-400 font-mono text-xs font-bold">
                {{ filteredTopics.length }} Topics
              </span>
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Official topics audited from the commission's syllabus notification with cognitive depth classifications.
            </p>
          </div>

          <!-- Quick Search Inside Syllabus -->
          <div class="w-full sm:w-64">
            <input
              v-model="syllabusSearch"
              type="text"
              placeholder="Filter topics..."
              class="w-full px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        <!-- Domain Filter Pills -->
        <div class="flex flex-wrap items-center gap-1.5 pb-2">
          <button
            v-for="d in availableDomains"
            :key="d"
            @click="selectedSyllabusDomain = d"
            class="px-2.5 py-1 rounded-lg text-xs font-medium transition-all"
            :class="
              selectedSyllabusDomain === d
                ? 'bg-emerald-500 text-white font-bold shadow-sm'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-slate-700'
            "
          >
            {{ d }} ({{ getTopicCountForDomain(d) }})
          </button>
        </div>

        <!-- Topics Grid -->
        <div v-if="filteredTopics.length === 0" class="py-12 text-center text-slate-400 text-xs">
          No syllabus topics match the selected domain or filter.
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          <div
            v-for="item in filteredTopics"
            :key="item.topic_id"
            class="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 transition-all space-y-2 shadow-xs"
          >
            <!-- Domain & Depth Badges -->
            <div class="flex items-center justify-between text-[11px] gap-1">
              <span class="px-2 py-0.5 rounded bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 font-semibold truncate">
                {{ item.domain }}
              </span>
              <span
                class="px-2 py-0.5 rounded font-mono text-[10px] font-bold border"
                :class="getDepthBadgeClass(item.depth)"
              >
                {{ item.depth || 'Foundation' }}
              </span>
            </div>

            <!-- Topic Title -->
            <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white leading-snug break-words">
              {{ item.topic_title }}
            </h4>

            <!-- Subdomain & Stage -->
            <div class="text-[11px] text-slate-500 dark:text-slate-400 space-y-0.5 pt-1 border-t border-slate-200 dark:border-slate-800/80">
              <div v-if="item.sub_domain" class="truncate">
                <span class="text-slate-400">Sub-domain:</span> {{ item.sub_domain }}
              </div>
              <div v-if="item.stage_name" class="text-emerald-600 dark:text-emerald-400 font-mono text-[10px] truncate">
                {{ item.stage_name }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import { useHiddenStore } from '@/stores/useHiddenStore';
import { AUTHORITATIVE_EXAM_RULES } from '@/services/eligibilityEngine';
import type { EligibilityVerdict } from '@/types/profile';

const route = useRoute();

const examStore = useExamMasterStore();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const vizStore = useSyllabusVisualizationStore();
const hiddenStore = useHiddenStore();

const examId = computed(() => route.params.id as string);
const exam = computed(() => examStore.examsMap[examId.value]);
const examRule = computed(() => AUTHORITATIVE_EXAM_RULES[examId.value]);

// Local Syllabus Domain & Search Filters
const selectedSyllabusDomain = ref<string>('ALL');
const syllabusSearch = ref<string>('');

onMounted(async () => {
  hiddenStore.loadHiddenItems();
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

const allExamTopics = computed(() => {
  const mappings = vizStore.allMappings.filter((m) => m.exam_id === examId.value);
  return mappings.map((m) => {
    const topic = vizStore.topicsMap[m.topic_id];
    return {
      topic_id: m.topic_id,
      topic_title: topic?.topic_title || m.topic_id,
      domain: topic?.domain || 'General Studies',
      sub_domain: topic?.sub_domain || 'General',
      depth: m.depth_level,
      stage_name: m.stage_name || '',
    };
  });
});

const availableDomains = computed(() => {
  const set = new Set<string>();
  set.add('ALL');
  for (const t of allExamTopics.value) {
    if (t.domain) set.add(t.domain);
  }
  return Array.from(set);
});

function getTopicCountForDomain(domain: string): number {
  if (domain === 'ALL') return allExamTopics.value.length;
  return allExamTopics.value.filter((t) => t.domain === domain).length;
}

const filteredTopics = computed(() => {
  let list = allExamTopics.value;
  if (selectedSyllabusDomain.value !== 'ALL') {
    list = list.filter((t) => t.domain === selectedSyllabusDomain.value);
  }
  if (syllabusSearch.value.trim()) {
    const q = syllabusSearch.value.toLowerCase().trim();
    list = list.filter(
      (t) =>
        t.topic_title.toLowerCase().includes(q) ||
        t.sub_domain.toLowerCase().includes(q) ||
        t.stage_name.toLowerCase().includes(q)
    );
  }
  return list;
});

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
      return '✅';
    case 'NEEDS_INFO':
      return '⚠️';
    case 'INELIGIBLE':
      return '❌';
    default:
      return 'ℹ️';
  }
}

function formatCategory(category?: string): string {
  return category ? category.replace(/-/g, ' ') : '';
}

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30';
    case 'NEEDS_INFO':
      return 'bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30';
    case 'INELIGIBLE':
      return 'bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30';
    default:
      return 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700';
  }
}

function getVerdictContainerClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-50/70 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/30';
    case 'NEEDS_INFO':
      return 'bg-amber-50/70 dark:bg-amber-950/20 border-amber-300 dark:border-amber-500/30';
    case 'INELIGIBLE':
      return 'bg-rose-50/70 dark:bg-rose-950/20 border-rose-300 dark:border-rose-500/30';
    default:
      return 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800';
  }
}

function getDepthBadgeClass(depth?: string): string {
  switch (depth) {
    case 'Foundation':
      return 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700';
    case 'Intermediate':
      return 'bg-sky-50 dark:bg-sky-950/30 text-sky-700 dark:text-sky-400 border-sky-300 dark:border-sky-500/30';
    case 'Advanced':
      return 'bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-400 border-purple-300 dark:border-purple-500/30';
    case 'Analytical':
      return 'bg-pink-50 dark:bg-pink-950/30 text-pink-700 dark:text-pink-400 border-pink-300 dark:border-pink-500/30';
    default:
      return 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700';
  }
}
</script>
