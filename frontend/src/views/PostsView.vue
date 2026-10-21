<template>
  <div class="space-y-6 pb-16 max-w-full overflow-hidden">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Government Posts & Lifestyle</h1>
        <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
          Explore the exact posts, starting salaries, executive authority, and lifestyle perks resulting from the 36 audited examinations.
        </p>
      </div>

      <!-- Search Input -->
      <div class="w-full md:w-80">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by post, perk, or authority..."
          class="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500 shadow-xs"
        />
      </div>
    </div>

    <!-- Hidden Posts Banner if any hidden -->
    <div
      v-if="hiddenStore.hiddenPostsCount > 0"
      class="p-3.5 rounded-xl bg-slate-100 dark:bg-slate-850 border border-slate-200 dark:border-slate-700/80 text-xs flex items-center justify-between"
    >
      <div class="flex items-center space-x-2 text-slate-600 dark:text-slate-300">
        <span>👁️‍🗨️</span>
        <span>
          <strong>{{ hiddenStore.hiddenPostsCount }}</strong> post(s) hidden from active list.
        </span>
      </div>
      <router-link
        to="/hidden"
        class="text-xs font-bold text-emerald-600 dark:text-emerald-400 hover:underline"
      >
        View Hidden Posts →
      </router-link>
    </div>

    <!-- Universal Government Family Benefits Banner -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-xs space-y-3">
      <div class="flex items-center justify-between cursor-pointer" @click="showUniversalPerks = !showUniversalPerks">
        <div class="flex items-center space-x-2.5">
          <span class="text-xl">🏛️</span>
          <div>
            <h3 class="text-sm sm:text-base font-bold text-slate-900 dark:text-white">
              Universal Government Family Benefits (Common to All Audited Posts)
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">
              Fundamental statutory protections, healthcare, and education allowances guaranteed by the Indian Union.
            </p>
          </div>
        </div>
        <button class="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
          {{ showUniversalPerks ? 'Collapse ▲' : 'Expand Details ▼' }}
        </button>
      </div>

      <div v-if="showUniversalPerks" class="grid grid-cols-1 md:grid-cols-3 gap-3.5 pt-3 border-t border-slate-200 dark:border-slate-800 text-xs">
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-1">
          <div class="font-bold text-slate-900 dark:text-white flex items-center space-x-1.5">
            <span>👨‍👩‍👧‍👦</span>
            <span>Children's Education (CEA)</span>
          </div>
          <p class="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
            {{ COMMON_GOVERNMENT_BENEFITS.children_education.amount }}
          </p>
        </div>

        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-1">
          <div class="font-bold text-slate-900 dark:text-white flex items-center space-x-1.5">
            <span>🏥</span>
            <span>Comprehensive Medical</span>
          </div>
          <p class="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
            {{ COMMON_GOVERNMENT_BENEFITS.medical.coverage }} {{ COMMON_GOVERNMENT_BENEFITS.medical.schemes }}
          </p>
        </div>

        <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-1">
          <div class="font-bold text-slate-900 dark:text-white flex items-center space-x-1.5">
            <span>💰</span>
            <span>Assured Pension & Security</span>
          </div>
          <p class="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
            {{ COMMON_GOVERNMENT_BENEFITS.pension.details }} Article 311 job security.
          </p>
        </div>
      </div>
    </div>

    <!-- Cluster Filters -->
    <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
      <button
        v-for="c in clusters"
        :key="c.value"
        @click="selectedCluster = c.value"
        class="px-3 py-1.5 rounded-xl text-xs font-semibold transition-all shadow-xs"
        :class="
          selectedCluster === c.value
            ? 'bg-emerald-500 text-white'
            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-750 border border-slate-200 dark:border-slate-700'
        "
      >
        {{ c.label }}
      </button>
    </div>

    <!-- Posts Grid -->
    <div v-if="displayedPosts.length === 0" class="py-16 text-center text-slate-400 text-sm">
      No posts match your current search or cluster filter.
    </div>

    <div v-else class="space-y-5">
      <div
        v-for="post in displayedPosts"
        :key="post.post_id"
        class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-4 transition-all"
      >
        <!-- Post Header Row -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="space-y-1">
            <div class="flex flex-wrap items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-md text-xs font-bold font-mono bg-slate-100 dark:bg-slate-800 text-emerald-600 dark:text-emerald-400 border border-slate-200 dark:border-slate-700">
                {{ post.post_id }}
              </span>
              <span class="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                {{ post.cluster }}
              </span>
              <span class="px-2.5 py-0.5 rounded-md text-[11px] font-mono bg-sky-50 dark:bg-sky-950/30 text-sky-700 dark:text-sky-400 border border-sky-200 dark:border-sky-500/30">
                {{ post.pay_info.starting_level }}
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight break-words">
              {{ post.post_name }}
            </h2>
            <div class="text-xs text-slate-500 dark:text-slate-400 flex flex-wrap items-center gap-2">
              <span>Entry Designation: <strong class="text-slate-700 dark:text-slate-200">{{ post.designation_at_entry }}</strong></span>
              <span>•</span>
              <router-link
                :to="`/exams/${post.parent_exam_id}`"
                class="text-emerald-600 dark:text-emerald-400 font-semibold hover:underline"
              >
                via {{ post.parent_exam_title }} →
              </router-link>
            </div>
          </div>

          <!-- Actions: Hide Post Button -->
          <div class="flex items-center space-x-2 self-start sm:self-auto">
            <button
              @click="hiddenStore.togglePostHidden(post.post_id)"
              class="px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors border"
              :class="
                hiddenStore.isPostHidden(post.post_id)
                  ? 'bg-rose-500/10 text-rose-600 border-rose-500/30 hover:bg-rose-500/20'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:text-rose-600 hover:border-rose-400'
              "
              title="Hide this post"
            >
              {{ hiddenStore.isPostHidden(post.post_id) ? '👁️ Unhide' : '🚫 Hide Post' }}
            </button>
          </div>
        </div>

        <!-- Compensation Highlights Strip -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 text-xs">
          <div>
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Monthly In-Hand (Estimated)</span>
            <span class="text-base font-extrabold font-mono text-emerald-600 dark:text-emerald-400">
              ₹{{ (post.pay_info.estimated_in_hand_monthly[0] / 1000).toFixed(0) }}k – ₹{{ (post.pay_info.estimated_in_hand_monthly[1] / 1000).toFixed(0) }}k / month
            </span>
          </div>
          <div>
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Estimated Annual CTC</span>
            <span class="text-base font-extrabold font-mono text-slate-900 dark:text-white">
              ₹{{ (post.pay_info.estimated_annual_ctc[0] / 100000).toFixed(1) }} – ₹{{ (post.pay_info.estimated_annual_ctc[1] / 100000).toFixed(1) }} LPA
            </span>
          </div>
          <div>
            <span class="text-slate-500 dark:text-slate-400 block text-[11px]">Starting Basic Pay</span>
            <span class="text-base font-extrabold font-mono text-sky-600 dark:text-sky-400">
              ₹{{ post.pay_info.starting_basic.toLocaleString('en-IN') }} / mo ({{ post.pay_info.pay_system }})
            </span>
          </div>
        </div>

        <!-- Key Perks Callout Box -->
        <div v-if="post.benefits.unique_perks?.length" class="space-y-1.5">
          <span class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">🌟 Hallmark Differentiators & Unique Perks:</span>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="perk in post.benefits.unique_perks"
              :key="perk"
              class="px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50 break-words"
            >
              ✓ {{ perk }}
            </span>
          </div>
        </div>

        <!-- Expandable Deep Dives: Housing, Lifestyle & Career -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs pt-2">
          <!-- Column 1: Housing & Family Perks -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-2.5">
            <div class="flex items-center space-x-1.5 font-bold text-slate-900 dark:text-white text-xs">
              <span>🏡</span>
              <span>Housing, Medical & Family Amenities</span>
            </div>
            <div class="space-y-2 text-slate-600 dark:text-slate-300">
              <div>
                <strong class="text-slate-800 dark:text-slate-200">Accommodation:</strong>
                <p class="mt-0.5 leading-relaxed">{{ post.benefits.housing }}</p>
              </div>
              <div>
                <strong class="text-slate-800 dark:text-slate-200">Medical Coverage:</strong>
                <p class="mt-0.5 leading-relaxed">{{ post.benefits.medical }}</p>
              </div>
              <div v-if="post.benefits.ltc">
                <strong class="text-slate-800 dark:text-slate-200">Leave Travel (LTC):</strong>
                <p class="mt-0.5 leading-relaxed">{{ post.benefits.ltc }}</p>
              </div>
            </div>
          </div>

          <!-- Column 2: Hypothetical Lifestyle, Authority & Transfers -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-2.5">
            <div class="flex items-center space-x-1.5 font-bold text-slate-900 dark:text-white text-xs">
              <span>💼</span>
              <span>Lifestyle, Authority & Career Ceiling</span>
            </div>
            <div class="space-y-2 text-slate-600 dark:text-slate-300">
              <div>
                <strong class="text-slate-800 dark:text-slate-200">Work Hours & Culture:</strong>
                <p class="mt-0.5 leading-relaxed">{{ post.lifestyle.work_hours }}</p>
              </div>
              <div>
                <strong class="text-slate-800 dark:text-slate-200">Statutory Authority:</strong>
                <p class="mt-0.5 leading-relaxed">{{ post.lifestyle.authority_level }}</p>
              </div>
              <div class="flex flex-col sm:flex-row sm:items-center justify-between pt-1 border-t border-slate-200 dark:border-slate-800 gap-1 text-[11px]">
                <span>
                  <strong class="text-slate-800 dark:text-slate-200">Transfers:</strong> {{ post.lifestyle.transfer_frequency }}
                </span>
                <span class="font-bold text-emerald-600 dark:text-emerald-400">
                  Apex: {{ post.lifestyle.career_ceiling }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { AUDITED_POSTS_DATA, COMMON_GOVERNMENT_BENEFITS } from '@/data/postsData';
import { useHiddenStore } from '@/stores/useHiddenStore';

const hiddenStore = useHiddenStore();

const showUniversalPerks = ref<boolean>(false);
const selectedCluster = ref<string>('ALL');
const searchQuery = ref<string>('');

const clusters = [
  { label: 'All Posts (50+)', value: 'ALL' },
  { label: 'Central Civil', value: 'Central-Civil' },
  { label: 'Regulatory', value: 'Regulatory' },
  { label: 'Defense', value: 'Defense' },
  { label: 'State PSC', value: 'State-PSC' },
  { label: 'PSU', value: 'PSU' },
];

onMounted(() => {
  hiddenStore.loadHiddenItems();
});

const displayedPosts = computed(() => {
  let list = AUDITED_POSTS_DATA;

  // Filter out hidden posts
  list = list.filter((p) => !hiddenStore.isPostHidden(p.post_id));

  // Cluster filter
  if (selectedCluster.value !== 'ALL') {
    list = list.filter((p) => p.cluster === selectedCluster.value);
  }

  // Search filter
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim();
    list = list.filter(
      (p) =>
        p.post_name.toLowerCase().includes(q) ||
        p.post_id.toLowerCase().includes(q) ||
        p.designation_at_entry.toLowerCase().includes(q) ||
        p.parent_exam_title.toLowerCase().includes(q) ||
        p.benefits.housing.toLowerCase().includes(q) ||
        p.lifestyle.authority_level.toLowerCase().includes(q)
    );
  }

  return list;
});
</script>
