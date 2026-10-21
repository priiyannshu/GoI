<template>
  <div class="space-y-6 pb-12">
    <!-- Header & Hero Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2">
          <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-[11px] font-bold">
            M4 D3.JS SET VISUALIZATIONS
          </span>
          <span class="text-slate-500 text-xs">•</span>
          <span class="text-slate-400 text-xs">Features 18, 19, 20 & 21</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white mt-1">Universal Syllabus Overlap Explorer</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-0.5">
          Topological set intersections, bipartite force networks, and preparation carry-over analytics across 192 normalized taxonomy topics.
        </p>
      </div>

      <!-- Quick Platform Metrics -->
      <div class="flex items-center space-x-3 bg-slate-850 border border-slate-800 rounded-xl px-4 py-2 text-xs">
        <div>
          <span class="text-slate-400 block text-[10px] uppercase font-semibold">Exams</span>
          <span class="text-white font-mono font-bold text-sm">36</span>
        </div>
        <div class="w-px h-6 bg-slate-700"></div>
        <div>
          <span class="text-slate-400 block text-[10px] uppercase font-semibold">Topics</span>
          <span class="text-emerald-400 font-mono font-bold text-sm">192</span>
        </div>
        <div class="w-px h-6 bg-slate-700"></div>
        <div>
          <span class="text-slate-400 block text-[10px] uppercase font-semibold">Mappings</span>
          <span class="text-sky-400 font-mono font-bold text-sm">1,123</span>
        </div>
      </div>
    </div>

    <!-- Syllabus Sync Toolbar -->
    <SyllabusSyncToolbar />

    <!-- Main Visualizer Container -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Visualization Canvas (8 or 12 cols depending on active selection) -->
      <div :class="store.activeTopicDetail ? 'lg:col-span-8' : 'lg:col-span-12'" class="transition-all duration-300">
        <!-- Bipartite Network View -->
        <div v-if="store.activeTab === 'bipartite'">
          <BipartiteGraphView />
        </div>

        <!-- UpSet Matrix View -->
        <div v-else-if="store.activeTab === 'upset'">
          <UpsetMatrixView />
        </div>

        <!-- Dynamic Venn Diagram View (2-4 Sets) -->
        <div v-else-if="store.activeTab === 'venn'">
          <VennDiagramView />
        </div>
      </div>

      <!-- Persistent Topic Detail Panel (4 cols when active) -->
      <div v-if="store.activeTopicDetail" class="lg:col-span-4 sticky top-6">
        <TopicDetailPanel />
      </div>
    </div>

    <!-- Educational Carry-Over Efficiency Guide -->
    <div class="rounded-2xl bg-slate-850 border border-slate-800 p-6 space-y-4">
      <div class="flex items-center space-x-2">
        <span class="text-base font-bold text-white">How to Read Multi-Exam Syllabus Topologies</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-400 leading-relaxed">
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
          <span class="font-bold text-emerald-400 text-sm block">1. Natural Clustering Kernels</span>
          <p>
            The center disk of the Bipartite Network highlights high-degree topics shared across multiple services. Mastering these central topics yields disproportionate returns across all your target examinations.
          </p>
        </div>
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
          <span class="font-bold text-sky-400 text-sm block">2. Cognitive Depth Carry-Over</span>
          <p>
            Edge stroke widths encode requirement depth (1.5px Foundation to 5.0px Analytical). Preparing a topic at Analytical depth for UPSC CSE instantly satisfies Intermediate and Foundation requirements for Regulatory or State exams.
          </p>
        </div>
        <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
          <span class="font-bold text-purple-400 text-sm block">3. Cross-View Synchrony</span>
          <p>
            Selecting any region or combination in UpSet, Venn, or Network immediately syncs the active intersection across views, isolating common topics and calculating collective syllabus coverage.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useSyllabusVisualizationStore } from '@/stores/useSyllabusVisualizationStore';
import SyllabusSyncToolbar from '@/components/visualizations/SyllabusSyncToolbar.vue';
import BipartiteGraphView from '@/components/visualizations/BipartiteGraphView.vue';
import UpsetMatrixView from '@/components/visualizations/UpsetMatrixView.vue';
import VennDiagramView from '@/components/visualizations/VennDiagramView.vue';
import TopicDetailPanel from '@/components/visualizations/TopicDetailPanel.vue';

const store = useSyllabusVisualizationStore();

onMounted(async () => {
  await store.loadSyllabusData();
});
</script>
