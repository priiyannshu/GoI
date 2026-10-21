<template>
  <div class="py-4 space-y-8">
    <!-- Mode 1: Quiz Stepper Flow (Steps 1 to 5) -->
    <div v-if="viewMode === 'quiz'">
      <div class="text-center mb-8">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Indian Grade A Examinations Profiler
        </h1>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2 max-w-xl mx-auto">
          Answer 5 brief statutory sections to instantly determine your eligibility across all 31 central civil, regulatory, defense, state PSC, and PSU posts for 2027.
        </p>
      </div>

      <QuizStepper @complete="handleEvaluationComplete">
        <transition name="fade" mode="out-in">
          <component :is="activeStepComponent" />
        </transition>
      </QuizStepper>
    </div>

    <!-- Mode 2: Explanatory Eligibility Report Card -->
    <div v-else-if="viewMode === 'report'">
      <EligibilityReportCard 
        :exams-map="examMasterStore.examsMap"
        @edit-profile="viewMode = 'quiz'"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';

import QuizStepper from '@/components/quiz/QuizStepper.vue';
import StepDemographics from '@/components/quiz/StepDemographics.vue';
import StepAcademics from '@/components/quiz/StepAcademics.vue';
import StepDomicileLanguages from '@/components/quiz/StepDomicileLanguages.vue';
import StepAttempts from '@/components/quiz/StepAttempts.vue';
import StepPhysicalStandards from '@/components/quiz/StepPhysicalStandards.vue';
import EligibilityReportCard from '@/components/quiz/EligibilityReportCard.vue';

const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const examMasterStore = useExamMasterStore();

const viewMode = ref<'quiz' | 'report'>('quiz');

const activeStepComponent = computed(() => {
  switch (profileStore.currentStep) {
    case 1: return StepDemographics;
    case 2: return StepAcademics;
    case 3: return StepDomicileLanguages;
    case 4: return StepAttempts;
    case 5: return StepPhysicalStandards;
    default: return StepDemographics;
  }
});

onMounted(async () => {
  // 1. Initialize profile from IndexedDB
  await profileStore.loadInitialProfile();

  // 2. Load cached verdicts if any
  await eligibilityStore.loadCachedVerdicts();

  // 3. Ensure exam catalog is loaded
  await examMasterStore.loadExams();
});

async function handleEvaluationComplete() {
  await eligibilityStore.evaluateAllExams(profileStore.profile);
  viewMode.value = 'report';
  if (typeof window !== 'undefined') {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
</script>
