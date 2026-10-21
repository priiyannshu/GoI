<template>
  <div class="min-h-screen flex flex-col bg-slate-900 text-slate-100 transition-colors duration-200">
    <AppHeader />
    
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive include="ProfileQuizView,SyllabusExplorerView">
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppHeader from '@/components/common/AppHeader.vue';
import AppFooter from '@/components/common/AppFooter.vue';
import { useThemeStore } from '@/stores/useThemeStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';

const themeStore = useThemeStore();
const examStore = useExamMasterStore();

onMounted(async () => {
  themeStore.initTheme();
  // Preload exam data into cache
  await examStore.loadExams();
});
</script>
