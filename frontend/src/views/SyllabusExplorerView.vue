<template>
  <div class="space-y-6 pb-12">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Syllabus Overlap Explorer</h1>
        <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1">
          Compare audited syllabi, identify shared topics, and streamline multi-exam preparation across Grade A cadres.
        </p>
      </div>

      <!-- Quick Platform Metrics -->
      <div class="flex items-center space-x-3 bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-xl px-4 py-2 text-xs shadow-xs">
        <div>
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-semibold">Audited Exams</span>
          <span class="text-slate-900 dark:text-white font-mono font-bold text-sm">31</span>
        </div>
        <div class="w-px h-6 bg-slate-300 dark:bg-slate-700"></div>
        <div>
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-semibold">Taxonomy Topics</span>
          <span class="text-emerald-500 dark:text-emerald-400 font-mono font-bold text-sm">192</span>
        </div>
        <div class="w-px h-6 bg-slate-300 dark:bg-slate-700"></div>
        <div>
          <span class="text-slate-500 dark:text-slate-400 block text-[10px] uppercase font-semibold">Total Mappings</span>
          <span class="text-sky-500 dark:text-sky-400 font-mono font-bold text-sm">1,123</span>
        </div>
      </div>
    </div>

    <!-- Syllabus Sync Toolbar -->
    <SyllabusSyncToolbar />

    <!-- Main Visualizer Container -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Visualization Canvas (8 or 12 cols depending on active selection) -->
      <div :class="store.activeTopicDetail ? 'lg:col-span-8' : 'lg:col-span-12'" class="transition-all duration-300">
        <!-- Side-by-Side Overlap Matrix & Topics View -->
        <div v-if="store.activeTab === 'matrix'">
          <OverlapMatrixView />
        </div>

        <!-- UpSet Intersection Matrix View -->
        <div v-else-if="store.activeTab === 'upset'">
          <UpsetMatrixView />
        </div>
      </div>

      <!-- Persistent Topic Detail Panel (4 cols when active) -->
      <div v-if="store.activeTopicDetail" class="lg:col-span-4 sticky top-6">
        <TopicDetailPanel />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import SyllabusSyncToolbar from '@/components/visualizations/SyllabusSyncToolbar.vue';
import OverlapMatrixView from '@/components/visualizations/OverlapMatrixView.vue';
import UpsetMatrixView from '@/components/visualizations/UpsetMatrixView.vue';
import TopicDetailPanel from '@/components/visualizations/TopicDetailPanel.vue';

const store = useSyllabusVisualizationStore();

onMounted(async () => {
  await store.loadSyllabusData();
});
</script>
