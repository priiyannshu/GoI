<template>
  <div class="py-4 space-y-6">
    <div v-if="eligibilityStore.totalCount === 0" class="max-w-2xl mx-auto py-12 text-center space-y-4">
      <div class="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto text-2xl font-bold">
        📋
      </div>
      <h1 class="text-2xl font-bold text-slate-900 dark:text-white">No Eligibility Profile Evaluated Yet</h1>
      <p class="text-sm text-slate-600 dark:text-slate-400">
        Complete our 5-step intake quiz to determine your statutory eligibility across audited Indian Grade A examinations.
      </p>
      <router-link
        to="/quiz"
        class="inline-block px-6 py-2.5 rounded-xl font-semibold bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg shadow-emerald-500/25 transition"
      >
        Start Eligibility Quiz →
      </router-link>
    </div>

    <EligibilityReportCard
      v-else
      :exams-map="examMasterStore.examsMap"
      @edit-profile="router.push('/quiz')"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useProfileStore } from '@/stores/useProfileStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import EligibilityReportCard from '@/components/quiz/EligibilityReportCard.vue';

const router = useRouter();
const eligibilityStore = useEligibilityStore();
const profileStore = useProfileStore();
const examMasterStore = useExamMasterStore();

onMounted(async () => {
  await examMasterStore.loadExams();
  await profileStore.loadInitialProfile();
  await eligibilityStore.loadCachedVerdicts();

  if (eligibilityStore.totalCount === 0) {
    // Automatically evaluate initial profile
    await eligibilityStore.evaluateAllExams(profileStore.profile);
  }
});
</script>
