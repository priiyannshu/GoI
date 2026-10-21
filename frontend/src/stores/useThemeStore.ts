import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export type AppTheme = 'theme-neon' | 'theme-paper' | 'theme-amoled';

export interface ThemeOption {
  id: AppTheme;
  name: string;
  description: string;
  icon: string;
  metaColor: string;
}

export const THEMES: ThemeOption[] = [
  {
    id: 'theme-neon',
    name: 'Neon',
    description: 'Cyberpunk dark mode with electric cyan & purple accents',
    icon: '⚡',
    metaColor: '#0d1117',
  },
  {
    id: 'theme-paper',
    name: 'Paper',
    description: 'High-readability warm parchment paper with deep teal accents',
    icon: '📜',
    metaColor: '#fbf7ee',
  },
  {
    id: 'theme-amoled',
    name: 'AMOLED',
    description: 'Pure pitch-black deep OLED background with vibrant neon cyan',
    icon: '🌑',
    metaColor: '#000000',
  },
];

export const useThemeStore = defineStore('theme', () => {
  const currentTheme = ref<AppTheme>('theme-neon');

  const isDark = computed<boolean>(() => currentTheme.value !== 'theme-paper');

  const currentThemeMeta = computed<ThemeOption>(() => {
    return THEMES.find((t) => t.id === currentTheme.value) || THEMES[0];
  });

  function initTheme() {
    if (typeof window === 'undefined') return;

    const saved =
      localStorage.getItem('sfiil_theme') ||
      localStorage.getItem('goi_theme') ||
      localStorage.getItem('grade_a_theme');

    if (saved === 'theme-neon' || saved === 'theme-paper' || saved === 'theme-amoled') {
      currentTheme.value = saved as AppTheme;
    } else if (saved === 'light') {
      currentTheme.value = 'theme-paper';
    } else if (saved === 'dark') {
      currentTheme.value = 'theme-neon';
    } else {
      currentTheme.value = 'theme-neon';
    }

    applyTheme();
  }

  function cycleTheme() {
    const currentIndex = THEMES.findIndex((t) => t.id === currentTheme.value);
    const nextIndex = (currentIndex + 1) % THEMES.length;
    setTheme(THEMES[nextIndex].id);
  }

  function toggleTheme() {
    cycleTheme();
  }

  function setTheme(theme: AppTheme) {
    currentTheme.value = theme;
    if (typeof window !== 'undefined') {
      localStorage.setItem('sfiil_theme', theme);
      localStorage.setItem('goi_theme', theme);
    }
    applyTheme();
  }

  function applyTheme() {
    if (typeof document === 'undefined') return;

    const root = document.documentElement;
    const body = document.body;

    // Clean old theme classes
    THEMES.forEach((t) => {
      root.classList.remove(t.id);
      body.classList.remove(t.id);
    });

    // Add active theme class
    root.classList.add(currentTheme.value);
    body.classList.add(currentTheme.value);

    // Dark/light mode alignment for Tailwind darkMode: 'class'
    if (currentTheme.value === 'theme-paper') {
      root.classList.remove('dark');
      root.style.colorScheme = 'light';
    } else {
      root.classList.add('dark');
      root.style.colorScheme = 'dark';
    }

    // Dynamic browser & PWA theme-color meta tag
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', currentThemeMeta.value.metaColor);
    }
  }

  return {
    currentTheme,
    isDark,
    currentThemeMeta,
    THEMES,
    initTheme,
    cycleTheme,
    toggleTheme,
    setTheme,
    applyTheme,
  };
});
