<template>
  <div class="w-full max-w-4xl mx-auto px-4 py-8">
    <!-- Stepper Navigation Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-3">
        <div>
          <span class="text-xs font-semibold tracking-wider uppercase text-emerald-400">Step {{ currentStep }} of {{ totalSteps }}</span>
          <h2 class="text-2xl font-bold text-white">{{ currentStepTitle }}</h2>
        </div>
        <div class="flex items-center space-x-2 text-xs text-slate-400">
          <span v-if="isSaving" class="flex items-center text-amber-400">
            <svg class="animate-spin -ml-1 mr-1.5 h-3.5 w-3.5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Saving...
          </span>
          <span v-else class="flex items-center text-emerald-400">
            <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            Saved offline
          </span>
        </div>
      </div>

      <!-- Progress Track -->
      <div class="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700/50">
        <div 
          class="bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 h-2.5 rounded-full transition-all duration-300 ease-out"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>

      <!-- Step Badges -->
      <div class="grid grid-cols-5 gap-2 mt-4">
        <button
          v-for="step in steps"
          :key="step.number"
          @click="goToStep(step.number)"
          :disabled="step.number > currentStep && !isStepValid(step.number - 1)"
          class="flex flex-col items-center p-2 rounded-lg text-xs font-medium transition-colors text-center"
          :class="[
            step.number === currentStep 
              ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/40' 
              : step.number < currentStep 
                ? 'bg-slate-800/80 text-slate-300 hover:bg-slate-800' 
                : 'text-slate-500 opacity-60 cursor-not-allowed'
          ]"
        >
          <div class="flex items-center justify-center w-5 h-5 rounded-full mb-1 text-[10px]"
            :class="step.number < currentStep ? 'bg-emerald-500/20 text-emerald-400' : step.number === currentStep ? 'bg-emerald-500 text-white' : 'bg-slate-700 text-slate-400'"
          >
            <span v-if="step.number < currentStep">✓</span>
            <span v-else>{{ step.number }}</span>
          </div>
          <span class="truncate max-w-[80px] hidden sm:inline">{{ step.shortTitle }}</span>
        </button>
      </div>
    </div>

    <!-- Active Step Content Card -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl backdrop-blur">
      <slot></slot>

      <!-- Stepper Controls Footer -->
      <div class="flex items-center justify-between mt-8 pt-6 border-t border-slate-800">
        <button
          v-if="currentStep > 1"
          @click="prevStep"
          class="px-5 py-2.5 rounded-xl text-sm font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 transition"
        >
          ← Back
        </button>
        <div v-else></div>

        <div class="flex items-center space-x-3">
          <button
            v-if="currentStep < totalSteps"
            @click="nextStep"
            :disabled="!canProceed"
            class="px-6 py-2.5 rounded-xl text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg shadow-emerald-600/30 flex items-center"
          >
            Continue
            <svg class="w-4 h-4 ml-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </button>
          <button
            v-else
            @click="$emit('complete')"
            :disabled="!canProceed"
            class="px-7 py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg shadow-emerald-600/30 flex items-center"
          >
            Evaluate All 31 Exams
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';

const profileStore = useProfileStore();

const steps = [
  { number: 1, title: 'Demographics & Category', shortTitle: 'Demographics' },
  { number: 2, title: 'Academic History & Degree', shortTitle: 'Academics' },
  { number: 3, title: 'Domicile & Languages', shortTitle: 'Domicile' },
  { number: 4, title: 'Prior Examination Attempts', shortTitle: 'Attempts' },
  { number: 5, title: 'Physical & Medical Standards', shortTitle: 'Physical' },
];

const currentStep = computed(() => profileStore.currentStep);
const totalSteps = computed(() => profileStore.totalSteps);
const progressPercentage = computed(() => profileStore.progressPercentage);
const canProceed = computed(() => profileStore.canProceed);
const isSaving = computed(() => profileStore.isSaving);

const currentStepTitle = computed(() => {
  const step = steps.find((s) => s.number === currentStep.value);
  return step ? step.title : '';
});

function isStepValid(stepNumber: number): boolean {
  return profileStore.isStepValid(stepNumber);
}

function goToStep(stepNumber: number) {
  if (stepNumber <= currentStep.value || profileStore.isStepValid(stepNumber - 1)) {
    profileStore.setStep(stepNumber);
  }
}

function nextStep() {
  profileStore.nextStep();
}

function prevStep() {
  profileStore.prevStep();
}

defineEmits(['complete']);
</script>
