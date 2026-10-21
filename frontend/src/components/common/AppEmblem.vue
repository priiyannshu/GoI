<template>
  <div class="w-full h-full flex items-center justify-center select-none" :class="wrapperClass">
    <!-- Classical Government Architecture Emblem (🏛️) -->
    <svg
      :viewBox="viewBox"
      class="w-full h-full overflow-visible"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <filter id="sky-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="8" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <linearGradient id="emblem-roof-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38BDF8" />
          <stop offset="100%" stop-color="#0284C7" />
        </linearGradient>
        <linearGradient id="emblem-col-grad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#38BDF8" />
          <stop offset="50%" stop-color="#0284C7" />
          <stop offset="100%" stop-color="#0369A1" />
        </linearGradient>
      </defs>

      <!-- Pediment Roof Triangle -->
      <path
        d="M120 16 L228 78 L12 78 Z"
        fill="url(#emblem-roof-grad)"
        stroke="#38BDF8"
        stroke-width="5"
        stroke-linejoin="round"
      />
      <!-- Circular Rose Window / Seal in Tympanum -->
      <circle cx="120" cy="54" r="11" fill="#0F172A" stroke="#38BDF8" stroke-width="3.5" />
      <circle cx="120" cy="54" r="4" fill="#38BDF8" />

      <!-- Architrave / Entablature below triangle -->
      <rect x="14" y="82" width="212" height="18" rx="4" fill="#38BDF8" />
      
      <!-- 4 Majestic Columns with fluted details -->
      <!-- Column 1 -->
      <rect x="22" y="104" width="40" height="9" rx="2" fill="#38BDF8" />
      <rect x="28" y="113" width="28" height="90" rx="4" fill="url(#emblem-col-grad)" />
      <line x1="37" y1="116" x2="37" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="47" y1="116" x2="47" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round" />
      <rect x="22" y="203" width="40" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 2 -->
      <rect x="78" y="104" width="40" height="9" rx="2" fill="#38BDF8" />
      <rect x="84" y="113" width="28" height="90" rx="4" fill="url(#emblem-col-grad)" />
      <line x1="93" y1="116" x2="93" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="103" y1="116" x2="103" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round" />
      <rect x="78" y="203" width="40" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 3 -->
      <rect x="134" y="104" width="40" height="9" rx="2" fill="#38BDF8" />
      <rect x="140" y="113" width="28" height="90" rx="4" fill="url(#emblem-col-grad)" />
      <line x1="149" y1="116" x2="149" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="159" y1="116" x2="159" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round" />
      <rect x="134" y="203" width="40" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 4 -->
      <rect x="190" y="104" width="40" height="9" rx="2" fill="#38BDF8" />
      <rect x="196" y="113" width="28" height="90" rx="4" fill="url(#emblem-col-grad)" />
      <line x1="205" y1="116" x2="205" y2="200" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round" />
      <line x1="215" y1="116" x2="215" y2="200" stroke="#0369A1" stroke-width="2.5" stroke-linecap="round" />
      <rect x="190" y="203" width="40" height="9" rx="2" fill="#38BDF8" />

      <!-- Stepped Stylobate / Base -->
      <rect x="10" y="214" width="220" height="14" rx="4" fill="#38BDF8" />
      <rect x="0" y="230" width="240" height="16" rx="4" fill="#0284C7" />
    </svg>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    wrapperClass?: string;
    viewBox?: string;
  }>(),
  {
    wrapperClass: '',
    viewBox: '0 0 240 250',
  }
);
</script>
