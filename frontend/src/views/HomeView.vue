<template>
  <div class="space-y-12 py-4">
    <!-- Hero Section -->
    <section class="text-center max-w-3xl mx-auto space-y-4">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
        <span>Offline-First PWA</span>
        <span>•</span>
        <span>2027 Examination Intelligence</span>
      </div>
      <h1 class="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
        Master All Indian <span class="text-emerald-400">Grade A</span> Government Examinations
      </h1>
      <p class="text-slate-400 text-base sm:text-lg">
        Multi-dimensional eligibility profiling, universal syllabus ontology, and interactive D3.js overlap visualizations spanning Central, Financial, State PSC, and PSU cadres.
      </p>

      <div class="flex flex-wrap items-center justify-center gap-4 pt-4">
        <router-link
          to="/quiz"
          class="px-6 py-3 rounded-lg font-semibold bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg shadow-emerald-500/25 transition-all hover:scale-105"
        >
          Evaluate My 2027 Eligibility
        </router-link>
        <router-link
          to="/syllabus"
          class="px-6 py-3 rounded-lg font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all hover:border-slate-600"
        >
          Explore Syllabus Matrix
        </router-link>
        <router-link
          to="/exams"
          class="px-6 py-3 rounded-lg font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all hover:border-slate-600"
        >
          Browse 36 Exams
        </router-link>
      </div>
    </section>

    <!-- Cluster Cards Grid -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="p-6 rounded-xl bg-slate-850 border border-slate-800 space-y-2">
        <div class="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 font-bold">
          C1
        </div>
        <h2 class="text-lg font-bold text-white">Central & Uniformed</h2>
        <p class="text-sm text-slate-400">8 Exams: UPSC CSE, ESE, IFoS, CAPF AC, CDS, AFCAT, CGSE, IES/ISS.</p>
      </div>

      <div class="p-6 rounded-xl bg-slate-850 border border-slate-800 space-y-2">
        <div class="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
          C2
        </div>
        <h2 class="text-lg font-bold text-white">Financial & Regulatory</h2>
        <p class="text-sm text-slate-400">7 Bodies: RBI Gr B, SEBI Gr A, NABARD, IFSCA, PFRDA, SIDBI, EXIM MT.</p>
      </div>

      <div class="p-6 rounded-xl bg-slate-850 border border-slate-800 space-y-2">
        <div class="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 font-bold">
          C3
        </div>
        <h2 class="text-lg font-bold text-white">State PSC Commissions</h2>
        <p class="text-sm text-slate-400">10 States: UPPSC, BPSC, MPSC, MPPSC, RPSC, TNPSC, APPSC, TSPSC, WBPSC, KPSC.</p>
      </div>

      <div class="p-6 rounded-xl bg-slate-850 border border-slate-800 space-y-2">
        <div class="w-10 h-10 rounded-lg bg-pink-500/10 border border-pink-500/30 flex items-center justify-center text-pink-400 font-bold">
          C4
        </div>
        <h2 class="text-lg font-bold text-white">PSU Executive Trainees</h2>
        <p class="text-sm text-slate-400">11 Maharatna/Navratna PSUs via GATE disciplines & BARC OCES.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useExamMasterStore } from '@/stores/useExamMasterStore';

const examStore = useExamMasterStore();
</script>
