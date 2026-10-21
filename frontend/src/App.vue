<template>
  <div class="min-h-screen flex flex-col app-root transition-colors duration-200 max-w-full overflow-x-hidden">
    <AppHeader />
    
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 min-w-0">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive include="ProfileView,ExamCatalogView,PostsView,HiddenItemsView">
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
import { useHiddenStore } from '@/stores/useHiddenStore';

const themeStore = useThemeStore();
const examStore = useExamMasterStore();
const hiddenStore = useHiddenStore();

onMounted(async () => {
  themeStore.initTheme();
  hiddenStore.loadHiddenItems();
  await examStore.loadExams();
});
</script>
