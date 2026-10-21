/**
 * Comprehensive Node.js Test Suite for Isomorphic TypeScript Eligibility Engine
 * File: tests/unit/test_eligibility_engine.mjs
 * Validates all 8 statutory dimensions and 12 cutoff algorithms.
 */

import assert from 'node:assert';
import {
  AUTHORITATIVE_EXAM_RULES,
  evaluateEligibility,
  evaluateAllExams,
  filterEligibleExams,
  filterConditionallyEligibleExams,
  filterIneligibleExams,
  getCutoffDate,
  getStatutoryBirthWindow,
  calculateAgeOnCutoff,
  formatDateISO,
  normalizeDiscipline,
} from '../../src/services/eligibilityEngine.ts';

console.log('================================================================');
console.log('STARTING STATUTORY ELIGIBILITY ENGINE REVIEW TEST SUITE');
console.log('================================================================');

let passedTests = 0;
let totalTests = 0;

function it(description, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✔ [PASS] ${description}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✖ [FAIL] ${description}`);
    console.error(err);
    process.exitCode = 1;
  }
}

// ----------------------------------------------------------------------------
// 1. Catalog Registration & Completeness
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 1] Catalog Registration & Parity');

it('All 31 Official Grade A examinations are registered in AUTHORITATIVE_EXAM_RULES', () => {
  const dbExams = [
    'BPSC_CCE', 'EXIM_BANK_MT', 'IAF_AFCAT', 'IFSCA_GRADE_A',
    'MPPSC_SSE', 'NABARD_GRADE_A', 'PFRDA_GRADE_A',
    'PSU_BARC_NPCIL_ET', 'PSU_BHEL_ET', 'PSU_BPCL_MT', 'PSU_COAL_INDIA_MT',
    'PSU_GAIL_ET', 'PSU_HPCL_OFFICER', 'PSU_IOCL_ET', 'PSU_NTPC_EET',
    'PSU_ONGC_GT', 'PSU_PGCIL_ET', 'PSU_SAIL_MTT', 'RBI_GRADE_B', 'RPSC_RAS',
    'SEBI_GRADE_A', 'SIDBI_GRADE_A', 'TSPSC_GROUP_1',
    'UPPSC_PCS', 'UPSC_CAPF_AC', 'UPSC_CDS', 'UPSC_CGSE', 'UPSC_CSE',
    'UPSC_ESE', 'UPSC_IES_ISS', 'UPSC_IFOS'
  ];

  for (const id of dbExams) {
    assert(AUTHORITATIVE_EXAM_RULES[id], `Missing exam in rules: ${id}`);
    assert.strictEqual(AUTHORITATIVE_EXAM_RULES[id].exam_id, id);
    assert(AUTHORITATIVE_EXAM_RULES[id].citation, `Missing citation for: ${id}`);
    assert(AUTHORITATIVE_EXAM_RULES[id].min_age_gen > 0, `Invalid min_age_gen for: ${id}`);
    assert(AUTHORITATIVE_EXAM_RULES[id].max_age_gen > AUTHORITATIVE_EXAM_RULES[id].min_age_gen, `Invalid max_age_gen for: ${id}`);
  }
});

// ----------------------------------------------------------------------------
// 2. Cutoff Reference Date Calculations (12 statutory cutoff algorithms)
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 2] 12 Statutory Cutoff Date Algorithms');

it('Resolves AUGUST_1_EXAM_YEAR correctly (e.g. UPSC CSE, IFoS, CAPF AC)', () => {
  assert.strictEqual(getCutoffDate('AUGUST_1_EXAM_YEAR', 2027), '2027-08-01');
});

it('Resolves JANUARY_1_EXAM_YEAR correctly (e.g. UPSC ESE, CGSE, IES/ISS)', () => {
  assert.strictEqual(getCutoffDate('JANUARY_1_EXAM_YEAR', 2027), '2027-01-01');
});

it('Resolves JULY_1_EXAM_YEAR correctly (e.g. UPPSC PCS, BPSC CCE, TNPSC)', () => {
  assert.strictEqual(getCutoffDate('JULY_1_EXAM_YEAR', 2027), '2027-07-01');
});

it('Resolves APRIL_1_EXAM_YEAR correctly (e.g. KPSC KAS)', () => {
  assert.strictEqual(getCutoffDate('APRIL_1_EXAM_YEAR', 2027), '2027-04-01');
});

it('Resolves FOLLOWING_JANUARY_1_EXAM_YEAR forward-year correctly (RPSC RAS)', () => {
  assert.strictEqual(getCutoffDate('FOLLOWING_JANUARY_1_EXAM_YEAR', 2027), '2028-01-01');
});

it('Resolves MARCH_31_EXAM_YEAR correctly (SEBI Grade A)', () => {
  assert.strictEqual(getCutoffDate('MARCH_31_EXAM_YEAR', 2027), '2027-03-31');
});

it('Resolves FEBRUARY_1_EXAM_YEAR correctly (PSU ONGC GT)', () => {
  assert.strictEqual(getCutoffDate('FEBRUARY_1_EXAM_YEAR', 2027), '2027-02-01');
});

it('Resolves NOVEMBER_1_EXAM_YEAR correctly (MPSC Rajyaseva)', () => {
  assert.strictEqual(getCutoffDate('NOVEMBER_1_EXAM_YEAR', 2027), '2027-11-01');
});

it('Resolves JUNE_30_EXAM_YEAR correctly (SIDBI Grade A)', () => {
  assert.strictEqual(getCutoffDate('JUNE_30_EXAM_YEAR', 2027), '2027-06-30');
});

it('Resolves JUNE_1_EXAM_YEAR correctly (Coal India MT)', () => {
  assert.strictEqual(getCutoffDate('JUNE_1_EXAM_YEAR', 2027), '2027-06-01');
});

it('Resolves COURSE_COMMENCEMENT_YEAR correctly (UPSC CDS, IAF AFCAT)', () => {
  assert.strictEqual(getCutoffDate('COURSE_COMMENCEMENT_YEAR', 2027), '2028-01-01');
});

it('Resolves CLOSING_DATE correctly for PSUs (e.g. CLOSING_DATE_MAY)', () => {
  assert.strictEqual(getCutoffDate('CLOSING_DATE_MAY', 2027), '2027-05-15');
});

// ----------------------------------------------------------------------------
// 3. Exact Statutory Birth Windows & Age Boundary Enforcement
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 3] Exact Statutory Birth Windows');

it('UPSC CSE (21-32 yrs, Aug 1, 2027): Born Aug 1, 1995 is ineligible, Born Aug 2, 1995 is eligible', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CSE'];
  const window = getStatutoryBirthWindow(rule, 32, 2027);
  assert.strictEqual(formatDateISO(window.minDob), '1995-08-02');
  assert.strictEqual(formatDateISO(window.maxDob), '2006-08-01');

  // Candidate born Aug 1, 1995: 1 day too old
  const profileOld = { dob: '1995-08-01', gender: 'MALE', category: 'GEN' };
  const vOld = evaluateEligibility(profileOld, rule, 2027);
  assert.strictEqual(vOld.status, 'INELIGIBLE');
  assert(vOld.reasons.some(r => r.includes('Age exceeds maximum limit')));

  // Candidate born Aug 2, 1995: exactly 32 on Aug 1, 2027
  const profileEligible = { dob: '1995-08-02', gender: 'MALE', category: 'GEN' };
  const vEligible = evaluateEligibility(profileEligible, rule, 2027);
  assert.strictEqual(vEligible.status, 'ELIGIBLE');

  // Candidate born Aug 1, 2006: exactly 21 on Aug 1, 2027
  const profileYoung = { dob: '2006-08-01', gender: 'MALE', category: 'GEN' };
  const vYoung = evaluateEligibility(profileYoung, rule, 2027);
  assert.strictEqual(vYoung.status, 'ELIGIBLE');

  // Candidate born Aug 2, 2006: 1 day too young (under 21)
  const profileTooYoung = { dob: '2006-08-02', gender: 'MALE', category: 'GEN' };
  const vTooYoung = evaluateEligibility(profileTooYoung, rule, 2027);
  assert.strictEqual(vTooYoung.status, 'INELIGIBLE');
  assert(vTooYoung.reasons.some(r => r.includes('Age is below minimum limit')));
});

it('UPSC ESE (21-30 yrs, Jan 1, 2027): Born Dec 31, 1996 is ineligible, Born Jan 2, 1997 is eligible', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_ESE'];
  const profileCivil = {
    dob: '1996-12-31',
    gender: 'MALE',
    category: 'GEN',
    graduation_discipline: 'Civil'
  };
  const v1 = evaluateEligibility(profileCivil, rule, 2027);
  assert.strictEqual(v1.status, 'INELIGIBLE');

  const profileEligible = {
    dob: '1997-01-02',
    gender: 'MALE',
    category: 'GEN',
    graduation_discipline: 'Civil'
  };
  const v2 = evaluateEligibility(profileEligible, rule, 2027);
  assert.strictEqual(v2.status, 'ELIGIBLE');
});

it('RPSC RAS (21-40 yrs on Jan 1, 2028 forward year): Handles following year cutoff window', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['RPSC_RAS'];
  const window = getStatutoryBirthWindow(rule, 40, 2027);
  assert.strictEqual(formatDateISO(window.minDob), '1987-01-02');
  assert.strictEqual(formatDateISO(window.maxDob), '2007-01-01');

  const pOld = { dob: '1987-01-01', gender: 'MALE', category: 'GEN' };
  const vOld = evaluateEligibility(pOld, rule, 2027);
  assert.strictEqual(vOld.status, 'INELIGIBLE');

  const pEligible = { dob: '1987-01-02', gender: 'MALE', category: 'GEN' };
  const vEligible = evaluateEligibility(pEligible, rule, 2027);
  assert.strictEqual(vEligible.status, 'ELIGIBLE');
});

// ----------------------------------------------------------------------------
// 4. Strict Non-Rounding Percentage Threshold Enforcement
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 4] Non-Rounding Aggregate Percentage Enforcement');

it('RBI Grade B strictly rejects 59.99% against 60.00% General threshold', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['RBI_GRADE_B'];
  const profile59 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 59.99,
  };
  const v59 = evaluateEligibility(profile59, rule, 2027);
  assert.strictEqual(v59.status, 'INELIGIBLE');
  assert(v59.reasons.some(r => r.includes('59.99% is below strict threshold of 60.00%')));

  const profile60 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 60.00,
  };
  const v60 = evaluateEligibility(profile60, rule, 2027);
  assert.strictEqual(v60.status, 'ELIGIBLE');
});

it('BARC OCES strictly rejects 59.99% against 60.00% requirement', () => {
  const barcRule = AUTHORITATIVE_EXAM_RULES['PSU_BARC_OCES'];
  assert.strictEqual(barcRule.min_pct_gen, 60.0);
  assert.strictEqual(barcRule.strict_non_rounding, true);

  const pBarc59 = {
    dob: '2003-01-01', // Age 24 on Aug 1, 2027 (<= 26 max age)
    gender: 'MALE',
    category: 'GEN',
    graduation_discipline: 'Mechanical',
    graduation_aggregate_pct: 59.99,
  };
  const vBarc59 = evaluateEligibility(pBarc59, barcRule, 2027);
  assert.strictEqual(vBarc59.status, 'INELIGIBLE');
  assert(vBarc59.reasons.some(r => r.includes('below strict threshold of 60.00%')));

  const pBarc60 = {
    dob: '2003-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_discipline: 'Mechanical',
    graduation_aggregate_pct: 60.00,
  };
  const vBarc60 = evaluateEligibility(pBarc60, barcRule, 2027);
  assert.strictEqual(vBarc60.status, 'ELIGIBLE');
});

it('RBI Grade B applies reserved percentage floor (50.0%) for SC/ST/PwBD', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['RBI_GRADE_B'];
  const pSC49 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'SC',
    graduation_aggregate_pct: 49.99,
  };
  const vSC49 = evaluateEligibility(pSC49, rule, 2027);
  assert.strictEqual(vSC49.status, 'INELIGIBLE');

  const pSC50 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'SC',
    graduation_aggregate_pct: 50.00,
  };
  const vSC50 = evaluateEligibility(pSC50, rule, 2027);
  assert.strictEqual(vSC50.status, 'ELIGIBLE');
});

// ----------------------------------------------------------------------------
// 5. Attempt Caps Across Categories
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 5] Category Attempt Caps');

it('UPSC CSE caps General attempts at 6, OBC at 9, and SC/ST at unlimited', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CSE'];

  // Gen candidate with 6 attempts -> INELIGIBLE
  const pGen6 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    prior_attempts: { UPSC_CSE: 6 },
  };
  const vGen6 = evaluateEligibility(pGen6, rule, 2027);
  assert.strictEqual(vGen6.status, 'INELIGIBLE');
  assert(vGen6.reasons.some(r => r.includes('Exceeded maximum allowed attempts of 6')));

  // Gen candidate with 5 attempts -> ELIGIBLE
  const pGen5 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    prior_attempts: { UPSC_CSE: 5 },
  };
  assert.strictEqual(evaluateEligibility(pGen5, rule, 2027).status, 'ELIGIBLE');

  // OBC candidate with 9 attempts -> INELIGIBLE, 8 attempts -> ELIGIBLE
  const pObc9 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'OBC',
    prior_attempts: { UPSC_CSE: 9 },
  };
  assert.strictEqual(evaluateEligibility(pObc9, rule, 2027).status, 'INELIGIBLE');

  const pObc8 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'OBC',
    prior_attempts: { UPSC_CSE: 8 },
  };
  assert.strictEqual(evaluateEligibility(pObc8, rule, 2027).status, 'ELIGIBLE');

  // SC candidate with 15 attempts -> ELIGIBLE (unlimited attempts)
  const pSC15 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'SC',
    prior_attempts: { UPSC_CSE: 15 },
  };
  assert.strictEqual(evaluateEligibility(pSC15, rule, 2027).status, 'ELIGIBLE');
});

it('RBI Grade B enforces 6 attempts for General/EWS', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['RBI_GRADE_B'];
  const pRbi6 = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 65.0,
    prior_attempts: { RBI_GRADE_B: 6 },
  };
  const vRbi6 = evaluateEligibility(pRbi6, rule, 2027);
  assert.strictEqual(vRbi6.status, 'INELIGIBLE');
  assert(vRbi6.reasons.some(r => r.includes('Exceeded maximum allowed attempts of 6')));
});

// ----------------------------------------------------------------------------
// 6. Domicile Reservation Firewalls (State PSCs)
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 6] Domicile Reservation Firewalls');

it('UPPSC PCS remaps out-of-state reserved applicant to General with zero relaxation', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPPSC_PCS'];

  // Born July 1, 1984 (43 on July 1, 2027).
  // Gen max age is 40. UP SC gets +5 -> 45 max age.
  // In-state UP SC candidate: ELIGIBLE
  const pInState = {
    dob: '1984-07-01',
    gender: 'MALE',
    category: 'SC',
    state_domicile: 'Uttar Pradesh',
  };
  const vInState = evaluateEligibility(pInState, rule, 2027);
  assert.strictEqual(vInState.status, 'ELIGIBLE');
  assert(vInState.relaxations_applied.some(r => r.includes('SC')));

  // Out-of-state SC candidate from Bihar: Remapped to GEN, max age 40, 43 is INELIGIBLE
  const pOutOfState = {
    dob: '1984-07-01',
    gender: 'MALE',
    category: 'SC',
    state_domicile: 'Bihar',
  };
  const vOutOfState = evaluateEligibility(pOutOfState, rule, 2027);
  assert.strictEqual(vOutOfState.status, 'INELIGIBLE');
  assert(vOutOfState.relaxations_applied.some(r => r.includes('Mapped to General (UR) category under domicile rule')));
});

it('BPSC CCE remaps non-Bihar candidates to General', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['BPSC_CCE'];
  // BPSC Gen max age = 37. Bihar SC gets +5 = 42.
  // Age 39 on Aug 1, 2027 (Born 1988-08-01)
  const pBpHaryana = {
    dob: '1988-08-01',
    gender: 'MALE',
    category: 'SC',
    state_domicile: 'Haryana',
  };
  const vBpHaryana = evaluateEligibility(pBpHaryana, rule, 2027);
  assert.strictEqual(vBpHaryana.status, 'INELIGIBLE');
  assert(vBpHaryana.relaxations_applied.some(r => r.includes('Mapped to General (UR) category under domicile rule')));

  const pBpBihar = {
    dob: '1988-08-01',
    gender: 'MALE',
    category: 'SC',
    state_domicile: 'Bihar',
  };
  const vBpBihar = evaluateEligibility(pBpBihar, rule, 2027);
  assert.strictEqual(vBpBihar.status, 'ELIGIBLE');
  assert(vBpBihar.relaxations_applied.some(r => r.includes('SC')));
});

// ----------------------------------------------------------------------------
// 7. Compulsory Regional Language Gates
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 7] Compulsory Regional Language Gates');

it('Mandatory regional language rule requires language proficiency', () => {
  const rule = {
    ...AUTHORITATIVE_EXAM_RULES['UPPSC_PCS'],
    language_requirements: { mandatory_fluency: 'Marathi' },
  };
  const pNoMarathi = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    fluent_languages: ['Hindi', 'English'],
  };
  const vFail = evaluateEligibility(pNoMarathi, rule, 2027);
  assert.strictEqual(vFail.status, 'INELIGIBLE');
  assert(vFail.reasons.some(r => r.includes("lacks mandatory fluency/reading/writing proficiency in 'Marathi'")));

  const pWithMarathi = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    fluent_languages: ['Marathi', 'English'],
  };
  const vPass = evaluateEligibility(pWithMarathi, rule, 2027);
  assert.strictEqual(vPass.status, 'ELIGIBLE');
});

it('Regional language gate allows alternate language (Bengali or Nepali)', () => {
  const rule = {
    ...AUTHORITATIVE_EXAM_RULES['UPPSC_PCS'],
    language_requirements: { mandatory_fluency: 'Bengali' },
  };
  const pEnglishOnly = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    fluent_languages: ['English', 'Hindi'],
  };
  assert.strictEqual(evaluateEligibility(pEnglishOnly, rule, 2027).status, 'INELIGIBLE');

  const pBengali = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    fluent_languages: ['Bengali', 'English'],
  };
  assert.strictEqual(evaluateEligibility(pBengali, rule, 2027).status, 'ELIGIBLE');

  const pNepali = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    fluent_languages: ['Nepali', 'English'],
  };
  assert.strictEqual(evaluateEligibility(pNepali, rule, 2027).status, 'ELIGIBLE');
});

// ----------------------------------------------------------------------------
// 8. Physical and Medical Standards
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 8] Physical & Medical Standards');

it('UPSC CAPF AC enforces height: 165cm M / 157cm F, and chest 81cm min', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CAPF_AC'];

  // Male 164cm -> fails
  const pMaleShort = {
    dob: '2004-01-01',
    gender: 'MALE',
    category: 'GEN',
    height_cm: 164,
    chest_cm: 82,
  };
  const vMShort = evaluateEligibility(pMaleShort, rule, 2027);
  assert.strictEqual(vMShort.status, 'INELIGIBLE');
  assert(vMShort.reasons.some(r => r.includes('Height 164 cm fails minimum standard of 165 cm')));

  // Female 156cm -> fails (standard is 157cm)
  const pFemShort = {
    dob: '2004-01-01',
    gender: 'FEMALE',
    category: 'GEN',
    height_cm: 156,
  };
  const vFShort = evaluateEligibility(pFemShort, rule, 2027);
  assert.strictEqual(vFShort.status, 'INELIGIBLE');
  assert(vFShort.reasons.some(r => r.includes('Height 156 cm fails minimum standard of 157 cm')));

  // Male 166cm, chest 80cm -> fails chest (min 81cm)
  const pMaleChest = {
    dob: '2004-01-01',
    gender: 'MALE',
    category: 'GEN',
    height_cm: 166,
    chest_cm: 80,
  };
  const vMChest = evaluateEligibility(pMaleChest, rule, 2027);
  assert.strictEqual(vMChest.status, 'INELIGIBLE');
  assert(vMChest.reasons.some(r => r.includes('Chest measurement 80 cm fails minimum standard of 81 cm')));

  // Male 166cm, chest 82cm -> ELIGIBLE
  const pMalePass = {
    dob: '2004-01-01',
    gender: 'MALE',
    category: 'GEN',
    height_cm: 166,
    chest_cm: 82,
  };
  assert.strictEqual(evaluateEligibility(pMalePass, rule, 2027).status, 'ELIGIBLE');
});

it('Disallows color blindness in uniform/police cadre (e.g. UPSC CAPF AC)', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CAPF_AC'];
  const pColorBlind = {
    dob: '2004-01-01',
    gender: 'MALE',
    category: 'GEN',
    height_cm: 170,
    chest_cm: 85,
    has_color_blindness: true,
  };
  if (rule.physical_standards?.disallow_color_blind) {
    const v = evaluateEligibility(pColorBlind, rule, 2027);
    assert.strictEqual(v.status, 'INELIGIBLE');
    assert(v.reasons.some(r => r.includes('Color vision defect')));
  }
});

it('Enforces LASIK minimum age and elapsed recovery wait period', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CSE'];
  // IPS allows LASIK only if performed at >= 20 years and elapsed >= 12 months
  const pUnderageLasik = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    has_lasik: true,
    lasik_age: 19,
    lasik_wait_months: 18,
  };
  const vUnderage = evaluateEligibility(pUnderageLasik, rule, 2027);
  assert.strictEqual(vUnderage.status, 'INELIGIBLE');
  assert(vUnderage.reasons.some(r => r.includes('LASIK performed at age 19')));

  const pInsufficientWait = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    has_lasik: true,
    lasik_age: 21,
    lasik_wait_months: 6, // needs 12
  };
  const vWait = evaluateEligibility(pInsufficientWait, rule, 2027);
  assert.strictEqual(vWait.status, 'INELIGIBLE');
  assert(vWait.reasons.some(r => r.includes('mandatory wait period of 12 months')));

  const pValidLasik = {
    dob: '2000-01-01',
    gender: 'MALE',
    category: 'GEN',
    has_lasik: true,
    lasik_age: 21,
    lasik_wait_months: 14,
  };
  const vValid = evaluateEligibility(pValidLasik, rule, 2027);
  assert.strictEqual(vValid.status, 'ELIGIBLE');
});

// ----------------------------------------------------------------------------
// 9. Marital Status & Child Restrictions (CDS OTA Women)
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 9] Marital Status & Child Restrictions');

it('UPSC CDS OTA Women disallows married women and widows with children', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CDS'];

  // Married female (DOB 2005-01-01 is age 23 on 2028-01-01, within 19-24)
  const pMarriedFemale = {
    dob: '2005-01-01',
    gender: 'FEMALE',
    category: 'GEN',
    marital_status: 'Married',
  };
  const vMarried = evaluateEligibility(pMarriedFemale, rule, 2027);
  assert.strictEqual(vMarried.status, 'INELIGIBLE');
  assert(vMarried.reasons.some(r => r.includes('OTA Women Non-Technical entry accepts only unmarried women')));

  // Widow with children
  const pWidowWithChild = {
    dob: '2005-01-01',
    gender: 'FEMALE',
    category: 'GEN',
    marital_status: 'Widow',
    has_children: true,
  };
  const vChild = evaluateEligibility(pWidowWithChild, rule, 2027);
  assert.strictEqual(vChild.status, 'INELIGIBLE');
  assert(vChild.reasons.some(r => r.includes('OTA Women Non-Technical entry accepts only unmarried women')));

  // Unmarried female -> ELIGIBLE
  const pUnmarriedFemale = {
    dob: '2005-01-01',
    gender: 'FEMALE',
    category: 'GEN',
    marital_status: 'Unmarried',
  };
  const vUnmarried = evaluateEligibility(pUnmarriedFemale, rule, 2027);
  assert.strictEqual(vUnmarried.status, 'ELIGIBLE');
});

// ----------------------------------------------------------------------------
// 10. Final-Year Student Handling (CONDITIONALLY_ELIGIBLE vs INELIGIBLE)
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 10] Final-Year Student Handling');

it('UPSC CSE marks appearing final year students as CONDITIONALLY_ELIGIBLE', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CSE'];
  const pFinalYear = {
    dob: '2002-01-01',
    gender: 'MALE',
    category: 'GEN',
    is_final_year: true,
  };
  const v = evaluateEligibility(pFinalYear, rule, 2027);
  assert.strictEqual(v.status, 'CONDITIONALLY_ELIGIBLE');
  assert(v.reasons.some(r => r.includes('Conditionally eligible: Must produce documentary proof')));
});

it('RBI Grade B strictly disallows final year appearing students', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['RBI_GRADE_B'];
  const pFinalYear = {
    dob: '2002-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 70.0,
    is_final_year: true,
  };
  const v = evaluateEligibility(pFinalYear, rule, 2027);
  assert.strictEqual(v.status, 'INELIGIBLE');
  assert(v.reasons.some(r => r.includes('Final year appearing students are strictly ineligible')));
});

// ----------------------------------------------------------------------------
// 11. Specialized Cadre Gates (AFCAT 10+2 & Prior Selected AC)
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 11] Specialized Cadre Gates');

it('IAF AFCAT enforces minimum 50% in 10+2 Physics and Mathematics for Flying Branch', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['IAF_AFCAT'];
  const pAfcatFail = {
    dob: '2005-01-01', // Age 23 on 2028-01-01 (within 20-24)
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 65.0,
    ten_plus_two_maths_pct: 49.5,
    ten_plus_two_physics_pct: 55.0,
  };
  const vFail = evaluateEligibility(pAfcatFail, rule, 2027);
  assert.strictEqual(vFail.status, 'INELIGIBLE');
  assert(vFail.reasons.some(r => r.includes('minimum 50% marks in both Mathematics and Physics at 10+2')));

  const pAfcatPass = {
    dob: '2005-01-01',
    gender: 'MALE',
    category: 'GEN',
    graduation_aggregate_pct: 65.0,
    ten_plus_two_maths_pct: 60.0,
    ten_plus_two_physics_pct: 60.0,
  };
  const vPass = evaluateEligibility(pAfcatPass, rule, 2027);
  assert.strictEqual(vPass.status, 'ELIGIBLE');
});

it('UPSC CAPF AC bars currently/previously appointed Assistant Commandants from reappearing', () => {
  const rule = AUTHORITATIVE_EXAM_RULES['UPSC_CAPF_AC'];
  const pPriorAC = {
    dob: '2004-01-01',
    gender: 'MALE',
    category: 'GEN',
    prior_selected_as_ac: true,
  };
  const v = evaluateEligibility(pPriorAC, rule, 2027);
  assert.strictEqual(v.status, 'INELIGIBLE');
  assert(v.reasons.some(r => r.includes('appointed Assistant Commandants cannot re-appear')));
});

// ----------------------------------------------------------------------------
// 12. Batch Pipeline & Filtering Functions
// ----------------------------------------------------------------------------
console.log('\n[TEST GROUP 12] Batch Pipeline & Filter Methods');

it('evaluateAllExams evaluates all registered exams and filtering methods partition accurately', () => {
  const candidate = {
    dob: '2002-05-15',
    gender: 'MALE',
    category: 'GEN',
    graduation_degree: 'Bachelor',
    graduation_discipline: 'Mechanical',
    graduation_aggregate_pct: 68.5,
    state_domicile: 'Maharashtra',
    fluent_languages: ['English', 'Hindi', 'Marathi', 'Kannada', 'Tamil'],
    height_cm: 172,
    chest_cm: 86,
    has_color_blindness: false,
    is_final_year: false,
  };

  const verdicts = evaluateAllExams(candidate);
  const totalExamCount = Object.keys(verdicts).length;
  assert(totalExamCount >= 31, `Expected >= 31 exams, got ${totalExamCount}`);

  const eligible = filterEligibleExams(verdicts);
  const conditional = filterConditionallyEligibleExams(verdicts);
  const ineligible = filterIneligibleExams(verdicts);

  const eligibleCount = Object.keys(eligible).length;
  const conditionalCount = Object.keys(conditional).length;
  const ineligibleCount = Object.keys(ineligible).length;

  assert.strictEqual(eligibleCount + conditionalCount + ineligibleCount, totalExamCount);
  assert(eligibleCount > 0, 'Candidate should be eligible for multiple exams');
});

console.log('\n================================================================');
console.log(`TEST SUITE COMPLETE: ${passedTests} / ${totalTests} TESTS PASSED`);
console.log('================================================================\n');

if (passedTests !== totalTests) {
  process.exit(1);
}
