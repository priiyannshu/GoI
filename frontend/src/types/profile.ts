/**
 * Canonical User Profile & Eligibility Types
 * Designed for 100% interoperability across Vue 3 UI, Pinia Stores, IndexedDB, and Cloudflare D1.
 */

export type Gender = 'Male' | 'Female' | 'Other';

export type Category = 
  | 'GEN' 
  | 'EWS' 
  | 'OBC' 
  | 'SC' 
  | 'ST' 
  | 'PWBD_GEN' 
  | 'PWBD_OBC' 
  | 'PWBD_SC_ST';

export type DegreeLevel = 
  | 'Bachelor' 
  | 'Master' 
  | 'Dual_UG_and_MBA';

export type MaritalStatus = 
  | 'Unmarried' 
  | 'Married' 
  | 'Widow' 
  | 'Divorcee';

export type ExamCategory = 
  | 'Central-Civil' 
  | 'Regulatory' 
  | 'Defense' 
  | 'State-PSC' 
  | 'PSU';

export interface UserProfileInput {
  // Demographics
  dob: string; // YYYY-MM-DD
  gender: Gender;
  category: Category;
  is_ex_serviceman: boolean;
  ex_service_years: number;
  marital_status: MaritalStatus;
  has_children: boolean;

  // Academics
  graduation_degree: DegreeLevel;
  degree?: DegreeLevel; // alias for test oracle compatibility
  graduation_discipline: string;
  discipline?: string; // alias
  graduation_aggregate_pct: number;
  aggregate_pct?: number; // alias
  is_final_year: boolean;
  ten_plus_two_maths_pct?: number | null;
  ten_plus_two_physics_pct?: number | null;

  // Domicile & Languages
  state_domicile: string;
  domicile_state?: string; // alias
  fluent_languages: string[];

  // Prior Attempts
  prior_attempts: Record<string, number>;
  prior_selected_as_ac?: boolean;

  // Physical & Medical Standards
  height_cm: number | null;
  chest_cm: number | null;
  chest_expansion_cm: number | null;
  has_color_blindness: boolean;
  has_lasik: boolean;
  lasik_age: number | null;
  lasik_wait_months: number | null;
  has_commercial_pilot_license: boolean;
  enable_skipped_check?: boolean;
  skipped_fields?: string[];
}

export interface EligibilityVerdict {
  exam_id: string;
  status: 'ELIGIBLE' | 'CONDITIONALLY_ELIGIBLE' | 'NEEDS_INFO' | 'INELIGIBLE';
  reasons: string[];
  relaxations_applied: string[];
  statutory_citation: string;
  skipped_requirements?: string[];
}

export interface ExamRecord {
  exam_id: string;
  title: string;
  short_code: string;
  category: ExamCategory;
  administering_body: string;
  frequency: string;
  official_website: string;
  latest_official_notification_url: string;
  latest_gazette_ref?: string;
  tentative_timeline_2027: Record<string, any>;
  description?: string;
  eligibility?: Record<string, any>;
}
