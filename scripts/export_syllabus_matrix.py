#!/usr/bin/env python3
"""
scripts/export_syllabus_matrix.py
==================================
High-Performance Mathematical Set Analysis & Syllabus Export Pipeline:
Generates:
1. data/syllabus_taxonomy.json: Hierarchical domain tree + O(1) lookup map + flat list
2. data/exam_syllabus_matrix.json: 36x36 Pairwise Jaccard, Szymkiewicz-Simpson Overlap,
   and Preparation Carry-Over (PCO) Efficiency accounting for cognitive depth sufficiency.
   Disjoint UpSet combinations and topic frequency rankings.
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("export_matrix")

DEPTH_RANK = {
    "Foundation": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Analytical": 4
}


def atomic_write_json(file_path: Path, data: Any, indent: int = 2) -> None:
    """Atomically writes JSON payload using temporary file replacement."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = file_path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    # Validate before replacing
    with open(temp_path, "r", encoding="utf-8") as f:
        json.load(f)
    os.replace(temp_path, file_path)
    logger.info(f"Wrote {file_path.name} ({os.path.getsize(file_path):,} bytes).")


def build_taxonomy_export(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Builds hierarchical structure and O(1) flat lookup map for syllabus taxonomy."""
    cursor = conn.cursor()

    # Query all topics with mapping statistics
    query = """
        SELECT 
            t.topic_id, t.domain, t.sub_domain, t.topic_title, t.description,
            COUNT(DISTINCT m.exam_id) as mapped_exams_count,
            COUNT(m.stage_name) as total_stage_appearances,
            SUM(CASE WHEN m.depth_level = 'Foundation' THEN 1 ELSE 0 END) as depth_foundation,
            SUM(CASE WHEN m.depth_level = 'Intermediate' THEN 1 ELSE 0 END) as depth_intermediate,
            SUM(CASE WHEN m.depth_level = 'Advanced' THEN 1 ELSE 0 END) as depth_advanced,
            SUM(CASE WHEN m.depth_level = 'Analytical' THEN 1 ELSE 0 END) as depth_analytical
        FROM syllabus_taxonomy t
        LEFT JOIN exam_syllabus_map m ON t.topic_id = m.topic_id
        GROUP BY t.topic_id
        ORDER BY t.domain, t.sub_domain, t.topic_id;
    """
    cursor.execute(query)
    topic_rows = cursor.fetchall()

    domain_tree: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    lookup_by_id: Dict[str, Dict[str, Any]] = {}
    topics_flat: List[Dict[str, Any]] = []

    # Get exam details for lookup
    cursor.execute("""
        SELECT topic_id, exam_id, stage_name, depth_level, is_optional, weightage_pct_estimate
        FROM exam_syllabus_map
        ORDER BY topic_id, exam_id, stage_name;
    """)
    map_details: Dict[str, List[Dict[str, Any]]] = {}
    for r in cursor.fetchall():
        tid, eid, stage, depth, opt, weight = r
        map_details.setdefault(tid, []).append({
            "exam_id": eid,
            "stage_name": stage,
            "depth_level": depth,
            "is_optional": bool(opt),
            "weightage_pct_estimate": weight
        })

    for r in topic_rows:
        tid, domain, sub_domain, title, desc, exam_cnt, stage_cnt, d_found, d_inter, d_adv, d_analy = r

        topic_obj = {
            "topic_id": tid,
            "domain": domain,
            "sub_domain": sub_domain,
            "topic_title": title,
            "description": desc,
            "mapped_exams_count": exam_cnt,
            "total_stage_appearances": stage_cnt,
            "depth_distribution": {
                "Foundation": d_found or 0,
                "Intermediate": d_inter or 0,
                "Advanced": d_adv or 0,
                "Analytical": d_analy or 0
            }
        }

        topics_flat.append(topic_obj)

        lookup_by_id[tid] = {
            **topic_obj,
            "mapped_exams": map_details.get(tid, [])
        }

        domain_tree.setdefault(domain, {}).setdefault(sub_domain, []).append(topic_obj)

    # Format domain tree array
    domains_array = []
    for domain_name, sub_domains in domain_tree.items():
        sub_array = []
        for sub_name, topics in sub_domains.items():
            sub_array.append({
                "sub_domain": sub_name,
                "topic_count": len(topics),
                "topics": topics
            })
        domains_array.append({
            "domain": domain_name,
            "sub_domain_count": len(sub_array),
            "total_topics": sum(s["topic_count"] for s in sub_array),
            "sub_domains": sub_array
        })

    return {
        "$schema": "https://raw.githubusercontent.com/grade-a/schema/v1/syllabus-taxonomy.json",
        "metadata": {
            "version": "1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_domains": len(domains_array),
            "total_topics": len(topics_flat),
            "total_exam_mappings": sum(len(m) for m in map_details.values())
        },
        "domains": domains_array,
        "topics_flat": topics_flat,
        "lookup_by_id": lookup_by_id
    }


def build_matrix_export(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Calculates all 36x36 pairwise metrics, UpSet combinations, and topic frequencies."""
    cursor = conn.cursor()

    # 1. Fetch all exams info
    cursor.execute("SELECT exam_id, title, short_code, category FROM exams ORDER BY exam_id;")
    exams_info = {r[0]: {"title": r[1], "short_code": r[2], "category": r[3]} for r in cursor.fetchall()}
    exam_ids = sorted(list(exams_info.keys()))

    # 2. Fetch all mappings: exam_id -> topic_id -> max_depth
    cursor.execute("""
        SELECT exam_id, topic_id, depth_level
        FROM exam_syllabus_map;
    """)
    exam_topic_depths: Dict[str, Dict[str, int]] = {eid: {} for eid in exam_ids}
    exam_topic_sets: Dict[str, Set[str]] = {eid: set() for eid in exam_ids}

    for r in cursor.fetchall():
        eid, tid, depth = r
        rank = DEPTH_RANK.get(depth, 1)
        exam_topic_sets[eid].add(tid)
        current = exam_topic_depths[eid].get(tid, 0)
        if rank > current:
            exam_topic_depths[eid][tid] = rank

    # 3. Exam summary statistics
    exam_summaries = {}
    for eid in exam_ids:
        t_set = exam_topic_sets[eid]
        d_map = exam_topic_depths[eid]
        depth_counts = {"Foundation": 0, "Intermediate": 0, "Advanced": 0, "Analytical": 0}
        for d_val in d_map.values():
            for d_name, d_rank in DEPTH_RANK.items():
                if d_val == d_rank:
                    depth_counts[d_name] += 1

        exam_summaries[eid] = {
            "exam_id": eid,
            "title": exams_info[eid]["title"],
            "short_code": exams_info[eid]["short_code"],
            "category": exams_info[eid]["category"],
            "total_topics": len(t_set),
            "max_depth_distribution": depth_counts
        }

    # 4. Compute 36x36 pairwise metrics
    pairwise_matrix: Dict[str, Dict[str, Any]] = {eid: {} for eid in exam_ids}

    for e_a in exam_ids:
        set_a = exam_topic_sets[e_a]
        depths_a = exam_topic_depths[e_a]

        for e_b in exam_ids:
            set_b = exam_topic_sets[e_b]
            depths_b = exam_topic_depths[e_b]

            intersection = set_a & set_b
            union = set_a | set_b
            inter_len = len(intersection)
            union_len = len(union)

            # Jaccard
            jaccard = (inter_len / union_len) if union_len > 0 else 1.0

            # Szymkiewicz-Simpson Overlap
            min_len = min(len(set_a), len(set_b))
            overlap_coeff = (inter_len / min_len) if min_len > 0 else 0.0

            # Preparation Carry-Over (PCO) from A -> B
            sufficient_topics = []
            depth_deficit_topics = []

            for tid in intersection:
                if depths_a.get(tid, 0) >= depths_b.get(tid, 0):
                    sufficient_topics.append(tid)
                else:
                    depth_deficit_topics.append(tid)

            len_b = len(set_b)
            pco_pct = (len(sufficient_topics) / len_b * 100.0) if len_b > 0 else 0.0

            unique_a = sorted(list(set_a - set_b))
            unique_b = sorted(list(set_b - set_a))

            pairwise_matrix[e_a][e_b] = {
                "source_exam_id": e_a,
                "target_exam_id": e_b,
                "intersection_count": inter_len,
                "union_count": union_len,
                "jaccard_similarity": round(jaccard, 4),
                "overlap_coefficient": round(overlap_coeff, 4),
                "pco_efficiency_pct": round(pco_pct, 2),
                "sufficient_topics_count": len(sufficient_topics),
                "depth_deficit_count": len(depth_deficit_topics),
                "uncovered_target_count": len(unique_b),
                "shared_topics": sorted(list(intersection)),
                "unique_to_source": unique_a,
                "unique_to_target": unique_b
            }

    # 5. UpSet disjoint intersection combinations
    topic_to_exams: Dict[str, List[str]] = {}
    for eid, t_set in exam_topic_sets.items():
        for tid in t_set:
            topic_to_exams.setdefault(tid, []).append(eid)

    membership_to_topics: Dict[Tuple[str, ...], List[str]] = {}
    for tid, e_list in topic_to_exams.items():
        mem_tuple = tuple(sorted(e_list))
        membership_to_topics.setdefault(mem_tuple, []).append(tid)

    upset_combinations = []
    for idx, (m_tuple, t_list) in enumerate(membership_to_topics.items()):
        upset_combinations.append({
            "combination_id": f"upset_comb_{idx + 1:04d}",
            "degree": len(m_tuple),
            "exam_ids": list(m_tuple),
            "topic_count": len(t_list),
            "topic_ids": sorted(t_list)
        })

    upset_combinations.sort(key=lambda c: (c["topic_count"], c["degree"]), reverse=True)

    # 6. Topic frequencies & High-Yield core ranking
    cursor.execute("SELECT topic_id, topic_title, domain, sub_domain FROM syllabus_taxonomy;")
    topic_meta = {r[0]: {"title": r[1], "domain": r[2], "sub_domain": r[3]} for r in cursor.fetchall()}

    topic_frequencies = []
    for tid, meta in topic_meta.items():
        m_exams = sorted(topic_to_exams.get(tid, []))
        freq = len(m_exams)
        topic_frequencies.append({
            "topic_id": tid,
            "topic_title": meta["title"],
            "domain": meta["domain"],
            "sub_domain": meta["sub_domain"],
            "exam_frequency": freq,
            "exam_frequency_pct": round((freq / len(exam_ids) * 100.0), 2) if exam_ids else 0.0,
            "exam_ids": m_exams
        })

    topic_frequencies.sort(key=lambda t: t["exam_frequency"], reverse=True)
    for rank, item in enumerate(topic_frequencies, start=1):
        item["high_yield_rank"] = rank

    return {
        "$schema": "https://raw.githubusercontent.com/grade-a/schema/v1/exam-syllabus-matrix.json",
        "metadata": {
            "version": "1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_exams": len(exam_ids),
            "total_topics": len(topic_meta),
            "total_combinations": len(upset_combinations)
        },
        "exam_summaries": exam_summaries,
        "pairwise_metrics": pairwise_matrix,
        "topic_frequencies": topic_frequencies,
        "disjoint_upset_combinations": upset_combinations
    }


def export_syllabus_matrix(db_path: Path, tax_out_path: Path, matrix_out_path: Path) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        logger.info(f"Generating {tax_out_path.name}...")
        tax_payload = build_taxonomy_export(conn)
        atomic_write_json(tax_out_path, tax_payload)

        logger.info(f"Generating {matrix_out_path.name}...")
        matrix_payload = build_matrix_export(conn)
        atomic_write_json(matrix_out_path, matrix_payload)

        logger.info("Export pipeline completed successfully.")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Export Syllabus Taxonomy and Overlap Matrix to JSON.")
    parser.add_argument("--db", default="data/grade_a_exams.db", help="Path to SQLite DB")
    parser.add_argument("--tax-out", default="data/syllabus_taxonomy.json", help="Taxonomy JSON destination")
    parser.add_argument("--matrix-out", default="data/exam_syllabus_matrix.json", help="Matrix JSON destination")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / args.db if not os.path.isabs(args.db) else Path(args.db)
    tax_out_path = project_root / args.tax_out if not os.path.isabs(args.tax_out) else Path(args.tax_out)
    matrix_out_path = project_root / args.matrix_out if not os.path.isabs(args.matrix_out) else Path(args.matrix_out)

    export_syllabus_matrix(db_path, tax_out_path, matrix_out_path)


if __name__ == "__main__":
    main()
