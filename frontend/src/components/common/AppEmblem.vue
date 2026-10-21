<template>
  <div class="w-full h-full flex items-center justify-center select-none" :class="wrapperClass">
    <!-- Perfectly Symmetrical Classical Government Architecture Emblem (🏛️) in Sky Blue -->
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

      <!-- Pediment Roof Triangle (Apex at 120, 16; Symmetrical base 12 to 228) -->
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

      <!-- Architrave / Entablature below triangle (Symmetrical 12 to 228) -->
      <rect x="12" y="82" width="216" height="18" rx="4" fill="#38BDF8" />
      
      <!-- 4 Majestic Columns with Fluted Details (Mathematically Symmetrical Spacing) -->
      <!-- Column 1 (Center: 39) -->
      <rect x="21" y="104" width="36" height="9" rx="2" fill="#38BDF8" />
      <rect x="26" y="113" width="26" height="90" rx="3" fill="url(#emblem-col-grad)" />
      <line x1="34" y1="116" x2="34" y2="200" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="44" y1="116" x2="44" y2="200" stroke="#0369A1" stroke-width="2" stroke-linecap="round" />
      <rect x="21" y="203" width="36" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 2 (Center: 93) -->
      <rect x="75" y="104" width="36" height="9" rx="2" fill="#38BDF8" />
      <rect x="80" y="113" width="26" height="90" rx="3" fill="url(#emblem-col-grad)" />
      <line x1="88" y1="116" x2="88" y2="200" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="98" y1="116" x2="98" y2="200" stroke="#0369A1" stroke-width="2" stroke-linecap="round" />
      <rect x="75" y="203" width="36" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 3 (Center: 147) -->
      <rect x="129" y="104" width="36" height="9" rx="2" fill="#38BDF8" />
      <rect x="134" y="113" width="26" height="90" rx="3" fill="url(#emblem-col-grad)" />
      <line x1="142" y1="116" x2="142" y2="200" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="152" y1="116" x2="152" y2="200" stroke="#0369A1" stroke-width="2" stroke-linecap="round" />
      <rect x="129" y="203" width="36" height="9" rx="2" fill="#38BDF8" />

      <!-- Column 4 (Center: 201) -->
      <rect x="183" y="104" width="36" height="9" rx="2" fill="#38BDF8" />
      <rect x="188" y="113" width="26" height="90" rx="3" fill="url(#emblem-col-grad)" />
      <line x1="196" y1="116" x2="196" y2="200" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" />
      <line x1="206" y1="116" x2="206" y2="200" stroke="#0369A1" stroke-width="2" stroke-linecap="round" />
      <rect x="183" y="203" width="36" height="9" rx="2" fill="#38BDF8" />

      <!-- Stepped Stylobate / Base (Symmetrical 10 to 230 and 0 to 240) -->
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
