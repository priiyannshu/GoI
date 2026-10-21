<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Academic Qualifications & Thresholds</h3>
      <p class="text-sm text-slate-400">
        Grade A posts enforce rigorous degree stream filters, Master's prerequisites, and non-rounding aggregate percentage floors.
      </p>
    </div>

    <!-- Degree Level Selection -->
    <div>
      <label class="block text-sm font-medium text-slate-300 mb-2">
        Highest Graduation Degree Level <span class="text-rose-400">*</span>
      </label>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <button
          type="button"
          v-for="deg in degreeOptions"
          :key="deg.id"
          @click="profileStore.profile.graduation_degree = deg.id as any"
          class="p-4 rounded-xl border text-left transition flex flex-col justify-between"
          :class="profileStore.profile.graduation_degree === deg.id 
            ? 'bg-emerald-600/20 border-emerald-500 text-white' 
            : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200'"
        >
          <div>
            <span class="block font-semibold text-sm">{{ deg.title }}</span>
            <span class="block text-xs text-slate-400 mt-1">{{ deg.desc }}</span>
          </div>
          <span class="text-[10px] mt-2 inline-block px-2 py-0.5 rounded bg-slate-800 text-emerald-300 border border-slate-700 self-start">
            {{ deg.badge }}
          </span>
        </button>
      </div>
    </div>

    <!-- Graduation Discipline Autocomplete / Categorized Select -->
    <div>
      <label for="discipline-select" class="block text-sm font-medium text-slate-300 mb-2">
        Graduation Discipline / Academic Major <span class="text-rose-400">*</span>
      </label>
      <select
        id="discipline-select"
        v-model="profileStore.profile.graduation_discipline"
        class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
      >
        <optgroup label="General / Any Discipline">
          <option value="ANY">Any Discipline (B.A., B.Sc., B.Com, General Graduate)</option>
        </optgroup>
        <optgroup label="Engineering & Technology">
          <option value="Civil">Civil Engineering</option>
          <option value="Mechanical">Mechanical Engineering</option>
          <option value="Electrical">Electrical Engineering</option>
          <option value="Electronics">Electronics & Telecommunication</option>
          <option value="Computer_Science">Computer Science & IT</option>
          <option value="Chemical">Chemical Engineering</option>
          <option value="Mining">Mining Engineering</option>
        </optgroup>
        <optgroup label="Economics, Finance & Commerce">
          <option value="Economics">Economics / Econometrics</option>
          <option value="Commerce">Commerce (B.Com / M.Com)</option>
          <option value="CA">Chartered Accountant (ICAI / CA)</option>
          <option value="CFA">Chartered Financial Analyst (CFA)</option>
          <option value="CS">Company Secretary (ICSI / CS)</option>
          <option value="MBA_Finance">MBA / Post Graduate Diploma in Finance</option>
        </optgroup>
        <optgroup label="Law, Science & Agriculture">
          <option value="Law">Law (LL.B / B.A. LL.B 5-Year)</option>
          <option value="Agriculture">Agriculture & Allied Sciences</option>
          <option value="Statistics">Statistics / Mathematical Statistics</option>
          <option value="Physics">Physics / Applied Physics</option>
          <option value="Chemistry">Chemistry</option>
          <option value="Geology">Geology / Applied Geophysics</option>
          <option value="MBBS">Medicine (M.B.B.S.)</option>
          <option value="Arts_History">Arts / Humanities / History</option>
        </optgroup>
      </select>
      <p class="text-xs text-slate-500 mt-1.5">
        Technical & Regulatory posts (UPSC ESE, SEBI Legal/Tech, GATE PSUs) require exact discipline matching.
      </p>
    </div>

    <!-- Aggregate Percentage & Strict Non-Rounding Alert -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <div>
        <label for="aggregate-input" class="block text-sm font-medium text-slate-300 mb-2">
          Aggregate Graduation Marks Percentage (%) <span class="text-rose-400">*</span>
        </label>
        <div class="relative">
          <input
            id="aggregate-input"
            type="number"
            step="0.01"
            min="35"
            max="100"
            v-model.number="profileStore.profile.graduation_aggregate_pct"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white pr-10 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            placeholder="e.g. 64.50"
            required
          />
          <span class="absolute right-4 top-2.5 text-slate-400 font-semibold">%</span>
        </div>
        <p class="text-xs text-slate-500 mt-1.5">
          Enter exact aggregate percentage across all semesters/years without rounding off.
        </p>
      </div>

      <!-- Statutory Non-Rounding Alert Pill -->
      <div class="bg-amber-950/40 border border-amber-800/60 rounded-xl p-4 text-xs text-amber-200">
        <div class="flex items-center space-x-2 font-semibold text-amber-300 mb-1">
          <svg class="w-4 h-4 text-amber-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
          <span>Strict Non-Rounding Rule</span>
        </div>
        <p>
          Statutory authorities (RBI Grade B, SEBI, PSU ETs) enforce strict cutoffs. An aggregate of <strong>59.99%</strong> strictly fails a <strong>60.00%</strong> requirement. No mathematical rounding is permitted.
        </p>
      </div>
    </div>

    <!-- Final Year Student Flag -->
    <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-sm font-medium text-slate-200">Final Year / Awaiting Final Semester Results</span>
          <p class="text-xs text-slate-400">Are you appearing in your final qualifying graduation examination in 2027?</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="profileStore.profile.is_final_year" class="sr-only peer">
          <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
        </label>
      </div>
      <div v-if="profileStore.profile.is_final_year" class="mt-3 text-xs text-purple-300 bg-purple-950/40 p-2.5 rounded-lg border border-purple-800/40">
        ℹ️ Final year candidates are marked as <strong>CONDITIONALLY ELIGIBLE</strong> for exams allowing final year candidates (e.g. UPSC CSE, ESE, State PSCs), subject to producing passing proof before the Mains cutoff.
      </div>
    </div>

    <!-- Optional 10+2 PCM Accordion for Defense Aviation (AFCAT) -->
    <details class="bg-slate-800/30 border border-slate-700/50 rounded-xl p-3.5 group">
      <summary class="text-xs font-semibold text-slate-300 cursor-pointer flex items-center justify-between">
        <span>Senior Secondary (10+2) Mathematics & Physics Scores (Optional / Defense Aviation)</span>
        <span class="text-emerald-400 group-open:rotate-180 transition">▼</span>
      </summary>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3 pt-3 border-t border-slate-700/50">
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">10+2 Mathematics Percentage</label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="100"
            v-model.number="profileStore.profile.ten_plus_two_maths_pct"
            placeholder="e.g. 62.0"
            class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-white focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">10+2 Physics Percentage</label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="100"
            v-model.number="profileStore.profile.ten_plus_two_physics_pct"
            placeholder="e.g. 58.5"
            class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-white focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <p class="col-span-full text-[11px] text-slate-500">
          * AFCAT Flying Branch requires minimum 50% in both Mathematics and Physics at 10+2 level.
        </p>
      </div>
    </details>
  </div>
</template>

<script setup lang="ts">
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const degreeOptions = [
  { 
    id: 'Bachelor', 
    title: 'Bachelor’s Degree', 
    desc: '3 or 4-year undergraduate degree (B.A., B.Sc., B.Tech, B.Com, LL.B)', 
    badge: 'Unlocks 90%+ Grade A posts' 
  },
  { 
    id: 'Master', 
    title: 'Master’s / Post Graduate', 
    desc: '2-year post-graduate degree (M.A., M.Sc., M.Tech, M.Com, LL.M)', 
    badge: 'Mandatory for IES/ISS, CGSE, specialized posts' 
  },
  { 
    id: 'Dual_UG_and_MBA', 
    title: 'Integrated Dual / MBA', 
    desc: '5-year integrated dual degree or undergraduate + MBA / PGDM', 
    badge: 'Satisfies both UG & Master thresholds' 
  },
];
</script>
