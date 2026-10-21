<template>
  <header class="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Brand Logo -->
      <router-link to="/" class="flex items-center space-x-3 group">
        <div class="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-lg group-hover:scale-105 transition-transform">
          A
        </div>
        <div>
          <span class="font-extrabold text-lg text-white tracking-tight">Grade-A</span>
          <span class="text-xs ml-1.5 px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-medium">2027</span>
        </div>
      </router-link>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center space-x-1">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="px-3.5 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="route.path === link.path ? 'bg-slate-800 text-emerald-400 font-semibold' : 'text-slate-300 hover:text-white hover:bg-slate-800/60'"
        >
          {{ link.name }}
        </router-link>
      </nav>

      <!-- Right Controls: Status & Theme -->
      <div class="flex items-center space-x-3">
        <OfflineBadge />
        <ThemeToggle />
        
        <router-link
          to="/quiz"
          class="hidden sm:inline-flex items-center justify-center px-4 py-2 rounded-lg text-sm font-semibold bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg shadow-emerald-500/20 transition-all hover:shadow-emerald-500/40"
        >
          Check Eligibility
        </router-link>

        <!-- Mobile hamburger button -->
        <button
          @click="toggleMenu"
          class="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
          aria-label="Toggle navigation menu"
        >
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <div v-show="isMobileMenuOpen" class="md:hidden border-b border-slate-800 bg-slate-900 px-4 pt-2 pb-4 space-y-1">
      <router-link
        v-for="link in navLinks"
        :key="link.path"
        :to="link.path"
        @click="isMobileMenuOpen = false"
        class="block px-3 py-2.5 rounded-lg text-base font-medium transition-colors"
        :class="route.path === link.path ? 'bg-slate-800 text-emerald-400 font-semibold' : 'text-slate-300 hover:text-white hover:bg-slate-800'"
      >
        {{ link.name }}
      </router-link>
      <div class="pt-2">
        <router-link
          to="/quiz"
          @click="isMobileMenuOpen = false"
          class="block text-center w-full px-4 py-2.5 rounded-lg text-sm font-semibold bg-emerald-500 hover:bg-emerald-600 text-white"
        >
          Check Eligibility
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import OfflineBadge from '@/components/common/OfflineBadge.vue';
import ThemeToggle from '@/components/common/ThemeToggle.vue';

const route = useRoute();
const isMobileMenuOpen = ref(false);

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Exam Catalog', path: '/exams' },
  { name: 'Syllabus Overlap', path: '/syllabus' },
  { name: 'Eligibility Quiz', path: '/quiz' },
  { name: 'My Report', path: '/report' },
];

function toggleMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
}
</script>
