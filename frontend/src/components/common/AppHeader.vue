<template>
  <header class="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left: Hamburger Drawer Trigger & Brand Logo -->
      <div class="flex items-center space-x-3">
        <!-- Hamburger Button (desktop & mobile) -->
        <button
          @click="isDrawerOpen = true"
          class="p-2 -ml-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
          aria-label="Open navigation menu"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Brand Mark -->
        <router-link to="/" class="flex items-center space-x-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-base group-hover:scale-105 transition-transform">
            A
          </div>
          <div class="flex items-baseline space-x-1.5">
            <span class="font-extrabold text-base sm:text-lg text-white tracking-tight">Grade-A</span>
            <span class="text-[10px] px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-400 font-semibold font-mono">2027</span>
          </div>
        </router-link>
      </div>

      <!-- Right: Profile Quick Status, Offline, Theme -->
      <div class="flex items-center space-x-2.5 sm:space-x-3">
        <OfflineBadge />
        <ThemeToggle />

        <!-- Profile Quick Action Badge -->
        <router-link
          to="/profile"
          class="flex items-center space-x-2 px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-750 text-slate-200 border border-slate-700 hover:border-emerald-500/50 transition-all shadow-sm group"
        >
          <div class="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[10px] font-bold">
            👤
          </div>
          <div class="hidden sm:flex flex-col text-left">
            <span class="text-[11px] font-bold text-white group-hover:text-emerald-400 transition-colors">Profile</span>
            <span class="text-[10px] text-slate-400 font-mono">{{ profileStore.completionPercentage }}% Complete</span>
          </div>
          <span class="sm:hidden text-emerald-400 font-mono text-[11px]">{{ profileStore.completionPercentage }}%</span>
        </router-link>
      </div>
    </div>

    <!-- Slide-Out App Drawer (Hamburger Menu) -->
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
        <div class="relative w-72 sm:w-80 max-w-[85vw] h-full bg-slate-900 border-r border-slate-800 shadow-2xl flex flex-col justify-between p-5 z-10 overflow-y-auto">
          <!-- Drawer Top: Brand & Close -->
          <div class="space-y-6">
            <div class="flex items-center justify-between pb-4 border-b border-slate-800">
              <div class="flex items-center space-x-2.5">
                <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-base">
                  A
                </div>
                <div>
                  <span class="font-extrabold text-lg text-white">Grade-A</span>
                  <span class="text-xs ml-1.5 px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono">2027</span>
                </div>
              </div>

              <button
                @click="isDrawerOpen = false"
                class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                aria-label="Close drawer"
              >
                ✕
              </button>
            </div>

            <!-- Profile Summary Card in Drawer -->
            <router-link
              to="/profile"
              @click="isDrawerOpen = false"
              class="block p-3.5 rounded-xl bg-slate-850 border border-slate-800 hover:border-emerald-500/40 transition-colors group"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="text-base">👤</span>
                  <span class="text-xs font-bold text-white group-hover:text-emerald-400 transition-colors">
                    Candidate Profile
                  </span>
                </div>
                <span class="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                  {{ profileStore.completionPercentage }}%
                </span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mb-2">
                <div class="bg-emerald-500 h-full" :style="{ width: `${profileStore.completionPercentage}%` }"></div>
              </div>
              <div class="flex items-center justify-between text-[11px] text-slate-400">
                <span>{{ eligibilityStore.eligibleCount }} Exams Eligible</span>
                <span class="text-emerald-400 font-medium">Edit Profile →</span>
              </div>
            </router-link>

            <!-- Navigation Links -->
            <nav class="space-y-1 text-sm font-medium">
              <router-link
                v-for="item in appNavItems"
                :key="item.path"
                :to="item.path"
                @click="isDrawerOpen = false"
                class="flex items-center space-x-3 px-3.5 py-3 rounded-xl transition-colors"
                :class="
                  route.path === item.path || (item.path === '/exams' && route.path === '/')
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-bold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800'
                "
              >
                <span class="text-lg">{{ item.icon }}</span>
                <span>{{ item.title }}</span>
              </router-link>
            </nav>
          </div>

          <!-- Drawer Footer -->
          <div class="pt-6 border-t border-slate-800 text-xs text-slate-500 space-y-1">
            <div class="flex items-center justify-between text-[11px]">
              <span>Grade-A Platform</span>
              <span class="font-mono text-emerald-400">v1.2 App</span>
            </div>
            <p class="text-[10px] leading-relaxed">
              Auditing 36 Grade A Govt Exams across UPSC, Regulatory, Defense, and State PSCs.
            </p>
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import OfflineBadge from '@/components/common/OfflineBadge.vue';
import ThemeToggle from '@/components/common/ThemeToggle.vue';

const route = useRoute();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();

const isDrawerOpen = ref(false);

const appNavItems = [
  { title: 'Exam Catalog', path: '/exams', icon: '📋' },
  { title: 'Syllabus Overlap', path: '/syllabus', icon: '🔀' },
  { title: 'Profile & Eligibility', path: '/profile', icon: '👤' },
];
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