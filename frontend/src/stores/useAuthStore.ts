import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { loginCandidate, registerCandidate } from '../services/apiWorkerClient';
import type { CandidateAccount } from '../types/auth';

const STORAGE_KEY = 'grade_a_candidate_session';
const GUEST_STORAGE_KEY = 'grade_a_guest_session';

export const useAuthStore = defineStore('candidateAuth', () => {
  const candidateName = ref<string>('');
  const candidateId = ref<string>('');
  const isGuest = ref<boolean>(false);
  const isAuthModalOpen = ref<boolean>(false);
  const isLoading = ref<boolean>(false);
  const authError = ref<string | null>(null);
  const accountsChoice = ref<CandidateAccount[]>([]);

  const isAuthenticated = computed(() => isGuest.value || (!!candidateId.value && !!candidateName.value));

  function initAuth() {
    try {
      const guestSaved = localStorage.getItem(GUEST_STORAGE_KEY);
      if (guestSaved === 'true') {
        isGuest.value = true;
        candidateName.value = 'Guest Candidate';
        candidateId.value = '';
        return;
      }

      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed.user_id && parsed.candidate_name) {
          candidateId.value = parsed.user_id;
          candidateName.value = parsed.candidate_name;
          isGuest.value = false;
        }
      }
    } catch {
      // Ignore local storage error
    }
  }

  function continueAsGuest() {
    isGuest.value = true;
    candidateId.value = '';
    candidateName.value = 'Guest Candidate';
    authError.value = null;
    accountsChoice.value = [];
    try {
      localStorage.setItem(GUEST_STORAGE_KEY, 'true');
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Ignore
    }
  }

  function saveSession(userId: string, name: string) {
    candidateId.value = userId;
    candidateName.value = name;
    isGuest.value = false;
    authError.value = null;
    accountsChoice.value = [];
    try {
      localStorage.removeItem(GUEST_STORAGE_KEY);
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          user_id: userId,
          candidate_name: name,
          logged_in_at: new Date().toISOString(),
        })
      );
    } catch {
      // Ignore
    }
  }

  async function login(name: string, pin: string, uniqueId?: string): Promise<{ success: boolean; profile?: any; multiple?: boolean }> {
    isLoading.value = true;
    authError.value = null;
    accountsChoice.value = [];

    try {
      const res = await loginCandidate(name, pin, uniqueId);
      if (res.multiple_accounts && res.accounts && res.accounts.length > 1) {
        accountsChoice.value = res.accounts;
        return { success: false, multiple: true };
      }

      if (res.success && res.user_id && res.candidate_name) {
        saveSession(res.user_id, res.candidate_name);
        return { success: true, profile: res.profile };
      }

      authError.value = res.message || 'Login failed. Please check credentials.';
      return { success: false };
    } catch (err: any) {
      authError.value = err.message || 'Login failed. Network or server error.';
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function register(name: string, pin: string): Promise<boolean> {
    isLoading.value = true;
    authError.value = null;
    accountsChoice.value = [];

    try {
      const res = await registerCandidate(name, pin);
      if (res.success && res.user_id && res.candidate_name) {
        saveSession(res.user_id, res.candidate_name);
        return true;
      }
      authError.value = res.message || 'Registration failed.';
      return false;
    } catch (err: any) {
      authError.value = err.message || 'Registration failed. Network or server error.';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  function logout() {
    candidateId.value = '';
    candidateName.value = '';
    isGuest.value = false;
    authError.value = null;
    accountsChoice.value = [];
    try {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(GUEST_STORAGE_KEY);
    } catch {
      // Ignore
    }
    // Also clear session-specific hidden items so subsequent guest or user starts clean
    try {
      import('./useHiddenStore').then(({ useHiddenStore }) => {
        const hiddenStore = useHiddenStore();
        hiddenStore.clearHiddenItemsLocal();
      });
    } catch {}
  }

  function openLoginModal() {
    authError.value = null;
    accountsChoice.value = [];
    isAuthModalOpen.value = true;
  }

  function closeLoginModal() {
    isAuthModalOpen.value = false;
  }

  return {
    candidateName,
    candidateId,
    isGuest,
    isAuthenticated,
    isAuthModalOpen,
    isLoading,
    authError,
    accountsChoice,
    initAuth,
    continueAsGuest,
    saveSession,
    login,
    register,
    logout,
    openLoginModal,
    closeLoginModal,
  };
});
