<template>
  <div
    class="flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-colors"
    :class="isOnline ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'"
    :title="isOnline ? 'Connected to edge API' : 'Operating in offline cache mode'"
  >
    <span class="w-2 h-2 rounded-full animate-pulse" :class="isOnline ? 'bg-emerald-400' : 'bg-amber-400'"></span>
    <span>{{ isOnline ? 'Online' : 'Offline' }}</span>
  </div>
</template>

<script setup lang="ts">
import { useOnline } from '@vueuse/core';

const isOnline = useOnline();
</script>
