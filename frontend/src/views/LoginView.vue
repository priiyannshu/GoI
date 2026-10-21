<template>
  <div class="max-w-md mx-auto py-16 px-4 sm:px-6">
    <!-- Super Clean Card -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-lg p-6 sm:p-8 space-y-6">
      <!-- Simple Heading -->
      <h1 class="text-2xl font-bold text-center text-slate-900 dark:text-white tracking-tight">
        Portal Access
      </h1>

      <!-- Already Logged In State -->
      <div v-if="authStore.isAuthenticated" class="text-center space-y-4 py-2">
        <p class="text-sm text-slate-600 dark:text-slate-300">
          Signed in as <strong class="text-slate-900 dark:text-white">{{ authStore.candidateName }}</strong>
        </p>
        <div class="flex items-center justify-center space-x-3">
          <router-link
            to="/profile"
            class="px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors"
          >
            Go to Profile →
          </router-link>
          <button
            @click="authStore.logout()"
            class="px-4 py-2 rounded-xl text-xs font-medium text-slate-500 hover:text-rose-500 dark:text-slate-400 dark:hover:text-rose-400 transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>

      <!-- Login Form -->
      <form v-else @submit.prevent="handleLogin" class="space-y-4">
        <!-- Error / Feedback -->
        <div
          v-if="errorMessage && !notFound"
          class="p-3 rounded-xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/50 text-xs text-rose-600 dark:text-rose-400"
        >
          {{ errorMessage }}
        </div>

        <!-- Not Found: Direct prompt to create new candidate profile -->
        <div
          v-if="notFound"
          class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 space-y-3 text-center"
        >
          <p class="text-xs text-slate-600 dark:text-slate-300">
            No profile found for <strong>{{ candidateName }}</strong>. Create a new profile with this PIN?
          </p>
          <button
            type="button"
            @click="handleCreateNew"
            :disabled="authStore.isLoading"
            class="w-full py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors flex items-center justify-center space-x-1.5"
          >
            <span v-if="authStore.isLoading">Creating...</span>
            <span v-else>Create New Profile</span>
          </button>
        </div>

        <!-- Success Message -->
        <div
          v-if="successMessage"
          class="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/50 text-xs text-emerald-600 dark:text-emerald-400 text-center"
        >
          {{ successMessage }}
        </div>

        <!-- Candidate Name Field -->
        <div>
          <input
            type="text"
            v-model="candidateName"
            placeholder="Candidate Name (e.g. Rahul Sharma)"
            autocomplete="name"
            required
            @input="notFound = false; errorMessage = null"
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
          />
        </div>

        <!-- Access PIN Field -->
        <div>
          <input
            type="password"
            v-model="pin"
            maxlength="4"
            pattern="[0-9]{4}"
            inputmode="numeric"
            placeholder="4-Digit Access PIN (e.g. 1234)"
            required
            @input="notFound = false; errorMessage = null"
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
          />
        </div>

        <!-- Submit Button -->
        <button
          v-if="!notFound"
          type="submit"
          :disabled="authStore.isLoading || pin.length !== 4 || !candidateName.trim()"
          class="w-full py-3 rounded-xl text-sm font-bold text-white transition-all flex items-center justify-center"
          :class="
            authStore.isLoading || pin.length !== 4 || !candidateName.trim()
              ? 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed'
              : 'bg-emerald-600 hover:bg-emerald-500 shadow-md shadow-emerald-600/20 active:scale-[0.99]'
          "
        >
          <span v-if="authStore.isLoading">Signing In...</span>
          <span v-else>Continue</span>
        </button>
      </form>
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

const candidateName = ref<string>(authStore.candidateName || profileStore.profile.full_name || '');
const pin = ref<string>('');
const notFound = ref<boolean>(false);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

async function handleLogin() {
  errorMessage.value = null;
  notFound.value = false;
  successMessage.value = null;

  if (!candidateName.value.trim() || pin.value.length !== 4) {
    return;
  }

  const res = await authStore.login(candidateName.value.trim(), pin.value);

  if (res.success) {
    successMessage.value = 'Welcome back!';
    profileStore.profile.user_id = authStore.candidateId;
    profileStore.profile.full_name = authStore.candidateName;

    if (res.profile) {
      profileStore.applyRemoteProfile(res.profile);
    }

    setTimeout(() => {
      router.push('/profile');
    }, 400);
  } else {
    // Check if account not found
    if (authStore.authError?.toLowerCase().includes('not found') || authStore.authError?.toLowerCase().includes('register')) {
      notFound.value = true;
    } else {
      errorMessage.value = authStore.authError || 'Incorrect PIN or login error.';
    }
  }
}

async function handleCreateNew() {
  errorMessage.value = null;
  const ok = await authStore.register(candidateName.value.trim(), pin.value);
  if (ok) {
    successMessage.value = 'Profile created!';
    profileStore.profile.user_id = authStore.candidateId;
    profileStore.profile.full_name = authStore.candidateName;

    if (profileStore.isProfileCompleteForD1) {
      await profileStore.propagateToCloudflareDB();
    }

    setTimeout(() => {
      router.push('/profile');
    }, 400);
  } else {
    errorMessage.value = authStore.authError || 'Could not create profile.';
  }
}
</script>
