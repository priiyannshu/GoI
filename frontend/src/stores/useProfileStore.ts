import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import type { UserProfileInput } from '../types/profile';
import { indexedDbStorage } from '../services/indexedDbStorage';
import { syncProfileToEdge } from '../services/apiWorkerClient';

export const DEFAULT_PROFILE: UserProfileInput = {
  full_name: '',
  dob: '',
  gender: '' as any,
  category: '' as any,
  is_ex_serviceman: false,
  ex_service_years: 0,
  marital_status: 'Unmarried',
  has_children: false,

  graduation_degree: '' as any,
  degree: '' as any,
  graduation_discipline: '',
  discipline: '',
  graduation_aggregate_pct: null as any,
  aggregate_pct: null as any,
  is_final_year: false,
  ten_plus_two_maths_pct: null,
  ten_plus_two_physics_pct: null,

  state_domicile: '',
  domicile_state: '',
  fluent_languages: [],

  prior_attempts: {},
  prior_selected_as_ac: false,

  height_cm: null,
  chest_cm: null,
  chest_expansion_cm: null,
  has_color_blindness: false,
  has_lasik: false,
  lasik_age: null,
  lasik_wait_months: null,
  has_commercial_pilot_license: false,
  enable_skipped_check: true,
  skipped_fields: [],
};

function calculateAgeOn(cutoffStr: string, dobStr: string): number {
  if (!dobStr) return 0;
  const cutoff = new Date(cutoffStr);
  const dob = new Date(dobStr);
  if (isNaN(dob.getTime())) return 0;
  let age = cutoff.getFullYear() - dob.getFullYear();
  if (
    cutoff.getMonth() < dob.getMonth() ||
    (cutoff.getMonth() === dob.getMonth() && cutoff.getDate() < dob.getDate())
  ) {
    age--;
  }
  return age;
}

export const useProfileStore = defineStore('userProfile', () => {
  // State
  const profile = ref<UserProfileInput>({ ...DEFAULT_PROFILE });
  const currentStep = ref<number>(1);
  const totalSteps = ref<number>(5);
  const isLoaded = ref<boolean>(false);
  const isSaving = ref<boolean>(false);
  const isSyncing = ref<boolean>(false);
  const lastSyncedAt = ref<string | null>(null);
  const syncStatus = ref<'idle' | 'saved_offline' | 'synced_online' | 'error'>('idle');

  // Keep aliases synchronized
  watch(
    profile,
    (newP) => {
      newP.degree = newP.graduation_degree;
      newP.discipline = newP.graduation_discipline;
      newP.aggregate_pct = newP.graduation_aggregate_pct;
      newP.domicile_state = newP.state_domicile;
      triggerDebouncedSave();
    },
    { deep: true }
  );

  let saveTimer: any = null;
  function triggerDebouncedSave() {
    isSaving.value = true;
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(async () => {
      await indexedDbStorage.saveProfile(profile.value);
      isSaving.value = false;
      syncStatus.value = 'saved_offline';

      // Background sync if online
      if (typeof navigator !== 'undefined' && navigator.onLine) {
        try {
          isSyncing.value = true;
          await syncProfileToEdge(profile.value);
          lastSyncedAt.value = new Date().toISOString();
          syncStatus.value = 'synced_online';
        } catch {
          syncStatus.value = 'saved_offline';
        } finally {
          isSyncing.value = false;
        }
      }
    }, 400);
  }

  // --- Getters ---

  const calculatedAge2027Aug1 = computed(() => calculateAgeOn('2027-08-01', profile.value.dob));
  const calculatedAge2027Jan1 = computed(() => calculateAgeOn('2027-01-01', profile.value.dob));
  const calculatedAge2027Jul1 = computed(() => calculateAgeOn('2027-07-01', profile.value.dob));

  const isStepValid = computed(() => (step: number): boolean => {
    switch (step) {
      case 1:
        return !!profile.value.dob && !!profile.value.gender && !!profile.value.category;
      case 2:
        return (
          !!profile.value.graduation_degree &&
          !!profile.value.graduation_discipline &&
          profile.value.graduation_aggregate_pct >= 35.0 &&
          profile.value.graduation_aggregate_pct <= 100.0
        );
      case 3:
        return !!profile.value.state_domicile && profile.value.fluent_languages.length > 0;
      case 4:
        return true; // Prior attempts defaults to 0, always valid
      case 5:
        return true; // Physical standards optional or defaults provided
      default:
        return true;
    }
  });

  const canProceed = computed(() => isStepValid.value(currentStep.value));
  const progressPercentage = computed(() =>
    Math.round(((currentStep.value - 1) / totalSteps.value) * 100)
  );

  const completionPercentage = computed(() => {
    let filled = 0;
    const p = profile.value;
    if (p.dob && p.gender && p.category) filled++;
    if (p.graduation_degree && p.graduation_discipline && p.graduation_aggregate_pct != null) filled++;
    if (p.state_domicile) filled++;
    if (p.height_cm != null) filled++;
    if (p.prior_attempts && Object.keys(p.prior_attempts).length > 0) filled++;
    return Math.round((filled / 5) * 100);
  });

  function toggleFieldSkipped(field: string) {
    if (!profile.value.skipped_fields) {
      profile.value.skipped_fields = [];
    }
    const idx = profile.value.skipped_fields.indexOf(field);
    if (idx >= 0) {
      profile.value.skipped_fields.splice(idx, 1);
    } else {
      profile.value.skipped_fields.push(field);
    }
    triggerDebouncedSave();
  }

  function isFieldSkipped(field: string): boolean {
    return profile.value.skipped_fields?.includes(field) ?? false;
  }

  // --- Actions ---

  async function loadInitialProfile() {
    const saved = await indexedDbStorage.loadProfile();
    if (saved) {
      profile.value = { ...DEFAULT_PROFILE, ...saved };
    }
    isLoaded.value = true;
  }

  // Backwards compatibility alias
  async function loadPersistedProfile() {
    return loadInitialProfile();
  }

  async function saveProgress() {
    await indexedDbStorage.saveProfile(profile.value);
    if (typeof navigator !== 'undefined' && navigator.onLine) {
      try {
        isSyncing.value = true;
        await syncProfileToEdge(profile.value);
        lastSyncedAt.value = new Date().toISOString();
        syncStatus.value = 'synced_online';
      } catch {
        syncStatus.value = 'saved_offline';
      } finally {
        isSyncing.value = false;
      }
    }
  }

  function setStep(step: number) {
    if (step >= 1 && step <= totalSteps.value) {
      currentStep.value = step;
    }
  }

  function nextStep() {
    if (currentStep.value < totalSteps.value && canProceed.value) {
      currentStep.value++;
    }
  }

  function prevStep() {
    if (currentStep.value > 1) {
      currentStep.value--;
    }
  }

  function resetToDefaults() {
    profile.value = { ...DEFAULT_PROFILE };
    currentStep.value = 1;
    indexedDbStorage.clearProfile();
  }

  function setPriorAttempt(examId: string, count: number) {
    if (!profile.value.prior_attempts) {
      profile.value.prior_attempts = {};
    }
    profile.value.prior_attempts[examId] = Math.max(0, count);
  }

  return {
    profile,
    currentStep,
    totalSteps,
    isLoaded,
    isSaving,
    isSyncing,
    lastSyncedAt,
    syncStatus,
    calculatedAge2027Aug1,
    calculatedAge2027Jan1,
    calculatedAge2027Jul1,
    isStepValid,
    canProceed,
    progressPercentage,
    completionPercentage,
    toggleFieldSkipped,
    isFieldSkipped,
    loadInitialProfile,
    loadPersistedProfile,
    saveProgress,
    setStep,
    nextStep,
    prevStep,
    resetToDefaults,
    setPriorAttempt,
  };
});

// Alias for PROJECT.md specification compatibility
export const useUserProfileStore = useProfileStore;
