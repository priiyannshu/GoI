<template>
  <transition name="splash-fade">
    <div
      v-if="isVisible"
      class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-slate-950 text-white select-none overflow-hidden"
    >
      <!-- Atmospheric Backdrop Ambient Lighting -->
      <div class="absolute inset-0 pointer-events-none overflow-hidden">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] bg-emerald-500/15 rounded-full blur-[130px] animate-pulse"></div>
        <div class="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-cyan-500/10 rounded-full blur-[90px]"></div>
        
        <!-- SFIIL Signature Accent Gradient Top Edge Bar -->
        <div class="absolute top-0 left-0 right-0 h-1 sfiil-gradient-bar"></div>
      </div>

      <!-- Main Central Content -->
      <div class="relative z-10 flex flex-col items-center text-center px-6 max-w-md w-full">
        <!-- Enlarged Central Icon matching the app icon alongside Govt. of India -->
        <div class="relative group mb-7">
          <!-- Outer Radiant Ring -->
          <div class="absolute -inset-4 rounded-3xl bg-gradient-to-tr from-emerald-500/30 via-emerald-400/20 to-teal-400/30 blur-xl opacity-80 animate-pulse"></div>
          
          <!-- Iconic Container (Enlarged version of the 🏛️ icon container) -->
          <div class="relative w-32 h-32 sm:w-36 sm:h-36 rounded-3xl bg-emerald-500/15 border-2 border-emerald-400/40 shadow-2xl shadow-emerald-950/80 flex items-center justify-center p-6 backdrop-blur-md transition-transform transform hover:scale-105 duration-300">
            <!-- Emulated Classical Building Emblem matching the icon -->
            <AppEmblem class="w-full h-full drop-shadow-[0_10px_20px_rgba(16,185,129,0.35)]" />
          </div>

          <!-- Official Portal Badge Pill -->
          <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-slate-900 border border-emerald-500/40 text-[10px] font-mono tracking-widest text-emerald-300 uppercase shadow-md flex items-center gap-1.5 whitespace-nowrap">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Official Portal</span>
          </div>
        </div>

        <!-- Heading: 'Govt. of India' in Elegant Cursive Font -->
        <div class="space-y-2 mt-2">
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 via-white to-emerald-300 font-goi-cursive drop-shadow-[0_4px_16px_rgba(16,185,129,0.3)]">
            Govt. of India
          </h1>
          <p class="text-xs sm:text-sm font-medium tracking-wider text-slate-400 uppercase font-sans">
            Audited Grade A Examinations & Cadres
          </p>
        </div>

        <!-- Bottom Loading Indicator / Status -->
        <div class="mt-12 flex flex-col items-center space-y-3 w-48">
          <div class="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-300 rounded-full animate-splash-progress"></div>
          </div>
          <span class="text-[11px] font-mono text-slate-500 tracking-wider">
            Initializing Intelligence System...
          </span>
        </div>
      </div>

      <!-- Quick Dismiss for Instant User Interaction -->
      <button
        @click="dismissSplash"
        class="absolute bottom-6 text-xs text-slate-500 hover:text-slate-300 transition-colors uppercase tracking-widest font-mono py-1 px-3 rounded-lg hover:bg-slate-900/60"
      >
        Skip [Enter]
      </button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AppEmblem from '@/components/common/AppEmblem.vue';

const isVisible = ref(true);

const dismissSplash = () => {
  isVisible.value = false;
};

onMounted(() => {
  // Key listener to skip on any keypress or touch
  const handleKey = (e: KeyboardEvent) => {
    if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') {
      dismissSplash();
    }
  };
  window.addEventListener('keydown', handleKey);

  // Automatic gentle transition after initialization
  const timer = setTimeout(() => {
    dismissSplash();
  }, 1400);

  return () => {
    window.removeEventListener('keydown', handleKey);
    clearTimeout(timer);
  };
});
</script>

<style scoped>
.splash-fade-enter-active,
.splash-fade-leave-active {
  transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.splash-fade-enter-from,
.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}

@keyframes splash-progress {
  0% {
    width: 0%;
    margin-left: 0%;
  }
  50% {
    width: 75%;
    margin-left: 15%;
  }
  100% {
    width: 100%;
    margin-left: 0%;
  }
}

.animate-splash-progress {
  animation: splash-progress 1.3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
</style>
