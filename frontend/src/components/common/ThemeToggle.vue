<template>
  <div class="relative inline-flex items-center">
    <!-- SFIIL Theme Cycle Button -->
    <button
      id="btnCycleTheme"
      @click="themeStore.cycleTheme"
      class="group inline-flex items-center space-x-2 px-3 py-1.5 rounded-xl border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[var(--accent)]/50"
      :class="buttonThemeClasses"
      title="Switch Theme (Neon / Paper / AMOLED)"
      aria-label="Switch Theme (Neon / Paper / AMOLED)"
    >
      <!-- Active Theme Icon -->
      <span class="text-sm transform group-hover:rotate-12 transition-transform duration-200">
        {{ themeStore.currentThemeMeta.icon }}
      </span>

      <!-- Theme Name Badge -->
      <span class="text-xs font-bold tracking-wide font-mono">
        {{ themeStore.currentThemeMeta.name }}
      </span>

      <!-- Rotating Cycle Icon -->
      <svg
        class="w-3.5 h-3.5 opacity-60 group-hover:opacity-100 group-hover:rotate-180 transition-all duration-300"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
        />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useThemeStore } from '@/stores/useThemeStore';

const themeStore = useThemeStore();

const buttonThemeClasses = computed(() => {
  switch (themeStore.currentTheme) {
    case 'theme-paper':
      return 'bg-[#eae0ce] hover:bg-[#e0d5c1] text-[#2a231b] border-[#d8c8af] shadow-xs';
    case 'theme-amoled':
      return 'bg-[#141414] hover:bg-[#1e1e1e] text-[#00e5ff] border-[#222222] shadow-xs shadow-cyan-950/30';
    case 'theme-neon':
    default:
      return 'bg-[#21262d] hover:bg-[#292e36] text-[#58d4f5] border-[#30363d] shadow-xs shadow-sky-950/30';
  }
});
</script>
