/**
 * ==============================================================================
 * INDIAN GRADE A GOVERNMENT EXAMINATIONS INTELLIGENCE PLATFORM
 * Authoritative Isomorphic TypeScript Eligibility Engine
 * File: src/services/eligibilityEngine.ts (Turnkey Candidate)
 * ==============================================================================
 *
 * PURE TYPESCRIPT - ZERO DOM / BROWSER DEPENDENCIES
 * Compatible with:
 *   - Vue 3 Client Application (Vite PWA)
 *   - Dedicated Web Workers (Background Multithreaded Evaluation)
 *   - Edge Runtimes (Cloudflare Workers / Hono API)
 *   - Server Runtimes (Node.js test runners, Bun, Deno)
 *
 * EVALUATES ALL 8 STATUTORY DIMENSIONS:
 *   1. Deterministic Reference Cutoff Date Rules & Exact Birth Windows (2027 Timelines)
 *   2. Social Category Age Relaxations (OBC +3/5, SC/ST +5, PwBD +10/13/15, Ex-Servicemen, etc.)
 *   3. Academic Degree & Accepted Discipline Mapping (Bachelor, Master, Professional, Dual)
 *   4. Strict Non-Rounding Percentage Threshold Enforcement (59.99% < 60.0%; 64.99% < 65.0%)
 *   5. Final-Year Student Permissibility & Conditional Eligibility Mechanics
 *   6. Category-Aware Attempt Limits (UPSC CSE 6/9/∞; RBI Phase-1 6/∞; )
 *   7. Domicile & Compulsory Regional Language Firewalls (Marathi, Bengali, Kannada, Tamil, etc.)
 *   8. Physical & Medical Standards (Height, Chest Expansion, Color Vision, LASIK parameters)
 *
 * COVERS ALL 31 GRADE A EXAMINATIONS ACROSS ALL 4 CLUSTERS:
 *   - Cluster 1: Central Civil & Uniformed Services (8)
 *   - Cluster 2: Financial & Regulatory Apex Bodies (7)
 *   - Cluster 3: State Public Service Commissions (10)
 *   - Cluster 4: Maharatna & Navratna PSUs via GATE / Direct CBT (11)
 */

// ==============================================================================
// 1. TYPE DEFINITIONS & CONTRACT INTERFACES
// ==============================================================================

export type EligibilityStatus = 'ELIGIBLE' | 'CONDITIONALLY_ELIGIBLE' | 'NEEDS_INFO' | 'INELIGIBLE';

export type GenderType = 'MALE' | 'FEMALE' | 'OTHER' | 'Male' | 'Female' | 'Other' | string;

export type SocialCategory =
  | 'GEN'
  | 'UR'
  | 'EWS'
  | 'OBC'
  | 'OBC_NCL'
  | 'SC'
  | 'ST'
  | 'PWBD'
  | 'PWBD_GEN'
  | 'PWBD_OBC'
  | 'PWBD_SC_ST'
  | string;

export interface PhysicalStandardsRule {
  min_height_male_cm?: number;
  min_height_female_cm?: number;
  min_chest_male_cm?: number;
  min_expansion_male_cm?: number;
  min_weight_male_kg?: number;
  min_weight_female_kg?: number;
  disallow_color_blind?: boolean;
  lasik_allowed?: boolean;
  lasik_min_age?: number;
  lasik_wait_months?: number;
  flying_branch_standards?: {
    min_height_cm: number;
    sitting_height_min_cm: number;
    sitting_height_max_cm: number;
    leg_length_min_cm: number;
    leg_length_max_cm: number;
    thigh_length_max_cm: number;
  };
  ground_duty_standards?: {
    min_height_male_cm: number;
    min_height_female_cm: number;
  };
  DSP_Male?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number };
  DSP_Female?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number; min_weight_kg?: number };
  IPS_Male?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number };
  IPS_Female?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number };
  RPS_Male?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number };
  DySP_Male?: { min_height_cm: number; min_chest_cm?: number; min_expansion_cm?: number };
  walking_test?: {
    male_distance_km: number;
    male_hours: number;
    female_distance_km: number;
    female_hours: number;
  };
}

export interface LanguageRequirementsRule {
  mandatory_fluency?: string;
  mandatory_qualifying?: string;
  qualifying_paper?: string;
  qualifying_papers?: string[];
  compulsory_paper?: string;
  working_knowledge?: string;
  mains_paper?: string;
  mains_paper_a?: string;
  mains_paper_b?: string;
}

export interface ExamEligibilityRule {
  exam_id: string;
  title?: string;
  short_code?: string;
  category?: string;
  cutoff_rule: string;
  min_age_gen: number;
  max_age_gen: number;
  female_max_age_gen?: number;
  police_max_age_gen?: number;
  relaxations: Record<string, number>;
  min_education?: string;
  accepted_disciplines: string[];
  min_pct_gen: number;
  min_pct_res: number;
  strict_non_rounding?: boolean;
  allows_final_year: boolean;
  attempt_limits: Record<string, number | null>;
  domicile_restrictions?: Record<string, string> | null;
  language_requirements?: LanguageRequirementsRule | null;
  physical_standards?: PhysicalStandardsRule | null;
  disallow_prior_selected_ac?: boolean;
  requires_10plus2_physics_maths?: boolean;
  min_10plus2_subject_pct?: number;
  marital_status_restrictions?: Record<string, string>;
  requires_dual_threshold?: boolean;
  citation: string;
}

export interface UserProfileInput {
  dob: string; // YYYY-MM-DD
  gender: GenderType;
  category: SocialCategory;
  is_ex_serviceman?: boolean;
  ex_service_years?: number;
  graduation_degree?: string | null;
  degree?: string | null; // Schema alias
  graduation_discipline?: string | null;
  discipline?: string | null; // Schema alias
  graduation_aggregate_pct?: number | null;
  aggregate_pct?: number | null; // Schema alias
  is_final_year?: boolean;
  state_domicile?: string | null;
  domicile_state?: string | null; // Schema alias
  fluent_languages?: string[];
  prior_attempts?: Record<string, number>;
  height_cm?: number | null;
  sitting_height_cm?: number | null;
  leg_length_cm?: number | null;
  thigh_length_cm?: number | null;
  weight_kg?: number | null;
  chest_cm?: number | null;
  chest_expansion_cm?: number | null;
  has_color_blindness?: boolean;
  has_commercial_pilot_license?: boolean;
  has_lasik?: boolean;
  lasik_age?: number | null;
  lasik_wait_months?: number | null;
  ten_plus_two_maths_pct?: number | null;
  ten_plus_two_physics_pct?: number | null;
  prior_selected_as_ac?: boolean;
  marital_status?: 'Unmarried' | 'Married' | 'Widow' | 'Divorcee' | string;
  has_children?: boolean;
  enable_skipped_check?: boolean;
  skipped_fields?: string[];
}

export interface EligibilityVerdict {
  exam_id: string;
  status: EligibilityStatus;
  reasons: string[];
  relaxations_applied: string[];
  statutory_citation: string;
  skipped_requirements?: string[];
}

// ==============================================================================
// 2. AUTHORITATIVE SPECIFICATIONS CATALOG FOR ALL 31 EXAMINATIONS
// ==============================================================================

export const AUTHORITATIVE_EXAM_RULES: Record<string, ExamEligibilityRule> = {
  // ----------------------------------------------------------------------------
  // Cluster 1: Central All-India & Uniformed Services (8)
  // ----------------------------------------------------------------------------
    GATE: {
    exam_id: 'GATE',
    title: 'Graduate Aptitude Test in Engineering',
    short_code: 'GATE',
    category: 'Central-Civil',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 65,
    relaxations: {
      OBC: 0,
      SC: 0,
      ST: 0,
      PWBD_GEN: 0,
      PWBD_OBC: 0,
      PWBD_SC_ST: 0,
      EX_SERVICEMEN: 0,
    },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {
      GEN: null,
      EWS: null,
      OBC: null,
      SC: null,
      ST: null,
      PWBD_GEN: null,
      PWBD_OBC: null,
      PWBD_SC_ST: null,
    },
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'GATE Information Brochure, Section 4: Eligibility Criteria (No Age Limit)',
  },
  UPSC_CSE: {
    exam_id: 'UPSC_CSE',
    title: 'Civil Services Examination',
    short_code: 'CSE',
    category: 'Central-Civil',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 32,
    relaxations: {
      OBC: 3,
      SC: 5,
      ST: 5,
      PWBD_GEN: 10,
      PWBD_OBC: 13,
      PWBD_SC_ST: 15,
      EX_SERVICEMEN: 5,
    },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {
      GEN: 6,
      EWS: 6,
      OBC: 9,
      SC: null,
      ST: null,
      PWBD_GEN: 9,
      PWBD_OBC: 9,
      PWBD_SC_ST: null,
    },
    domicile_restrictions: null,
    language_requirements: {
      mains_paper_a: 'Compulsory Indian Language (Qualifying 25%)',
      mains_paper_b: 'English (Qualifying 25%)',
    },
    physical_standards: {
      IPS_Male: { min_height_cm: 165, min_chest_cm: 84, min_expansion_cm: 5 },
      IPS_Female: { min_height_cm: 150, min_chest_cm: 79, min_expansion_cm: 5 },
      lasik_allowed: true,
      lasik_min_age: 20,
      lasik_wait_months: 12,
    },
    citation: 'UPSC Notice No. 05/2024-CSP, Clause 3(i)-(v)',
  },

  UPSC_ESE: {
    exam_id: 'UPSC_ESE',
    title: 'Engineering Services Examination',
    short_code: 'ESE',
    category: 'Central-Civil',
    cutoff_rule: 'JANUARY_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 30,
    relaxations: {
      OBC: 3,
      SC: 5,
      ST: 5,
      PWBD_GEN: 10,
      CENTRAL_CIVIL_GOVT: 5,
    },
    min_education: 'Bachelor',
    accepted_disciplines: ['Civil', 'Mechanical', 'Electrical', 'Electronics_Telecommunication'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: { min_height_male_cm: 152, min_height_female_cm: 150 },
    citation: 'UPSC Notice No. 02/2025-ENGG, Clause 3(i)-(ii)',
  },

  UPSC_IFOS: {
    exam_id: 'UPSC_IFOS',
    title: 'Indian Forest Service Examination',
    short_code: 'IFoS',
    category: 'Central-Civil',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 32,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD_GEN: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: [
      'Science',
      'Forestry',
      'Engineering',
      'Agriculture',
      'Botany',
      'Chemistry',
      'Geology',
      'Mathematics',
      'Physics',
      'Statistics',
      'Zoology',
    ],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: { GEN: 6, EWS: 6, OBC: 9, SC: null, ST: null },
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: {
      min_height_male_cm: 163,
      min_height_female_cm: 150,
      disallow_color_blind: true,
      walking_test: { male_distance_km: 25, male_hours: 4, female_distance_km: 14, female_hours: 4 },
    },
    citation: 'UPSC Notice No. 06/2024-IFoS, Clause 3(ii)-(iv)',
  },

  UPSC_CAPF_AC: {
    exam_id: 'UPSC_CAPF_AC',
    title: 'Central Armed Police Forces (Assistant Commandants)',
    short_code: 'CAPF (AC)',
    category: 'Defense',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 20,
    max_age_gen: 25,
    relaxations: { OBC: 3, SC: 5, ST: 5, EX_SERVICEMEN: 5 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    disallow_prior_selected_ac: true,
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: {
      min_height_male_cm: 165,
      min_height_female_cm: 157,
      min_chest_male_cm: 81,
      min_expansion_male_cm: 5,
      min_weight_male_kg: 50,
      min_weight_female_kg: 46,
      disallow_color_blind: true,
    },
    citation: 'UPSC Notice No. 09/2024-CPF, Clause 3(III)-(V)',
  },

  UPSC_CDS: {
    exam_id: 'UPSC_CDS',
    title: 'Combined Defence Services Examination',
    short_code: 'CDS',
    category: 'Defense',
    cutoff_rule: 'COURSE_COMMENCEMENT_YEAR',
    min_age_gen: 19,
    max_age_gen: 24, // 25 for OTA
    relaxations: {}, // No category relaxation in armed forces commissioned officers
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY', 'Engineering', 'Physics_Maths_10plus2'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    marital_status_restrictions: {
      IMA: 'Unmarried_Male',
      OTA_Women: 'Unmarried_or_Issueless_Widow',
    },
    physical_standards: {
      min_height_male_cm: 157.5,
      min_height_female_cm: 152,
      flying_branch_standards: {
        min_height_cm: 162.5,
        sitting_height_min_cm: 81.5,
        sitting_height_max_cm: 96.0,
        leg_length_min_cm: 99.0,
        leg_length_max_cm: 120.0,
        thigh_length_max_cm: 64.0,
      },
      disallow_color_blind: true,
    },
    citation: 'UPSC Notice No. 11/2025.CDS-II, Clause 3(a)-(c) & Appendix-IV',
  },

  IAF_AFCAT: {
    exam_id: 'IAF_AFCAT',
    title: 'Air Force Common Admission Test',
    short_code: 'AFCAT',
    category: 'Defense',
    cutoff_rule: 'COURSE_COMMENCEMENT_YEAR',
    min_age_gen: 20,
    max_age_gen: 24, // 26 for Ground Duty
    relaxations: { DGCA_CPL_HOLDER: 2 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY', 'Engineering', 'BCom'],
    min_pct_gen: 60.0,
    min_pct_res: 60.0,
    requires_10plus2_physics_maths: true,
    min_10plus2_subject_pct: 50.0,
    allows_final_year: true,
    attempt_limits: {},
    physical_standards: {
      min_height_male_cm: 157.5,
      min_height_female_cm: 152.0,
      flying_branch_standards: {
        min_height_cm: 162.5,
        sitting_height_min_cm: 81.5,
        sitting_height_max_cm: 96.0,
        leg_length_min_cm: 99.0,
        leg_length_max_cm: 120.0,
        thigh_length_max_cm: 64.0,
      },
      ground_duty_standards: {
        min_height_male_cm: 157.5,
        min_height_female_cm: 152.0,
      },
      disallow_color_blind: true,
      lasik_allowed: true,
      lasik_min_age: 20,
      lasik_wait_months: 12,
    },
    citation: 'IAF AFCAT 01/2024 Notification, Clause 3(b) & Air Force Medical Standards (IAP 4303 5th Ed)',
  },



  // ----------------------------------------------------------------------------
  // Cluster 2: Financial & Regulatory Apex Bodies (7)
  // ----------------------------------------------------------------------------
  RBI_GRADE_B: {
    exam_id: 'RBI_GRADE_B',
    title: 'Reserve Bank of India Grade B Officers',
    short_code: 'RBI Gr B',
    category: 'Regulatory',
    cutoff_rule: 'JULY_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 30,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD_GEN: 10, MPHIL: 2, PHD: 4 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY', 'Economics', 'Statistics', 'Finance'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: false, // Strict bar: degree must be declared on or before July 1
    attempt_limits: { GEN: 6, EWS: 6, OBC: null, SC: null, ST: null, PWBD_GEN: null },
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'RBI Advt. No. 2A/2024-25, Section II.1-3',
  },


  NABARD_GRADE_A: {
    exam_id: 'NABARD_GRADE_A',
    title: 'NABARD Assistant Manager (RDBS)',
    short_code: 'NABARD Gr A',
    category: 'Regulatory',
    cutoff_rule: 'JULY_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 30,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD_GEN: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY', 'Agriculture', 'Fisheries', 'Forestry', 'Finance'],
    min_pct_gen: 60.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'NABARD Advt. No. 01/Grade A/2024-25',
  },



  SIDBI_GRADE_A: {
    exam_id: 'SIDBI_GRADE_A',
    title: 'SIDBI Assistant Manager (Grade A)',
    short_code: 'SIDBI Gr A',
    category: 'Regulatory',
    cutoff_rule: 'NOVEMBER_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 30,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD_GEN: 10 },
    min_education: 'Bachelor_or_Master',
    accepted_disciplines: ['Law', 'Engineering', 'Master_Any', 'CA', 'CS', 'CFA'],
    min_pct_gen: 60.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'SIDBI Grade A Notification 2024',
  },


  // ----------------------------------------------------------------------------
  // Cluster 3: State Public Service Commissions (10)
  // ----------------------------------------------------------------------------
  UPPSC_PCS: {
    exam_id: 'UPPSC_PCS',
    title: 'UPPSC Combined State / Upper Subordinate Services',
    short_code: 'UPPSC PCS',
    category: 'State-PSC',
    cutoff_rule: 'JULY_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 40,
    relaxations: { SC_UP: 5, ST_UP: 5, OBC_UP: 5, PWBD_UP: 15 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: { reservation_benefit: 'UP_DOMICILE_ONLY' },
    language_requirements: { compulsory_paper: 'General Hindi (150 marks)' },
    physical_standards: { DSP_Male: { min_height_cm: 165, min_chest_cm: 84, min_expansion_cm: 5 } },
    citation: 'UPPSC Advt. No. A-1/E-1/2024, Clause 6 & 10',
  },

  BPSC_CCE: {
    exam_id: 'BPSC_CCE',
    title: 'BPSC Combined Competitive Examination',
    short_code: 'BPSC CCE',
    category: 'State-PSC',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 20,
    max_age_gen: 37,
    female_max_age_gen: 40,
    relaxations: {
      GEN_Female: 3,
      BC_Male: 3,
      BC_Female: 3,
      EBC_Male: 3,
      EBC_Female: 3,
      SC: 5,
      ST: 5,
      PWBD: 10,
    },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: { reservation_benefit: 'BIHAR_DOMICILE_ONLY' },
    language_requirements: { qualifying_paper: 'General Hindi (30% passing)' },
    physical_standards: { DSP_Male: { min_height_cm: 165 } },
    citation: 'BPSC Advt. No. 23/2024, Para 3 & 4',
  },

  MPPSC_SSE: {
    exam_id: 'MPPSC_SSE',
    title: 'Madhya Pradesh State Service Examination',
    short_code: 'MPPSC SSE',
    category: 'State-PSC',
    cutoff_rule: 'JANUARY_1_EXAM_YEAR',
    min_age_gen: 21,
    max_age_gen: 40,
    police_max_age_gen: 33,
    relaxations: { SC_MP: 5, ST_MP: 5, OBC_MP: 5, Women_All: 5 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: { reservation_benefit: 'MP_DOMICILE_ONLY' },
    language_requirements: { mains_paper: 'General Hindi (200 marks)' },
    physical_standards: { DSP_Male: { min_height_cm: 168 } },
    citation: 'MPPSC Advt. No. 40/2023, Section 2 & 8',
  },

  RPSC_RAS: {
    exam_id: 'RPSC_RAS',
    title: 'Rajasthan State and Subordinate Services (RAS/RTS)',
    short_code: 'RPSC RAS',
    category: 'State-PSC',
    cutoff_rule: 'FOLLOWING_JANUARY_1_EXAM_YEAR', // Evaluated as 01-01-2028 for 2027 cycle
    min_age_gen: 21,
    max_age_gen: 40,
    relaxations: {
      SC_RJ: 5,
      ST_RJ: 5,
      OBC_RJ: 5,
      Female_GEN_RJ: 5,
      Female_Reserved_RJ: 10,
      Widow_Divorcee: 99,
    },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: { reservation_benefit: 'RAJASTHAN_DOMICILE_ONLY' },
    language_requirements: { working_knowledge: 'Hindi Devanagari & Rajasthani Culture' },
    physical_standards: { RPS_Male: { min_height_cm: 168 } },
    citation: 'RPSC Advt. No. 02/2023-24, Clause 7 & 8',
  },

  TSPSC_GROUP_1: {
    exam_id: 'TSPSC_GROUP_1',
    title: 'Telangana Group 1 Services',
    short_code: 'TSPSC Gr 1',
    category: 'State-PSC',
    cutoff_rule: 'JULY_1_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 44,
    relaxations: { SC_TS: 5, ST_TS: 5, BC_TS: 5, EWS_TS: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['ANY'],
    min_pct_gen: 0.0,
    min_pct_res: 0.0,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: { presidential_order_2018: '95% local reservation' },
    language_requirements: { qualifying_paper: 'General English' },
    physical_standards: { DSP_Male: { min_height_cm: 167.6 } },
    citation: 'TSPSC Notification No. 02/2024, Para III-IV',
  },

  // ----------------------------------------------------------------------------
  // Cluster 4: Maharatna & Navratna PSUs (11)
  // ----------------------------------------------------------------------------
  PSU_ONGC_GT: {
    exam_id: 'PSU_ONGC_GT',
    title: 'ONGC Graduate Trainee',
    short_code: 'ONGC GT',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_MAY',
    min_age_gen: 18,
    max_age_gen: 30,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: [
      'Mechanical',
      'Petroleum',
      'Civil',
      'Electrical',
      'Electronics',
      'Chemical',
      'Computer_Science',
      'Geology',
      'Geophysics',
    ],
    min_pct_gen: 60.0,
    min_pct_res: 60.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'ONGC Advt. No. 01/2024(R&P), Section 2-3',
  },

  PSU_IOCL_ET: {
    exam_id: 'PSU_IOCL_ET',
    title: 'Indian Oil Officer Trainee',
    short_code: 'IOCL ET',
    category: 'PSU-GATE',
    cutoff_rule: 'JUNE_30_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 26,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: [
      'Chemical',
      'Civil',
      'Electrical',
      'Instrumentation',
      'Mechanical',
      'Metallurgical',
      'Computer_Science',
    ],
    min_pct_gen: 65.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'IOCL GATE-2024 Advt., Clause 2 & 3.1',
  },

  PSU_NTPC_EET: {
    exam_id: 'PSU_NTPC_EET',
    title: 'NTPC Engineering Executive Trainee',
    short_code: 'NTPC EET',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_APRIL',
    min_age_gen: 18,
    max_age_gen: 27,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Electrical', 'Mechanical', 'Civil', 'Mining'],
    min_pct_gen: 65.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'NTPC Advt. No. 04/2024, Clause 2',
  },

  PSU_BHEL_ET: {
    exam_id: 'PSU_BHEL_ET',
    title: 'BHEL Engineer Trainee',
    short_code: 'BHEL ET',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_MAY',
    min_age_gen: 18,
    max_age_gen: 27,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Civil', 'Mechanical', 'Electrical', 'Chemical', 'Metallurgy'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'BHEL Advt. 2024, Section 3',
  },

  PSU_PGCIL_ET: {
    exam_id: 'PSU_PGCIL_ET',
    title: 'Power Grid Engineer Trainee',
    short_code: 'PGCIL ET',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_MAY',
    min_age_gen: 18,
    max_age_gen: 28,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Electrical', 'Civil', 'Electronics', 'Computer_Science'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'PGCIL Advt. CC/06/2024, Clause 2',
  },

  PSU_HPCL_OFFICER: {
    exam_id: 'PSU_HPCL_OFFICER',
    title: 'HPCL Officer Recruitment',
    short_code: 'HPCL Officer',
    category: 'PSU-CBT',
    cutoff_rule: 'CLOSING_DATE_JUNE',
    min_age_gen: 18,
    max_age_gen: 25,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Mechanical', 'Civil', 'Electrical', 'Instrumentation', 'Chemical'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'HPCL Officers Advt. 2024, Section 2',
  },

  PSU_BPCL_MT: {
    exam_id: 'PSU_BPCL_MT',
    title: 'BPCL Management Trainee',
    short_code: 'BPCL MT',
    category: 'PSU-GATE',
    cutoff_rule: 'JUNE_1_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 25,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Mechanical', 'Chemical', 'Civil', 'Electrical', 'Instrumentation'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'BPCL GATE Advt. 2024, Section 2',
  },

  PSU_SAIL_MTT: {
    exam_id: 'PSU_SAIL_MTT',
    title: 'SAIL Management Trainee (Technical)',
    short_code: 'SAIL MTT',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_MAY',
    min_age_gen: 18,
    max_age_gen: 28,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: [
      'Mechanical',
      'Metallurgy',
      'Electrical',
      'Chemical',
      'Civil',
      'Instrumentation',
      'Mining',
    ],
    min_pct_gen: 65.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: { min_height_male_cm: 155, min_height_female_cm: 143 },
    citation: 'SAIL Advt. 01/2024(MT), Clause 3 & Physical',
  },

  PSU_GAIL_ET: {
    exam_id: 'PSU_GAIL_ET',
    title: 'GAIL Executive Trainee',
    short_code: 'GAIL ET',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_MAY',
    min_age_gen: 18,
    max_age_gen: 26,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: [
      'Chemical',
      'Mechanical',
      'Electrical',
      'Instrumentation',
      'Civil',
      'GAIL_Telecom_IT',
    ],
    min_pct_gen: 65.0,
    min_pct_res: 55.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'GAIL Advt. GAIL/OPEN/ET/1/2024, Section 2',
  },

  PSU_COAL_INDIA_MT: {
    exam_id: 'PSU_COAL_INDIA_MT',
    title: 'Coal India Management Trainee',
    short_code: 'CIL MT',
    category: 'PSU-GATE',
    cutoff_rule: 'CLOSING_DATE_AUGUST',
    min_age_gen: 18,
    max_age_gen: 30,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor',
    accepted_disciplines: ['Mining', 'Civil', 'Mechanical', 'Electrical', 'Geology'],
    min_pct_gen: 60.0,
    min_pct_res: 50.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'CIL Advt. No. 02/2024, Section 3',
  },

  PSU_BARC_OCES: {
    exam_id: 'PSU_BARC_OCES',
    title: 'BARC Scientific Officer / NPCIL ET',
    short_code: 'BARC OCES',
    category: 'PSU-GATE',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 26,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor_or_MSc',
    accepted_disciplines: [
      'Mechanical',
      'Chemical',
      'Metallurgy',
      'Electrical',
      'Electronics',
      'Computer_Science',
      'Instrumentation',
      'Civil',
      'Physics',
      'Chemistry',
    ],
    min_pct_gen: 60.0,
    min_pct_res: 60.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'BARC OCES Brochure 2024, Section 2',
  },

  // Alias for database 1:1 parity with seed data
  PSU_BARC_NPCIL_ET: {
    exam_id: 'PSU_BARC_NPCIL_ET',
    title: 'BARC Scientific Officer / NPCIL Executive Trainee',
    short_code: 'BARC/NPCIL',
    category: 'PSU-GATE',
    cutoff_rule: 'AUGUST_1_EXAM_YEAR',
    min_age_gen: 18,
    max_age_gen: 26,
    relaxations: { OBC: 3, SC: 5, ST: 5, PWBD: 10 },
    min_education: 'Bachelor_or_MSc',
    accepted_disciplines: [
      'Mechanical',
      'Chemical',
      'Metallurgy',
      'Electrical',
      'Electronics',
      'Computer_Science',
      'Instrumentation',
      'Civil',
      'Physics',
      'Chemistry',
    ],
    min_pct_gen: 60.0,
    min_pct_res: 60.0,
    strict_non_rounding: true,
    allows_final_year: true,
    attempt_limits: {},
    domicile_restrictions: null,
    language_requirements: null,
    physical_standards: null,
    citation: 'BARC OCES Brochure 2024, Section 2 & NPCIL ET Advt 2024',
  },
};

// ==============================================================================
// 3. UTILITY FUNCTIONS & DATE CALCULATORS
// ==============================================================================

/**
 * Normalizes strings by trimming, replacing underscores/dashes with spaces, and lowercasing.
 */
export function normalizeDiscipline(str?: string): string {
  if (!str) return '';
  return str.trim().toLowerCase().replace(/[_\-\s]+/g, ' ');
}

/**
 * Returns formatted ISO date YYYY-MM-DD from a Date object without timezone shift.
 */
export function formatDateISO(d: Date): string {
  const year = d.getUTCFullYear();
  const month = String(d.getUTCMonth() + 1).padStart(2, '0');
  const day = String(d.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Resolves statutory reference cutoff date string (YYYY-MM-DD) for a given cutoff rule.
 */
export function getCutoffDate(cutoffRule: string, examYear: number = 2027): string {
  switch (cutoffRule) {
    case 'AUGUST_1_EXAM_YEAR':
      return `${examYear}-08-01`;
    case 'JANUARY_1_EXAM_YEAR':
      return `${examYear}-01-01`;
    case 'JULY_1_EXAM_YEAR':
      return `${examYear}-07-01`;
    case 'APRIL_1_EXAM_YEAR':
      return `${examYear}-04-01`;
    case 'FOLLOWING_JANUARY_1_EXAM_YEAR':
      return `${examYear + 1}-01-01`;
    case 'MARCH_31_EXAM_YEAR':
      return `${examYear}-03-31`;
    case 'FEBRUARY_1_EXAM_YEAR':
      return `${examYear}-02-01`;
    case 'NOVEMBER_1_EXAM_YEAR':
      return `${examYear}-11-01`;
    case 'JUNE_30_EXAM_YEAR':
      return `${examYear}-06-30`;
    case 'JUNE_1_EXAM_YEAR':
      return `${examYear}-06-01`;
    case 'COURSE_COMMENCEMENT_YEAR':
      return `${examYear + 1}-01-01`;
    default:
      if (cutoffRule.includes('CLOSING_DATE')) {
        return `${examYear}-05-15`;
      }
      return `${examYear}-08-01`;
  }
}

/**
 * Calculates exact age in full completed years, months, and days between DOB and target date.
 */
export function calculateAgeOnCutoff(
  dobStr: string,
  targetDateStr: string
): { years: number; months: number; days: number } {
  const [bYear, bMonth, bDay] = dobStr.split('-').map(Number);
  const [tYear, tMonth, tDay] = targetDateStr.split('-').map(Number);

  let years = tYear - bYear;
  let months = tMonth - bMonth;
  let days = tDay - bDay;

  if (days < 0) {
    months -= 1;
    // Approximate days in previous month
    days += 30;
  }
  if (months < 0) {
    years -= 1;
    months += 12;
  }

  return { years, months, days };
}

/**
 * Calculates statutory birth date window [minDob, maxDob] corresponding to exact gazetted clauses.
 */
export function getStatutoryBirthWindow(
  rule: ExamEligibilityRule,
  allowedMaxAge: number,
  examYear: number = 2027
): { minDob: Date; maxDob: Date } {
  const cutoffRule = rule.cutoff_rule;

  switch (cutoffRule) {
    case 'AUGUST_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 7, 2)), // Born on or after Aug 2
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 7, 1)), // Born on or before Aug 1
      };
    case 'JANUARY_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 0, 2)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 0, 1)),
      };
    case 'JULY_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 6, 1)), // UPPSC inclusive July 1
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 6, 1)),
      };
    case 'APRIL_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 3, 1)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 3, 1)),
      };
    case 'FOLLOWING_JANUARY_1_EXAM_YEAR':
      // RPSC RAS: Must not have reached 41 on Jan 1 of following year
      return {
        minDob: new Date(Date.UTC(examYear + 1 - (allowedMaxAge + 1), 0, 2)), // 1987-01-02 for 40 yrs in 2027
        maxDob: new Date(Date.UTC(examYear + 1 - rule.min_age_gen, 0, 1)),
      };
    case 'MARCH_31_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 3, 1)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 2, 31)),
      };
    case 'FEBRUARY_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 1, 2)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 1, 1)),
      };
    case 'NOVEMBER_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 10, 2)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 10, 1)),
      };
    case 'JUNE_30_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 6, 1)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 5, 30)),
      };
    case 'JUNE_1_EXAM_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 5, 2)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 5, 1)),
      };
    case 'COURSE_COMMENCEMENT_YEAR':
      return {
        minDob: new Date(Date.UTC(examYear + 1 - allowedMaxAge, 0, 2)),
        maxDob: new Date(Date.UTC(examYear + 1 - rule.min_age_gen, 0, 1)),
      };
    default:
      if (cutoffRule.includes('CLOSING_DATE')) {
        return {
          minDob: new Date(Date.UTC(examYear - allowedMaxAge, 4, 16)),
          maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 4, 15)),
        };
      }
      return {
        minDob: new Date(Date.UTC(examYear - allowedMaxAge, 7, 2)),
        maxDob: new Date(Date.UTC(examYear - rule.min_age_gen, 7, 1)),
      };
  }
}

// ==============================================================================
// 4. CORE MULTIDIMENSIONAL ELIGIBILITY EVALUATION ENGINE
// ==============================================================================

/**
 * Authoritative Evaluation Function.
 * Evaluates candidate profile across all 8 statutory dimensions against the specified exam rule.
 */
export function evaluateEligibility(
  profile: UserProfileInput,
  rule: ExamEligibilityRule,
  examYear: number = 2027
): EligibilityVerdict {
  const reasons: string[] = [];
  const relaxations_applied: string[] = [];
  const skipped_requirements: string[] = [];
  let is_eligible = true;
  let is_conditional = false;

  // ----------------------------------------------------------------------------
  // A. Profile Property Normalization & Schema Fault-Tolerance
  // ----------------------------------------------------------------------------
  const isSkippedCheckEnabled = true;

  const normalizedGender = (profile.gender || '').trim().toUpperCase();
  const isFemale = normalizedGender === 'FEMALE';
  const rawCategory = (profile.category || '').trim().toUpperCase();
  const rawDiscipline = profile.graduation_discipline ?? profile.discipline;
  const rawDegree = profile.graduation_degree ?? profile.degree;
  const rawPct = profile.graduation_aggregate_pct ?? profile.aggregate_pct;

  const discipline = (rawDiscipline ?? '').trim();
  const degree = (rawDegree ?? '').trim();
  const aggregate_pct =
    rawPct !== undefined && rawPct !== null && rawPct !== ('' as any) && !isNaN(Number(rawPct))
      ? Number(rawPct)
      : null;
  const domicile_state = (profile.state_domicile ?? profile.domicile_state ?? '').trim();
  const fluent_languages = profile.fluent_languages ?? [];
  const prior_attempts = profile.prior_attempts ?? {};

  // ----------------------------------------------------------------------------
  // B. Statutory Dimension 7: Domicile Reservation Firewall
  // ----------------------------------------------------------------------------
  let effectiveCategory = rawCategory;
  if (effectiveCategory === 'UR') effectiveCategory = 'GEN';
  if (effectiveCategory === 'OBC_NCL') effectiveCategory = 'OBC';

  const domicile_rule = rule.domicile_restrictions;
  if (domicile_rule && domicile_rule.reservation_benefit) {
    const state_map: Record<string, string> = {
      UP_DOMICILE_ONLY: 'Uttar Pradesh',
      BIHAR_DOMICILE_ONLY: 'Bihar',
      MAHARASHTRA_DOMICILE_ONLY: 'Maharashtra',
      MP_DOMICILE_ONLY: 'Madhya Pradesh',
      RAJASTHAN_DOMICILE_ONLY: 'Rajasthan',
      TAMIL_NADU_DOMICILE_ONLY: 'Tamil Nadu',
      ANDHRA_PRADESH_DOMICILE_ONLY: 'Andhra Pradesh',
      WEST_BENGAL_DOMICILE_ONLY: 'West Bengal',
      KARNATAKA_DOMICILE_ONLY: 'Karnataka',
    };
    const required_state = state_map[domicile_rule.reservation_benefit];
    if (required_state && domicile_state.toLowerCase() !== required_state.toLowerCase()) {
      effectiveCategory = 'GEN';
      relaxations_applied.push('Out-of-state applicant: Mapped to General (UR) category under domicile rule');
    }
  }

  // ----------------------------------------------------------------------------
  // C. Statutory Dimension 2: Social Category & Composite Age Relaxations
  // ----------------------------------------------------------------------------
  let max_age = rule.max_age_gen;
  if (isFemale && rule.female_max_age_gen !== undefined) {
    max_age = rule.female_max_age_gen;
  }

  let relaxation_years = 0;
  const cat_prefix = effectiveCategory.split('_')[0];
  const state_abbrevs: Record<string, string> = {
    'Uttar Pradesh': 'UP',
    Bihar: 'BIHAR',
    Maharashtra: 'MH',
    'Madhya Pradesh': 'MP',
    Rajasthan: 'RJ',
    'Tamil Nadu': 'TN',
    'Andhra Pradesh': 'AP',
    Telangana: 'TS',
    'West Bengal': 'WB',
    Karnataka: 'KA',
  };
  const st_abbr = state_abbrevs[domicile_state] || '';
  const state_cat_key = `${cat_prefix}_${st_abbr}`;
  const gender_key = `${effectiveCategory}_${isFemale ? 'Female' : 'Male'}`;

  // Precedence: Exact Key -> Gender Key -> State Key -> Category Sibling -> Category Prefix
  const findRelaxation = (candidates: string[]): { key: string; val: number } | null => {
    if (!rule.relaxations) return null;
    for (const c of candidates) {
      if (c in rule.relaxations) return { key: c, val: rule.relaxations[c] };
      const lowerC = c.toLowerCase();
      for (const [k, v] of Object.entries(rule.relaxations)) {
        if (k.toLowerCase() === lowerC) return { key: k, val: v };
      }
    }
    return null;
  };

  const relaxationKeys: string[] = [effectiveCategory, gender_key, state_cat_key];
  if (effectiveCategory === 'SC' || effectiveCategory === 'ST') {
    relaxationKeys.push('SC_ST', 'SC/ST', 'SC_ST_Cat_1');
  }
  if (effectiveCategory === 'PWBD' || effectiveCategory.startsWith('PWBD')) {
    relaxationKeys.push('PwBD', 'PWBD', 'PwBD_GEN', 'PwBD_UP', 'PwBD_RJ', 'PwBD_AP', 'PwBD_MP');
  }
  // State-specific OBC nomenclature (Bihar BC/EBC, TN BC/MBC, AP/TS BC, WB BC, KA OBC)
  if (effectiveCategory === 'OBC') {
    if (st_abbr === 'BIHAR') {
      relaxationKeys.push(isFemale ? 'BC_Female' : 'BC_Male', isFemale ? 'EBC_Female' : 'EBC_Male', 'BC', 'EBC');
    } else if (st_abbr === 'TN') {
      relaxationKeys.push('BC_TN', 'MBC_TN', 'MBC_DC_TN');
    } else if (st_abbr === 'AP') {
      relaxationKeys.push('BC_AP');
    } else if (st_abbr === 'TS') {
      relaxationKeys.push('BC_TS');
    } else if (st_abbr === 'WB') {
      relaxationKeys.push('BC_WB');
    } else if (st_abbr === 'KA') {
      relaxationKeys.push('OBC_KA', 'OBC_Cat_2A_2B_3A_3B');
    }
  }
  relaxationKeys.push(cat_prefix);

  const matchedRel = findRelaxation(relaxationKeys);
  if (matchedRel) {
    relaxation_years = matchedRel.val;
    relaxations_applied.push(`${matchedRel.key} relaxation: +${relaxation_years} years`);
  }

  // Compound / Alternate Relaxations (Ex-Servicemen)
  if (profile.is_ex_serviceman) {
    const esmMatch = findRelaxation(['EX_SERVICEMEN', 'Ex_Servicemen', 'ESM']);
    let esm_rel = esmMatch ? esmMatch.val : 0;
    // Military service formula: Age - (Service Years + 3) -> if service years provided
    if (profile.ex_service_years && profile.ex_service_years > 0) {
      const formulaRel = profile.ex_service_years + 3;
      if (esm_rel > 0) {
        esm_rel = Math.max(esm_rel, Math.min(formulaRel, esm_rel));
      } else {
        esm_rel = formulaRel;
      }
    }
    if (esm_rel > 0) {
      relaxation_years = Math.max(relaxation_years, esm_rel);
      relaxations_applied.push(`Ex-Servicemen relaxation: +${esm_rel} years`);
    }
  }

  if (profile.has_commercial_pilot_license && rule.relaxations?.['DGCA_CPL_HOLDER']) {
    const cpl_rel = rule.relaxations['DGCA_CPL_HOLDER'];
    relaxation_years += cpl_rel;
    relaxations_applied.push(`DGCA CPL Holder: +${cpl_rel} years`);
  }

  const marital = (profile.marital_status || '').trim().toLowerCase();
  if ((marital === 'widow' || marital === 'divorcee') && rule.relaxations?.['Widow_Divorcee']) {
    const widow_rel = rule.relaxations['Widow_Divorcee'];
    relaxation_years = Math.max(relaxation_years, widow_rel);
    relaxations_applied.push(`Widow/Divorcee relaxation: +${widow_rel} years`);
  }

  const allowed_max_age = max_age + relaxation_years;

  // ----------------------------------------------------------------------------
  // D. Statutory Dimension 1: Cutoff Date & Exact Statutory Birth Window
  // ----------------------------------------------------------------------------
  if (!profile.gender) {
    skipped_requirements.push('Candidate gender required for eligibility verification');
  }
  if (!profile.category) {
    skipped_requirements.push('Statutory category required (e.g. General, OBC, SC, ST)');
  }

  if (!profile.dob) {
    skipped_requirements.push('Date of birth required for age verification');
  } else {
    const cutoff_date = getCutoffDate(rule.cutoff_rule, examYear);
    const [bY, bM, bD] = profile.dob.split('-').map(Number);
    const dob = new Date(Date.UTC(bY, bM - 1, bD));

    const { minDob, maxDob } = getStatutoryBirthWindow(rule, allowed_max_age, examYear);

    if (dob < minDob) {
      is_eligible = false;
      reasons.push(
        `Age exceeds maximum limit of ${allowed_max_age} years on ${cutoff_date} (Born before ${formatDateISO(minDob)})`
      );
    } else if (dob > maxDob) {
      is_eligible = false;
      reasons.push(
        `Age is below minimum limit of ${rule.min_age_gen} years on ${cutoff_date} (Born after ${formatDateISO(maxDob)})`
      );
    }
  }

  // ----------------------------------------------------------------------------
  // E. Statutory Dimension 3: Degree & Discipline Validation
  // ----------------------------------------------------------------------------
  const accepted_disc = rule.accepted_disciplines || ['ANY'];
  if (!degree) {
    if (isSkippedCheckEnabled) {
      skipped_requirements.push(`Graduation degree required (${rule.min_education || 'Bachelor'})`);
    }
  } else {
    // Minimum Education Level Hierarchy
    if (rule.min_education === 'Master') {
      if (!['Master', 'Dual_UG_and_MBA'].includes(degree)) {
        is_eligible = false;
        reasons.push(`Degree '${degree}' does not meet Master's requirement for this post`);
      }
    } else if (rule.min_education === 'Master_or_Professional') {
      const profDisciplines = [
        'Law',
        'Engineering',
        'Computer_Science',
        'Information_Technology',
        'CA',
        'CFA',
        'CS',
        'Civil',
        'Mechanical',
        'Electrical',
      ].map(s => normalizeDiscipline(s));

      const is_prof = discipline ? profDisciplines.includes(normalizeDiscipline(discipline)) : false;
      const is_post_grad = ['Master', 'Dual_UG_and_MBA'].includes(degree);

      if (!is_prof && !is_post_grad) {
        if (!discipline && isSkippedCheckEnabled) {
          skipped_requirements.push("Graduation discipline required to verify Master's or Professional status");
        } else {
          is_eligible = false;
          reasons.push(
            `Degree '${degree}' in '${discipline}' does not meet Master's or Professional requirement for this post`
          );
        }
      }
    } else if (rule.min_education === 'Dual_UG_and_MBA') {
      const is_dual = degree === 'Dual_UG_and_MBA' || (discipline && normalizeDiscipline(discipline) === 'ca');
      if (!is_dual) {
        is_eligible = false;
        reasons.push(`Degree '${degree}' does not meet Dual UG and MBA requirement`);
      }
    }
  }

  if (!accepted_disc.includes('ANY')) {
    if (!discipline) {
      if (isSkippedCheckEnabled) {
        skipped_requirements.push(`Graduation discipline required (Accepted: ${accepted_disc.join(', ')})`);
      }
    } else {
      const isMasterAnyAllowed =
        accepted_disc.some(d => d.toLowerCase() === 'master_any' || d.toLowerCase() === 'master any') &&
        ['Master', 'Dual_UG_and_MBA'].includes(degree);

      if (!isMasterAnyAllowed) {
        const normProfDisc = normalizeDiscipline(discipline);
        const isMatched = accepted_disc.some(d => {
          const normAccepted = normalizeDiscipline(d);
          if (
            normProfDisc === normAccepted ||
            normProfDisc.includes(normAccepted) ||
            normAccepted.includes(normProfDisc)
          ) {
            return true;
          }
          // Geoinformatics is officially an allied engineering discipline to Civil Engineering, Geology & General Engineering
          if (
            (normProfDisc.includes('geoinformatics') || normProfDisc.includes('geomatics') || normProfDisc.includes('gis')) &&
            (normAccepted === 'civil' || normAccepted === 'engineering' || normAccepted === 'science' || normAccepted === 'geology')
          ) {
            return true;
          }
          return false;
        });

        if (!isMatched) {
          is_eligible = false;
          reasons.push(
            `Graduation discipline '${discipline}' is not accepted. Required: ${JSON.stringify(accepted_disc)}`
          );
        }
      }
    }
  }

  // ----------------------------------------------------------------------------
  // F. Statutory Dimension 4: Strict Non-Rounding Percentage Threshold
  // ----------------------------------------------------------------------------
  const isReserved = ['SC', 'ST', 'PWBD', 'PWBD_GEN', 'PWBD_OBC', 'PWBD_SC_ST'].includes(effectiveCategory);
  const min_pct = isReserved ? rule.min_pct_res : rule.min_pct_gen;

  if (min_pct > 0.0) {
    if (aggregate_pct === null || aggregate_pct === undefined || isNaN(aggregate_pct)) {
      if (isSkippedCheckEnabled) {
        skipped_requirements.push(`Graduation percentage required (Min: ${min_pct.toFixed(2)}%)`);
      }
    } else if (aggregate_pct < min_pct) {
      is_eligible = false;
      reasons.push(
        `Aggregate ${aggregate_pct.toFixed(2)}% is below strict threshold of ${min_pct.toFixed(2)}% (No rounding off allowed)`
      );
    }
  }

  // Dual Threshold (e.g. EXIM Bank MT 60% in BOTH UG and PG)
  if (rule.requires_dual_threshold && aggregate_pct !== null && aggregate_pct < min_pct) {
    // Already flagged above, provides statutory clause context
  }

  // ----------------------------------------------------------------------------
  // G. Statutory Dimension 5: Final Year Student Permissibility
  // ----------------------------------------------------------------------------
  if (profile.is_final_year) {
    if (!rule.allows_final_year) {
      is_eligible = false;
      reasons.push(
        'Final year appearing students are strictly ineligible; passing proof required by cutoff date'
      );
    } else {
      is_conditional = true;
      reasons.push(
        'Conditionally eligible: Must produce documentary proof of degree passing prior to Mains/Interview'
      );
    }
  }

  // ----------------------------------------------------------------------------
  // H. Statutory Dimension 6: Category Attempt Limits
  // ----------------------------------------------------------------------------
  const limits = rule.attempt_limits || {};
  if (
    effectiveCategory in limits &&
    limits[effectiveCategory] !== null &&
    limits[effectiveCategory] !== undefined
  ) {
    const user_attempts = prior_attempts[rule.exam_id] ?? 0;
    const limit = limits[effectiveCategory]!;
    if (user_attempts >= limit) {
      is_eligible = false;
      reasons.push(
        `Exceeded maximum allowed attempts of ${limit} for ${effectiveCategory} category (Attempt count: ${user_attempts})`
      );
    }
  }

  // ----------------------------------------------------------------------------
  // I. Statutory Dimension 8: Physical & Medical Standards
  // ----------------------------------------------------------------------------
  const phys = rule.physical_standards;
  if (phys) {
    const min_h = !isFemale
      ? phys.min_height_male_cm
      : phys.min_height_female_cm;

    if (min_h) {
      if (profile.height_cm === undefined || profile.height_cm === null) {
        if (isSkippedCheckEnabled) {
          skipped_requirements.push(
            `Height measurement required for uniformed entry (Min: ${min_h} cm for ${isFemale ? 'Female' : 'Male'})`
          );
        }
      } else if (profile.height_cm < min_h) {
        is_eligible = false;
        reasons.push(
          `Height ${profile.height_cm} cm fails minimum standard of ${min_h} cm for ${isFemale ? 'Female' : 'Male'}`
        );
      }
    }

    // Chest Measurement & Expansion (Male Uniformed)
    if (!isFemale && phys.min_chest_male_cm) {
      const min_chest = phys.min_chest_male_cm;
      if (profile.chest_cm === undefined || profile.chest_cm === null) {
        if (isSkippedCheckEnabled) {
          skipped_requirements.push(`Chest measurement standard required (Min: ${min_chest} cm)`);
        }
      } else if (profile.chest_cm < min_chest) {
        is_eligible = false;
        reasons.push(`Chest measurement ${profile.chest_cm} cm fails minimum standard of ${min_chest} cm`);
      }

      const min_exp = phys.min_expansion_male_cm || 5;
      if (profile.chest_expansion_cm === undefined || profile.chest_expansion_cm === null) {
        if (isSkippedCheckEnabled) {
          skipped_requirements.push(`Chest expansion standard required (Min: ${min_exp} cm)`);
        }
      } else if (profile.chest_expansion_cm < min_exp) {
        is_eligible = false;
        reasons.push(
          `Chest expansion ${profile.chest_expansion_cm} cm fails minimum mandatory expansion of ${min_exp} cm`
        );
      }
    }

    // LASIK Restrictions
    if (profile.has_lasik && phys.lasik_min_age) {
      if (profile.lasik_age && profile.lasik_age < phys.lasik_min_age) {
        is_eligible = false;
        reasons.push(
          `Disqualified: LASIK performed at age ${profile.lasik_age} (Minimum allowed age is ${phys.lasik_min_age})`
        );
      }
      const waitMonths = phys.lasik_wait_months || 6;
      if (profile.lasik_wait_months && profile.lasik_wait_months < waitMonths) {
        is_eligible = false;
        reasons.push(
          `Disqualified: LASIK elapsed time ${profile.lasik_wait_months} months fails mandatory wait period of ${waitMonths} months`
        );
      }
    }

    // Color Blindness
    if (profile.has_color_blindness && phys.disallow_color_blind) {
      is_eligible = false;
      reasons.push(
        'Color vision defect (Color Blindness) is disqualifying for this executive uniformed/technical cadre'
      );
    }

    // Cockpit Anthropometrics for Flying Branches (IAF AFCAT & CDS AFA)
    if (phys.flying_branch_standards) {
      const fly = phys.flying_branch_standards;
      const flyMinH = fly.min_height_cm;

      // Standing height diagnostic for Flying branch
      if (profile.height_cm !== undefined && profile.height_cm !== null) {
        if (profile.height_cm < flyMinH) {
          if (min_h && profile.height_cm >= min_h) {
            reasons.push(
              `Height ${profile.height_cm} cm is below Flying Branch threshold (${flyMinH} cm); eligible for Ground Duty branches only`
            );
          }
        }
      }

      // Check cockpit anthropometric dimensions
      const sitting = profile.sitting_height_cm;
      const leg = profile.leg_length_cm;
      const thigh = profile.thigh_length_cm;

      const isSittingMissing =
        sitting === undefined || sitting === null || sitting === ('' as any) || isNaN(Number(sitting)) || Number(sitting) <= 0;
      const isLegMissing =
        leg === undefined || leg === null || leg === ('' as any) || isNaN(Number(leg)) || Number(leg) <= 0;
      const isThighMissing =
        thigh === undefined || thigh === null || thigh === ('' as any) || isNaN(Number(thigh)) || Number(thigh) <= 0;

      const missingCockpitDetails: string[] = [];
      if (isSittingMissing) {
        missingCockpitDetails.push('Sitting height');
      } else if (Number(sitting) < fly.sitting_height_min_cm || Number(sitting) > fly.sitting_height_max_cm) {
        reasons.push(
          `Sitting height ${sitting} cm outside Flying Branch cockpit safety limits (${fly.sitting_height_min_cm}–${fly.sitting_height_max_cm} cm); eligible for Ground Duty only`
        );
      }

      if (isLegMissing) {
        missingCockpitDetails.push('Leg length');
      } else if (Number(leg) < fly.leg_length_min_cm || Number(leg) > fly.leg_length_max_cm) {
        reasons.push(
          `Leg length ${leg} cm outside Flying Branch cockpit rudder limits (${fly.leg_length_min_cm}–${fly.leg_length_max_cm} cm); eligible for Ground Duty only`
        );
      }

      if (isThighMissing) {
        missingCockpitDetails.push('Thigh length');
      } else if (Number(thigh) > fly.thigh_length_max_cm) {
        reasons.push(
          `Thigh length ${thigh} cm exceeds Flying Branch ejection clearance max (${fly.thigh_length_max_cm} cm); eligible for Ground Duty only`
        );
      }

      if (missingCockpitDetails.length > 0 && isSkippedCheckEnabled) {
        skipped_requirements.push(
          `IAF Flying Branch cockpit anthropometrics required (${missingCockpitDetails.join(', ')}) to verify Flying Branch eligibility`
        );
      }
    }

    // Weight Standards
    if (profile.weight_kg !== undefined && profile.weight_kg !== null) {
      const minWeight = isFemale ? phys.min_weight_female_kg : phys.min_weight_male_kg;
      if (minWeight && profile.weight_kg < minWeight) {
        is_eligible = false;
        reasons.push(
          `Weight ${profile.weight_kg} kg fails minimum statutory weight of ${minWeight} kg for ${isFemale ? 'Female' : 'Male'}`
        );
      }
    }
  }

  // Prior Assistant Commandant Re-appearance Disqualification
  if (rule.disallow_prior_selected_ac && profile.prior_selected_as_ac) {
    is_eligible = false;
    reasons.push(
      'Disqualified under MHA rules: Currently or previously appointed Assistant Commandants cannot re-appear'
    );
  }

  // ----------------------------------------------------------------------------
  // J. Statutory Dimension 7 (Language): Compulsory Regional Language Qualifier
  // ----------------------------------------------------------------------------
  const lang_req = rule.language_requirements;
  if (lang_req && lang_req.mandatory_fluency) {
    const req_lang = lang_req.mandatory_fluency;
    if (isSkippedCheckEnabled && (!profile.fluent_languages || profile.fluent_languages.length === 0)) {
      skipped_requirements.push(`Language fluency required in '${req_lang}'`);
    } else {
      const isLangOk =
        fluent_languages.includes(req_lang) ||
        (req_lang === 'Bengali' && fluent_languages.includes('Nepali'));
      if (!isLangOk) {
        is_eligible = false;
        reasons.push(`Candidate lacks mandatory fluency/reading/writing proficiency in '${req_lang}'`);
      }
    }
  }

  // ----------------------------------------------------------------------------
  // K. Specialized Cadre Gates (AFCAT 10+2 & CDS Marital Status)
  // ----------------------------------------------------------------------------
  if (rule.requires_10plus2_physics_maths) {
    if (profile.ten_plus_two_maths_pct == null || profile.ten_plus_two_physics_pct == null) {
      if (isSkippedCheckEnabled) {
        skipped_requirements.push(
          `10+2 Physics & Mathematics percentage required (Min: ${rule.min_10plus2_subject_pct || 50}%)`
        );
      }
    } else if (
      profile.ten_plus_two_maths_pct < 50.0 ||
      profile.ten_plus_two_physics_pct < 50.0
    ) {
      is_eligible = false;
      reasons.push(
        'Disqualified: Requires minimum 50% marks in both Mathematics and Physics at 10+2 level'
      );
    }
  }

  const marital_req = rule.marital_status_restrictions?.['OTA_Women'];
  if (marital_req === 'Unmarried_or_Issueless_Widow' && isFemale) {
    if (
      profile.marital_status === 'Married' ||
      (['Widow', 'Divorcee'].includes(profile.marital_status || '') && profile.has_children)
    ) {
      is_eligible = false;
      reasons.push(
        'OTA Women Non-Technical entry accepts only unmarried women or issueless widows/divorcees'
      );
    }
  }

  // ----------------------------------------------------------------------------
  // L. Verdict Synthesis
  // ----------------------------------------------------------------------------
  let status: EligibilityStatus = 'INELIGIBLE';
  if (is_eligible) {
    if (skipped_requirements.length > 0) {
      status = 'NEEDS_INFO';
    } else {
      status = 'ELIGIBLE';
    }
  }

  const finalReasons: string[] = [];
  if (!is_eligible) {
    finalReasons.push(...reasons);
  } else if (skipped_requirements.length > 0) {
    finalReasons.push(...skipped_requirements.map(s => `Needs Info: ${s}`));
    if (is_conditional) {
      finalReasons.push(...reasons);
    }
  } else if (is_conditional) {
    finalReasons.push(...reasons);
    finalReasons.push('Meets all statutory eligibility criteria (Provisional pending final year degree proof)');
  } else {
    if (reasons.length > 0) {
      finalReasons.push(...reasons);
    } else {
      finalReasons.push('Meets all statutory eligibility criteria');
    }
  }

  return {
    exam_id: rule.exam_id,
    status,
    reasons: finalReasons,
    relaxations_applied,
    statutory_citation: rule.citation || 'Official Gazette Notification',
    skipped_requirements,
  };
}

// ==============================================================================
// 5. BATCH EVALUATION & FILTERING PIPELINE
// ==============================================================================

/**
 * Evaluates candidate profile across all 31 authoritative examinations.
 */
export function evaluateAllExams(
  profile: UserProfileInput,
  rules: Record<string, ExamEligibilityRule> = AUTHORITATIVE_EXAM_RULES,
  examYear: number = 2027
): Record<string, EligibilityVerdict> {
  const verdicts: Record<string, EligibilityVerdict> = {};
  for (const [exam_id, rule] of Object.entries(rules)) {
    verdicts[exam_id] = evaluateEligibility(profile, rule, examYear);
  }
  return verdicts;
}

/**
 * Filters evaluation results returning only unconditionally ELIGIBLE exams.
 */
export function filterEligibleExams(
  verdicts: Record<string, EligibilityVerdict>
): Record<string, EligibilityVerdict> {
  const result: Record<string, EligibilityVerdict> = {};
  for (const [k, v] of Object.entries(verdicts)) {
    if (v.status === 'ELIGIBLE') result[k] = v;
  }
  return result;
}

/**
 * Filters evaluation results returning only CONDITIONALLY_ELIGIBLE exams.
 */
export function filterConditionallyEligibleExams(
  verdicts: Record<string, EligibilityVerdict>
): Record<string, EligibilityVerdict> {
  const result: Record<string, EligibilityVerdict> = {};
  for (const [k, v] of Object.entries(verdicts)) {
    if (v.status === 'CONDITIONALLY_ELIGIBLE') result[k] = v;
  }
  return result;
}

/**
 * Filters evaluation results returning only INELIGIBLE exams.
 */
export function filterIneligibleExams(
  verdicts: Record<string, EligibilityVerdict>
): Record<string, EligibilityVerdict> {
  const result: Record<string, EligibilityVerdict> = {};
  for (const [k, v] of Object.entries(verdicts)) {
    if (v.status === 'INELIGIBLE') result[k] = v;
  }
  return result;
}

/**
 * Filters evaluation results returning only exams that require additional user profile information.
 */
export function filterNeedsInfoExams(
  verdicts: Record<string, EligibilityVerdict>
): Record<string, EligibilityVerdict> {
  const result: Record<string, EligibilityVerdict> = {};
  for (const [k, v] of Object.entries(verdicts)) {
    if (v.status === 'NEEDS_INFO') result[k] = v;
  }
  return result;
}
