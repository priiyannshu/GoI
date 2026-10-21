import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'Grade-A: Indian Government Examinations Intelligence Platform' },
  },
  {
    path: '/exams',
    name: 'exams',
    component: () => import('@/views/ExamCatalogView.vue'),
    alias: ['/catalog'],
    meta: { title: 'Exam Catalog (36 Grade A Posts) - Grade-A' },
  },
  {
    path: '/syllabus',
    name: 'syllabus',
    component: () => import('@/views/SyllabusExplorerView.vue'),
    meta: { title: 'Universal Syllabus Overlap Explorer - Grade-A' },
  },
  {
    path: '/quiz',
    name: 'quiz',
    component: () => import('@/views/ProfileQuizView.vue'),
    meta: { title: 'Eligibility Profile Intake Quiz - Grade-A' },
  },
  {
    path: '/report',
    name: 'report',
    component: () => import('@/views/EligibilityReportView.vue'),
    meta: { title: 'Statutory Eligibility Report Card - Grade-A' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition;
    return { top: 0 };
  },
});

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }
});

export default router;
