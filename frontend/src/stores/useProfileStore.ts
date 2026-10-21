import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import type { UserProfileInput } from '../types/profile';
import { indexedDbStorage } from '../services/indexedDbStorage';
import { syncProfileToEdge } from '../services/apiWorkerClient';
import { useAuthStore } from './useAuthStore';

export const DEFAULT_PROFILE: UserProfileInput = {
  user_id: '',
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
  sitting_height_cm: null,
  leg_length_cm: null,
  thigh_length_cm: null,
  weight_kg: null,
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
  const authStore = useAuthStore();

  // State
  const profile = ref<UserProfileInput>({ ...DEFAULT_PROFILE });
  const currentStep = ref<number>(1);
  const totalSteps = ref<number>(5);
  const isLoaded = ref<boolean>(false);
  const isSaving = ref<boolean>(false);
  const isSyncing = ref<boolean>(false);
  const lastSyncedAt = ref<string | null>(null);
  const syncStatus = ref<'idle' | 'saved_offline' | 'synced_online' | 'error'>('idle');
  const syncError = ref<string | null>(null);

  // Check if mandatory fields required by Cloudflare D1 are satisfied
  function getMissingMandatoryFields(): string[] {
    const p = profile.value;
    const missing: string[] = [];
    if (!p.dob) missing.push('Date of Birth');
    if (!p.gender) missing.push('Gender');
    if (!p.category) missing.push('Reservation Category');
    if (!p.graduation_degree) missing.push('Degree Level');
    if (!p.graduation_discipline) missing.push('Discipline/Branch');
    if (p.graduation_aggregate_pct == null || isNaN(Number(p.graduation_aggregate_pct))) {
      missing.push('Graduation Aggregate %');
    }
    if (!p.state_domicile) missing.push('Home State Domicile');
    return missing;
  }

  const isProfileCompleteForD1 = computed(() => {
    return getMissingMandatoryFields().length === 0;
  });

  // Prepare normalized payload for Cloudflare D1
  function getD1Payload() {
    const p = profile.value;
    const userId = p.user_id || authStore.candidateId || `cand_${Date.now().toString(36)}`;
    const candidateName = p.full_name || authStore.candidateName || 'Candidate';

    return {
      user_id: userId,
      name: candidateName,
      dob: p.dob,
      gender: p.gender,
      category: p.category,
      graduation_degree: p.graduation_degree,
      graduation_discipline: p.graduation_discipline,
      graduation_aggregate_pct: Number(p.graduation_aggregate_pct),
      is_final_year: p.is_final_year ? 1 : 0,
      state_domicile: p.state_domicile,
      mother_tongue: p.fluent_languages && p.fluent_languages.length > 0 ? p.fluent_languages[0] : null,
      height_cm: p.height_cm != null ? Number(p.height_cm) : null,
      chest_cm: p.chest_cm != null ? Number(p.chest_cm) : null,
      prior_attempts: p.prior_attempts || {},
    };
  }

  // Keep aliases synchronized
  watch(
    profile,
    (newP) => {
      newP.degree = newP.graduation_degree;
      newP.discipline = newP.graduation_discipline;
      newP.aggregate_pct = newP.graduation_aggregate_pct;
      newP.domicile_state = newP.state_domicile;
      if (authStore.candidateId && !newP.user_id) {
        newP.user_id = authStore.candidateId;
      }
      if (authStore.candidateName && !newP.full_name) {
        newP.full_name = authStore.candidateName;
      }
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

      // Background propagation if online and all required fields are filled
      if (typeof navigator !== 'undefined' && navigator.onLine && isProfileCompleteForD1.value) {
        try {
          isSyncing.value = true;
          const payload = getD1Payload();
          await syncProfileToEdge(payload);
          lastSyncedAt.value = new Date().toISOString();
          syncStatus.value = 'synced_online';
          syncError.value = null;
        } catch (err: any) {
          syncStatus.value = 'saved_offline';
          syncError.value = err.message || 'Auto-sync failed';
        } finally {
          isSyncing.value = false;
        }
      }
    }, 600);
  }

  // Explicit method to propagate candidate profile to Cloudflare D1
  async function propagateToCloudflareDB(): Promise<{ success: boolean; message: string; missing_fields?: string[] }> {
    const missing = getMissingMandatoryFields();
    if (missing.length > 0) {
      syncStatus.value = 'error';
      syncError.value = `Please fill required fields before syncing: ${missing.join(', ')}`;
      return {
        success: false,
        message: syncError.value,
        missing_fields: missing,
      };
    }

    try {
      isSyncing.value = true;
      syncError.value = null;
      const payload = getD1Payload();
      const res = await syncProfileToEdge(payload);

      if (res && res.success) {
        lastSyncedAt.value = res.synced_at || new Date().toISOString();
        syncStatus.value = 'synced_online';
        if (payload.user_id && !profile.value.user_id) {
          profile.value.user_id = payload.user_id;
        }
        await indexedDbStorage.saveProfile(profile.value);
        return {
          success: true,
          message: 'Profile successfully propagated and persisted to Cloudflare D1 Database!',
        };
      } else {
        throw new Error(res?.message || 'Sync failed');
      }
    } catch (err: any) {
      syncStatus.value = 'error';
      syncError.value = err.message || 'Failed to propagate profile to Cloudflare D1';
      return {
        success: false,
        message: syncError.value || 'Failed to propagate profile to Cloudflare D1',
      };
    } finally {
      isSyncing.value = false;
    }
  }

  // Apply a profile row retrieved from Cloudflare D1 (e.g. after candidate login)
  function applyRemoteProfile(remote: any) {
    if (!remote) return;
    if (remote.name) profile.value.full_name = remote.name;
    if (remote.user_id) profile.value.user_id = remote.user_id;
    if (remote.dob) profile.value.dob = remote.dob;
    if (remote.gender) {
      const g = remote.gender.toUpperCase();
      if (g === 'MALE') profile.value.gender = 'Male';
      else if (g === 'FEMALE') profile.value.gender = 'Female';
      else profile.value.gender = 'Other';
    }
    if (remote.category) profile.value.category = remote.category;
    if (remote.graduation_degree) profile.value.graduation_degree = remote.graduation_degree;
    if (remote.graduation_discipline) profile.value.graduation_discipline = remote.graduation_discipline;
    if (remote.graduation_aggregate_pct != null) profile.value.graduation_aggregate_pct = Number(remote.graduation_aggregate_pct);
    if (remote.is_final_year != null) profile.value.is_final_year = !!remote.is_final_year;
    if (remote.state_domicile) profile.value.state_domicile = remote.state_domicile;
    if (remote.mother_tongue) {
      profile.value.fluent_languages = [remote.mother_tongue];
    }
    if (remote.height_cm != null) profile.value.height_cm = Number(remote.height_cm);
    if (remote.chest_cm != null) profile.value.chest_cm = Number(remote.chest_cm);

    if (remote.prior_attempts_json) {
      try {
        profile.value.prior_attempts = JSON.parse(remote.prior_attempts_json);
      } catch {}
    }

    lastSyncedAt.value = remote.updated_at || new Date().toISOString();
    syncStatus.value = 'synced_online';
    indexedDbStorage.saveProfile(profile.value);
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
        return true;
      case 5:
        return true;
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
    // Section 1: Candidate Identity & Demographics
    if (p.dob && p.gender && p.category) filled++;
    // Section 2: Academic Qualifications
    if (p.graduation_degree && p.graduation_discipline && p.graduation_aggregate_pct != null) filled++;
    // Section 3: Home State Domicile & Languages
    if (p.state_domicile) filled++;
    // Section 4: Physical & Medical Standards
    if (p.height_cm != null || p.weight_kg != null || p.chest_cm != null || p.has_color_blindness) filled++;
    return Math.round((filled / 4) * 100);
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
    authStore.initAuth();
    const saved = await indexedDbStorage.loadProfile();
    if (saved) {
      Object.assign(profile.value, DEFAULT_PROFILE, saved);
    }
    if (authStore.candidateId && !profile.value.user_id) {
      profile.value.user_id = authStore.candidateId;
    }
    if (authStore.candidateName && !profile.value.full_name) {
      profile.value.full_name = authStore.candidateName;
    }
    isLoaded.value = true;
  }

  // Backwards compatibility alias
  async function loadPersistedProfile() {
    return loadInitialProfile();
  }

  async function saveProgress() {
    await indexedDbStorage.saveProfile(profile.value);
    if (typeof navigator !== 'undefined' && navigator.onLine && isProfileCompleteForD1.value) {
      await propagateToCloudflareDB();
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
    Object.assign(profile.value, DEFAULT_PROFILE);
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
    syncError,
    isProfileCompleteForD1,
    getMissingMandatoryFields,
    propagateToCloudflareDB,
    applyRemoteProfile,
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

