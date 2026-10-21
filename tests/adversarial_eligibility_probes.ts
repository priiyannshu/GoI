/**
 * ==============================================================================
 * ADVERSARIAL ELIGIBILITY ENGINE PROBE SUITE
 * File: tests/adversarial_eligibility_probes.ts
 *
 * Systematic stress-testing of all 8 statutory dimensions and boundary gates:
 * 1. Triplet Cutoff Dates (1 day before, exact cutoff, 1 day after)
 * 2. Strict Floating Point Non-Rounding (59.99% vs 60.00%, etc.)
 * 3. Domicile Reservation Firewall Across All 10 State PSCs
 * 4. Dual-Threshold Degrees & Discipline Hierarchies
 * 5. Military Service Calculations & Formula Enforcement
 * 6. Physical Standards (Height, Chest, Expansion, LASIK, Color Blindness)
 * ==============================================================================
 */

import {
  evaluateEligibility,
  evaluateAllExams,
  AUTHORITATIVE_EXAM_RULES,
} from '../src/services/eligibilityEngine.ts';
import type {
  UserProfileInput,
  ExamEligibilityRule,
} from '../src/services/eligibilityEngine.ts';

interface ProbeResult {
  category: string;
  name: string;
  passed: boolean;
  expected: any;
  actual: any;
  details?: string;
}

const results: ProbeResult[] = [];

function assertProbe(
  category: string,
  name: string,
  actual: any,
  expected: any,
  details?: string
) {
  const passed = JSON.stringify(actual) === JSON.stringify(expected);
  results.push({ category, name, passed, expected, actual, details });
}

// Default base valid profile
const baseValidProfile: UserProfileInput = {
  dob: '2000-01-01',
  gender: 'MALE',
  category: 'GEN',
  graduation_degree: 'Bachelor',
  graduation_discipline: 'ANY',
  graduation_aggregate_pct: 65.0,
  is_final_year: false,
  state_domicile: 'Delhi',
  fluent_languages: ['Hindi', 'English'],
  prior_attempts: {},
  height_cm: 172,
  chest_cm: 85,
  chest_expansion_cm: 6,
  has_color_blindness: false,
  has_commercial_pilot_license: false,
  has_lasik: false,
};

// ==============================================================================
// 1. CUTOFF DATE EXACT BOUNDARIES (1 day before, boundary, 1 day after)
// ==============================================================================
console.log('--- RUNNING SECTION 1: Cutoff Date Boundaries ---');

// UPSC CSE: August 1, 2027. Max Gen 32 (1995-08-02), Min Gen 21 (2006-08-01)
const cseRule = AUTHORITATIVE_EXAM_RULES.UPSC_CSE;

// Upper Age Boundary
assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 1995-08-01 (1 day before boundary) -> INELIGIBLE (overage)',
  evaluateEligibility({ ...baseValidProfile, dob: '1995-08-01' }, cseRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 1995-08-02 (exact cutoff boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1995-08-02' }, cseRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 1995-08-03 (1 day after boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1995-08-03' }, cseRule).status,
  'ELIGIBLE'
);

// Lower Age Boundary
assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 2006-07-31 (1 day before boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '2006-07-31' }, cseRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 2006-08-01 (exact lower cutoff boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '2006-08-01' }, cseRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC CSE: Born 2006-08-02 (1 day after boundary) -> INELIGIBLE (underage)',
  evaluateEligibility({ ...baseValidProfile, dob: '2006-08-02' }, cseRule).status,
  'INELIGIBLE'
);

// UPSC ESE: January 1, 2027. Max Gen 30 (1997-01-02), Min Gen 21 (2006-01-01)
const eseRule = AUTHORITATIVE_EXAM_RULES.UPSC_ESE;
const eseProfile = { ...baseValidProfile, graduation_discipline: 'Civil' };

assertProbe(
  'Cutoff Date',
  'UPSC ESE: Born 1997-01-01 (1 day before boundary) -> INELIGIBLE',
  evaluateEligibility({ ...eseProfile, dob: '1997-01-01' }, eseRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC ESE: Born 1997-01-02 (exact boundary) -> ELIGIBLE',
  evaluateEligibility({ ...eseProfile, dob: '1997-01-02' }, eseRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC ESE: Born 2006-01-01 (exact lower boundary) -> ELIGIBLE',
  evaluateEligibility({ ...eseProfile, dob: '2006-01-01' }, eseRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPSC ESE: Born 2006-01-02 (1 day underage) -> INELIGIBLE',
  evaluateEligibility({ ...eseProfile, dob: '2006-01-02' }, eseRule).status,
  'INELIGIBLE'
);

// UPPSC PCS: July 1, 2027. Max Gen 40 (1987-07-01), Min Gen 21 (2006-07-01)
const uppscRule = AUTHORITATIVE_EXAM_RULES.UPPSC_PCS;

assertProbe(
  'Cutoff Date',
  'UPPSC PCS: Born 1987-06-30 (1 day before boundary) -> INELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1987-06-30' }, uppscRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'UPPSC PCS: Born 1987-07-01 (exact boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1987-07-01' }, uppscRule).status,
  'ELIGIBLE'
);

// RPSC RAS: January 1 of FOLLOWING year (2028). Max Gen 40 (1987-01-02), Min Gen 21 (2007-01-01)
const rpscRule = AUTHORITATIVE_EXAM_RULES.RPSC_RAS;

assertProbe(
  'Cutoff Date',
  'RPSC RAS: Born 1987-01-01 (41 on Jan 1, 2028) -> INELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1987-01-01' }, rpscRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'RPSC RAS: Born 1987-01-02 (exact upper boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '1987-01-02' }, rpscRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'RPSC RAS: Born 2007-01-01 (exact lower boundary) -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '2007-01-01' }, rpscRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Cutoff Date',
  'RPSC RAS: Born 2007-01-02 (underage) -> INELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, dob: '2007-01-02' }, rpscRule).status,
  'INELIGIBLE'
);

// ==============================================================================
// 2. STRICT FLOATING POINT NON-ROUNDING (59.99% vs 60.00%)
// ==============================================================================
console.log('--- RUNNING SECTION 2: Strict Non-Rounding Thresholds ---');

// RBI Grade B (Gen 60.00%, Res 50.00%)
const rbiRule = AUTHORITATIVE_EXAM_RULES.RBI_GRADE_B;

assertProbe(
  'Strict Non-Rounding',
  'RBI Grade B: Gen 59.99% -> INELIGIBLE (no rounding up)',
  evaluateEligibility({ ...baseValidProfile, graduation_aggregate_pct: 59.99 }, rbiRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'RBI Grade B: Gen 59.999% -> INELIGIBLE (no rounding)',
  evaluateEligibility({ ...baseValidProfile, graduation_aggregate_pct: 59.999 }, rbiRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'RBI Grade B: Gen 60.00% -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, graduation_aggregate_pct: 60.0 }, rbiRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'RBI Grade B: SC 49.99% -> INELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, category: 'SC', graduation_aggregate_pct: 49.99 }, rbiRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'RBI Grade B: SC 50.00% -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, category: 'SC', graduation_aggregate_pct: 50.0 }, rbiRule).status,
  'ELIGIBLE'
);

// PSU IOCL ET (Gen 65.00%, Res 55.00%)
const ioclRule = AUTHORITATIVE_EXAM_RULES.PSU_IOCL_ET;
const ioclProfile = { ...baseValidProfile, dob: '2002-01-01', graduation_discipline: 'Chemical' };

assertProbe(
  'Strict Non-Rounding',
  'PSU IOCL ET: Gen 64.99% -> INELIGIBLE',
  evaluateEligibility({ ...ioclProfile, graduation_aggregate_pct: 64.99 }, ioclRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'PSU IOCL ET: Gen 65.00% -> ELIGIBLE',
  evaluateEligibility({ ...ioclProfile, graduation_aggregate_pct: 65.0 }, ioclRule).status,
  'ELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'PSU IOCL ET: SC 54.99% -> INELIGIBLE',
  evaluateEligibility({ ...ioclProfile, category: 'SC', graduation_aggregate_pct: 54.99 }, ioclRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'PSU IOCL ET: SC 55.00% -> ELIGIBLE',
  evaluateEligibility({ ...ioclProfile, category: 'SC', graduation_aggregate_pct: 55.0 }, ioclRule).status,
  'ELIGIBLE'
);

// PSU BARC/NPCIL (Gen 60.00%, Res 60.00% - No relaxation!)
const barcRule = AUTHORITATIVE_EXAM_RULES.PSU_BARC_NPCIL_ET;
const barcProfile = { ...baseValidProfile, graduation_discipline: 'Mechanical', dob: '2002-01-01' };

assertProbe(
  'Strict Non-Rounding',
  'PSU BARC/NPCIL: SC with 59.99% -> INELIGIBLE (mandates 60% for all categories)',
  evaluateEligibility({ ...barcProfile, category: 'SC', graduation_aggregate_pct: 59.99 }, barcRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Strict Non-Rounding',
  'PSU BARC/NPCIL: SC with 60.00% -> ELIGIBLE',
  evaluateEligibility({ ...barcProfile, category: 'SC', graduation_aggregate_pct: 60.0 }, barcRule).status,
  'ELIGIBLE'
);

// ==============================================================================
// 3. DOMICILE RESERVATION FIREWALL ACROSS ALL 10 STATE PSCS
// ==============================================================================
console.log('--- RUNNING SECTION 3: Domicile Reservation Firewall ---');

const statePscExams = [
  { id: 'UPPSC_PCS', homeState: 'Uttar Pradesh', requiredLang: null, overageOBCDob: '1984-06-01' },
  { id: 'BPSC_CCE', homeState: 'Bihar', requiredLang: null, overageOBCDob: '1988-06-01' },
  { id: 'MPSC_RAJYASEVA', homeState: 'Maharashtra', requiredLang: 'Marathi', overageOBCDob: '1986-06-01' },
  { id: 'MPPSC_SSE', homeState: 'Madhya Pradesh', requiredLang: null, overageOBCDob: '1984-06-01' },
  { id: 'RPSC_RAS', homeState: 'Rajasthan', requiredLang: null, overageOBCDob: '1984-06-01' },
  { id: 'TNPSC_GROUP_1', homeState: 'Tamil Nadu', requiredLang: 'Tamil', overageOBCDob: '1990-06-01' },
  { id: 'APPSC_GROUP_1', homeState: 'Andhra Pradesh', requiredLang: null, overageOBCDob: '1980-06-01' },
  { id: 'TSPSC_GROUP_1', homeState: 'Telangana', requiredLang: null, overageOBCDob: '1980-06-01' },
  { id: 'WBPSC_WBCS', homeState: 'West Bengal', requiredLang: 'Bengali', overageOBCDob: '1989-06-01' },
  { id: 'KPSC_KAS', homeState: 'Karnataka', requiredLang: 'Kannada', overageOBCDob: '1990-06-01' },
];

for (const psc of statePscExams) {
  const rule = AUTHORITATIVE_EXAM_RULES[psc.id];
  if (!rule) continue;

  const langs = ['Hindi', 'English'];
  if (psc.requiredLang) langs.push(psc.requiredLang);

  // Out-of-state candidate with OBC category, aged beyond General limit but within OBC limit
  const outOfStateProfile: UserProfileInput = {
    ...baseValidProfile,
    category: 'OBC',
    state_domicile: 'Delhi', // non-domicile
    dob: psc.overageOBCDob,
    fluent_languages: langs,
  };

  const v_out = evaluateEligibility(outOfStateProfile, rule);

  // Home-state candidate with OBC category (gets relaxation)
  const homeStateProfile: UserProfileInput = {
    ...baseValidProfile,
    category: 'OBC',
    state_domicile: psc.homeState,
    dob: psc.overageOBCDob,
    fluent_languages: langs,
  };

  const v_home = evaluateEligibility(homeStateProfile, rule);

  assertProbe(
    'Domicile Firewall',
    `${psc.id}: Out-of-state candidate denied category relaxation (re-mapped to Gen)`,
    v_out.status,
    'INELIGIBLE',
    `Verdict: ${v_out.status}, relaxations: ${JSON.stringify(v_out.relaxations_applied)}`
  );

  assertProbe(
    'Domicile Firewall',
    `${psc.id}: Home-state candidate receives statutory relaxation`,
    v_home.status,
    'ELIGIBLE',
    `Verdict: ${v_home.status}, relaxations: ${JSON.stringify(v_home.relaxations_applied)}`
  );
}

// ==============================================================================
// 4. DUAL-THRESHOLD DEGREES & DISCIPLINE HIERARCHIES
// ==============================================================================
console.log('--- RUNNING SECTION 4: Dual Threshold & Degrees ---');

// EXIM Bank MT: Requires Dual_UG_and_MBA (or CA) with 60% aggregate
const eximRule = AUTHORITATIVE_EXAM_RULES.EXIM_BANK_MT;

assertProbe(
  'Dual Threshold Degree',
  'EXIM Bank MT: Plain Bachelor degree -> INELIGIBLE (Requires Dual UG and MBA)',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Bachelor', graduation_discipline: 'MBA_Finance', graduation_aggregate_pct: 65.0 },
    eximRule
  ).status,
  'INELIGIBLE'
);

assertProbe(
  'Dual Threshold Degree',
  'EXIM Bank MT: Dual UG and MBA with 58.5% -> INELIGIBLE (< 60%)',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Dual_UG_and_MBA', graduation_discipline: 'MBA_Finance', graduation_aggregate_pct: 58.5 },
    eximRule
  ).status,
  'INELIGIBLE'
);

assertProbe(
  'Dual Threshold Degree',
  'EXIM Bank MT: Dual UG and MBA with 65.0% -> ELIGIBLE',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Dual_UG_and_MBA', graduation_discipline: 'MBA_Finance', graduation_aggregate_pct: 65.0 },
    eximRule
  ).status,
  'ELIGIBLE'
);

assertProbe(
  'Dual Threshold Degree',
  'EXIM Bank MT: CA qualification with 60.0% -> ELIGIBLE',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Bachelor', graduation_discipline: 'CA', graduation_aggregate_pct: 60.0 },
    eximRule
  ).status,
  'ELIGIBLE'
);

// SEBI Grade A: Requires Master or Professional qualification
const sebiRule = AUTHORITATIVE_EXAM_RULES.SEBI_GRADE_A;

assertProbe(
  'Degree Hierarchy',
  'SEBI Grade A: Bachelor in Arts (non-professional) -> INELIGIBLE',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Bachelor', graduation_discipline: 'Arts_History', graduation_aggregate_pct: 70.0 },
    sebiRule
  ).status,
  'INELIGIBLE'
);

assertProbe(
  'Degree Hierarchy',
  'SEBI Grade A: Bachelor in Law (LLB, professional) -> ELIGIBLE',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Bachelor', graduation_discipline: 'Law', graduation_aggregate_pct: 70.0 },
    sebiRule
  ).status,
  'ELIGIBLE'
);

assertProbe(
  'Degree Hierarchy',
  'SEBI Grade A: Master in Commerce (M.Com) -> ELIGIBLE',
  evaluateEligibility(
    { ...baseValidProfile, graduation_degree: 'Master', graduation_discipline: 'Commerce', graduation_aggregate_pct: 70.0 },
    sebiRule
  ).status,
  'ELIGIBLE'
);

// ==============================================================================
// 5. MILITARY SERVICE CALCULATIONS
// ==============================================================================
console.log('--- RUNNING SECTION 5: Military Service Calculations ---');

// UPSC CSE has statutory +5 years ESM relaxation
const esmProfileCse: UserProfileInput = {
  ...baseValidProfile,
  dob: '1990-08-02', // age 37 on 1 Aug 2027. Gen cap is 32. With ESM +5 (cap 37), eligible.
  is_ex_serviceman: true,
  ex_service_years: 5,
};

assertProbe(
  'Military Service',
  'UPSC CSE: Ex-Serviceman age 37 with 5 years service -> ELIGIBLE (+5 years)',
  evaluateEligibility(esmProfileCse, cseRule).status,
  'ELIGIBLE'
);

// Military Service formula check: Age - (Service Years + 3)
// A candidate aged 38 with 8 years military service:
// Age - (Years + 3) = 38 - 11 = 27 <= 32.
const esmLongServiceProfile: UserProfileInput = {
  ...baseValidProfile,
  dob: '1989-08-01', // age 38 on 1 Aug 2027
  is_ex_serviceman: true,
  ex_service_years: 8,
};

const v_esm_long = evaluateEligibility(esmLongServiceProfile, cseRule);
assertProbe(
  'Military Service',
  'UPSC CSE: Ex-Serviceman aged 38 with 8 yrs service (statutory CSE cap is +5)',
  v_esm_long.status,
  'INELIGIBLE', // UPSC CSE notification clause 3(v) explicitly fixes maximum ESM relaxation at 5 years
  `Status: ${v_esm_long.status}, reasons: ${JSON.stringify(v_esm_long.reasons)}`
);

// ==============================================================================
// 6. PHYSICAL STANDARDS & BIOMETRICS (IPS, CAPF, Chest Expansion, LASIK)
// ==============================================================================
console.log('--- RUNNING SECTION 6: Physical Standards & Biometrics ---');

const capfRule = AUTHORITATIVE_EXAM_RULES.UPSC_CAPF_AC;
const capfBaseProfile: UserProfileInput = {
  ...baseValidProfile,
  dob: '2003-01-01', // age 24, within 20-25 limit
};

// IPS Male Height Boundary (164.9 cm vs 165.0 cm)
assertProbe(
  'Physical Standards',
  'UPSC CSE (IPS): Male height 164.9 cm -> INELIGIBLE (< 165 cm standard)',
  evaluateEligibility({ ...baseValidProfile, height_cm: 164.9 }, cseRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Physical Standards',
  'UPSC CSE (IPS): Male height 165.0 cm -> ELIGIBLE (meets standard)',
  evaluateEligibility({ ...baseValidProfile, height_cm: 165.0 }, cseRule).status,
  'ELIGIBLE'
);

// IPS Female Height Boundary (149.9 cm vs 150.0 cm)
assertProbe(
  'Physical Standards',
  'UPSC CSE (IPS): Female height 149.9 cm -> INELIGIBLE (< 150 cm standard)',
  evaluateEligibility({ ...baseValidProfile, gender: 'FEMALE', height_cm: 149.9 }, cseRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Physical Standards',
  'UPSC CSE (IPS): Female height 150.0 cm -> ELIGIBLE (meets standard)',
  evaluateEligibility({ ...baseValidProfile, gender: 'FEMALE', height_cm: 150.0 }, cseRule).status,
  'ELIGIBLE'
);

// CAPF AC Female Height Boundary (156.9 cm vs 157.0 cm)
assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Female height 156.9 cm -> INELIGIBLE (< 157 cm)',
  evaluateEligibility({ ...capfBaseProfile, gender: 'FEMALE', height_cm: 156.9 }, capfRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Female height 157.0 cm -> ELIGIBLE',
  evaluateEligibility({ ...capfBaseProfile, gender: 'FEMALE', height_cm: 157.0 }, capfRule).status,
  'ELIGIBLE'
);

// CAPF AC Male Chest Circumference (80.9 cm vs 81.0 cm)
assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Male chest 80.9 cm -> INELIGIBLE (< 81 cm)',
  evaluateEligibility({ ...capfBaseProfile, chest_cm: 80.9 }, capfRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Male chest 81.0 cm -> ELIGIBLE',
  evaluateEligibility({ ...capfBaseProfile, chest_cm: 81.0 }, capfRule).status,
  'ELIGIBLE'
);

// Chest Expansion Check (4.9 cm vs 5.0 cm)
assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Chest expansion 4.9 cm -> INELIGIBLE (< 5.0 cm expansion requirement)',
  evaluateEligibility({ ...capfBaseProfile, chest_cm: 85, chest_expansion_cm: 4.9 }, capfRule).status,
  'INELIGIBLE',
  'Adversarial probe checking statutory minimum 5cm chest expansion'
);

assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Chest expansion 5.0 cm -> ELIGIBLE',
  evaluateEligibility({ ...capfBaseProfile, chest_cm: 85, chest_expansion_cm: 5.0 }, capfRule).status,
  'ELIGIBLE'
);

// Color Blindness in CAPF AC vs Civil (IAS/IRS)
assertProbe(
  'Physical Standards',
  'UPSC CAPF AC: Color blindness -> INELIGIBLE (strictly disqualifying)',
  evaluateEligibility({ ...capfBaseProfile, has_color_blindness: true }, capfRule).status,
  'INELIGIBLE'
);

// LASIK age under 20 disqualification (UPSC CSE IPS rule)
assertProbe(
  'Physical Standards',
  'UPSC CSE IPS: LASIK performed at age 19 -> INELIGIBLE (min age 20)',
  evaluateEligibility({ ...baseValidProfile, has_lasik: true, lasik_age: 19, lasik_wait_months: 14 }, cseRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Physical Standards',
  'UPSC CSE IPS: LASIK performed at age 20 with 14 months wait -> ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, has_lasik: true, lasik_age: 20, lasik_wait_months: 14 }, cseRule).status,
  'ELIGIBLE'
);

// Final Year Appearing Permissibility
assertProbe(
  'Final Year',
  'RBI Grade B: Final year student -> INELIGIBLE (degree proof mandatory before cutoff)',
  evaluateEligibility({ ...baseValidProfile, is_final_year: true }, rbiRule).status,
  'INELIGIBLE'
);

assertProbe(
  'Final Year',
  'UPSC CSE: Final year student -> CONDITIONALLY_ELIGIBLE',
  evaluateEligibility({ ...baseValidProfile, is_final_year: true }, cseRule).status,
  'CONDITIONALLY_ELIGIBLE'
);

// ==============================================================================
// SUMMARY & OUTPUT
// ==============================================================================
console.log('\n==============================================================================');
console.log('ADVERSARIAL PROBE EXECUTION SUMMARY');
console.log('==============================================================================');

let passedCount = 0;
let failedCount = 0;

for (const r of results) {
  if (r.passed) {
    passedCount++;
    console.log(`  [PASS] [${r.category}] ${r.name}`);
  } else {
    failedCount++;
    console.log(`  [FAIL] [${r.category}] ${r.name}`);
    console.log(`         Expected: ${JSON.stringify(r.expected)}`);
    console.log(`         Actual:   ${JSON.stringify(r.actual)}`);
    if (r.details) console.log(`         Details:  ${r.details}`);
  }
}

console.log('==============================================================================');
console.log(`TOTAL PROBES: ${results.length} | PASSED: ${passedCount} | FAILED: ${failedCount}`);
console.log('==============================================================================');

if (failedCount > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
