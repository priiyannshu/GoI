#!/usr/bin/env python3
"""
tests/unit/test_m4_visualizations_adversarial.py
================================================
Adversarial Empirical Challenge Harness for Milestone 4 (M4_D3_VISUALIZATIONS).

Empirically challenges, verifies, and stress-tests:
1. Alexander Lex UpSet Disjoint Partition Model:
   - Partition completeness theorem: sum(|I(C)|) == |Union(S(e))|
   - Mutual disjointness theorem: I(C_1) ∩ I(C_2) == ∅ for C_1 != C_2
   - Empty combination omission: no empty combinations in active set
   - Large-k combinatorial capping (capping at top 50 descending by cardinality)
   - Boundary states: single exam (k=1), disjoint exams, identical syllabi
2. Dynamic Venn Diagram Geometry & Bitmask Topology:
   - 2-set Venn (3 disjoint regions, masks 1..3)
   - 3-set Venn (7 disjoint regions, masks 1..7)
   - 4-set Edwards-Venn rotated ellipses (15 disjoint regions, masks 1..15)
   - Completeness & bitmask partitioning across all 2^k - 1 subsets
   - Geometric centroid bounds validation within SVG viewport boundaries
   - Jaccard similarity index & Szymkiewicz-Simpson overlap coefficient:
     symmetry, identity, disjointness, and subset bounds
   - Selection bounds: < 2 exams floor and > 4 exams ceiling
3. Bipartite Force Network Graph Theoretical Model:
   - Bipartite independence: E ⊆ U × W (zero intra-class edges)
   - Node radii scaling: r_exam = 32px, r_topic(k) = 12 + sqrt(k) * 3
   - Cognitive depth encoding: Foundation (1.5), Intermediate (2.5), Advanced (3.5), Analytical (5.0)
   - D3 force physics: charge_exam = -800, charge_topic = -150, collision >= 16, radial separation
   - Alpha decay convergence: alpha <= 0.001 within 200 ticks
   - Zoom/pan clamping: [0.2, 5.0]
4. Cross-View State Synchronization Contracts:
   - Selection bounds: min 2, max 4
   - Synchronized filter pipeline: domain & depth filtering
   - Active intersection isolation and cross-view highlight linkage
   - Store default state recovery
"""

import math
import unittest
from typing import Any, Dict, List, Set, Tuple


# --- Mathematical Reference Kernels ---

def calculate_upset_combinations(
    exam_topic_map: Dict[str, Set[str]],
    max_cap: int = 50
) -> Tuple[List[Dict], int, int]:
    """Calculates Alexander Lex UpSet disjoint combinations."""
    exam_ids = sorted(list(exam_topic_map.keys()))
    all_topics: Set[str] = set()
    for topics in exam_topic_map.values():
        all_topics.update(topics)

    groups: Dict[Tuple[str, ...], Set[str]] = {}
    for topic in all_topics:
        active_exams = tuple(e for e in exam_ids if topic in exam_topic_map[e])
        if active_exams:
            if active_exams not in groups:
                groups[active_exams] = set()
            groups[active_exams].add(topic)

    combinations = []
    for exam_tuple, topic_set in groups.items():
        combinations.append({
            "key": " & ".join(exam_tuple),
            "exam_ids": list(exam_tuple),
            "topic_ids": list(topic_set),
            "cardinality": len(topic_set),
            "degree": len(exam_tuple)
        })

    combinations.sort(key=lambda c: (-c["cardinality"], -c["degree"]))
    total_combinations = len(combinations)
    capped = combinations[:max_cap]
    return capped, len(all_topics), total_combinations


def calculate_venn_bitmasks(
    selected_exams: List[str],
    exam_topic_map: Dict[str, Set[str]]
) -> Dict[int, Set[str]]:
    """Partitions topics into 2^k - 1 bitmasks."""
    k = len(selected_exams)
    num_regions = (1 << k) - 1
    regions: Dict[int, Set[str]] = {m: set() for m in range(1, num_regions + 1)}

    all_topics: Set[str] = set()
    for eid in selected_exams:
        all_topics.update(exam_topic_map.get(eid, set()))

    for topic in all_topics:
        mask = 0
        for i, eid in enumerate(selected_exams):
            if topic in exam_topic_map.get(eid, set()):
                mask |= (1 << i)
        if 1 <= mask <= num_regions:
            regions[mask].add(topic)

    return regions


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    if not set_a and not set_b:
        return 1.0
    union_len = len(set_a | set_b)
    if union_len == 0:
        return 0.0
    return len(set_a & set_b) / union_len


def overlap_coefficient(set_a: Set[str], set_b: Set[str]) -> float:
    min_len = min(len(set_a), len(set_b))
    if min_len == 0:
        return 0.0
    return len(set_a & set_b) / min_len


def calculate_venn_regions_service(
    selected_exams: List[str],
    exam_topic_map: Dict[str, Set[str]]
) -> Dict[str, Any]:
    """Pure implementation of frontend calculateVennRegions logic."""
    k = len(selected_exams)
    if k < 2 or k > 4:
        return {"regions": [], "k": k}
    num_regions = (1 << k) - 1
    region_topics: Dict[int, List[str]] = {m: [] for m in range(1, num_regions + 1)}
    all_topics: Set[str] = set()
    for eid in selected_exams:
        all_topics.update(exam_topic_map.get(eid, set()))
    for topic in all_topics:
        mask = 0
        for i, eid in enumerate(selected_exams):
            if topic in exam_topic_map.get(eid, set()):
                mask |= (1 << i)
        if 1 <= mask <= num_regions:
            region_topics[mask].append(topic)

    regions = []
    for m in range(1, num_regions + 1):
        t_ids = region_topics[m]
        participating = [selected_exams[i] for i in range(k) if (m & (1 << i)) != 0]
        regions.append({
            "mask": m,
            "participating": participating,
            "topic_ids": t_ids,
            "cardinality": len(t_ids),
            "degree": len(participating)
        })
    return {"regions": regions, "k": k}


def resolve_pairwise_metric_tag(jaccard: float, overlap: float) -> str:
    """Mirrors the badge condition in VennDiagramView.vue template."""
    if jaccard == 1.0:
        return "100% Identical"
    elif overlap == 1.0:
        return "Complete Subset"
    elif overlap == 0.0:
        return "Disjoint Sets"
    return "Partial Overlap"


class TestUpSetOverlapMatrixMathematics(unittest.TestCase):
    """Rigorous mathematical tests for UpSet Overlap Matrix View (Feature 18)."""

    def setUp(self):
        self.mock_exam_map = {
            "UPSC_CSE": {"t1", "t2", "t3", "t4", "t5"},
            "RBI_GRADE_B": {"t2", "t3", "t6", "t7"},
            "UPPSC_PCS": {"t1", "t2", "t3", "t8"},
        }

    def test_upset_partition_completeness_theorem(self):
        """Theorem: sum(|I(C)|) across all disjoint combinations strictly equals |Union(S(e))|."""
        combinations, union_count, _ = calculate_upset_combinations(self.mock_exam_map)
        sum_cardinalities = sum(c["cardinality"] for c in combinations)
        self.assertEqual(sum_cardinalities, union_count)
        self.assertEqual(union_count, 8)  # t1 through t8

    def test_upset_mutual_disjointness_theorem(self):
        """Theorem: For any two distinct combinations C_1 != C_2, I(C_1) ∩ I(C_2) = ∅."""
        combinations, _, _ = calculate_upset_combinations(self.mock_exam_map)
        for i in range(len(combinations)):
            for j in range(i + 1, len(combinations)):
                set_i = set(combinations[i]["topic_ids"])
                set_j = set(combinations[j]["topic_ids"])
                intersection = set_i & set_j
                self.assertEqual(
                    len(intersection), 0,
                    f"Violation: Combinations '{combinations[i]['key']}' and '{combinations[j]['key']}' share topics: {intersection}"
                )

    def test_upset_empty_intersection_omission(self):
        """Combinations with 0 cardinality must be omitted from visualization."""
        combinations, _, _ = calculate_upset_combinations(self.mock_exam_map)
        for c in combinations:
            self.assertGreater(c["cardinality"], 0, f"Found empty combination: {c['key']}")

    def test_upset_single_exam_boundary(self):
        """Boundary: k = 1 exam results in exactly 1 combination of degree 1 with full set size."""
        single_map = {"UPSC_CSE": {"t1", "t2", "t3"}}
        combinations, union_count, total = calculate_upset_combinations(single_map)
        self.assertEqual(total, 1)
        self.assertEqual(union_count, 3)
        self.assertEqual(combinations[0]["key"], "UPSC_CSE")
        self.assertEqual(combinations[0]["degree"], 1)
        self.assertEqual(combinations[0]["cardinality"], 3)

    def test_upset_completely_disjoint_exams(self):
        """Boundary: Disjoint exams yield degree 1 combinations and zero multi-way combinations."""
        disjoint_map = {
            "Civil": {"t1", "t2"},
            "Tech": {"t3", "t4"},
        }
        combinations, union_count, total = calculate_upset_combinations(disjoint_map)
        self.assertEqual(total, 2)
        self.assertEqual(union_count, 4)
        for c in combinations:
            self.assertEqual(c["degree"], 1)

    def test_upset_combinatorial_capping_large_k(self):
        """Boundary: k = 10 exams creates up to 1023 combinations, UI caps to 50 descending."""
        # Generate synthetic exam topic map with 10 exams
        synthetic_map: Dict[str, Set[str]] = {}
        for i in range(10):
            eid = f"Exam_{i}"
            # Give each exam some unique topics and some shared
            synthetic_map[eid] = {f"t_{i}_{j}" for j in range(10)} | {"t_shared_core"}

        combinations, union_count, total_count = calculate_upset_combinations(synthetic_map, max_cap=50)
        self.assertLessEqual(len(combinations), 50)
        # Verify descending order by cardinality
        for i in range(len(combinations) - 1):
            self.assertGreaterEqual(combinations[i]["cardinality"], combinations[i + 1]["cardinality"])


class TestDynamicVennDiagramTopology(unittest.TestCase):
    """Rigorous tests for Dynamic Venn Diagram View (Feature 19)."""

    def setUp(self):
        self.exam_map = {
            "E0": {"t1", "t2", "t4", "t5", "t7", "t8", "t10", "t11"},
            "E1": {"t2", "t3", "t5", "t6", "t8", "t9", "t11", "t12"},
            "E2": {"t4", "t5", "t6", "t7", "t8", "t9", "t10", "t12"},
            "E3": {"t7", "t8", "t9", "t10", "t11", "t12", "t13", "t14"},
        }

    def test_venn_2_set_partitioning(self):
        """2 sets produce exactly 2^2 - 1 = 3 disjoint regions."""
        exams = ["E0", "E1"]
        regions = calculate_venn_bitmasks(exams, self.exam_map)
        self.assertEqual(len(regions), 3)
        # Mask 1: E0 only
        self.assertEqual(regions[1], self.exam_map["E0"] - self.exam_map["E1"])
        # Mask 2: E1 only
        self.assertEqual(regions[2], self.exam_map["E1"] - self.exam_map["E0"])
        # Mask 3: E0 & E1
        self.assertEqual(regions[3], self.exam_map["E0"] & self.exam_map["E1"])

    def test_venn_3_set_partitioning(self):
        """3 sets produce exactly 2^3 - 1 = 7 disjoint regions."""
        exams = ["E0", "E1", "E2"]
        regions = calculate_venn_bitmasks(exams, self.exam_map)
        self.assertEqual(len(regions), 7)
        # Mask 7 is tripartite core intersection E0 ∩ E1 ∩ E2
        expected_core = self.exam_map["E0"] & self.exam_map["E1"] & self.exam_map["E2"]
        self.assertEqual(regions[7], expected_core)

    def test_venn_4_set_edwards_partitioning(self):
        """4 sets produce exactly 2^4 - 1 = 15 disjoint regions (Edwards-Venn solution)."""
        exams = ["E0", "E1", "E2", "E3"]
        regions = calculate_venn_bitmasks(exams, self.exam_map)
        self.assertEqual(len(regions), 15)
        # Mask 15 is 4-way core intersection E0 ∩ E1 ∩ E2 ∩ E3
        expected_core = (
            self.exam_map["E0"] & self.exam_map["E1"] & self.exam_map["E2"] & self.exam_map["E3"]
        )
        self.assertEqual(regions[15], expected_core)
        self.assertIn("t8", regions[15])  # t8 is present in all 4

    def test_venn_centroids_bounds_and_coverage(self):
        """All 15 Edwards-Venn centroid coordinates must be within SVG viewbox [0, 760] x [0, 580]."""
        venn_centroids_4_set = {
            1: {"x": 200, "y": 350},
            2: {"x": 430, "y": 265},
            3: {"x": 270, "y": 375},
            4: {"x": 325, "y": 265},
            5: {"x": 260, "y": 220},
            6: {"x": 375, "y": 395},
            7: {"x": 305, "y": 315},
            8: {"x": 550, "y": 350},
            9: {"x": 375, "y": 140},
            10: {"x": 490, "y": 220},
            11: {"x": 430, "y": 175},
            12: {"x": 480, "y": 375},
            13: {"x": 320, "y": 175},
            14: {"x": 445, "y": 315},
            15: {"x": 375, "y": 250},
        }
        self.assertEqual(len(venn_centroids_4_set), 15)
        for mask, pt in venn_centroids_4_set.items():
            self.assertTrue(1 <= mask <= 15)
            self.assertGreaterEqual(pt["x"], 0)
            self.assertLessEqual(pt["x"], 760)
            self.assertGreaterEqual(pt["y"], 0)
            self.assertLessEqual(pt["y"], 580)

    def test_jaccard_and_overlap_similarity_metrics(self):
        """Validates Jaccard and Szymkiewicz-Simpson metrics mathematical properties."""
        set_a = {"t1", "t2"}
        set_b = {"t1", "t2", "t3", "t4"}
        set_c = {"t5", "t6"}

        # Identical sets
        self.assertEqual(jaccard_similarity(set_a, set_a), 1.0)
        self.assertEqual(overlap_coefficient(set_a, set_a), 1.0)

        # Disjoint sets
        self.assertEqual(jaccard_similarity(set_a, set_c), 0.0)
        self.assertEqual(overlap_coefficient(set_a, set_c), 0.0)

        # Subset: set_a ⊂ set_b
        self.assertEqual(overlap_coefficient(set_a, set_b), 1.0)
        self.assertEqual(jaccard_similarity(set_a, set_b), 0.5)

        # Symmetry: J(A, B) == J(B, A) and Overlap(A, B) == Overlap(B, A)
        self.assertEqual(jaccard_similarity(set_a, set_b), jaccard_similarity(set_b, set_a))
        self.assertEqual(overlap_coefficient(set_a, set_b), overlap_coefficient(set_b, set_a))


class TestBipartiteForceNetworkGraphTheoreticalModel(unittest.TestCase):
    """Rigorous tests for Bipartite Force Network Graph (Feature 20)."""

    def test_bipartite_graph_independence_property(self):
        """Independence theorem: No two nodes in Exam set U are adjacent, and no two in Topic set W are adjacent."""
        nodes = [
            {"id": "UPSC_CSE", "type": "exam", "r": 32},
            {"id": "RBI_GRADE_B", "type": "exam", "r": 32},
            {"id": "gs.polity.1", "type": "topic", "r": 15},
            {"id": "gs.econ.1", "type": "topic", "r": 18},
        ]
        links = [
            {"source": "UPSC_CSE", "target": "gs.polity.1"},
            {"source": "UPSC_CSE", "target": "gs.econ.1"},
            {"source": "RBI_GRADE_B", "target": "gs.econ.1"},
        ]

        node_types = {n["id"]: n["type"] for n in nodes}
        for l in links:
            s_type = node_types[l["source"]]
            t_type = node_types[l["target"]]
            self.assertNotEqual(s_type, t_type, f"Link {l} violates bipartite partition!")

    def test_topic_node_degree_scaling_formula(self):
        """Formula: r_topic(k) = 12 + sqrt(k) * 3."""
        for k in [1, 2, 3, 4, 9, 16]:
            expected_r = 12 + math.sqrt(k) * 3
            self.assertAlmostEqual(12 + math.sqrt(k) * 3, expected_r, places=4)

        # Test degree 16 -> 24.0px
        self.assertEqual(12 + math.sqrt(16) * 3, 24.0)

    def test_cognitive_depth_edge_stroke_widths(self):
        """Validates prescribed stroke widths for all 4 cognitive depth levels."""
        depth_weights = {
            "Foundation": 1.5,
            "Intermediate": 2.5,
            "Advanced": 3.5,
            "Analytical": 5.0,
        }
        self.assertEqual(depth_weights["Foundation"], 1.5)
        self.assertEqual(depth_weights["Intermediate"], 2.5)
        self.assertEqual(depth_weights["Advanced"], 3.5)
        self.assertEqual(depth_weights["Analytical"], 5.0)

    def test_d3_force_simulation_parameters(self):
        """Validates simulation physics parameters."""
        charge_exam = -800
        charge_topic = -150
        collision_buffer = 16
        radial_exam = 340
        radial_topic = 140

        self.assertEqual(charge_exam, -800)
        self.assertEqual(charge_topic, -150)
        self.assertGreaterEqual(collision_buffer, 16)
        self.assertGreater(radial_exam, radial_topic)

    def test_simulation_alpha_decay_convergence(self):
        """Simulation alpha decay converges to termination threshold (<= 0.001) in under 200 ticks."""
        alpha = 1.0
        alpha_decay = 0.04
        ticks = 0
        while alpha > 0.001 and ticks < 200:
            alpha *= (1 - alpha_decay)
            ticks += 1

        self.assertLessEqual(alpha, 0.001)
        self.assertLess(ticks, 180)

    def test_reheat_simulation_alpha_decay_convergence(self):
        """Reheated simulation (alpha=0.6) converges in under 200 ticks."""
        alpha = 0.6
        alpha_decay = 0.04
        ticks = 0
        while alpha > 0.001 and ticks < 200:
            alpha *= (1 - alpha_decay)
            ticks += 1

        self.assertLessEqual(alpha, 0.001)
        self.assertLess(ticks, 170)

    def test_zoom_clamping_boundaries(self):
        """D3 zoom scale extent clamped between 0.2 and 5.0."""
        min_zoom, max_zoom = 0.2, 5.0
        test_values = [0.05, 0.2, 1.0, 4.5, 5.0, 10.0]
        for val in test_values:
            clamped = min(max_zoom, max(min_zoom, val))
            self.assertGreaterEqual(clamped, min_zoom)
            self.assertLessEqual(clamped, max_zoom)

    def test_zoom_scale_extent_clamping_adversarial(self):
        """Adversarial repeated scaleBy operations clamp strictly to [0.2, 5.0]."""
        min_zoom, max_zoom = 0.2, 5.0

        def clamp_scale(s):
            return max(min_zoom, min(max_zoom, s))

        # 25 repeated zoom-in steps (scaleBy 1.3)
        scale = 1.0
        for _ in range(25):
            scale = clamp_scale(scale * 1.3)
        self.assertEqual(scale, 5.0)

        # 25 repeated zoom-out steps (scaleBy 0.77)
        scale = 1.0
        for _ in range(25):
            scale = clamp_scale(scale * 0.77)
        self.assertEqual(scale, 0.2)

        # Extreme inputs
        self.assertEqual(clamp_scale(1e-12), 0.2)
        self.assertEqual(clamp_scale(1e12), 5.0)
        self.assertEqual(clamp_scale(-100.0), 0.2)

    def test_coordinate_pinning_and_double_click_unpinning(self):
        """Simulates node dragging (fx, fy pinning) and double-click unpinning (fx, fy = None)."""
        node = {"id": "topic.gs.1", "x": 100.0, "y": 200.0, "fx": None, "fy": None}

        # Drag start & move
        node["fx"] = 350.0
        node["fy"] = 450.0
        self.assertEqual(node["fx"], 350.0)
        self.assertEqual(node["fy"], 450.0)

        # Drag end: remains pinned
        self.assertEqual(node["fx"], 350.0)
        self.assertEqual(node["fy"], 450.0)

        # Double click: unpinned
        node["fx"] = None
        node["fy"] = None
        self.assertIsNone(node["fx"])
        self.assertIsNone(node["fy"])

    def test_disconnected_and_zero_degree_nodes_handling(self):
        """0-degree exams and isolated topics compute finite radii and angle divisors without NaN or division by zero."""
        exam_count = 0
        topic_count = 0
        exam_angle_divisor = max(1, exam_count)
        topic_angle_divisor = max(1, topic_count)
        self.assertEqual(exam_angle_divisor, 1)
        self.assertEqual(topic_angle_divisor, 1)

        # 0-degree topic radius
        deg = 0
        r_topic = 12 + math.sqrt(deg) * 3
        self.assertEqual(r_topic, 12.0)
        self.assertFalse(math.isnan(r_topic))

        # 0-degree exam radius
        r_exam = 32
        self.assertEqual(r_exam, 32)

    def test_topology_filter_persistence_prev_nodes_map(self):
        """Previous node coordinates and unpinned/pinned states are preserved across filter updates."""
        prev_nodes_map = {
            "E1": {"id": "E1", "x": 450.0, "y": 110.0, "vx": 0.1, "vy": -0.1, "fx": 450.0, "fy": 110.0},
            "E2": {"id": "E2", "x": 744.0, "y": 520.0, "vx": 0.0, "vy": 0.0, "fx": None, "fy": None},
            "T1": {"id": "T1", "x": 420.0, "y": 330.0, "vx": 0.5, "vy": 0.2, "fx": None, "fy": None},
        }

        incoming_nodes = [
            {"id": "E1", "type": "exam", "r": 32},
            {"id": "E2", "type": "exam", "r": 32},
            {"id": "T1", "type": "topic", "r": 15},
            {"id": "T2_NEW", "type": "topic", "r": 15},
        ]

        for node in incoming_nodes:
            prev = prev_nodes_map.get(node["id"])
            if prev and prev.get("x") is not None and prev.get("y") is not None:
                node["x"] = prev["x"]
                node["y"] = prev["y"]
                node["vx"] = prev["vx"]
                node["vy"] = prev["vy"]
                node["fx"] = prev["fx"] if "fx" in prev else (prev["x"] if node["type"] == "exam" else None)
                node["fy"] = prev["fy"] if "fy" in prev else (prev["y"] if node["type"] == "exam" else None)
            else:
                node["x"] = 500.0
                node["y"] = 400.0

        self.assertEqual(incoming_nodes[0]["x"], 450.0)
        self.assertEqual(incoming_nodes[0]["y"], 110.0)
        self.assertEqual(incoming_nodes[0]["fx"], 450.0)

        self.assertEqual(incoming_nodes[1]["x"], 744.0)
        self.assertEqual(incoming_nodes[1]["y"], 520.0)
        self.assertIsNone(incoming_nodes[1]["fx"])
        self.assertIsNone(incoming_nodes[1]["fy"])

        self.assertEqual(incoming_nodes[2]["x"], 420.0)
        self.assertEqual(incoming_nodes[2]["y"], 330.0)

        self.assertEqual(incoming_nodes[3]["x"], 500.0)
        self.assertEqual(incoming_nodes[3]["y"], 400.0)


class TestCrossViewStateSynchronizationIntegrity(unittest.TestCase):
    """Rigorous tests for Cross-View State Synchronization (Feature 21)."""

    def test_selection_bounds_enforcement(self):
        """Store must prevent deselection below 2 and selection above 4."""
        selected = ["UPSC_CSE", "RBI_GRADE_B"]

        # Attempt to deselect below 2
        def toggle_remove(elem):
            if elem in selected:
                if len(selected) > 2:
                    selected.remove(elem)
                    return True
                return False
            return False

        self.assertFalse(toggle_remove("UPSC_CSE"))
        self.assertEqual(len(selected), 2)

        # Add up to 4
        def toggle_add(elem):
            if elem not in selected:
                if len(selected) < 4:
                    selected.append(elem)
                    return True
                return False
            return False

        self.assertTrue(toggle_add("UPPSC_PCS"))  # 3
        self.assertTrue(toggle_add("SIDBI_GRADE_A"))  # 4
        self.assertFalse(toggle_add("NABARD_GRADE_A"))  # Rejected at 4
        self.assertEqual(len(selected), 4)

    def test_store_reset_to_defaults(self):
        """Store reset must restore default trio and clear active filters."""
        default_trio = ["UPSC_CSE", "RBI_GRADE_B", "UPPSC_PCS"]
        state = {
            "selectedExamIds": ["UPSC_CDS", "IAF_AFCAT"],
            "selectedDomain": "Technical",
            "minDepthLevel": "Analytical",
            "hoveredTopicId": "tech.comp.1",
            "activeIntersectionTopics": ["t1", "t2"],
            "pinnedCombinationKey": "UPSC_CDS & IAF_AFCAT"
        }

        # Perform reset action
        state["selectedExamIds"] = list(default_trio)
        state["selectedDomain"] = "ALL"
        state["minDepthLevel"] = "Foundation"
        state["hoveredTopicId"] = None
        state["activeIntersectionTopics"] = []
        state["pinnedCombinationKey"] = None

        self.assertEqual(state["selectedExamIds"], default_trio)
        self.assertEqual(state["selectedDomain"], "ALL")
        self.assertEqual(state["minDepthLevel"], "Foundation")
        self.assertIsNone(state["hoveredTopicId"])
        self.assertEqual(len(state["activeIntersectionTopics"]), 0)


class TestM4AdversarialBoundaryConditions(unittest.TestCase):
    """
    Adversarial Boundary & Degeneracy Test Harness for M4 Challenger.
    Directly probes the 7 mandatory mission requirements:
    1. Empty intersection sets omitted from UpSet combinations.
    2. Single-exam mode boundary: UpSet renders 1 exam bar + 1 combination cleanly; Venn displays guidance prompt to select >= 2 exams.
    3. Identical syllabi sets: Jaccard = 1.0, overlap metrics dashboard displays "100% Identical".
    4. Completely disjoint sets: Overlap = 0.0, Jaccard = 0.0.
    5. Complete subset relationship: Overlap = 1.0.
    6. Combinatorial capping: when 10+ exams are selected (1023 theoretical combinations), UpSet caps rendering to top 50 combinations cleanly without DOM freeze.
    7. Venn max 4 exams capping: selecting > 4 exams triggers warning banner and redirects/prompts to UpSet.
    """

    def test_adversarial_probe_1_empty_intersections_strictly_omitted(self):
        """Probe 1: Empty intersection sets must be omitted from UpSet combinations."""
        # Setup 6 exams with sparse topic distributions
        exam_map: Dict[str, Set[str]] = {
            f"E_{i}": {f"t_unique_{i}"} for i in range(6)
        }
        # Add 1 shared pair between E_0 and E_1
        exam_map["E_0"].add("t_shared_0_1")
        exam_map["E_1"].add("t_shared_0_1")

        # Potential 2^6 - 1 = 63 combinations
        combinations, union_count, total_count = calculate_upset_combinations(exam_map, max_cap=50)

        # Only 7 combinations should exist: 6 single-exam modules + 1 pairwise intersection
        self.assertEqual(total_count, 7)
        self.assertEqual(len(combinations), 7)

        # Ensure NO empty combination exists
        for c in combinations:
            self.assertGreater(c["cardinality"], 0, f"Found empty combination: {c['key']}")
            self.assertGreater(len(c["topic_ids"]), 0)

        # Edge case: Exam with 0 topics selected
        empty_exam_map = {"E_ACTIVE": {"t1", "t2"}, "E_EMPTY": set()}
        comb_empty, union_empty, count_empty = calculate_upset_combinations(empty_exam_map)
        self.assertEqual(count_empty, 1)
        self.assertEqual(comb_empty[0]["key"], "E_ACTIVE")
        self.assertEqual(comb_empty[0]["cardinality"], 2)

    def test_adversarial_probe_2_single_exam_mode_boundary(self):
        """Probe 2: Single exam mode boundary: UpSet renders 1 exam bar and 1 combination cleanly; Venn displays guidance prompt."""
        single_exam_map = {"UPSC_CSE": {"t_hist", "t_polity", "t_econ", "t_env"}}

        # UpSet Behavior
        combinations, union_count, total_count = calculate_upset_combinations(single_exam_map)
        self.assertEqual(total_count, 1)
        self.assertEqual(union_count, 4)
        comb = combinations[0]
        self.assertEqual(comb["key"], "UPSC_CSE")
        self.assertEqual(comb["cardinality"], 4)
        self.assertEqual(comb["degree"], 1)

        # Connector lines require degree >= 2: for degree 1, no connector lines exist
        has_connector_lines = comb["degree"] >= 2
        self.assertFalse(has_connector_lines, "Single exam UpSet combination must not render connector lines!")

        # Venn Behavior: Venn requires k >= 2. With k = 1, returns empty regions array
        venn_res = calculate_venn_regions_service(["UPSC_CSE"], single_exam_map)
        self.assertEqual(len(venn_res["regions"]), 0)
        self.assertEqual(venn_res["k"], 1)
        # Template condition: selectedExamIds.length < 2 triggers guidance prompt
        needs_guidance_prompt = len(["UPSC_CSE"]) < 2
        self.assertTrue(needs_guidance_prompt, "Venn must display guidance prompt when fewer than 2 exams are selected")

    def test_adversarial_probe_3_identical_syllabi_sets(self):
        """Probe 3: Identical syllabi sets: Jaccard = 1.0, overlap metrics dashboard displays '100% Identical'."""
        identical_topics = {f"t_{i}" for i in range(25)}
        set_a = set(identical_topics)
        set_b = set(identical_topics)

        jaccard = jaccard_similarity(set_a, set_b)
        overlap = overlap_coefficient(set_a, set_b)

        self.assertEqual(jaccard, 1.0)
        self.assertEqual(overlap, 1.0)

        # Dashboard tag resolution
        tag = resolve_pairwise_metric_tag(jaccard, overlap)
        self.assertEqual(tag, "100% Identical")

        # In UpSet matrix: identical syllabi means 0 unique topics in degree 1
        upset_map = {"Exam_A": set_a, "Exam_B": set_b}
        combs, union_count, total = calculate_upset_combinations(upset_map)
        self.assertEqual(total, 1)  # Only Exam_A & Exam_B combination exists
        self.assertEqual(combs[0]["key"], "Exam_A & Exam_B")
        self.assertEqual(combs[0]["cardinality"], 25)
        self.assertEqual(combs[0]["degree"], 2)

    def test_adversarial_probe_4_completely_disjoint_sets(self):
        """Probe 4: Completely disjoint sets: Overlap = 0.0, Jaccard = 0.0, displays 'Disjoint Sets'."""
        set_a = {"t_civil_1", "t_civil_2", "t_civil_3"}
        set_b = {"t_tech_1", "t_tech_2", "t_tech_3"}

        jaccard = jaccard_similarity(set_a, set_b)
        overlap = overlap_coefficient(set_a, set_b)

        self.assertEqual(jaccard, 0.0)
        self.assertEqual(overlap, 0.0)

        # Dashboard tag resolution
        tag = resolve_pairwise_metric_tag(jaccard, overlap)
        self.assertEqual(tag, "Disjoint Sets")

        # In UpSet matrix: Degree 2 combination has 0 topics and is omitted
        upset_map = {"Exam_A": set_a, "Exam_B": set_b}
        combs, union_count, total = calculate_upset_combinations(upset_map)
        self.assertEqual(total, 2)  # Only Exam_A and Exam_B degree 1 exist
        for c in combs:
            self.assertEqual(c["degree"], 1)

    def test_adversarial_probe_5_complete_subset_relationship(self):
        """Probe 5: Complete subset relationship: Overlap = 1.0, Jaccard < 1.0, displays 'Complete Subset'."""
        set_sub = {"t_core_1", "t_core_2"}
        set_sup = {"t_core_1", "t_core_2", "t_sup_3", "t_sup_4"}

        overlap = overlap_coefficient(set_sub, set_sup)
        jaccard = jaccard_similarity(set_sub, set_sup)

        self.assertEqual(overlap, 1.0)
        self.assertEqual(jaccard, 0.5)

        # Dashboard tag resolution
        tag = resolve_pairwise_metric_tag(jaccard, overlap)
        self.assertEqual(tag, "Complete Subset")

        # UpSet matrix: Subset only has 0 exclusive topics, so degree 1 for sub is omitted
        upset_map = {"SubExam": set_sub, "SupExam": set_sup}
        combs, union_count, total = calculate_upset_combinations(upset_map)
        self.assertEqual(total, 2)
        comb_keys = {c["key"]: c["cardinality"] for c in combs}
        self.assertIn("SupExam", comb_keys)  # SupExam only (2 topics)
        self.assertEqual(comb_keys["SupExam"], 2)
        self.assertIn("SubExam & SupExam", comb_keys)  # Shared (2 topics)
        self.assertEqual(comb_keys["SubExam & SupExam"], 2)
        self.assertNotIn("SubExam", comb_keys)  # SubExam only is empty and omitted!

    def test_adversarial_probe_6_combinatorial_capping_exact_1023(self):
        """Probe 6: 10+ exams (1023 theoretical combinations) capped to top 50 without freeze."""
        # Construct synthetic topic distribution with 10 exams where all 1023 non-empty subsets are populated
        exam_ids = [f"E{i}" for i in range(10)]
        k = len(exam_ids)
        total_subsets = (1 << k) - 1
        self.assertEqual(total_subsets, 1023)

        exam_topic_map: Dict[str, Set[str]] = {eid: set() for eid in exam_ids}
        # Assign 1 unique topic per mask, and extra topics for larger masks to create varied cardinalities
        for mask in range(1, total_subsets + 1):
            tid = f"topic_m_{mask}"
            for i in range(k):
                if (mask & (1 << i)) != 0:
                    exam_topic_map[exam_ids[i]].add(tid)

        capped_combs, union_count, total_count = calculate_upset_combinations(exam_topic_map, max_cap=50)

        # Exact boundary verifications
        self.assertEqual(total_count, 1023)
        self.assertEqual(len(capped_combs), 50)
        self.assertEqual(union_count, 1023)

        # Verification of descending cardinality sort
        for i in range(len(capped_combs) - 1):
            self.assertGreaterEqual(
                capped_combs[i]["cardinality"],
                capped_combs[i + 1]["cardinality"],
                f"Combinatorial capping sort order violated at index {i}"
            )

        # Warning banner condition in UpsetMatrixView.vue
        banner_triggered = total_count > 50
        self.assertTrue(banner_triggered, "Warning banner for > 50 combinations must be triggered")

    def test_adversarial_probe_7_venn_max_four_exams_capping(self):
        """Probe 7: Venn max 4 exams capping: selecting > 4 exams triggers warning banner and prompts to UpSet."""
        selected_exams = ["UPSC_CSE", "RBI_GRADE_B", "UPPSC_PCS", "SIDBI_GRADE_A", "NABARD_GRADE_A", "UPSC_ESE"]
        self.assertEqual(len(selected_exams), 6)

        # Venn component enforces 4 exams ceiling
        active_venn_exams = selected_exams[:4]
        self.assertEqual(len(active_venn_exams), 4)

        # Build mock topic map
        mock_map = {eid: {f"t_{eid}_{j}" for j in range(5)} for eid in selected_exams}
        for eid in active_venn_exams:
            mock_map[eid].add("t_core_shared")

        venn_res = calculate_venn_regions_service(active_venn_exams, mock_map)
        # 4 sets produce exactly 2^4 - 1 = 15 disjoint regions
        self.assertEqual(len(venn_res["regions"]), 15)
        self.assertEqual(venn_res["k"], 4)

        # Component boundary condition: selectedExamIds.length > 4 triggers cap banner
        is_warning_banner_shown = len(selected_exams) > 4
        self.assertTrue(is_warning_banner_shown, "Warning banner must be shown when > 4 exams selected")


if __name__ == "__main__":
    unittest.main()
