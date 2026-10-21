import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/ExamCatalogView.vue'),
    meta: { title: 'Government of India — Official Examinations Portal' },
  },
  {
    path: '/exams',
    name: 'exams',
    component: () => import('@/views/ExamCatalogView.vue'),
    alias: ['/catalog'],
    meta: { title: 'Official Examinations — Government of India' },
  },
  {
    path: '/exams/:id',
    name: 'exam-detail',
    component: () => import('@/views/ExamDetailView.vue'),
    meta: { title: 'Examination Rules & Syllabus — Government of India' },
  },
  {
    path: '/posts',
    name: 'posts',
    component: () => import('@/views/PostsView.vue'),
    meta: { title: 'Government Posts & Lifestyle — Government of India' },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { title: 'Candidate Profile & Eligibility — Government of India' },
  },
  {
    path: '/hidden',
    name: 'hidden',
    component: () => import('@/views/HiddenItemsView.vue'),
    meta: { title: 'Hidden Examinations & Posts — Government of India' },
  },
  // Syllabus Overlap Explorer hidden per user request until refined
  {
    path: '/syllabus',
    redirect: '/exams',
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
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
});

router.afterEach((to) => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title as string;
  }
});

export default router;
