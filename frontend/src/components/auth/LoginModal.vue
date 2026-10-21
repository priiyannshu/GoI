<template>
  <Teleport to="body">
    <transition name="modal-fade">
      <div
        v-if="authStore.isAuthModalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/75 backdrop-blur-sm"
        @click.self="authStore.closeLoginModal"
        @keydown.escape="authStore.closeLoginModal"
      >
        <div class="relative w-full max-w-md bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl p-6 sm:p-7 space-y-5 overflow-hidden">
          <!-- Close Button -->
          <button
            @click="authStore.closeLoginModal"
            class="absolute top-4 right-4 p-1.5 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            aria-label="Close modal"
          >
            ✕
          </button>

          <!-- Header -->
          <div class="text-center space-y-1">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-xl mb-1 shadow-xs">
              🏛️
            </div>
            <h2 class="text-xl font-extrabold text-slate-900 dark:text-white">Candidate Authentication</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">
              Sign in with your Name & 4-Digit PIN to propagate your profile to Cloudflare D1.
            </p>
          </div>

          <!-- Mode Switcher -->
          <div class="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1 border border-slate-200 dark:border-slate-700/80">
            <button
              type="button"
              @click="mode = 'login'; reset()"
              class="flex-1 py-1.5 text-xs font-bold rounded-lg transition-all"
              :class="mode === 'login' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-xs' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            >
              Sign In
            </button>
            <button
              type="button"
              @click="mode = 'register'; reset()"
              class="flex-1 py-1.5 text-xs font-bold rounded-lg transition-all"
              :class="mode === 'register' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-xs' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            >
              Register Profile
            </button>
          </div>

          <!-- Error Alert -->
          <div
            v-if="errorMsg"
            class="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-300 dark:border-rose-500/40 text-xs text-rose-700 dark:text-rose-300 flex items-start space-x-2"
          >
            <span>⚠️</span>
            <div class="flex-1">{{ errorMsg }}</div>
          </div>

          <!-- Success Alert -->
          <div
            v-if="successMsg"
            class="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-300 dark:border-emerald-500/40 text-xs text-emerald-700 dark:text-emerald-300 flex items-center space-x-2"
          >
            <span>✓</span>
            <div>{{ successMsg }}</div>
          </div>

          <!-- Form -->
          <form @submit.prevent="submit" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1 uppercase tracking-wider">
                Candidate Name
              </label>
              <input
                type="text"
                v-model="name"
                placeholder="Candidate Full Name"
                required
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                  4-Digit PIN
                </label>
                <button
                  type="button"
                  @click="showPin = !showPin"
                  class="text-[10px] text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                >
                  {{ showPin ? 'Hide' : 'Show' }}
                </button>
              </div>
              <input
                :type="showPin ? 'text' : 'password'"
                v-model="pin"
                maxlength="4"
                pattern="[0-9]{4}"
                placeholder="••••"
                required
                class="w-full text-center tracking-[0.5em] font-mono text-xl py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
            </div>

            <button
              type="submit"
              :disabled="authStore.isLoading || pin.length !== 4 || !name.trim()"
              class="w-full py-2.5 rounded-xl text-xs font-bold text-white transition-all duration-200 flex items-center justify-center"
              :class="
                authStore.isLoading || pin.length !== 4 || !name.trim()
                  ? 'bg-slate-300 dark:bg-slate-800 cursor-not-allowed text-slate-400'
                  : 'bg-emerald-600 hover:bg-emerald-500 active:scale-[0.99] shadow-md shadow-emerald-600/20'
              "
            >
              <span v-if="authStore.isLoading" class="mr-2">🔄</span>
              <span>
                {{
                  authStore.isLoading
                    ? 'Processing...'
                    : mode === 'login'
                    ? 'Log In'
                    : 'Create Account & Unique ID'
                }}
              </span>
            </button>
          </form>

          <!-- Footer Info -->
          <div class="text-[11px] text-slate-500 dark:text-slate-400 text-center">
            Unique Candidate ID automatically links matching name & PIN in Cloudflare D1.
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { useProfileStore } from '@/stores/useProfileStore';

const authStore = useAuthStore();
const profileStore = useProfileStore();

const mode = ref<'login' | 'register'>('login');
const name = ref<string>(authStore.candidateName || profileStore.profile.full_name || '');
const pin = ref<string>('');
const showPin = ref<boolean>(false);
const errorMsg = ref<string | null>(null);
const successMsg = ref<string | null>(null);

function reset() {
  pin.value = '';
  errorMsg.value = null;
  successMsg.value = null;
}

async function submit() {
  errorMsg.value = null;
  successMsg.value = null;

  if (mode.value === 'login') {
    const res = await authStore.login(name.value.trim(), pin.value);
    if (res.success) {
      successMsg.value = `Logged in as ${authStore.candidateName}`;
      profileStore.profile.user_id = authStore.candidateId;
      profileStore.profile.full_name = authStore.candidateName;
      if (res.profile) {
        profileStore.applyRemoteProfile(res.profile);
      }
      setTimeout(() => {
        authStore.closeLoginModal();
      }, 700);
    } else {
      errorMsg.value = authStore.authError || 'Login failed.';
    }
  } else {
    const ok = await authStore.register(name.value.trim(), pin.value);
    if (ok) {
      successMsg.value = `Account created! ID: ${authStore.candidateId}`;
      profileStore.profile.user_id = authStore.candidateId;
      profileStore.profile.full_name = authStore.candidateName;
      if (profileStore.isProfileCompleteForD1) {
        profileStore.propagateToCloudflareDB();
      }
      setTimeout(() => {
        authStore.closeLoginModal();
      }, 900);
    } else {
      errorMsg.value = authStore.authError || 'Registration failed.';
    }
  }
}
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
