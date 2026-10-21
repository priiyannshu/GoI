<template>
  <div class="space-y-6 pb-16">
    <!-- Profile View Header & Tabs -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Candidate Profile & Eligibility</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">
          Save your academic, statutory, and physical attributes. Sections are skippable to audit exams with whatever details you provide.
        </p>
      </div>

      <!-- Tab Switcher -->
      <div class="flex rounded-xl bg-slate-800 p-1 border border-slate-700/80 self-start sm:self-auto">
        <button
          @click="activeTab = 'profile'"
          class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all"
          :class="activeTab === 'profile' ? 'bg-emerald-500 text-white shadow' : 'text-slate-400 hover:text-white'"
        >
          👤 My Profile
        </button>
        <button
          @click="activeTab = 'summary'"
          class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5"
          :class="activeTab === 'summary' ? 'bg-emerald-500 text-white shadow' : 'text-slate-400 hover:text-white'"
        >
          <span>🎯 Eligibility Summary</span>
          <span
            v-if="eligibilityStore.needsInfoCount > 0"
            class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40"
          >
            {{ eligibilityStore.needsInfoCount }}
          </span>
        </button>
      </div>
    </div>

    <!-- TAB 1: MY PROFILE (SKIPPABLE SECTIONS) -->
    <div v-if="activeTab === 'profile'" class="space-y-6">
      <!-- Profile Completion Gauge & Auto-Save Banner -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-lg">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span class="text-xs font-bold text-white uppercase tracking-wider">Profile Completeness</span>
            <span class="text-xs font-mono font-bold text-emerald-400">{{ profileStore.completionPercentage }}%</span>
          </div>
          <div class="w-48 sm:w-64 h-2 rounded-full bg-slate-800 overflow-hidden">
            <div
              class="h-full bg-emerald-500 transition-all duration-500"
              :style="{ width: `${profileStore.completionPercentage}%` }"
            ></div>
          </div>
        </div>

        <div class="flex items-center space-x-3 text-xs text-slate-400">
          <span class="flex items-center space-x-1 text-slate-400">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>All changes saved automatically</span>
          </span>
          <button
            @click="profileStore.resetToDefaults()"
            class="text-xs text-slate-500 hover:text-rose-400 underline transition-colors"
          >
            Reset All
          </button>
        </div>
      </div>

      <!-- SECTION 1: DEMOGRAPHICS -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🆔</span>
            <h3 class="text-base font-bold text-white">Demographics & Statutory Category</h3>
          </div>
          <span class="text-xs text-emerald-400 font-medium">Core Category & Age</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- DOB -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">
              Date of Birth <span class="text-rose-400">*</span>
            </label>
            <input
              type="date"
              v-model="profile.dob"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
            />
            <p class="text-[11px] text-slate-500 mt-1">Calculates age against 2027 statutory reference cutoff dates.</p>
          </div>

          <!-- Calculated Age Badges -->
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-3 flex items-center justify-around text-center">
            <div>
              <span class="text-xs text-slate-400 block">Aug 1, 2027 (UPSC)</span>
              <span class="text-lg font-bold font-mono text-emerald-400">{{ profileStore.calculatedAge2027Aug1 }} yrs</span>
            </div>
            <div class="w-px h-8 bg-slate-750"></div>
            <div>
              <span class="text-xs text-slate-400 block">Jan 1, 2027 (ESE)</span>
              <span class="text-lg font-bold font-mono text-sky-400">{{ profileStore.calculatedAge2027Jan1 }} yrs</span>
            </div>
            <div class="w-px h-8 bg-slate-750"></div>
            <div>
              <span class="text-xs text-slate-400 block">Jul 1, 2027 (State)</span>
              <span class="text-lg font-bold font-mono text-purple-400">{{ profileStore.calculatedAge2027Jul1 }} yrs</span>
            </div>
          </div>
        </div>

        <!-- Gender & Category -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          <!-- Gender -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Gender</label>
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="g in ['Male', 'Female', 'Other']"
                :key="g"
                type="button"
                @click="profile.gender = g as any"
                class="py-2 px-3 rounded-xl text-xs font-semibold border transition-all"
                :class="profile.gender === g ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-750'"
              >
                {{ g }}
              </button>
            </div>
          </div>

          <!-- Social Category -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Reservation Category</label>
            <select
              v-model="profile.category"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="GEN">General (UR)</option>
              <option value="EWS">Economically Weaker Section (EWS)</option>
              <option value="OBC">Other Backward Classes (OBC-NCL)</option>
              <option value="SC">Scheduled Caste (SC)</option>
              <option value="ST">Scheduled Tribe (ST)</option>
              <option value="PWBD_GEN">PwBD - General (10 yrs relaxation)</option>
              <option value="PWBD_OBC">PwBD - OBC (13 yrs relaxation)</option>
              <option value="PWBD_SC_ST">PwBD - SC/ST (15 yrs relaxation)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- SECTION 2: ACADEMICS (SKIPPABLE) -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🎓</span>
            <h3 class="text-base font-bold text-white">Academic Qualifications</h3>
          </div>
          <div class="flex items-center space-x-2">
            <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-slate-400 hover:text-white">
              <input
                type="checkbox"
                :checked="profileStore.isFieldSkipped('academics')"
                @change="profileStore.toggleFieldSkipped('academics')"
                class="rounded border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span>Skip Academics for now</span>
            </label>
          </div>
        </div>

        <div v-if="!profileStore.isFieldSkipped('academics')" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Degree Level -->
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Degree Level</label>
              <select
                v-model="profile.graduation_degree"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="Bachelor">Bachelor Degree (B.A., B.Sc., B.Tech, etc.)</option>
                <option value="Master">Master Degree (M.A., M.Sc., M.Tech, etc.)</option>
                <option value="Dual_UG_and_MBA">Dual UG and MBA / Professional</option>
              </select>
            </div>

            <!-- Discipline -->
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Discipline / Branch</label>
              <select
                v-model="profile.graduation_discipline"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="ANY">Any / General Graduate</option>
                <option value="Civil">Civil Engineering</option>
                <option value="Mechanical">Mechanical Engineering</option>
                <option value="Electrical">Electrical Engineering</option>
                <option value="Electronics">Electronics & Telecom</option>
                <option value="Computer_Science">Computer Science & IT</option>
                <option value="Chemical">Chemical Engineering</option>
                <option value="Economics">Economics / Finance</option>
                <option value="Commerce">Commerce / B.Com / M.Com</option>
                <option value="CA">Chartered Accountant (CA / ICAI)</option>
                <option value="CFA">Chartered Financial Analyst (CFA)</option>
                <option value="Law">Law (LL.B / B.A. LL.B)</option>
                <option value="Statistics">Statistics / Mathematical Statistics</option>
                <option value="Geology">Geology / Geophysics</option>
                <option value="Physics">Physics / Applied Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Agriculture">Agriculture & Allied</option>
              </select>
            </div>

            <!-- Aggregate Percentage -->
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5">Graduation Aggregate %</label>
              <input
                type="number"
                step="0.01"
                min="35"
                max="100"
                v-model.number="profile.graduation_aggregate_pct"
                placeholder="e.g. 65.50"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
              />
              <span class="text-[10px] text-slate-500">Strict non-rounding (e.g. 59.99% &lt; 60%)</span>
            </div>
          </div>

          <!-- Final Year Toggle & 10+2 Marks -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t border-slate-800 items-center">
            <label class="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                v-model="profile.is_final_year"
                class="rounded border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span>Currently in Final Year of Graduation</span>
            </label>

            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1">10+2 Maths % (AFCAT/Defense)</label>
              <input
                type="number"
                step="0.1"
                v-model.number="profile.ten_plus_two_maths_pct"
                placeholder="Optional (min 50% for Flying)"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1">10+2 Physics % (AFCAT/Defense)</label>
              <input
                type="number"
                step="0.1"
                v-model.number="profile.ten_plus_two_physics_pct"
                placeholder="Optional (min 50% for Flying)"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>
        </div>

        <div v-else class="text-xs text-amber-300/80 bg-amber-500/10 p-3 rounded-xl border border-amber-500/20">
          ⚠️ Academics marked as skipped. Examinations with strict degree or percentage requirements will indicate <strong>Needs Info</strong>.
        </div>
      </div>

      <!-- SECTION 3: DOMICILE & LANGUAGES (SKIPPABLE) -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🗺️</span>
            <h3 class="text-base font-bold text-white">Domicile & Regional Languages</h3>
          </div>
          <span class="text-xs text-slate-400">Controls State PSC reservation benefits</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Home State Domicile</label>
            <select
              v-model="profile.state_domicile"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="Delhi">Delhi (NCT)</option>
              <option value="Uttar Pradesh">Uttar Pradesh</option>
              <option value="Bihar">Bihar</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Madhya Pradesh">Madhya Pradesh</option>
              <option value="Rajasthan">Rajasthan</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Telangana">Telangana</option>
              <option value="West Bengal">West Bengal</option>
              <option value="Other">Other State / UT</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Fluent Regional Languages</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="lang in ['Hindi', 'English', 'Marathi', 'Bengali', 'Kannada', 'Tamil', 'Telugu', 'Nepali']"
                :key="lang"
                type="button"
                @click="toggleLanguage(lang)"
                class="px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors"
                :class="profile.fluent_languages?.includes(lang) ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200'"
              >
                {{ lang }} {{ profile.fluent_languages?.includes(lang) ? '✓' : '' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 4: PHYSICAL STANDARDS (SKIPPABLE) -->
      <div class="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🏃</span>
            <h3 class="text-base font-bold text-white">Physical & Medical Standards</h3>
          </div>
          <label class="flex items-center space-x-1.5 cursor-pointer text-xs text-slate-400 hover:text-white">
            <input
              type="checkbox"
              :checked="profileStore.isFieldSkipped('physical_standards')"
              @change="profileStore.toggleFieldSkipped('physical_standards')"
              class="rounded border-slate-700 text-emerald-500 focus:ring-0"
            />
            <span>Not targeting uniformed posts (Skip)</span>
          </label>
        </div>

        <div v-if="!profileStore.isFieldSkipped('physical_standards')" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Height (cm)</label>
            <input
              type="number"
              v-model.number="profile.height_cm"
              placeholder="e.g. 170"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            />
            <span class="text-[10px] text-slate-500">CAPF AC / Defense / Police entry</span>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-300 mb-1.5">Chest (cm, Unexpanded)</label>
            <input
              type="number"
              v-model.number="profile.chest_cm"
              placeholder="e.g. 84"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            />
            <span class="text-[10px] text-slate-500">Male uniformed standard: min 81–84 cm</span>
          </div>

          <div class="flex items-center space-x-3 pt-4">
            <label class="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                v-model="profile.has_color_blindness"
                class="rounded border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span>Color Blindness</span>
            </label>
          </div>
        </div>

        <div v-else class="text-xs text-amber-300/80 bg-amber-500/10 p-3 rounded-xl border border-amber-500/20">
          ⚠️ Physical standards skipped. Uniformed posts (CAPF AC, CDS, State Police DSP) will show <strong>Needs Info</strong> regarding height and chest.
        </div>
      </div>
    </div>

    <!-- TAB 2: ELIGIBILITY SUMMARY REPORT -->
    <div v-else-if="activeTab === 'summary'" class="space-y-6">
      <!-- 4-Tier Metrics Row -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div
          @click="statusFilter = 'ELIGIBLE'"
          class="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 cursor-pointer hover:border-emerald-500 transition-all text-center space-y-1"
          :class="statusFilter === 'ELIGIBLE' ? 'ring-2 ring-emerald-500' : ''"
        >
          <span class="text-xs uppercase font-bold text-emerald-400">Eligible</span>
          <span class="block text-2xl font-extrabold text-white font-mono">{{ eligibilityStore.eligibleCount }}</span>
        </div>

        <div
          @click="statusFilter = 'CONDITIONALLY_ELIGIBLE'"
          class="p-4 rounded-2xl bg-blue-950/20 border border-blue-500/30 cursor-pointer hover:border-blue-500 transition-all text-center space-y-1"
          :class="statusFilter === 'CONDITIONALLY_ELIGIBLE' ? 'ring-2 ring-blue-500' : ''"
        >
          <span class="text-xs uppercase font-bold text-blue-400">Conditional</span>
          <span class="block text-2xl font-extrabold text-white font-mono">{{ eligibilityStore.conditionallyEligibleCount }}</span>
        </div>

        <div
          @click="statusFilter = 'NEEDS_INFO'"
          class="p-4 rounded-2xl bg-amber-950/20 border border-amber-500/30 cursor-pointer hover:border-amber-500 transition-all text-center space-y-1"
          :class="statusFilter === 'NEEDS_INFO' ? 'ring-2 ring-amber-500' : ''"
        >
          <span class="text-xs uppercase font-bold text-amber-400">Needs Info</span>
          <span class="block text-2xl font-extrabold text-white font-mono">{{ eligibilityStore.needsInfoCount }}</span>
        </div>

        <div
          @click="statusFilter = 'INELIGIBLE'"
          class="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/30 cursor-pointer hover:border-rose-500 transition-all text-center space-y-1"
          :class="statusFilter === 'INELIGIBLE' ? 'ring-2 ring-rose-500' : ''"
        >
          <span class="text-xs uppercase font-bold text-rose-400">Ineligible</span>
          <span class="block text-2xl font-extrabold text-white font-mono">{{ eligibilityStore.ineligibleCount }}</span>
        </div>
      </div>

      <!-- Filter / Search Row -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center space-x-2 text-xs">
          <span class="text-slate-400">Showing:</span>
          <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-white font-semibold">
            {{ statusFilter === 'ALL' ? 'All 36 Audited Exams' : statusFilter }}
          </span>
          <button
            v-if="statusFilter !== 'ALL'"
            @click="statusFilter = 'ALL'"
            class="text-xs text-slate-500 hover:text-white underline ml-2"
          >
            Show All
          </button>
        </div>

        <div class="text-xs text-slate-400">
          Click any card to inspect full statutory rules, syllabus & 2027 dates
        </div>
      </div>

      <!-- Verdict Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="verdict in summaryVerdicts"
          :key="verdict.exam_id"
          @click="router.push(`/exams/${verdict.exam_id}`)"
          class="p-4 rounded-xl bg-slate-850 border hover:border-slate-700 transition-all cursor-pointer flex flex-col justify-between space-y-3 group shadow"
          :class="getCardBorder(verdict.status)"
        >
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-white">{{ getExamCode(verdict.exam_id) }}</span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
                :class="getStatusBadgeClass(verdict.status)"
              >
                {{ formatStatus(verdict.status) }}
              </span>
            </div>

            <h4 class="text-sm font-bold text-white group-hover:text-emerald-400 transition-colors leading-snug">
              {{ getExamTitle(verdict.exam_id) }}
            </h4>

            <!-- Skipped criteria callout if Needs Info -->
            <div
              v-if="verdict.status === 'NEEDS_INFO' && verdict.skipped_requirements?.length"
              class="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-[11px] text-amber-300 space-y-0.5"
            >
              <div class="font-semibold">Missing from profile:</div>
              <div class="truncate text-amber-200">{{ verdict.skipped_requirements[0] }}</div>
            </div>

            <!-- Reasons Snippet -->
            <div class="text-[11px] text-slate-400 line-clamp-2">
              {{ verdict.reasons[0] }}
            </div>
          </div>

          <div class="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px]">
            <span class="text-slate-500">{{ getExamAdmin(verdict.exam_id) }}</span>
            <span class="text-emerald-400 font-semibold group-hover:translate-x-0.5 transition-transform">
              Audit Details →
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import type { EligibilityVerdict } from '@/types/profile';

const router = useRouter();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const examStore = useExamMasterStore();

const activeTab = ref<'profile' | 'summary'>('profile');
const statusFilter = ref<string>('ALL');

const profile = profileStore.profile;

onMounted(async () => {
  await examStore.loadExams();
  await profileStore.loadInitialProfile();
  await eligibilityStore.evaluateAllExams(profileStore.profile);
});

// Re-evaluate eligibility when profile changes
watch(
  () => profileStore.profile,
  async () => {
    await eligibilityStore.evaluateAllExams(profileStore.profile);
  },
  { deep: true }
);

function toggleLanguage(lang: string) {
  if (!profile.fluent_languages) {
    profile.fluent_languages = [];
  }
  const idx = profile.fluent_languages.indexOf(lang);
  if (idx >= 0) {
    profile.fluent_languages.splice(idx, 1);
  } else {
    profile.fluent_languages.push(lang);
  }
}

function getExamCode(examId: string): string {
  return examStore.examsMap[examId]?.short_code || examId;
}

function getExamTitle(examId: string): string {
  return examStore.examsMap[examId]?.title || examId;
}

function getExamAdmin(examId: string): string {
  return examStore.examsMap[examId]?.administering_body || 'Official Commission';
}

const summaryVerdicts = computed<EligibilityVerdict[]>(() => {
  let list = eligibilityStore.verdictList;
  if (statusFilter.value !== 'ALL') {
    list = list.filter((v) => v.status === statusFilter.value);
  }
  return list;
});

function formatStatus(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'Eligible';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'Conditional';
    case 'NEEDS_INFO':
      return 'Needs Info';
    case 'INELIGIBLE':
      return 'Ineligible';
    default:
      return status;
  }
}

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'bg-blue-500/15 text-blue-300 border-blue-500/40';
    case 'NEEDS_INFO':
      return 'bg-amber-500/15 text-amber-300 border-amber-500/40';
    case 'INELIGIBLE':
      return 'bg-rose-500/15 text-rose-300 border-rose-500/40';
    default:
      return 'bg-slate-800 text-slate-300 border-slate-700';
  }
}

function getCardBorder(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'border-emerald-500/30 hover:border-emerald-500/60';
    case 'CONDITIONALLY_ELIGIBLE':
      return 'border-blue-500/30 hover:border-blue-500/60';
    case 'NEEDS_INFO':
      return 'border-amber-500/30 hover:border-amber-500/60';
    case 'INELIGIBLE':
      return 'border-slate-800 hover:border-slate-700';
    default:
      return 'border-slate-800';
  }
}
</script>