<template>
  <div class="max-w-xl mx-auto py-8 px-4 sm:px-6 space-y-6">
    <!-- Header / Branding -->
    <div class="text-center space-y-2">
      <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-2xl mb-1 shadow-xs">
        🏛️
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
        Candidate Portal Access
      </h1>
      <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto">
        Sign in to save and propagate your statutory eligibility profile across Cloudflare D1 edge database.
      </p>
    </div>

    <!-- Already Logged In Banner -->
    <div
      v-if="authStore.isAuthenticated"
      class="bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-300 dark:border-emerald-500/40 rounded-2xl p-5 text-center space-y-3"
    >
      <div class="flex items-center justify-center space-x-2 text-emerald-700 dark:text-emerald-300 font-bold text-sm">
        <span>✓</span>
        <span>Currently Signed In</span>
      </div>
      <div class="space-y-1">
        <div class="text-base font-extrabold text-slate-900 dark:text-white">{{ authStore.candidateName }}</div>
        <div class="text-xs font-mono font-bold text-emerald-600 dark:text-emerald-400">
          Candidate ID: {{ authStore.candidateId }}
        </div>
      </div>
      <div class="flex items-center justify-center space-x-3 pt-2">
        <router-link
          to="/profile"
          class="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white transition-colors"
        >
          Go to My Profile →
        </router-link>
        <button
          @click="handleLogout"
          class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors"
        >
          Sign Out
        </button>
      </div>
    </div>

    <!-- Main Auth Card -->
    <div v-else class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl p-6 sm:p-8 space-y-6">
      <!-- Tab Switcher: Login vs Register -->
      <div class="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1 border border-slate-200 dark:border-slate-700/80">
        <button
          type="button"
          @click="activeMode = 'login'; resetForm()"
          class="flex-1 py-2 text-xs font-bold rounded-lg transition-all"
          :class="activeMode === 'login' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
        >
          🔑 Existing Candidate Login
        </button>
        <button
          type="button"
          @click="activeMode = 'register'; resetForm()"
          class="flex-1 py-2 text-xs font-bold rounded-lg transition-all"
          :class="activeMode === 'register' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
        >
          ✨ New Candidate Profile
        </button>
      </div>

      <!-- Multiple Accounts Disambiguation Picker (In case identical name + PIN) -->
      <div
        v-if="authStore.accountsChoice.length > 1"
        class="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-500/40 space-y-3"
      >
        <div class="text-xs font-bold text-amber-900 dark:text-amber-200 flex items-center space-x-1.5">
          <span>⚠️</span>
          <span>Multiple Candidate Records Detected</span>
        </div>
        <p class="text-[11px] text-amber-800 dark:text-amber-300">
          Multiple profiles share this Name & PIN. Please select your unique Candidate ID:
        </p>
        <div class="space-y-2">
          <div
            v-for="acc in authStore.accountsChoice"
            :key="acc.user_id"
            @click="selectAccountAndLogin(acc.user_id)"
            class="p-3 rounded-xl bg-white dark:bg-slate-800 border border-amber-200 dark:border-amber-700/50 hover:border-emerald-500 cursor-pointer flex items-center justify-between transition-colors"
          >
            <div>
              <div class="font-mono text-xs font-bold text-slate-900 dark:text-white">{{ acc.user_id }}</div>
              <div class="text-[10px] text-slate-500">{{ acc.candidate_name }}</div>
            </div>
            <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400">Select & Login →</span>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div
        v-if="errorMessage"
        class="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-300 dark:border-rose-500/40 text-xs font-medium text-rose-700 dark:text-rose-300 flex items-start space-x-2"
      >
        <span class="text-sm leading-none">⚠️</span>
        <div class="flex-1">{{ errorMessage }}</div>
      </div>

      <!-- Success Notification -->
      <div
        v-if="successMessage"
        class="p-3.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-300 dark:border-emerald-500/40 text-xs font-medium text-emerald-700 dark:text-emerald-300 flex items-center space-x-2"
      >
        <span class="text-sm leading-none">✓</span>
        <div>{{ successMessage }}</div>
      </div>

      <!-- Form Inputs -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <!-- 1. Candidate Full Name -->
        <div>
          <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5 uppercase tracking-wider">
            Candidate Full Name
          </label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              👤
            </span>
            <input
              type="text"
              v-model="candidateName"
              placeholder="e.g. Rahul Sharma"
              autocomplete="name"
              required
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl pl-10 pr-3.5 py-2.5 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Official candidate name as shown on matriculation certificates.
          </p>
        </div>

        <!-- 2. 4-Digit Security PIN -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
              4-Digit Access PIN
            </label>
            <button
              type="button"
              @click="showPin = !showPin"
              class="text-[11px] text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
            >
              {{ showPin ? 'Hide PIN 🙈' : 'Show PIN 👁️' }}
            </button>
          </div>

          <!-- PIN Inputs -->
          <div class="space-y-3">
            <div class="relative">
              <input
                :type="showPin ? 'text' : 'password'"
                v-model="pin"
                maxlength="4"
                inputmode="numeric"
                pattern="[0-9]{4}"
                placeholder="4-digit PIN (e.g. 1234)"
                required
                class="w-full text-center tracking-[0.5em] font-mono text-xl py-3 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
            </div>

            <!-- PIN Digit Indicators -->
            <div class="flex justify-center space-x-3">
              <div
                v-for="i in 4"
                :key="i"
                class="w-3 h-3 rounded-full border transition-all duration-200"
                :class="pin.length >= i ? 'bg-emerald-500 border-emerald-500 scale-110' : 'bg-slate-200 dark:bg-slate-700 border-slate-300 dark:border-slate-600'"
              ></div>
            </div>
          </div>

          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-2 text-center">
            Exactly 4 numeric digits. Keep this PIN safe to access your profile.
          </p>
        </div>

        <!-- Optional Unique Candidate ID input for disambiguation -->
        <div v-if="activeMode === 'login' && showCandidateIdInput" class="pt-1">
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Unique Candidate ID <span class="text-slate-400 font-normal">(Optional, e.g. CAN-XXXXXXXX)</span>
          </label>
          <input
            type="text"
            v-model="candidateIdInput"
            placeholder="CAN-XXXXXXXX"
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-xs font-mono text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-emerald-500 uppercase"
          />
        </div>

        <div v-if="activeMode === 'login'" class="text-right">
          <button
            type="button"
            @click="showCandidateIdInput = !showCandidateIdInput"
            class="text-[11px] text-slate-500 hover:text-emerald-500 underline transition-colors"
          >
            {{ showCandidateIdInput ? 'Hide Candidate ID field' : 'Have a unique Candidate ID? Enter directly' }}
          </button>
        </div>

        <!-- Action Button -->
        <button
          type="submit"
          :disabled="authStore.isLoading || pin.length !== 4 || !candidateName.trim()"
          class="w-full py-3 rounded-xl text-sm font-bold text-white transition-all duration-200 flex items-center justify-center space-x-2"
          :class="
            authStore.isLoading || pin.length !== 4 || !candidateName.trim()
              ? 'bg-slate-300 dark:bg-slate-800 cursor-not-allowed text-slate-400 dark:text-slate-600'
              : 'bg-emerald-600 hover:bg-emerald-500 active:scale-[0.99] shadow-lg shadow-emerald-600/20'
          "
        >
          <span v-if="authStore.isLoading" class="inline-block animate-spin mr-2">🔄</span>
          <span>
            {{
              authStore.isLoading
                ? 'Processing...'
                : activeMode === 'login'
                ? 'Sign In to Portal'
                : 'Create Candidate Account & Assign ID'
            }}
          </span>
        </button>
      </form>
    </div>

    <!-- Behind the Scenes Architecture Notice -->
    <div class="bg-slate-50 dark:bg-slate-850/60 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 sm:p-5 space-y-2 text-xs text-slate-600 dark:text-slate-400">
      <div class="flex items-center space-x-2 font-bold text-slate-800 dark:text-white">
        <span>🛡️</span>
        <span>Behind the Scenes: Unique Candidate Identity Management</span>
      </div>
      <p class="leading-relaxed">
        To prevent profile collisions when two or more candidates have identical names, our Cloudflare D1 system computes a cryptographic digest of candidate name + 4-digit PIN and assigns a globally unique statutory Candidate ID (<code class="font-mono text-emerald-600 dark:text-emerald-400">CAN-XXXXXXXX</code>).
      </p>
      <p class="leading-relaxed">
        Your candidate profile is isolated in the edge database and automatically propagates whenever you edit or sync your statutory eligibility credentials.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/useAuthStore';
import { useProfileStore } from '@/stores/useProfileStore';

const router = useRouter();
const authStore = useAuthStore();
const profileStore = useProfileStore();

const activeMode = ref<'login' | 'register'>('login');
const candidateName = ref<string>(authStore.candidateName || profileStore.profile.full_name || '');
const pin = ref<string>('');
const candidateIdInput = ref<string>('');
const showCandidateIdInput = ref<boolean>(false);
const showPin = ref<boolean>(false);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

function resetForm() {
  pin.value = '';
  errorMessage.value = null;
  successMessage.value = null;
  authStore.accountsChoice = [];
}

async function handleSubmit() {
  errorMessage.value = null;
  successMessage.value = null;

  if (!candidateName.value.trim()) {
    errorMessage.value = 'Please enter your candidate name.';
    return;
  }

  if (!/^\d{4}$/.test(pin.value)) {
    errorMessage.value = 'Please enter exactly 4 numeric digits for your PIN.';
    return;
  }

  if (activeMode.value === 'login') {
    const res = await authStore.login(
      candidateName.value.trim(),
      pin.value,
      candidateIdInput.value.trim() || undefined
    );

    if (res.success) {
      successMessage.value = `Login successful! Welcome back, ${authStore.candidateName}.`;
      profileStore.profile.user_id = authStore.candidateId;
      profileStore.profile.full_name = authStore.candidateName;

      // If remote profile was returned, apply it
      if (res.profile) {
        profileStore.applyRemoteProfile(res.profile);
      }

      setTimeout(() => {
        router.push('/profile');
      }, 800);
    } else if (res.multiple) {
      errorMessage.value = 'Multiple accounts found with this Name and PIN. Please select your unique Candidate ID.';
    } else {
      errorMessage.value = authStore.authError || 'Login failed. Please check credentials or register as a new candidate.';
    }
  } else {
    // Register
    const ok = await authStore.register(candidateName.value.trim(), pin.value);
    if (ok) {
      successMessage.value = `Account created! Your unique ID is ${authStore.candidateId}.`;
      profileStore.profile.user_id = authStore.candidateId;
      profileStore.profile.full_name = authStore.candidateName;

      // Propagate initial profile if candidate had already filled fields
      if (profileStore.isProfileCompleteForD1) {
        await profileStore.propagateToCloudflareDB();
      }

      setTimeout(() => {
        router.push('/profile');
      }, 1000);
    } else {
      errorMessage.value = authStore.authError || 'Registration failed.';
    }
  }
}

async function selectAccountAndLogin(selectedUserId: string) {
  candidateIdInput.value = selectedUserId;
  await handleSubmit();
}

function handleLogout() {
  authStore.logout();
  successMessage.value = null;
  errorMessage.value = null;
  pin.value = '';
}
</script>
