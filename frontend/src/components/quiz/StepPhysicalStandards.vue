<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Physical & Medical Standards</h3>
      <p class="text-sm text-slate-400">
        Uniformed executive services (IPS, CAPF AC, Defense, State DSP) enforce statutory biometric thresholds and visual acuity regulations.
      </p>
    </div>

    <!-- Height (cm) with Comparison Gauge -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <div>
        <label for="height-input" class="block text-sm font-medium text-slate-300 mb-2">
          Height in Centimeters (cm) <span class="text-rose-400">*</span>
        </label>
        <div class="relative">
          <input
            id="height-input"
            type="number"
            step="0.5"
            min="120"
            max="230"
            v-model.number="profileStore.profile.height_cm"
            placeholder="e.g. 170.0"
            class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white pr-12 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <span class="absolute right-4 top-2.5 text-slate-400 font-semibold text-sm">cm</span>
        </div>
        <p class="text-xs text-slate-500 mt-1.5">
          Measured barefoot by official statutory medical board.
        </p>
      </div>

      <!-- Live Uniformed Service Cutoff Meter -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 text-xs space-y-2">
        <span class="font-semibold text-slate-300 block uppercase tracking-wider text-[11px]">
          Statutory Height Benchmarks ({{ profileStore.profile.gender }})
        </span>
        <div class="space-y-1.5">
          <div class="flex justify-between items-center">
            <span class="text-slate-400">IPS / Police Services:</span>
            <span :class="heightMeetsIps ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ profileStore.profile.gender === 'Female' ? '150 cm' : '165 cm' }}
              ({{ heightMeetsIps ? 'Eligible ✓' : 'Below Standard ✗' }})
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-slate-400">CAPF Assistant Commandant:</span>
            <span :class="heightMeetsCapf ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ profileStore.profile.gender === 'Female' ? '157 cm' : '165 cm' }}
              ({{ heightMeetsCapf ? 'Eligible ✓' : 'Below Standard ✗' }})
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-slate-400">Civil & Regulatory (IAS, IRS, RBI, SEBI):</span>
            <span class="text-emerald-400 font-bold">No Height Requirement ✓</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Chest Standards (Applicable for Male candidates) -->
    <div v-if="profileStore.profile.gender === 'Male'" class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
      <span class="text-sm font-semibold text-white block mb-1">Male Chest Expansion Standards</span>
      <p class="text-xs text-slate-400 mb-3">Statutory requirement for CAPF AC, IPS, and State DSP posts.</p>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Unexpanded Chest (cm)</label>
          <div class="relative">
            <input
              type="number"
              step="0.5"
              v-model.number="profileStore.profile.chest_cm"
              placeholder="e.g. 84.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white pr-10 focus:ring-2 focus:ring-emerald-500"
            />
            <span class="absolute right-3 top-2 text-slate-400 text-xs">cm</span>
          </div>
          <span class="text-[11px] text-slate-500 mt-1 block">Minimum: 81 cm</span>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Chest Expansion (cm)</label>
          <div class="relative">
            <input
              type="number"
              step="0.5"
              v-model.number="profileStore.profile.chest_expansion_cm"
              placeholder="e.g. 5.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white pr-10 focus:ring-2 focus:ring-emerald-500"
            />
            <span class="absolute right-3 top-2 text-slate-400 text-xs">cm</span>
          </div>
          <span class="text-[11px] text-slate-500 mt-1 block">Minimum expansion: 5 cm</span>
        </div>
      </div>
    </div>

    <!-- Visual Acuity & Eye Conditions -->
    <div class="space-y-4">
      <!-- Color Blindness Toggle -->
      <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-sm font-medium text-slate-200">Color Blindness / Color Vision Defect</span>
            <p class="text-xs text-slate-400">Ishihara 38-plate test failure or red-green color deficiency.</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="profileStore.profile.has_color_blindness" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-rose-600"></div>
          </label>
        </div>
        <p v-if="profileStore.profile.has_color_blindness" class="text-xs text-rose-300 mt-2 font-medium bg-rose-950/40 p-2.5 rounded-lg border border-rose-800/40">
          ⚠️ Color blindness is strictly disqualifying for IPS, CAPF AC, Indian Air Force, Indian Forest Service, and Railway Engineering technical cadres. It does NOT disqualify from IAS, IFS, IRS, or RBI/SEBI regulatory posts.
        </p>
      </div>

      <!-- LASIK / Refractive Surgery -->
      <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-sm font-medium text-slate-200">History of LASIK / PRK / Refractive Surgery</span>
            <p class="text-xs text-slate-400">Corrective laser eye procedure history.</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="profileStore.profile.has_lasik" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
          </label>
        </div>

        <div v-if="profileStore.profile.has_lasik" class="mt-4 pt-4 border-t border-slate-700/60 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Age When LASIK Was Performed</label>
            <input
              type="number"
              min="16"
              max="45"
              v-model.number="profileStore.profile.lasik_age"
              placeholder="e.g. 21"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-white focus:ring-2 focus:ring-emerald-500"
            />
            <span class="text-[11px] text-slate-500 mt-1 block">Armed forces require minimum age of 20 at surgery.</span>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Months Elapsed Since Surgery</label>
            <input
              type="number"
              min="0"
              max="120"
              v-model.number="profileStore.profile.lasik_wait_months"
              placeholder="e.g. 12"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-sm text-white focus:ring-2 focus:ring-emerald-500"
            />
            <span class="text-[11px] text-slate-500 mt-1 block">Statutory mandatory minimum: 6 months prior to medical test.</span>
          </div>
        </div>
      </div>

      <!-- DGCA Commercial Pilot License (AFCAT Flying Relaxation) -->
      <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-sm font-medium text-slate-200">DGCA Commercial Pilot License (CPL)</span>
            <p class="text-xs text-slate-400">Current valid CPL issued by DGCA India.</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="profileStore.profile.has_commercial_pilot_license" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
          </label>
        </div>
        <p v-if="profileStore.profile.has_commercial_pilot_license" class="text-xs text-emerald-300 mt-2 font-medium bg-emerald-950/40 p-2.5 rounded-lg border border-emerald-800/40">
          ✓ Grants +2 years age relaxation for IAF AFCAT Flying Branch (extends upper limit from 24 to 26 years).
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const heightMeetsIps = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.gender === 'Female' ? profileStore.profile.height_cm >= 150 : profileStore.profile.height_cm >= 165;
});

const heightMeetsCapf = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.gender === 'Female' ? profileStore.profile.height_cm >= 157 : profileStore.profile.height_cm >= 165;
});
</script>
