<template>
  <div class="space-y-6">
    <div class="border-b border-slate-800 pb-4">
      <h3 class="text-lg font-semibold text-white">Prior Examination Attempts & Statutory Caps</h3>
      <p class="text-sm text-slate-400">
        Statutory commissions count every official appearance at the Preliminary/Phase 1 stage against lifetime attempt caps.
      </p>
    </div>

    <!-- UPSC CSE Attempt Counter -->
    <div class="bg-slate-800/50 border border-slate-700/60 rounded-xl p-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold text-xs border border-emerald-500/30">UPSC CSE</span>
            <h4 class="font-semibold text-white text-base">Civil Services Examination</h4>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            Count any CSAT / GS Prelims appearance where you marked attendance.
          </p>
          <div class="mt-2 text-xs font-medium text-slate-300">
            Permissible Limit for Category <strong class="text-emerald-400">{{ profileStore.profile.category }}</strong>:
            <span class="text-emerald-400 font-bold">{{ cseMaxLimitText }}</span>
          </div>
        </div>

        <!-- Counter Buttons -->
        <div class="flex items-center space-x-3 self-end sm:self-center">
          <button
            type="button"
            @click="decrementAttempt('UPSC_CSE')"
            :disabled="cseAttempts <= 0"
            class="w-10 h-10 rounded-xl bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed text-white text-lg font-bold flex items-center justify-center transition"
          >
            −
          </button>
          <span class="w-12 text-center text-xl font-bold text-white">{{ cseAttempts }}</span>
          <button
            type="button"
            @click="incrementAttempt('UPSC_CSE')"
            class="w-10 h-10 rounded-xl bg-slate-700 hover:bg-slate-600 text-white text-lg font-bold flex items-center justify-center transition"
          >
            +
          </button>
        </div>
      </div>

      <!-- Attempt Progress Bar / Warning -->
      <div v-if="cseLimitNumber !== null" class="mt-4 pt-4 border-t border-slate-700/50">
        <div class="flex justify-between text-xs mb-1 font-medium">
          <span :class="cseAttempts >= cseLimitNumber ? 'text-rose-400' : 'text-slate-400'">
            {{ cseAttempts }} of {{ cseLimitNumber }} attempts used
          </span>
          <span :class="cseAttempts >= cseLimitNumber ? 'text-rose-400' : 'text-emerald-400'">
            {{ Math.max(0, cseLimitNumber - cseAttempts) }} remaining
          </span>
        </div>
        <div class="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
          <div 
            class="h-2 rounded-full transition-all duration-300"
            :class="cseAttempts >= cseLimitNumber ? 'bg-rose-500' : cseAttempts >= cseLimitNumber - 1 ? 'bg-amber-500' : 'bg-emerald-500'"
            :style="{ width: `${Math.min(100, (cseAttempts / cseLimitNumber) * 100)}%` }"
          ></div>
        </div>
        <p v-if="cseAttempts >= cseLimitNumber" class="text-xs text-rose-400 mt-2 font-semibold">
          ⚠️ Disqualified: You have exhausted all permissible attempts for UPSC Civil Services.
        </p>
      </div>
    </div>

    <!-- RBI Grade B Attempt Counter -->
    <div class="bg-slate-800/50 border border-slate-700/60 rounded-xl p-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-bold text-xs border border-blue-500/30">RBI Gr B</span>
            <h4 class="font-semibold text-white text-base">RBI Grade B (Phase 1 Prelims)</h4>
          </div>
          <p class="text-xs text-slate-400 mt-1">
            General & EWS candidates are restricted to 6 lifetime Phase 1 appearances.
          </p>
          <div class="mt-2 text-xs font-medium text-slate-300">
            Limit for Category <strong class="text-blue-400">{{ profileStore.profile.category }}</strong>:
            <span class="text-emerald-400 font-bold">{{ rbiMaxLimitText }}</span>
          </div>
        </div>

        <!-- Counter Buttons -->
        <div class="flex items-center space-x-3 self-end sm:self-center">
          <button
            type="button"
            @click="decrementAttempt('RBI_GRADE_B')"
            :disabled="rbiAttempts <= 0"
            class="w-10 h-10 rounded-xl bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed text-white text-lg font-bold flex items-center justify-center transition"
          >
            −
          </button>
          <span class="w-12 text-center text-xl font-bold text-white">{{ rbiAttempts }}</span>
          <button
            type="button"
            @click="incrementAttempt('RBI_GRADE_B')"
            class="w-10 h-10 rounded-xl bg-slate-700 hover:bg-slate-600 text-white text-lg font-bold flex items-center justify-center transition"
          >
            +
          </button>
        </div>
      </div>

      <div v-if="rbiLimitNumber !== null" class="mt-4 pt-4 border-t border-slate-700/50">
        <p v-if="rbiAttempts >= rbiLimitNumber" class="text-xs text-rose-400 font-semibold">
          ⚠️ Disqualified: General/EWS Phase 1 attempt cap reached (6 appearances).
        </p>
      </div>
    </div>

    <!-- Prior Selection as Assistant Commandant (CAPF Disqualification Check) -->
    <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-sm font-medium text-slate-200">Prior CAPF Assistant Commandant Selection</span>
          <p class="text-xs text-slate-400">
            Have you previously been selected and appointed as an Assistant Commandant in BSF, CRPF, CISF, ITBP, or SSB?
          </p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="profileStore.profile.prior_selected_as_ac" class="sr-only peer">
          <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-rose-600"></div>
        </label>
      </div>
      <p v-if="profileStore.profile.prior_selected_as_ac" class="text-xs text-rose-300 mt-2 font-medium bg-rose-950/40 p-2.5 rounded-lg border border-rose-800/40">
        ⚠️ Under statutory MHA notification rules, candidates who were previously appointed as Assistant Commandant in any CAPF are legally barred from appearing in subsequent CAPF (AC) examinations.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const cseAttempts = computed(() => profileStore.profile.prior_attempts['UPSC_CSE'] || 0);
const rbiAttempts = computed(() => profileStore.profile.prior_attempts['RBI_GRADE_B'] || 0);

const cseLimitNumber = computed<number | null>(() => {
  switch (profileStore.profile.category) {
    case 'GEN':
    case 'EWS': return 6;
    case 'OBC': return 9;
    case 'PWBD_GEN':
    case 'PWBD_OBC': return 9;
    case 'SC':
    case 'ST':
    case 'PWBD_SC_ST': return null; // Unlimited
    default: return 6;
  }
});

const cseMaxLimitText = computed(() => {
  return cseLimitNumber.value === null ? 'Unlimited Attempts' : `${cseLimitNumber.value} Attempts Max`;
});

const rbiLimitNumber = computed<number | null>(() => {
  if (profileStore.profile.category === 'GEN' || profileStore.profile.category === 'EWS') return 6;
  return null; // Unlimited for reserved
});

const rbiMaxLimitText = computed(() => {
  return rbiLimitNumber.value === null ? 'Unlimited (Exempt from Cap)' : '6 Phase-1 Appearances Max';
});

function incrementAttempt(examId: string) {
  const current = profileStore.profile.prior_attempts[examId] || 0;
  profileStore.setPriorAttempt(examId, current + 1);
}

function decrementAttempt(examId: string) {
  const current = profileStore.profile.prior_attempts[examId] || 0;
  profileStore.setPriorAttempt(examId, Math.max(0, current - 1));
}
</script>
