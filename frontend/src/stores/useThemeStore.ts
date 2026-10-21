import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref<boolean>(true);

  function initTheme() {
    if (typeof window === 'undefined') return;
    const saved = localStorage.getItem('grade_a_theme');
    if (saved) {
      isDark.value = saved === 'dark';
    } else {
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    applyTheme();
  }

  function toggleTheme() {
    isDark.value = !isDark.value;
    if (typeof window !== 'undefined') {
      localStorage.setItem('grade_a_theme', isDark.value ? 'dark' : 'light');
    }
    applyTheme();
  }

  function applyTheme() {
    if (typeof document === 'undefined') return;
    if (isDark.value) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  return {
    isDark,
    initTheme,
    toggleTheme,
    applyTheme,
  };
});
