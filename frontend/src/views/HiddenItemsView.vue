<template>
  <div class="space-y-6 pb-16 max-w-full overflow-hidden">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Hidden Examinations & Posts</h1>
      </div>

      <!-- Quick Restore All Actions -->
      <div v-if="hiddenStore.totalHiddenCount > 0" class="flex items-center space-x-2">
        <button
          @click="hiddenStore.unhideAll()"
          class="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-600 text-white shadow-xs transition-colors"
        >
          Restore All Items ({{ hiddenStore.totalHiddenCount }})
        </button>
      </div>
    </div>

    <!-- Tab Switcher -->
    <div class="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1 border border-slate-200 dark:border-slate-700/80 self-start sm:self-auto w-fit">
      <button
        @click="activeTab = 'exams'"
        class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5"
        :class="activeTab === 'exams' ? 'bg-emerald-500 text-white shadow' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
      >
        <span>📋 Hidden Examinations</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200">
          {{ hiddenStore.hiddenExamsCount }}
        </span>
      </button>

      <button
        @click="activeTab = 'posts'"
        class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5"
        :class="activeTab === 'posts' ? 'bg-emerald-500 text-white shadow' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
      >
        <span>🏛️ Hidden Posts & Cadres</span>
        <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200">
          {{ hiddenStore.hiddenPostsCount }}
        </span>
      </button>
    </div>

    <!-- TAB 1: HIDDEN EXAMINATIONS -->
    <div v-if="activeTab === 'exams'" class="space-y-4">
      <div v-if="hiddenExamsList.length === 0" class="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-2">
        <span class="text-3xl block">👁️</span>
        <h3 class="text-base font-bold text-slate-900 dark:text-white">No Examinations Currently Hidden</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 max-w-md mx-auto">
          When browsing the Exam Catalog, you can click the '🚫 Hide' button on any examination that you are definitely not eligible for or not interested in.
        </p>
        <div class="pt-2">
          <router-link to="/exams" class="inline-block px-4 py-2 rounded-xl text-xs font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">
            Browse Exam Catalog →
          </router-link>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="exam in hiddenExamsList"
          :key="exam.exam_id"
          class="p-4 rounded-xl bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-800 shadow-xs flex flex-col justify-between space-y-3"
        >
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-slate-800 dark:text-white">{{ exam.short_code }}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                {{ exam.category }}
              </span>
            </div>

            <h4 class="text-sm font-bold text-slate-900 dark:text-white leading-snug break-words">
              {{ exam.title }}
            </h4>

            <p class="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">
              {{ exam.description }}
            </p>
          </div>

          <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <button
              @click="hiddenStore.unhideExam(exam.exam_id)"
              class="px-3 py-1 rounded-lg text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 transition-colors"
            >
              👁️ Restore Visibility
            </button>
            <router-link
              :to="`/exams/${exam.exam_id}`"
              class="text-xs text-slate-500 hover:text-slate-900 dark:hover:text-white underline"
            >
              Inspect →
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: HIDDEN POSTS -->
    <div v-else-if="activeTab === 'posts'" class="space-y-4">
      <div v-if="hiddenPostsList.length === 0" class="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-2">
        <span class="text-3xl block">🏛️</span>
        <h3 class="text-base font-bold text-slate-900 dark:text-white">No Career Posts Currently Hidden</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 max-w-md mx-auto">
          In the Posts & Lifestyle section, you can click '🚫 Hide Post' on any cadre or designation you wish to filter out of your active career options.
        </p>
        <div class="pt-2">
          <router-link to="/posts" class="inline-block px-4 py-2 rounded-xl text-xs font-bold bg-emerald-500 text-white hover:bg-emerald-600 transition-colors">
            Explore Government Posts →
          </router-link>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="post in hiddenPostsList"
          :key="post.post_id"
          class="p-4 rounded-xl bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-800 shadow-xs flex flex-col justify-between space-y-3"
        >
          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-emerald-600 dark:text-emerald-400">{{ post.post_id }}</span>
              <span class="text-[11px] text-slate-500 dark:text-slate-400">{{ post.cluster }}</span>
            </div>

            <h4 class="text-sm font-bold text-slate-900 dark:text-white leading-snug break-words">
              {{ post.post_name }}
            </h4>

            <div class="text-xs text-slate-600 dark:text-slate-400">
              Entry: <strong>{{ post.designation_at_entry }}</strong>
            </div>

            <div class="text-xs font-mono text-emerald-600 dark:text-emerald-400 font-bold">
              ₹{{ (post.pay_info.estimated_annual_ctc[0] / 100000).toFixed(1) }} – ₹{{ (post.pay_info.estimated_annual_ctc[1] / 100000).toFixed(1) }} LPA
            </div>
          </div>

          <div class="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <button
              @click="hiddenStore.unhidePost(post.post_id)"
              class="px-3 py-1 rounded-lg text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 transition-colors"
            >
              👁️ Restore Visibility
            </button>
            <router-link
              :to="`/exams/${post.parent_exam_id}`"
              class="text-xs text-slate-500 hover:text-slate-900 dark:hover:text-white underline"
            >
              View Exam →
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useHiddenStore } from '@/stores/useHiddenStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { AUDITED_POSTS_DATA, GovernmentPost } from '@/data/postsData';
import type { ExamRecord } from '@/types/profile';

const hiddenStore = useHiddenStore();
const examStore = useExamMasterStore();

const activeTab = ref<'exams' | 'posts'>('exams');

onMounted(async () => {
  hiddenStore.loadHiddenItems();
  await examStore.loadExams();
});

const hiddenExamsList = computed<ExamRecord[]>(() => {
  return hiddenStore.hiddenExamIds
    .map((id) => examStore.examsMap[id])
    .filter(Boolean) as ExamRecord[];
});

const hiddenPostsList = computed<GovernmentPost[]>(() => {
  const postsMap = new Map<string, GovernmentPost>();
  for (const p of AUDITED_POSTS_DATA) {
    postsMap.set(p.post_id, p);
  }
  return hiddenStore.hiddenPostIds
    .map((id) => postsMap.get(id))
    .filter(Boolean) as GovernmentPost[];
});
</script>
