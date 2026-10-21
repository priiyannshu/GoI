<template>
  <div class="relative inline-flex items-center">
    <!-- SFIIL Theme Cycle Button (Icon Only) -->
    <button
      id="btnCycleTheme"
      @click="themeStore.cycleTheme"
      class="group inline-flex items-center justify-center p-2 rounded-xl border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[var(--accent)]/50"
      :class="buttonThemeClasses"
      title="Switch Theme"
      aria-label="Switch Theme"
    >
      <!-- Active Theme Emoji Icon -->
      <span class="text-base leading-none transform group-hover:scale-110 transition-transform duration-200">
        {{ themeStore.currentThemeMeta.icon }}
      </span>
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
