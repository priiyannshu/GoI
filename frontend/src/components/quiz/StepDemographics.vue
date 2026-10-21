<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Candidate Demographics & Statutory Category</h3>
      <p class="text-sm text-slate-400">
        Your exact age on the statutory reference cutoff dates determines your eligibility across all 31 Grade A examinations.
      </p>
    </div>

    <!-- Date of Birth & Live Age Gauges -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="dob-input" class="block text-sm font-medium text-slate-300 mb-2">
          Date of Birth <span class="text-rose-400">*</span>
        </label>
        <input
          id="dob-input"
          type="date"
          v-model="profileStore.profile.dob"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
          required
        />
        <p class="text-xs text-slate-500 mt-1.5">
          Standard candidate window for 2027 cycle: born between 1985 and 2006.
        </p>
      </div>

      <!-- Real-Time Calculated Age Panel -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 flex flex-col justify-between">
        <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Calculated Age on 2027 Cutoffs</span>
        <div class="grid grid-cols-3 gap-2 mt-2 text-center">
          <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
            <span class="block text-lg font-bold text-emerald-400">{{ calculatedAgeAug1 }}</span>
            <span class="text-[10px] text-slate-400">1 Aug 2027 (UPSC)</span>
          </div>
          <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
            <span class="block text-lg font-bold text-blue-400">{{ calculatedAgeJan1 }}</span>
            <span class="text-[10px] text-slate-400">1 Jan 2027 (ESE)</span>
          </div>
          <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
            <span class="block text-lg font-bold text-purple-400">{{ calculatedAgeJul1 }}</span>
            <span class="text-[10px] text-slate-400">1 Jul 2027 (RBI/State)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Gender Selector -->
    <div>
      <label class="block text-sm font-medium text-slate-300 mb-2">
        Gender <span class="text-rose-400">*</span>
      </label>
      <div class="grid grid-cols-3 gap-3">
        <button
          type="button"
          v-for="g in ['Male', 'Female', 'Other']"
          :key="g"
          @click="profileStore.profile.gender = (g as any)"
          class="py-3 px-4 rounded-xl text-sm font-medium border text-center transition"
          :class="profileStore.profile.gender === g 
            ? 'bg-emerald-600/20 border-emerald-500 text-white shadow-sm' 
            : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:text-slate-200 hover:bg-slate-800'"
        >
          {{ g }}
        </button>
      </div>
    </div>

    <!-- Category Selector & Statutory Relaxations -->
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-sm font-medium text-slate-300">
          Statutory Social Category <span class="text-rose-400">*</span>
        </label>
        <span class="text-xs text-emerald-400 font-medium">
          {{ categoryRelaxationSummary }}
        </span>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        <button
          type="button"
          v-for="cat in categories"
          :key="cat.id"
          @click="profileStore.profile.category = (cat.id as any)"
          class="p-3 rounded-xl border text-left transition flex flex-col justify-between"
          :class="profileStore.profile.category === cat.id 
            ? 'bg-emerald-600/20 border-emerald-500 text-white' 
            : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200'"
        >
          <span class="font-semibold text-sm">{{ cat.label }}</span>
          <span class="text-[11px] mt-1 text-slate-400">{{ cat.badge }}</span>
        </button>
      </div>
    </div>

    <!-- Ex-Servicemen & Defense Personnel -->
    <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-sm font-medium text-slate-200">Ex-Servicemen (ESM) Status</span>
          <p class="text-xs text-slate-400">Regular armed forces service of at least 6 months.</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="profileStore.profile.is_ex_serviceman" class="sr-only peer">
          <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
        </label>
      </div>

      <div v-if="profileStore.profile.is_ex_serviceman" class="mt-4 pt-4 border-t border-slate-700/60 flex items-center space-x-4">
        <label for="esm-years" class="text-xs text-slate-300">Completed Years of Military Service:</label>
        <input
          id="esm-years"
          type="number"
          min="1"
          max="35"
          v-model.number="profileStore.profile.ex_service_years"
          class="w-24 bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-white text-sm focus:ring-2 focus:ring-emerald-500"
        />
        <span class="text-xs text-emerald-400 font-medium">
          Deduction: Age − (Years + 3)
        </span>
      </div>
    </div>

    <!-- Marital Status & Children (CDS / State Concessions) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label class="block text-xs font-medium text-slate-400 mb-1.5">Marital Status</label>
        <select
          v-model="profileStore.profile.marital_status"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:ring-2 focus:ring-emerald-500"
        >
          <option value="Unmarried">Unmarried (Single)</option>
          <option value="Married">Married</option>
          <option value="Widow">Widow</option>
          <option value="Divorcee">Divorcee</option>
        </select>
      </div>

      <div v-if="profileStore.profile.marital_status === 'Widow' || profileStore.profile.marital_status === 'Divorcee'" class="flex items-center pt-6">
        <label class="flex items-center text-xs text-slate-300 cursor-pointer">
          <input type="checkbox" v-model="profileStore.profile.has_children" class="rounded bg-slate-800 border-slate-700 text-emerald-600 mr-2 focus:ring-emerald-500">
          Has dependent children (Issueless required for CDS OTA Women)
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const calculatedAgeAug1 = computed(() => profileStore.calculatedAge2027Aug1);
const calculatedAgeJan1 = computed(() => profileStore.calculatedAge2027Jan1);
const calculatedAgeJul1 = computed(() => profileStore.calculatedAge2027Jul1);

const categories = [
  { id: 'GEN', label: 'General (UR)', badge: 'No Age Relaxation' },
  { id: 'EWS', label: 'EWS', badge: 'Same as General' },
  { id: 'OBC', label: 'OBC (Non-Creamy)', badge: '+3 Years Relaxation' },
  { id: 'SC', label: 'SC', badge: '+5 Years Relaxation' },
  { id: 'ST', label: 'ST', badge: '+5 Years Relaxation' },
  { id: 'PWBD_GEN', label: 'PwBD (General)', badge: '+10 Years Relaxation' },
  { id: 'PWBD_OBC', label: 'PwBD (OBC)', badge: '+13 Years Relaxation' },
  { id: 'PWBD_SC_ST', label: 'PwBD (SC/ST)', badge: '+15 Years Relaxation' },
];

const categoryRelaxationSummary = computed(() => {
  switch (profileStore.profile.category) {
    case 'OBC': return 'Statutory concession: +3 years age relaxation, 9 attempts for CSE';
    case 'SC':
    case 'ST': return 'Statutory concession: +5 years age relaxation, unlimited attempts';
    case 'PWBD_GEN': return 'Statutory concession: +10 years age relaxation, 9 attempts';
    case 'PWBD_OBC': return 'Statutory concession: +13 years age relaxation, 9 attempts';
    case 'PWBD_SC_ST': return 'Statutory concession: +15 years age relaxation, unlimited attempts';
    case 'EWS': return 'Income & Asset Certificate required; age limits equal to General';
    default: return 'Standard statutory limits apply (Max age 32 for CSE, 30 for RBI)';
  }
});
</script>
