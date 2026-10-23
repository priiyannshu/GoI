<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Physical & Medical Standards</h3>
      <p class="text-sm text-slate-400">
        Uniformed executive services (IPS, CAPF AC, Defense, State DSP) enforce statutory biometric thresholds and visual acuity regulations.
      </p>
    </div>

    <!-- Height & Weight with Comparison Gauge -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <div class="space-y-4">
        <div>
          <label for="height-input" class="block text-sm font-medium text-slate-300 mb-2">
            Standing Height in Centimeters (cm) <span class="text-rose-400">*</span>
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

        <div>
          <label for="weight-input" class="block text-sm font-medium text-slate-300 mb-2">
            Body Weight (kg)
          </label>
          <div class="relative">
            <input
              id="weight-input"
              type="number"
              step="0.5"
              min="30"
              max="160"
              v-model.number="profileStore.profile.weight_kg"
              placeholder="e.g. 65.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white pr-12 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <span class="absolute right-4 top-2.5 text-slate-400 font-semibold text-sm">kg</span>
          </div>
          <p class="text-xs text-slate-500 mt-1.5">
            Statutory minimum: CAPF AC (50kg M / 46kg F); UP Police (40kg F); RPSC Police (47.5kg F).
          </p>
        </div>
      </div>

      <!-- Live Uniformed Service Cutoff Meter -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 text-xs space-y-2">
        <span class="font-semibold text-slate-300 block uppercase tracking-wider text-[11px]">
          Statutory Standing Height Benchmarks ({{ profileStore.profile.gender }})
        </span>
        <div class="space-y-1.5">
          <div class="flex justify-between items-center">
            <span class="text-slate-400">IAF Flying Branch (AFCAT / CDS AFA):</span>
            <span :class="heightMeetsFlying ? 'text-emerald-400 font-bold' : 'text-amber-400 font-semibold'">
              162.5 cm (Both M/F)
              ({{ heightMeetsFlying ? 'Eligible ✓' : 'Below Standard (Ground Duty Only) ✗' }})
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-slate-400">IAF Ground Duty / Defense Army & Navy:</span>
            <span :class="heightMeetsGroundDuty ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ profileStore.profile.gender === 'Female' ? '152 cm' : '157.5 cm' }}
              ({{ heightMeetsGroundDuty ? 'Eligible ✓' : 'Below Standard ✗' }})
            </span>
          </div>
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

    <!-- Specialized Aviation & Cockpit Anthropometrics Card (AFCAT & CDS Flying) -->
    <div class="bg-sky-950/20 border border-sky-800/40 rounded-2xl p-5 space-y-4">
      <div class="flex items-start justify-between gap-2">
        <div>
          <div class="flex items-center space-x-2">
            <span class="text-base font-bold text-sky-400">✈️ IAF Cockpit Anthropometrics</span>
            <span class="px-2 py-0.5 rounded-full bg-sky-900/60 text-sky-300 text-[10px] font-semibold border border-sky-700/50">AFCAT & CDS AFA Flying Branch</span>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            Mandatory ejection seat clearance and rudder pedal reach standards under <em>Air Force Medical Regulations (IAP 4303 5th Edition)</em>.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <!-- Sitting Height -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-medium text-slate-300">Sitting Height (cm)</label>
            <button
              type="button"
              @click="toggleMetricGuide('sitting')"
              class="p-1 -mr-1 rounded-md text-slate-400 hover:text-sky-400 hover:bg-slate-800 transition-colors flex items-center space-x-1"
              aria-label="Toggle Sitting Height Guide"
              title="Tap to toggle measuring rules"
            >
              <span class="text-[10px] font-medium text-sky-400">Guide</span>
              <svg
                class="w-3.5 h-3.5 transform transition-transform duration-200"
                :class="expandedMetrics.sitting ? 'rotate-180 text-sky-400' : ''"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
          <div class="relative">
            <input
              type="number"
              step="0.5"
              v-model.number="profileStore.profile.sitting_height_cm"
              placeholder="e.g. 88.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white pr-10 focus:ring-2 focus:ring-sky-500"
            />
            <span class="absolute right-3 top-2 text-slate-400 text-xs">cm</span>
          </div>
          <div class="flex items-center justify-between text-[11px] mt-1">
            <span class="text-slate-500">Range: 81.5 – 96.0 cm</span>
            <span v-if="profileStore.profile.sitting_height_cm" :class="sittingHeightValid ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ sittingHeightValid ? 'Safe ✓' : (profileStore.profile.sitting_height_cm < 81.5 ? 'Too Short ✗' : 'Too Tall ✗') }}
            </span>
          </div>

          <!-- Expandable rules under sitting height -->
          <div
            v-if="expandedMetrics.sitting"
            class="mt-2.5 p-3 rounded-xl bg-sky-950/40 border border-sky-800/60 text-xs text-slate-300 space-y-1.5"
          >
            <div class="font-bold text-[11px] text-sky-300 flex items-center space-x-1">
              <span>📐 How to measure Sitting Height (81.5 – 96.0 cm):</span>
            </div>
            <ul class="text-[11px] space-y-1 list-disc pl-4 text-slate-300">
              <li>Sit flat on a hard floor or chair with your buttocks and upper back pressed against a wall.</li>
              <li>Look straight ahead without slouching. Place a flat book on top of your head against the wall at 90°.</li>
              <li>Measure vertically from the sitting surface up to the book mark.</li>
              <li class="italic text-[10px] text-sky-400">Includes head, spine, and pelvic cushion (not just torso)—usually ~52–53% of standing height!</li>
            </ul>
          </div>
        </div>

        <!-- Leg Length -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-medium text-slate-300">Leg Length (cm)</label>
            <button
              type="button"
              @click="toggleMetricGuide('leg')"
              class="p-1 -mr-1 rounded-md text-slate-400 hover:text-sky-400 hover:bg-slate-800 transition-colors flex items-center space-x-1"
              aria-label="Toggle Leg Length Guide"
              title="Tap to toggle measuring rules"
            >
              <span class="text-[10px] font-medium text-sky-400">Guide</span>
              <svg
                class="w-3.5 h-3.5 transform transition-transform duration-200"
                :class="expandedMetrics.leg ? 'rotate-180 text-sky-400' : ''"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
          <div class="relative">
            <input
              type="number"
              step="0.5"
              v-model.number="profileStore.profile.leg_length_cm"
              placeholder="e.g. 108.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white pr-10 focus:ring-2 focus:ring-sky-500"
            />
            <span class="absolute right-3 top-2 text-slate-400 text-xs">cm</span>
          </div>
          <div class="flex items-center justify-between text-[11px] mt-1">
            <span class="text-slate-500">Range: 99.0 – 120.0 cm</span>
            <span v-if="profileStore.profile.leg_length_cm" :class="legLengthValid ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ legLengthValid ? 'Safe ✓' : (profileStore.profile.leg_length_cm < 99.0 ? 'Below Pedal Reach ✗' : 'Exceeds Cockpit ✗') }}
            </span>
          </div>

          <!-- Expandable rules under leg length -->
          <div
            v-if="expandedMetrics.leg"
            class="mt-2.5 p-3 rounded-xl bg-sky-950/40 border border-sky-800/60 text-xs text-slate-300 space-y-1.5"
          >
            <div class="font-bold text-[11px] text-sky-300 flex items-center space-x-1">
              <span>📐 How to measure Leg Length (99.0 – 120.0 cm):</span>
            </div>
            <ul class="text-[11px] space-y-1 list-disc pl-4 text-slate-300">
              <li>Sit on the floor with your back and buttocks pressed firmly against the wall.</li>
              <li>Stretch legs straight forward flat on the floor, knees locked, with toes flexed straight up at 90°.</li>
              <li>Measure horizontally along the floor from the wall behind your butt all the way to the bottom of your heel.</li>
              <li class="italic text-[10px] text-sky-400">NOT standing pant inseam! It measures rudder reach starting behind hips, so it's 10–15 cm longer than standing leg length.</li>
            </ul>
          </div>
        </div>

        <!-- Thigh Length -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-medium text-slate-300">Thigh Length (cm)</label>
            <button
              type="button"
              @click="toggleMetricGuide('thigh')"
              class="p-1 -mr-1 rounded-md text-slate-400 hover:text-sky-400 hover:bg-slate-800 transition-colors flex items-center space-x-1"
              aria-label="Toggle Thigh Length Guide"
              title="Tap to toggle measuring rules"
            >
              <span class="text-[10px] font-medium text-sky-400">Guide</span>
              <svg
                class="w-3.5 h-3.5 transform transition-transform duration-200"
                :class="expandedMetrics.thigh ? 'rotate-180 text-sky-400' : ''"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>
          <div class="relative">
            <input
              type="number"
              step="0.5"
              v-model.number="profileStore.profile.thigh_length_cm"
              placeholder="e.g. 58.0"
              class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white pr-10 focus:ring-2 focus:ring-sky-500"
            />
            <span class="absolute right-3 top-2 text-slate-400 text-xs">cm</span>
          </div>
          <div class="flex items-center justify-between text-[11px] mt-1">
            <span class="text-slate-500">Max limit: 64.0 cm</span>
            <span v-if="profileStore.profile.thigh_length_cm" :class="thighLengthValid ? 'text-emerald-400 font-bold' : 'text-rose-400 font-semibold'">
              {{ thighLengthValid ? 'Safe ✓' : 'Exceeds Ejection Limit ✗' }}
            </span>
          </div>

          <!-- Expandable rules under thigh length -->
          <div
            v-if="expandedMetrics.thigh"
            class="mt-2.5 p-3 rounded-xl bg-sky-950/40 border border-sky-800/60 text-xs text-slate-300 space-y-1.5"
          >
            <div class="font-bold text-[11px] text-sky-300 flex items-center space-x-1">
              <span>📐 How to measure Thigh Length (Max 64.0 cm):</span>
            </div>
            <ul class="text-[11px] space-y-1 list-disc pl-4 text-slate-300">
              <li>Sit on a chair or the floor with your back and buttocks touching the wall, knees bent at 90°.</li>
              <li>Measure horizontally along the top of your thigh from the wall behind your hips to the front curve of your kneecap.</li>
              <li>Must be 64.0 cm or less to safely clear ejection seat handles and the dashboard.</li>
              <li class="italic text-[10px] text-sky-400">If your total standing height is under 180 cm, you will easily fall below this 64 cm limit.</li>
            </ul>
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
import { ref, computed } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const expandedMetrics = ref<Record<string, boolean>>({
  sitting: false,
  leg: false,
  thigh: false,
});

function toggleMetricGuide(metric: string) {
  expandedMetrics.value[metric] = !expandedMetrics.value[metric];
}

const heightMeetsFlying = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.height_cm >= 162.5;
});

const heightMeetsGroundDuty = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.gender === 'Female' ? profileStore.profile.height_cm >= 152.0 : profileStore.profile.height_cm >= 157.5;
});

const heightMeetsIps = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.gender === 'Female' ? profileStore.profile.height_cm >= 150 : profileStore.profile.height_cm >= 165;
});

const heightMeetsCapf = computed(() => {
  if (!profileStore.profile.height_cm) return false;
  return profileStore.profile.gender === 'Female' ? profileStore.profile.height_cm >= 157 : profileStore.profile.height_cm >= 165;
});

const sittingHeightValid = computed(() => {
  const s = profileStore.profile.sitting_height_cm;
  if (s === undefined || s === null) return true;
  return s >= 81.5 && s <= 96.0;
});

const legLengthValid = computed(() => {
  const l = profileStore.profile.leg_length_cm;
  if (l === undefined || l === null) return true;
  return l >= 99.0 && l <= 120.0;
});

const thighLengthValid = computed(() => {
  const t = profileStore.profile.thigh_length_cm;
  if (t === undefined || t === null) return true;
  return t <= 64.0;
});
</script>
