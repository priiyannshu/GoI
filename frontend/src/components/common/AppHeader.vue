<template>
  <header class="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
    <!-- SFIIL Signature Accent Gradient Stripe -->
    <div class="sfiil-gradient-bar w-full"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left: Hamburger Drawer Trigger & Brand Logo -->
      <div class="flex items-center space-x-3">
        <!-- Hamburger Button (desktop & mobile) -->
        <button
          @click="isDrawerOpen = true"
          class="p-2 -ml-2 rounded-xl text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
          aria-label="Open navigation menu"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Brand Mark: Government of India -->
        <router-link to="/" class="flex items-center space-x-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center p-1.5 text-sky-400 group-hover:scale-105 transition-transform">
            <AppEmblem class="w-full h-full" />
          </div>
          <div class="flex items-baseline space-x-1.5">
            <span class="font-goi-cursive font-bold text-lg sm:text-xl text-slate-900 dark:text-white tracking-tight">Government of India</span>
          </div>
        </router-link>
      </div>

      <!-- Right: Working Theme Toggle -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <ThemeToggle />
      </div>
    </div>

    <!-- Slide-Out App Drawer (Teleported to body so it displays over the full screen) -->
    <Teleport to="body">
      <transition name="drawer-fade">
        <div
          v-if="isDrawerOpen"
          class="fixed inset-0 z-50 flex"
          @keydown.escape="isDrawerOpen = false"
        >
          <!-- Backdrop Overlay -->
          <div
            class="fixed inset-0 bg-slate-950/75 backdrop-blur-sm transition-opacity"
            @click="isDrawerOpen = false"
          ></div>

          <!-- Drawer Panel -->
          <div class="relative w-72 sm:w-80 max-w-[85vw] h-full bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 shadow-2xl flex flex-col justify-between p-5 z-10 overflow-y-auto transition-colors">
            <!-- Drawer Top: Brand & Close -->
            <div class="space-y-6">
              <div class="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
                <div class="flex items-center space-x-2.5">
                  <div class="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center p-1.5 text-sky-400">
                    <AppEmblem class="w-full h-full" />
                  </div>
                  <div>
                    <span class="font-goi-cursive font-bold text-lg sm:text-xl text-slate-900 dark:text-white">Government of India</span>
                  </div>
                </div>

                <button
                  @click="isDrawerOpen = false"
                  class="p-1.5 rounded-lg text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  aria-label="Close drawer"
                >
                  ✕
                </button>
              </div>

              <!-- Candidate Card in Drawer (Non-clickable, Name & ID only) -->
              <div
                class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800"
              >
                <div class="flex items-center space-x-2.5 min-w-0">
                  <span class="text-base flex-shrink-0">{{ authStore.isGuest ? '👀' : '👤' }}</span>
                  <div class="min-w-0 flex-1">
                    <div class="text-xs font-bold text-slate-900 dark:text-white truncate">
                      {{ candidateDisplayName }}
                    </div>
                    <div v-if="authStore.candidateId" class="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-bold truncate">
                      ID: {{ authStore.candidateId }}
                    </div>
                    <div v-else-if="authStore.isGuest" class="text-[10px] text-slate-500 dark:text-slate-400 font-medium">
                      Browsing as Guest
                    </div>
                  </div>
                </div>
              </div>

              <!-- Navigation Links -->
              <nav class="space-y-1 text-sm font-medium">
                <router-link
                  v-for="item in appNavItems"
                  :key="item.path"
                  :to="item.path"
                  @click="isDrawerOpen = false"
                  class="flex items-center justify-between px-3.5 py-3 rounded-xl transition-colors"
                  :class="
                    route.path === item.path || (item.path === '/exams' && route.path === '/')
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 font-bold'
                      : 'text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
                  "
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-lg">{{ item.icon }}</span>
                    <span>{{ item.title }}</span>
                  </div>
                  <span
                    v-if="item.badge"
                    class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                  >
                    {{ item.badge }}
                  </span>
                </router-link>
              </nav>
            </div>

            <!-- Drawer Footer: Sign Out (for logged-in) or Login (for guest) -->
            <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <!-- If Guest: show Login button -->
              <button
                v-if="authStore.isGuest"
                @click="handleGoToLogin"
                class="flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/40 dark:hover:bg-emerald-900/50 transition-colors"
                title="Log In"
                aria-label="Log In"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <span>Log In</span>
              </button>

              <!-- If Logged In: show Sign Out icon -->
              <button
                v-else
                @click="handleLogout"
                class="p-2.5 rounded-xl text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-all flex items-center justify-center"
                title="Sign Out"
                aria-label="Sign Out"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppEmblem from '@/components/common/AppEmblem.vue';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { useHiddenStore } from '@/stores/useHiddenStore';
import { useAuthStore } from '@/stores/useAuthStore';
import { AUDITED_POSTS_DATA } from '@/data/postsData';
import ThemeToggle from '@/components/common/ThemeToggle.vue';

const route = useRoute();
const router = useRouter();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const examStore = useExamMasterStore();
const hiddenStore = useHiddenStore();
const authStore = useAuthStore();

const isDrawerOpen = ref(false);

function handleLogout() {
  authStore.logout();
  isDrawerOpen.value = false;
  router.push('/login');
}

function handleGoToLogin() {
  authStore.logout();
  isDrawerOpen.value = false;
  router.push('/login');
}

const candidateDisplayName = computed(() => {
  return authStore.candidateName || profileStore.profile.full_name?.trim() || 'Candidate Profile';
});

const appNavItems = computed(() => [
  { title: 'Profile & Eligibility', path: '/profile', icon: '👤' },
  {
    title: 'Official Examinations',
    path: '/exams',
    icon: '📋',
    badge: examStore.totalExamsCount,
  },
  {
    title: 'Posts & Lifestyle Perks',
    path: '/posts',
    icon: '🏛️',
    badge: AUDITED_POSTS_DATA.length,
  },
  {
    title: 'Hidden Items',
    path: '/hidden',
    icon: '👁️‍🗨️',
    badge: hiddenStore.totalHiddenCount > 0 ? hiddenStore.totalHiddenCount : undefined,
  },
]);
</script>

<style scoped>
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.25s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
</style>
