<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Domicile & Regional Language Proficiencies</h3>
      <p class="text-sm text-slate-400">
        State Public Service Commissions (PSCs) enforce strict domicile reservation firewalls and mandatory local language tests.
      </p>
    </div>

    <!-- Domicile State Selector -->
    <div>
      <label for="domicile-select" class="block text-sm font-medium text-slate-300 mb-2">
        Bona Fide Home State / UT of Domicile <span class="text-rose-400">*</span>
      </label>
      <select
        id="domicile-select"
        v-model="profileStore.profile.state_domicile"
        class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
      >
        <option disabled value="">Select Home State / Union Territory</option>
        <optgroup label="States">
          <option v-for="state in indianStates" :key="state" :value="state">{{ state }}</option>
        </optgroup>
        <optgroup label="Union Territories">
          <option v-for="ut in unionTerritories" :key="ut" :value="ut">{{ ut }}</option>
        </optgroup>
      </select>
    </div>

    <!-- Statutory Domicile Firewall Notice -->
    <div class="bg-indigo-950/40 border border-indigo-800/60 rounded-xl p-4 text-xs text-indigo-200">
      <div class="flex items-center space-x-2 font-semibold text-indigo-300 mb-1">
        <svg class="w-4 h-4 text-indigo-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>Statutory State Reservation Firewall</span>
      </div>
      <p>
        In state civil services (UPPSC, BPSC, MPPSC, RPSC, TSPSC), reservation benefits and age concessions apply <strong>strictly to candidates holding bona fide domicile</strong> of that state. Candidates from other states are classified under <strong>General (UR)</strong> with 0 age relaxation.
      </p>
    </div>

    <!-- Fluent Languages Multi-select Chips -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-sm font-medium text-slate-300">
          Verified Language Fluencies (Reading, Writing & Speaking) <span class="text-rose-400">*</span>
        </label>
        <span class="text-xs text-slate-400">Selected: {{ profileStore.profile.fluent_languages.length }}</span>
      </div>
      <p class="text-xs text-slate-500 mb-3">
        Select all languages in which you possess matriculation level proficiency or higher.
      </p>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">
        <button
          type="button"
          v-for="lang in languageOptions"
          :key="lang.id"
          @click="toggleLanguage(lang.id)"
          class="p-2.5 rounded-xl border text-left transition flex items-center justify-between"
          :class="profileStore.profile.fluent_languages.includes(lang.id)
            ? 'bg-emerald-600/20 border-emerald-500 text-white shadow-sm'
            : 'bg-slate-800/60 border-slate-700/80 text-slate-400 hover:bg-slate-800 hover:text-slate-300'"
        >
          <div>
            <span class="block text-sm font-medium">{{ lang.name }}</span>
            <span v-if="lang.reqTag" class="block text-[10px] text-amber-400 font-semibold mt-0.5">
              {{ lang.reqTag }}
            </span>
          </div>
          <span 
            class="w-5 h-5 rounded-full flex items-center justify-center text-xs ml-2"
            :class="profileStore.profile.fluent_languages.includes(lang.id) ? 'bg-emerald-500 text-white' : 'border border-slate-600 text-transparent'"
          >
            ✓
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const indianStates = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa',
  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
  'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
  'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
];

const unionTerritories = [
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
];

const languageOptions = [
  { id: 'Hindi', name: 'Hindi', reqTag: 'Central & State PSCs' },
  { id: 'English', name: 'English', reqTag: 'Universal / Regulatory' },
  { id: 'Marathi', name: 'Marathi', reqTag: null },
  { id: 'Bengali', name: 'Bengali', reqTag: null },
  { id: 'Nepali', name: 'Nepali', reqTag: null },
  { id: 'Kannada', name: 'Kannada', reqTag: null },
  { id: 'Tamil', name: 'Tamil', reqTag: null },
  { id: 'Telugu', name: 'Telugu', reqTag: null },
  { id: 'Gujarati', name: 'Gujarati', reqTag: null },
  { id: 'Odia', name: 'Odia', reqTag: null },
  { id: 'Punjabi', name: 'Punjabi', reqTag: null },
  { id: 'Malayalam', name: 'Malayalam', reqTag: null },
  { id: 'Assamese', name: 'Assamese', reqTag: null },
  { id: 'Sanskrit', name: 'Sanskrit', reqTag: null },
  { id: 'Urdu', name: 'Urdu', reqTag: null }
];

function toggleLanguage(lang: string) {
  const list = profileStore.profile.fluent_languages;
  const idx = list.indexOf(lang);
  if (idx >= 0) {
    if (list.length > 1) {
      list.splice(idx, 1);
    }
  } else {
    list.push(lang);
  }
}
</script>
