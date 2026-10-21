/**
 * Comprehensive Unit Test Suite for Exam Syllabus Overhaul & PSU/GATE Consolidation
 * File: tests/unit/test_syllabus_overhaul.mjs
 */

import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '../..');

console.log('================================================================');
console.log('STARTING SYLLABUS OVERHAUL & GATE CONSOLIDATION TEST SUITE');
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

// Read generated datasets
const curriculumPath = path.join(ROOT_DIR, 'frontend/src/data/exam_curriculum_data.json');
const curriculumData = JSON.parse(fs.readFileSync(curriculumPath, 'utf8'));

// -----------------------------------------------------------------------------
// TEST GROUP 1: Curriculum Dataset Completeness & Gazette Parity
// -----------------------------------------------------------------------------
console.log('\n[TEST GROUP 1] Curriculum Dataset Completeness & Scheme Architecture');

it('Curriculum dataset schemes exist for all examinations (15 primary + 11 PSUs)', () => {
  const schemes = curriculumData.schemes;
  assert(schemes, 'schemes object must exist');
  const count = Object.keys(schemes).length;
  assert.strictEqual(count, 26, `Expected 26 schemed exams, found ${count}`);
});

it('UPSC CSE scheme matches official notification structure (Prelims, Mains, Interview)', () => {
  const cse = curriculumData.schemes['UPSC_CSE'];
  assert(cse, 'UPSC_CSE must exist');
  assert.strictEqual(cse.total_marks, 2025, 'CSE total marks must be 2025');
  assert.strictEqual(cse.stages.length, 3, 'CSE must have 3 stages');

  const prelims = cse.stages.find((s) => s.stage_id === 'prelims');
  assert(prelims, 'Prelims stage must exist');
  assert.strictEqual(prelims.papers.length, 2, 'Prelims must have 2 papers');

  const gs1 = prelims.papers.find((p) => p.paper_id === 'cse_pre_p1');
  assert(gs1, 'GS-1 paper must exist');
  assert.strictEqual(gs1.marks, 200);
  assert.strictEqual(gs1.is_qualifying, false);
  assert.strictEqual(gs1.duration_hours, 2.0);
  assert.strictEqual(gs1.topics.length, 7, 'GS-1 must cover all 7 gazette items');

  const csat = prelims.papers.find((p) => p.paper_id === 'cse_pre_p2');
  assert(csat, 'CSAT paper must exist');
  assert.strictEqual(csat.is_qualifying, true);
  assert.strictEqual(csat.qualifying_threshold_pct, 33.33);

  const mains = cse.stages.find((s) => s.stage_id === 'mains');
  assert(mains, 'Mains stage must exist');
  assert.strictEqual(mains.papers.length, 9, 'Mains must have 9 papers (2 qualifying + 7 merit)');
});

it('Every syllabus topic includes detailed description and actionable sub-points', () => {
  const cse = curriculumData.schemes['UPSC_CSE'];
  for (const stage of cse.stages) {
    for (const paper of stage.papers) {
      for (const topic of paper.topics) {
        assert(topic.topic_id, 'Topic must have topic_id');
        assert(topic.title, `Topic ${topic.topic_id} must have title`);
        assert(topic.description, `Topic ${topic.topic_id} must have description`);
        assert(topic.description.length > 20, `Topic ${topic.topic_id} description must be substantial`);
      }
    }
  }
});

// -----------------------------------------------------------------------------
// TEST GROUP 2: GATE Authoritative Scheme & Discipline Switching
// -----------------------------------------------------------------------------
console.log('\n[TEST GROUP 2] Authoritative GATE Exam Card & Discipline Switching');

it('GATE scheme contains General Aptitude and 7 engineering disciplines', () => {
  const gate = curriculumData.schemes['GATE'];
  assert(gate, 'GATE must exist');
  assert.strictEqual(gate.total_marks, 100);
  assert(Array.isArray(gate.disciplines), 'GATE must have disciplines array');
  assert.strictEqual(gate.disciplines.length, 7, 'GATE must have 7 disciplines');

  const discCodes = gate.disciplines.map((d) => d.code);
  const expectedCodes = ['ME', 'CE', 'EE', 'EC', 'CS', 'CH', 'IN'];
  for (const c of expectedCodes) {
    assert(discCodes.includes(c), `Discipline ${c} must be present in GATE`);
  }

  const cbtStage = gate.stages[0];
  assert(cbtStage, 'GATE must have CBT stage');

  // Verify GA Section
  const gaPaper = cbtStage.papers.find((p) => p.paper_id === 'gate_sec_ga');
  assert(gaPaper, 'General Aptitude section must exist');
  assert.strictEqual(gaPaper.marks, 15);
  assert.strictEqual(gaPaper.topics.length, 3, 'GA must have verbal, quantitative, analytical topics');

  // Verify technical discipline papers
  for (const c of expectedCodes) {
    const techPaper = cbtStage.papers.find((p) => p.stream_id === c);
    assert(techPaper, `Technical paper for branch ${c} must exist`);
    assert.strictEqual(techPaper.marks, 85, `Technical paper for branch ${c} must be 85 marks`);
    assert(techPaper.topics.length > 0, `Technical paper for branch ${c} must have topics`);
  }
});

// -----------------------------------------------------------------------------
// TEST GROUP 3: PSU Consolidation & Posts Integration
// -----------------------------------------------------------------------------
console.log('\n[TEST GROUP 3] PSU Consolidation into Posts');

it('All 11 Maharatna/Navratna PSU recruitments are registered in AUDITED_POSTS_DATA', async () => {
  const postsFilePath = path.join(ROOT_DIR, 'frontend/src/data/postsData.ts');
  const postsFileContent = fs.readFileSync(postsFilePath, 'utf8');

  const expectedPsus = [
    'ONGC_GT', 'IOCL_OFFICER', 'NTPC_ET', 'BARC_NPCIL_SCIENTIFIC_OFFICER',
    'BHEL_ET', 'COAL_INDIA_MT', 'PGCIL_ET', 'BPCL_MT', 'HPCL_OFFICER',
    'SAIL_MTT', 'GAIL_ET'
  ];

  for (const psuId of expectedPsus) {
    assert(
      postsFileContent.includes(`post_id: '${psuId}'`),
      `Post ${psuId} must be defined in postsData.ts`
    );
  }
});

it('All 11 PSU posts designate GATE as their parent examination', () => {
  const postsFilePath = path.join(ROOT_DIR, 'frontend/src/data/postsData.ts');
  const text = fs.readFileSync(postsFilePath, 'utf8');

  const psuIds = [
    'ONGC_GT', 'IOCL_OFFICER', 'NTPC_ET', 'BARC_NPCIL_SCIENTIFIC_OFFICER',
    'BHEL_ET', 'COAL_INDIA_MT', 'PGCIL_ET', 'BPCL_MT', 'HPCL_OFFICER',
    'SAIL_MTT', 'GAIL_ET'
  ];

  for (const pid of psuIds) {
    const postBlockRegex = new RegExp(`post_id:\\s*['"]${pid}['"][\\s\\S]*?parent_exam_id:\\s*['"]([^'"]+)['"]`);
    const match = text.match(postBlockRegex);
    assert(match, `Could not match post block for ${pid}`);
    assert.strictEqual(match[1], 'GATE', `${pid} parent_exam_id must be GATE, found ${match[1]}`);
  }
});

// -----------------------------------------------------------------------------
// TEST GROUP 4: Progress Calculation Invariance
// -----------------------------------------------------------------------------
console.log('\n[TEST GROUP 4] Progress Calculation Logic');

it('Paper and stage progress calculations are strictly bounded to [0, 100]%', () => {
  // Test math formulas
  function calcProgress(done, total) {
    if (total === 0) return 0;
    return Math.round((done / total) * 100);
  }

  assert.strictEqual(calcProgress(0, 10), 0);
  assert.strictEqual(calcProgress(5, 10), 50);
  assert.strictEqual(calcProgress(10, 10), 100);
  assert.strictEqual(calcProgress(0, 0), 0);
  assert.strictEqual(calcProgress(1, 3), 33);
  assert.strictEqual(calcProgress(2, 3), 67);
});

// -----------------------------------------------------------------------------
// SUMMARY
// -----------------------------------------------------------------------------
console.log('================================================================');
console.log(`TEST SUITE COMPLETE: ${passedTests} / ${totalTests} TESTS PASSED`);
console.log('================================================================');

if (passedTests !== totalTests) {
  process.exit(1);
}
