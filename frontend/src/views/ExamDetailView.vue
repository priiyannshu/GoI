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
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        <!-- Card 1: 2027 Key Dates & Timeline -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-lg overflow-hidden">
          <button
            type="button"
            @click="isScheduleOpen = !isScheduleOpen"
            class="w-full p-6 flex items-center justify-between text-left transition-colors hover:bg-slate-50/60 dark:hover:bg-slate-850/40 select-none cursor-pointer"
          >
            <div class="flex items-center space-x-2">
              <span class="text-lg">📅</span>
              <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-wide">2027 Examination Schedule & Dates</h3>
            </div>
            <svg
              class="w-4 h-4 text-slate-500 transform transition-transform duration-200 shrink-0"
              :class="isScheduleOpen ? 'rotate-180' : ''"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <div v-show="isScheduleOpen" class="px-6 pb-6 pt-0 border-t border-slate-200 dark:border-slate-800 space-y-4">
            <div v-if="!timelineEntries.length" class="text-xs text-slate-500 dark:text-slate-400 pt-4">
              Tentative schedule for 2027 cycle pending official gazette release.
            </div>

            <div v-else class="space-y-2.5 pt-4">
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
        </div>

        <!-- Card 2: Official Statutory Rules Summary -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-lg overflow-hidden min-w-0">
          <button
            type="button"
            @click="isRequirementsOpen = !isRequirementsOpen"
            class="w-full p-6 flex items-center justify-between text-left transition-colors hover:bg-slate-50/60 dark:hover:bg-slate-850/40 select-none cursor-pointer"
          >
            <div class="flex items-center space-x-2">
              <span class="text-lg">⚖️</span>
              <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-wide">Official Statutory Requirements</h3>
            </div>
            <svg
              class="w-4 h-4 text-slate-500 transform transition-transform duration-200 shrink-0"
              :class="isRequirementsOpen ? 'rotate-180' : ''"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <div v-show="isRequirementsOpen" class="px-6 pb-6 pt-0 border-t border-slate-200 dark:border-slate-800">
            <div class="space-y-2 text-xs text-slate-700 dark:text-slate-300 pt-4">
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
      </div>

      <!-- PSU Notice Banner (if viewing a consolidated PSU recruitment) -->
      <div
        v-if="examStore.isPsuRecruitment(examId)"
        class="p-4 sm:p-5 rounded-2xl bg-sky-50 dark:bg-sky-950/30 border border-sky-300 dark:border-sky-500/40 text-xs text-sky-900 dark:text-sky-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs"
      >
        <div class="space-y-1">
          <div class="font-bold flex items-center space-x-1.5 text-sky-800 dark:text-sky-300 text-sm">
            <span>ℹ️</span>
            <span>PSU Grade A Recruitment through GATE 2027</span>
          </div>
          <p class="text-slate-600 dark:text-slate-300 leading-relaxed">
            This Maharatna / Navratna PSU cadre shortlists candidates using primary GATE examination scores followed by group discussion and technical interview.
          </p>
        </div>
        <div class="flex items-center space-x-2 shrink-0">
          <router-link
            to="/exams/GATE"
            class="px-3.5 py-2 rounded-xl font-bold bg-sky-500 text-white hover:bg-sky-600 transition-colors shadow-xs"
          >
            Inspect GATE Syllabus →
          </router-link>
          <router-link
            to="/posts"
            class="px-3 py-2 rounded-xl font-semibold bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-700 hover:bg-slate-100 transition-colors"
          >
            View Post & Perks →
          </router-link>
        </div>
      </div>

      <!-- Grade A PSU Recruitment Opportunities (Collapsible card for GATE) -->
      <div
        v-if="examId === 'GATE'"
        class="bg-white dark:bg-slate-900 rounded-2xl border border-sky-200 dark:border-sky-800/70 shadow-sm dark:shadow-lg overflow-hidden"
      >
        <button
          type="button"
          @click="isPsuOpportunitiesOpen = !isPsuOpportunitiesOpen"
          class="w-full p-6 flex items-center justify-between text-left transition-colors hover:bg-sky-50/50 dark:hover:bg-slate-850/50 select-none cursor-pointer"
        >
          <div class="flex items-center space-x-3">
            <span class="text-xl">🏢</span>
            <div>
              <div class="flex items-center space-x-2">
                <h3 class="text-base font-bold text-slate-900 dark:text-white tracking-wide">
                  Grade A PSU Recruitment Opportunities via GATE 2027
                </h3>
                <span class="hidden sm:inline-flex px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-500/15 text-sky-600 dark:text-sky-400 border border-sky-500/30">
                  11 Maharatna & Navratna PSUs
                </span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Executive Engineer & Management Trainee direct recruitment using GATE scores
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <svg
              class="w-4 h-4 text-slate-500 transform transition-transform duration-200 shrink-0"
              :class="isPsuOpportunitiesOpen ? 'rotate-180' : ''"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>

        <div v-show="isPsuOpportunitiesOpen" class="px-6 pb-6 pt-0 border-t border-slate-200 dark:border-slate-800 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-4">
            <p class="text-xs text-slate-600 dark:text-slate-300">
              Top Public Sector Undertakings (PSUs) utilize valid GATE scores to shortlist Executive Engineers and Scientific Officers with starting CTCs ranging from ₹15.5L to ₹21L.
            </p>
            <router-link
              to="/posts"
              class="px-3 py-1.5 rounded-xl text-xs font-bold bg-sky-500 text-white hover:bg-sky-600 transition-colors self-start sm:self-auto shrink-0 shadow-xs"
            >
              Explore All 11 PSU Posts →
            </router-link>
          </div>

          <!-- PSU Quick Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <div
              v-for="(psu, psuIdx) in psuOpportunities"
              :key="psuIdx"
              class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850/80 border border-slate-200 dark:border-slate-800 space-y-1.5 hover:border-sky-400 dark:hover:border-sky-600 transition-colors shadow-2xs"
            >
              <div class="flex items-center justify-between">
                <strong class="font-bold text-slate-900 dark:text-white">{{ psu.company }}</strong>
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/20">
                  {{ psu.cadre }}
                </span>
              </div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400">
                Starting Pay: <span class="font-semibold text-slate-800 dark:text-slate-200">{{ psu.pay }}</span>
              </div>
              <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono">
                Selection: {{ psu.weightage }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- REDESIGNED ASPIRANT-FIRST EXAMINATION SYLLABUS & PATTERN SECTION -->
      <ExamSyllabusSection
        v-if="curriculumScheme"
        :scheme="curriculumScheme"
      />
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
import { useSyllabusTrackerStore } from '@/stores/useSyllabusTrackerStore';
import ExamSyllabusSection from '@/components/syllabus/ExamSyllabusSection.vue';
import { AUTHORITATIVE_EXAM_RULES } from '@/services/eligibilityEngine';
import type { EligibilityVerdict } from '@/types/profile';

const route = useRoute();

const examStore = useExamMasterStore();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const vizStore = useSyllabusVisualizationStore();
const hiddenStore = useHiddenStore();
const trackerStore = useSyllabusTrackerStore();

const examId = computed(() => route.params.id as string);
const exam = computed(() => examStore.examsMap[examId.value]);
const examRule = computed(() => AUTHORITATIVE_EXAM_RULES[examId.value]);
const curriculumScheme = computed(() => trackerStore.getScheme(examId.value));

// Collapsible section states (start collapsed)
const isScheduleOpen = ref(false);
const isRequirementsOpen = ref(false);
const isPsuOpportunitiesOpen = ref(false);

// 11 Connected PSUs for GATE
const psuOpportunities = [
  { company: 'IOCL', cadre: 'Executive Trainee (E-2)', pay: '₹60,000 – ₹1,80,000 (CTC ~₹17L)', weightage: '85% GATE + 3% GD + 12% PI' },
  { company: 'ONGC', cadre: 'Graduate Trainee (E-1)', pay: '₹60,000 – ₹1,80,000 (CTC ~₹21L)', weightage: '60% GATE + 25% Qual + 15% PI' },
  { company: 'NTPC', cadre: 'Engg Exec Trainee (EET)', pay: '₹60,000 – ₹1,80,000 (CTC ~₹16.5L)', weightage: '85% GATE + 15% GD & PI' },
  { company: 'PowerGrid', cadre: 'Engineer Trainee', pay: '₹60,000 – ₹1,80,000 (CTC ~₹18L)', weightage: '85% GATE + 3% GD + 12% PI' },
  { company: 'BPCL', cadre: 'Management Trainee', pay: '₹60,000 – ₹1,80,000 (CTC ~₹18.5L)', weightage: 'GATE Score + Case Study + PI' },
  { company: 'HPCL', cadre: 'Officer Engineering', pay: '₹60,000 – ₹1,80,000 (CTC ~₹16.8L)', weightage: '85% GATE/CBT + 5% GT + 10% PI' },
  { company: 'SAIL', cadre: 'Management Trainee Tech', pay: '₹60,000 – ₹1,80,000 (CTC ~₹16L)', weightage: 'GATE Score + GD & Interview' },
  { company: 'GAIL', cadre: 'Executive Trainee', pay: '₹60,000 – ₹1,80,000 (CTC ~₹18L)', weightage: '85% GATE + 15% GD & PI' },
  { company: 'Coal India', cadre: 'Management Trainee', pay: '₹60,000 – ₹1,80,000 (CTC ~₹16L)', weightage: 'GATE Score / CBT + Interview' },
  { company: 'BHEL', cadre: 'Engineer Trainee', pay: '₹60,000 – ₹1,80,000 (CTC ~₹15.5L)', weightage: '75% GATE/CBT + 25% Interview' },
  { company: 'BARC / NPCIL', cadre: 'Scientific Officer / ET', pay: 'Level 10 (7th CPC) / E-1', weightage: 'GATE Score Screening + Tech Viva' }
];

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

  // Handle multi-cycle examinations (CDS, AFCAT)
  if (t.cds_1 || t.cds_2) {
    if (t.cds_1) {
      if (t.cds_1.notification_date || t.cds_1.notification_month) {
        entries.push({ label: 'CDS (I) Notification Date', value: t.cds_1.notification_date || t.cds_1.notification_month });
      }
      if (t.cds_1.application_window) {
        entries.push({ label: 'CDS (I) Application Window', value: t.cds_1.application_window });
      }
      if (t.cds_1.exam_date) {
        entries.push({ label: 'CDS (I) Examination Date', value: t.cds_1.exam_date });
      }
      if (t.cds_1.ssb_interview) {
        entries.push({ label: 'CDS (I) SSB Interview', value: t.cds_1.ssb_interview });
      }
      if (t.cds_1.course_commencement) {
        entries.push({ label: 'CDS (I) Course Commencement', value: t.cds_1.course_commencement });
      }
    }
    if (t.cds_2) {
      if (t.cds_2.notification_date || t.cds_2.notification_month) {
        entries.push({ label: 'CDS (II) Notification Date', value: t.cds_2.notification_date || t.cds_2.notification_month });
      }
      if (t.cds_2.application_window) {
        entries.push({ label: 'CDS (II) Application Window', value: t.cds_2.application_window });
      }
      if (t.cds_2.exam_date) {
        entries.push({ label: 'CDS (II) Examination Date', value: t.cds_2.exam_date });
      }
      if (t.cds_2.ssb_interview) {
        entries.push({ label: 'CDS (II) SSB Interview', value: t.cds_2.ssb_interview });
      }
      if (t.cds_2.course_commencement) {
        entries.push({ label: 'CDS (II) Course Commencement', value: t.cds_2.course_commencement });
      }
    }
    return entries;
  }

  if (t.afcat_1 || t.afcat_2) {
    if (t.afcat_1) {
      if (t.afcat_1.notification_month) entries.push({ label: 'AFCAT (1) Notification', value: t.afcat_1.notification_month });
      if (t.afcat_1.application_window) entries.push({ label: 'AFCAT (1) Application Window', value: t.afcat_1.application_window });
      if (t.afcat_1.exam_date) entries.push({ label: 'AFCAT (1) Exam Window', value: t.afcat_1.exam_date });
      if (t.afcat_1.afsb_interview) entries.push({ label: 'AFCAT (1) AFSB Interview', value: t.afcat_1.afsb_interview });
      if (t.afcat_1.course_commencement) entries.push({ label: 'AFCAT (1) Course Commencement', value: t.afcat_1.course_commencement });
    }
    if (t.afcat_2) {
      if (t.afcat_2.notification_month) entries.push({ label: 'AFCAT (2) Notification', value: t.afcat_2.notification_month });
      if (t.afcat_2.application_window) entries.push({ label: 'AFCAT (2) Application Window', value: t.afcat_2.application_window });
      if (t.afcat_2.exam_date) entries.push({ label: 'AFCAT (2) Exam Window', value: t.afcat_2.exam_date });
      if (t.afcat_2.afsb_interview) entries.push({ label: 'AFCAT (2) AFSB Interview', value: t.afcat_2.afsb_interview });
      if (t.afcat_2.course_commencement) entries.push({ label: 'AFCAT (2) Course Commencement', value: t.afcat_2.course_commencement });
    }
    return entries;
  }

  if (t.notification_date || t.notification_month) entries.push({ label: 'Notification Window', value: t.notification_date || t.notification_month });
  if (t.application_window) entries.push({ label: 'Application Window', value: t.application_window });
  if (t.prelims_stage_1 || t.prelims_date) entries.push({ label: 'Prelims / Phase 1 Exam', value: t.prelims_stage_1 || t.prelims_date });
  if (t.mains_stage_2 || t.mains_date) entries.push({ label: 'Mains / Phase 2 Exam', value: t.mains_stage_2 || t.mains_date });
  if (t.interview_window) entries.push({ label: 'Interview & Personality Test', value: t.interview_window });
  if (t.final_result) entries.push({ label: 'Final Result Declaration', value: t.final_result });

  return entries;
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
</script>
