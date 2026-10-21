<template>
  <header class="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
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
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400 font-bold text-base group-hover:scale-105 transition-transform">
            🏛️
          </div>
          <div class="flex items-baseline space-x-1.5">
            <span class="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white tracking-tight">Government of India</span>
          </div>
        </router-link>
      </div>

      <!-- Right: Working Theme Toggle Only (No online tag, no profile icon) -->
      <div class="flex items-center space-x-2.5 sm:space-x-3">
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
                  <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400 font-bold text-base">
                    🏛️
                  </div>
                  <div>
                    <span class="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white">Government of India</span>
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

              <!-- Profile Summary Card in Drawer -->
              <router-link
                to="/profile"
                @click="isDrawerOpen = false"
                class="block p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/40 transition-colors group"
              >
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center space-x-2">
                    <span class="text-base">👤</span>
                    <span class="text-xs font-bold text-slate-800 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                      Candidate Profile
                    </span>
                  </div>
                  <span class="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    {{ profileStore.completionPercentage }}%
                  </span>
                </div>
                <div class="w-full bg-slate-200 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden mb-2">
                  <div class="bg-emerald-500 h-full transition-all duration-300" :style="{ width: `${profileStore.completionPercentage}%` }"></div>
                </div>
                <div class="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
                  <span>{{ eligibilityStore.eligibleCount }} Exams Eligible</span>
                  <span class="text-emerald-600 dark:text-emerald-400 font-medium">Edit Profile →</span>
                </div>
              </router-link>

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

            <!-- Drawer Footer -->
            <div class="pt-6 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 space-y-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="font-semibold text-slate-700 dark:text-slate-300">Government of India</span>
                <span class="font-mono text-emerald-600 dark:text-emerald-400">Official Portal</span>
              </div>
              <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Statutory eligibility, recruitment cadres, syllabus intelligence, and career benefits.
              </p>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useHiddenStore } from '@/stores/useHiddenStore';
import ThemeToggle from '@/components/common/ThemeToggle.vue';

const route = useRoute();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const hiddenStore = useHiddenStore();

const isDrawerOpen = ref(false);

const appNavItems = computed(() => [
  { title: 'Official Examinations', path: '/exams', icon: '📋' },
  { title: 'Posts & Lifestyle Perks', path: '/posts', icon: '🏛️' },
  { title: 'Profile & Eligibility', path: '/profile', icon: '👤' },
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
