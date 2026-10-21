import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/ExamCatalogView.vue'),
    meta: { title: 'Grade-A: Audited Indian Government Examinations' },
  },
  {
    path: '/exams',
    name: 'exams',
    component: () => import('@/views/ExamCatalogView.vue'),
    alias: ['/catalog'],
    meta: { title: 'Exam Catalog (36 Grade A Posts) - Grade-A' },
  },
  {
    path: '/exams/:id',
    name: 'exam-detail',
    component: () => import('@/views/ExamDetailView.vue'),
    meta: { title: 'Examination Audit Details - Grade-A' },
  },
  {
    path: '/syllabus',
    name: 'syllabus',
    component: () => import('@/views/SyllabusExplorerView.vue'),
    meta: { title: 'Syllabus Overlap Explorer - Grade-A' },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: 'Candidate Profile & Eligibility - Grade-A' },
  },
  {
    path: '/quiz',
    redirect: '/profile',
  },
  {
    path: '/report',
    redirect: '/profile',
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
