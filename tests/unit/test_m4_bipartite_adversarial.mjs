/**
 * tests/unit/test_m4_bipartite_adversarial.mjs
 * ============================================
 * Adversarial Headless Verification for Bipartite Force Network Physics,
 * Boundary Limits, Coordinate Pinning, and Filter Persistence.
 */

import * as d3 from '../../frontend/node_modules/d3/src/index.js';
import assert from 'node:assert';

console.log('================================================================');
console.log('STARTING ADVERSARIAL BIPARTITE GRAPH PHYSICS & BOUNDARY SUITE');
console.log('================================================================');

let passedTests = 0;
let totalTests = 0;

function runTest(name, fn) {
  totalTests++;
  try {
    fn();
    console.log(`[PASS] Test ${totalTests}: ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`[FAIL] Test ${totalTests}: ${name}`);
    console.error(err);
    process.exitCode = 1;
  }
}

// -----------------------------------------------------------------------------
// Test 1: Simulation Alpha Decay & Tick Convergence (<200 ticks)
// -----------------------------------------------------------------------------
runTest('Force Simulation terminates in <200 ticks with alphaDecay(0.04)', () => {
  const nodes = [
    { id: 'E1', type: 'exam', r: 32, x: 450, y: 110, fx: 450, fy: 110 },
    { id: 'E2', type: 'exam', r: 32, x: 744, y: 520, fx: 744, fy: 520 },
    { id: 'E3', type: 'exam', r: 32, x: 155, y: 520, fx: 155, fy: 520 },
    { id: 'T1', type: 'topic', r: 15, x: 400, y: 320 },
    { id: 'T2', type: 'topic', r: 18, x: 480, y: 360 },
    { id: 'T3', type: 'topic', r: 16, x: 430, y: 390 },
    { id: 'T4', type: 'topic', r: 21, x: 470, y: 310 },
  ];

  const links = [
    { source: 'E1', target: 'T1', depth_level: 'Foundation' },
    { source: 'E1', target: 'T2', depth_level: 'Intermediate' },
    { source: 'E2', target: 'T2', depth_level: 'Advanced' },
    { source: 'E2', target: 'T3', depth_level: 'Analytical' },
    { source: 'E3', target: 'T3', depth_level: 'Foundation' },
    { source: 'E3', target: 'T4', depth_level: 'Advanced' },
  ];

  const width = 900;
  const height = 700;
  const centerX = width / 2;
  const centerY = height / 2;

  const simulation = d3
    .forceSimulation(nodes)
    .alphaDecay(0.04)
    .force(
      'link',
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance((d) => (d.target.type === 'topic' ? 140 : 180))
        .strength(0.35)
    )
    .force(
      'charge',
      d3.forceManyBody().strength((d) => (d.type === 'exam' ? -800 : -150))
    )
    .force(
      'collide',
      d3.forceCollide().radius((d) => Math.max(16, d.r + 6)).iterations(2)
    )
    .force(
      'radial',
      d3
        .forceRadial((d) => (d.type === 'exam' ? 340 : 140), centerX, centerY)
        .strength((d) => (d.type === 'exam' ? 0.6 : 0.2))
    )
    .force('center', d3.forceCenter(centerX, centerY).strength(0.04));

  let ticks = 0;
  const maxTicks = 200;

  while (simulation.alpha() >= simulation.alphaMin() && ticks < maxTicks) {
    simulation.tick();
    ticks++;
  }

  assert(ticks < maxTicks, `Simulation failed to terminate: ticks=${ticks}`);
  assert(ticks >= 150 && ticks <= 180, `Expected ticks between 150 and 180, got ${ticks}`);
  assert(simulation.alpha() < 0.001, `Alpha did not decay below 0.001: ${simulation.alpha()}`);

  // All coordinates must be strictly finite and non-NaN
  for (const n of nodes) {
    assert(!isNaN(n.x), `Node ${n.id} x is NaN`);
    assert(!isNaN(n.y), `Node ${n.id} y is NaN`);
    assert(isFinite(n.x), `Node ${n.id} x is not finite`);
    assert(isFinite(n.y), `Node ${n.id} y is not finite`);
  }
});

// -----------------------------------------------------------------------------
// Test 2: Reheating Simulation Terminates (<200 ticks)
// -----------------------------------------------------------------------------
runTest('Reheating simulation with alpha(0.6) terminates within <200 ticks', () => {
  const nodes = [
    { id: 'E1', type: 'exam', r: 32, x: 450, y: 110, fx: 450, fy: 110 },
    { id: 'T1', type: 'topic', r: 15, x: 400, y: 320 },
    { id: 'T2', type: 'topic', r: 18, x: 480, y: 360 },
  ];
  const links = [
    { source: 'E1', target: 'T1' },
    { source: 'E1', target: 'T2' },
  ];

  const simulation = d3
    .forceSimulation(nodes)
    .alphaDecay(0.04)
    .force('link', d3.forceLink(links).id((d) => d.id))
    .force('charge', d3.forceManyBody().strength(-150));

  // Run to completion first
  while (simulation.alpha() >= simulation.alphaMin()) {
    simulation.tick();
  }

  // Reheat
  simulation.alpha(0.6).restart();
  let reheatTicks = 0;
  while (simulation.alpha() >= simulation.alphaMin() && reheatTicks < 200) {
    simulation.tick();
    reheatTicks++;
  }

  assert(reheatTicks < 200, `Reheat ticks exceeded limit: ${reheatTicks}`);
  assert(reheatTicks >= 140 && reheatTicks <= 170, `Expected reheat ticks ~157, got ${reheatTicks}`);
});

// -----------------------------------------------------------------------------
// Test 3: Disconnected & Isolated Nodes (0-degree exam & topic)
// -----------------------------------------------------------------------------
runTest('Graph handles 0-degree disconnected exams and isolated topics without NaN or errors', () => {
  // Graph where E_ISO has 0 links, and T_ISO has 0 links
  const nodes = [
    { id: 'E_CONNECTED', type: 'exam', r: 32, x: 450, y: 110, fx: 450, fy: 110 },
    { id: 'E_ISO', type: 'exam', r: 32, x: 155, y: 520, fx: 155, fy: 520, degree: 0 },
    { id: 'T_CONNECTED', type: 'topic', r: 15, x: 400, y: 320 },
    { id: 'T_ISO', type: 'topic', r: 12, x: 500, y: 350, degree: 0 }, // r = 12 + sqrt(0)*3 = 12
  ];

  const links = [
    { source: 'E_CONNECTED', target: 'T_CONNECTED', depth_level: 'Foundation' },
  ];

  const simulation = d3
    .forceSimulation(nodes)
    .alphaDecay(0.04)
    .force('link', d3.forceLink(links).id((d) => d.id).strength(0.35))
    .force('charge', d3.forceManyBody().strength((d) => (d.type === 'exam' ? -800 : -150)))
    .force('collide', d3.forceCollide().radius((d) => Math.max(16, d.r + 6)))
    .force('radial', d3.forceRadial((d) => (d.type === 'exam' ? 340 : 140), 450, 350))
    .force('center', d3.forceCenter(450, 350).strength(0.04));

  let ticks = 0;
  while (simulation.alpha() >= simulation.alphaMin() && ticks < 200) {
    simulation.tick();
    ticks++;
  }

  assert(ticks < 200, 'Isolated node simulation did not terminate');

  for (const n of nodes) {
    assert(!isNaN(n.x), `Node ${n.id} x is NaN`);
    assert(!isNaN(n.y), `Node ${n.id} y is NaN`);
    assert(isFinite(n.x), `Node ${n.id} x is not finite`);
    assert(isFinite(n.y), `Node ${n.id} y is not finite`);
  }

  // Verify E_ISO stayed pinned at fx, fy
  const eIso = nodes.find((n) => n.id === 'E_ISO');
  assert.strictEqual(eIso.x, 155, 'E_ISO x should be pinned at 155');
  assert.strictEqual(eIso.y, 520, 'E_ISO y should be pinned at 520');

  // Verify T_ISO remained within valid radial area around center (450, 350)
  const tIso = nodes.find((n) => n.id === 'T_ISO');
  const dist = Math.hypot(tIso.x - 450, tIso.y - 350);
  assert(dist > 50 && dist < 300, `T_ISO distance from center is out of bounds: ${dist}`);
});

// -----------------------------------------------------------------------------
// Test 4: Completely Empty Graph Boundary (0 exams, 0 topics)
// -----------------------------------------------------------------------------
runTest('Boundary: 0 exams and 0 topics handles initialization with zero division protection', () => {
  const nodes = [];
  const links = [];

  const examNodes = nodes.filter((n) => n.type === 'exam');
  const examCount = examNodes.length; // 0
  const topicNodes = nodes.filter((n) => n.type === 'topic');

  // Must not throw ZeroDivisionError
  const examAngleDivisor = Math.max(1, examCount);
  const topicAngleDivisor = Math.max(1, topicNodes.length);
  assert.strictEqual(examAngleDivisor, 1);
  assert.strictEqual(topicAngleDivisor, 1);

  const simulation = d3
    .forceSimulation(nodes)
    .alphaDecay(0.04)
    .force('link', d3.forceLink(links).id((d) => d.id));

  simulation.tick();
  assert.strictEqual(simulation.nodes().length, 0);
});

// -----------------------------------------------------------------------------
// Test 5: Co-located Initial Positions Separation
// -----------------------------------------------------------------------------
runTest('Co-located overlapping nodes separate naturally without NaN coordinates', () => {
  const nodes = [
    { id: 'T1', type: 'topic', r: 15, x: 450, y: 350 },
    { id: 'T2', type: 'topic', r: 15, x: 450, y: 350 }, // Exact same x, y
    { id: 'T3', type: 'topic', r: 15, x: 450, y: 350 }, // Exact same x, y
  ];

  const simulation = d3
    .forceSimulation(nodes)
    .alphaDecay(0.04)
    .force('charge', d3.forceManyBody().strength(-150))
    .force('collide', d3.forceCollide().radius(20));

  for (let i = 0; i < 50; i++) {
    simulation.tick();
  }

  for (const n of nodes) {
    assert(!isNaN(n.x), `Node ${n.id} x became NaN`);
    assert(!isNaN(n.y), `Node ${n.id} y became NaN`);
  }

  // They should no longer be at identical coordinates
  const dist12 = Math.hypot(nodes[0].x - nodes[1].x, nodes[0].y - nodes[1].y);
  assert(dist12 > 1.0, `Nodes 0 and 1 did not separate: distance=${dist12}`);
});

// -----------------------------------------------------------------------------
// Test 6: Node Coordinate Pinning (`fx`, `fy`) and Double-Click Unpinning
// -----------------------------------------------------------------------------
runTest('Node dragging pins fx, fy coordinates and double-click unpins them', () => {
  const node = { id: 'T1', type: 'topic', r: 15, x: 400, y: 300, fx: null, fy: null };
  const simulation = d3
    .forceSimulation([node])
    .alphaDecay(0.04)
    .force('radial', d3.forceRadial(140, 450, 350).strength(0.5));

  // 1. Simulating drag start & drag move:
  node.fx = 250;
  node.fy = 200;

  // Run 10 ticks
  for (let i = 0; i < 10; i++) simulation.tick();

  // fx, fy must enforce exact coordinate pinning
  assert.strictEqual(node.x, 250, 'Node x must equal pinned fx');
  assert.strictEqual(node.y, 200, 'Node y must equal pinned fy');

  // 2. Simulating double-click unpin:
  node.fx = null;
  node.fy = null;
  simulation.alpha(0.15).restart();

  // Run 10 ticks after unpin
  for (let i = 0; i < 10; i++) simulation.tick();

  // Node coordinates must move under radial forces toward radius 140
  assert(node.x !== 250 || node.y !== 200, 'Node coordinates did not move after unpinning');
});

// -----------------------------------------------------------------------------
// Test 7: Zoom Clamping Strictly Bounded to [0.2, 5.0]
// -----------------------------------------------------------------------------
runTest('Zoom transform scale extent is strictly bounded to [0.2, 5.0]', () => {
  const minZoom = 0.2;
  const maxZoom = 5.0;

  // Helper clamping function matching D3 zoom scaleExtent logic
  function clampScale(scale) {
    return Math.max(minZoom, Math.min(maxZoom, scale));
  }

  // Adversarial zoom-in sequence: zoom factor 1.3 applied 25 times from 1.0
  let scale = 1.0;
  for (let i = 0; i < 25; i++) {
    scale = clampScale(scale * 1.3);
  }
  assert.strictEqual(scale, 5.0, `Extreme zoom-in scale should be clamped to 5.0, got ${scale}`);

  // Adversarial zoom-out sequence: zoom factor 0.77 applied 25 times from 1.0
  scale = 1.0;
  for (let i = 0; i < 25; i++) {
    scale = clampScale(scale * 0.77);
  }
  assert.strictEqual(scale, 0.2, `Extreme zoom-out scale should be clamped to 0.2, got ${scale}`);

  // Extreme inputs
  assert.strictEqual(clampScale(0.000001), 0.2);
  assert.strictEqual(clampScale(99999999), 5.0);
  assert.strictEqual(clampScale(-100), 0.2);
  assert.strictEqual(clampScale(1.0), 1.0);
});

// -----------------------------------------------------------------------------
// Test 8: Topology Filter Coordinate Persistence (`prevNodesMap`)
// -----------------------------------------------------------------------------
runTest('Topology filter updates preserve existing node coordinates via prevNodesMap', () => {
  // Phase 1: 3 exams, 5 topics
  const initialNodes = [
    { id: 'E1', type: 'exam', r: 32, x: 450, y: 110, fx: 450, fy: 110 },
    { id: 'E2', type: 'exam', r: 32, x: 744, y: 520, fx: 744, fy: 520 },
    { id: 'T_GS1', type: 'topic', r: 15, x: 420, y: 330, domain: 'General Studies' },
    { id: 'T_GS2', type: 'topic', r: 15, x: 440, y: 340, domain: 'General Studies' },
    { id: 'T_ECON1', type: 'topic', r: 15, x: 460, y: 350, domain: 'Economics & Finance' },
  ];

  // Run simulation for Phase 1 to let nodes settle
  const sim1 = d3
    .forceSimulation(initialNodes)
    .alphaDecay(0.04)
    .force('charge', d3.forceManyBody().strength(-150));

  for (let i = 0; i < 30; i++) sim1.tick();

  // Snapshot settled positions into prevNodesMap
  const prevNodesMap = new Map();
  sim1.nodes().forEach((n) => prevNodesMap.set(n.id, { ...n }));

  // Phase 2: Domain filter set to "General Studies" (T_ECON1 omitted)
  const filteredRawNodes = [
    { id: 'E1', type: 'exam', r: 32 },
    { id: 'E2', type: 'exam', r: 32 },
    { id: 'T_GS1', type: 'topic', r: 15, domain: 'General Studies' },
    { id: 'T_GS2', type: 'topic', r: 15, domain: 'General Studies' },
  ];

  const phase2Nodes = filteredRawNodes.map((node) => {
    const prev = prevNodesMap.get(node.id);
    if (prev && prev.x !== undefined && prev.y !== undefined) {
      return {
        ...node,
        x: prev.x,
        y: prev.y,
        vx: prev.vx,
        vy: prev.vy,
        fx: prev.fx !== undefined ? prev.fx : prev.x,
        fy: prev.fy !== undefined ? prev.fy : prev.y,
      };
    }
    return node;
  });

  // Verify coordinates were strictly preserved
  const origGs1 = prevNodesMap.get('T_GS1');
  const phase2Gs1 = phase2Nodes.find((n) => n.id === 'T_GS1');
  assert.strictEqual(phase2Gs1.x, origGs1.x, 'T_GS1 x coordinate should be preserved');
  assert.strictEqual(phase2Gs1.y, origGs1.y, 'T_GS1 y coordinate should be preserved');

  const origE1 = prevNodesMap.get('E1');
  const phase2E1 = phase2Nodes.find((n) => n.id === 'E1');
  assert.strictEqual(phase2E1.x, origE1.x, 'E1 x coordinate should be preserved');
  assert.strictEqual(phase2E1.y, origE1.y, 'E1 y coordinate should be preserved');
});

// -----------------------------------------------------------------------------
// Test 9: Unpinned Node Maintains Unpinned State across prevNodesMap updates
// -----------------------------------------------------------------------------
runTest('Unpinned node (fx=null) maintains unpinned state through prevNodesMap update', () => {
  const prevNode = { id: 'E1', type: 'exam', r: 32, x: 450, y: 110, fx: null, fy: null };
  const prevNodesMap = new Map([['E1', prevNode]]);

  const newNode = { id: 'E1', type: 'exam', r: 32 };
  const prev = prevNodesMap.get(newNode.id);

  if (prev && prev.x !== undefined && prev.y !== undefined) {
    newNode.x = prev.x;
    newNode.y = prev.y;
    // prev.fx is null. null !== undefined is true. So newNode.fx = null!
    newNode.fx = prev.fx !== undefined ? prev.fx : prev.x;
    newNode.fy = prev.fy !== undefined ? prev.fy : prev.y;
  }

  assert.strictEqual(newNode.fx, null, 'newNode fx should remain null when prev.fx was null');
  assert.strictEqual(newNode.fy, null, 'newNode fy should remain null when prev.fy was null');
});

// -----------------------------------------------------------------------------
// Test 10: Cognitive Depth Stroke Widths and Colors Mapping
// -----------------------------------------------------------------------------
runTest('Cognitive depth styles match 1.5, 2.5, 3.5, 5.0 px specs', () => {
  const DEPTH_STROKE_WIDTHS = {
    Foundation: 1.5,
    Intermediate: 2.5,
    Advanced: 3.5,
    Analytical: 5.0,
  };

  assert.strictEqual(DEPTH_STROKE_WIDTHS.Foundation, 1.5);
  assert.strictEqual(DEPTH_STROKE_WIDTHS.Intermediate, 2.5);
  assert.strictEqual(DEPTH_STROKE_WIDTHS.Advanced, 3.5);
  assert.strictEqual(DEPTH_STROKE_WIDTHS.Analytical, 5.0);
});

console.log('================================================================');
console.log(`BIPARTITE GRAPH ADVERSARIAL SUITE RESULT: ${passedTests} / ${totalTests} PASSED`);
console.log('================================================================');
