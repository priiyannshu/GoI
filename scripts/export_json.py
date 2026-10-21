#!/usr/bin/env python3
"""
scripts/export_json.py
======================
High-Performance Master JSON Export Pipeline for the Indian Grade A Examinations Platform.

Exports:
1. Complete relational database (exams, eligibility_criteria, source_audit_log, exam_syllabus_map)
   into a clean, fully denormalized JSON artifact (`data/grade_a_exams.json`).
2. Structured metadata, cluster distribution counts, and category aggregations.
3. Precomputed D3.js visualization indexes (set combinations and cluster sets).
4. Atomic writing via temporary file replacement (`.tmp` -> `.json`) and post-write JSON validation.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Canonical Cluster Grouping Mapping
CLUSTER_MAP = {
    "UPSC_CSE": "Cluster 1: Central All-India & Uniformed",
    "UPSC_ESE": "Cluster 1: Central All-India & Uniformed",
    "UPSC_IFOS": "Cluster 1: Central All-India & Uniformed",
    "UPSC_CAPF_AC": "Cluster 1: Central All-India & Uniformed",
    "UPSC_CDS": "Cluster 1: Central All-India & Uniformed",
    "IAF_AFCAT": "Cluster 1: Central All-India & Uniformed",

    "RBI_GRADE_B": "Cluster 2: Premier Financial & Regulatory",
    "NABARD_GRADE_A": "Cluster 2: Premier Financial & Regulatory",
    "SIDBI_GRADE_A": "Cluster 2: Premier Financial & Regulatory",

    "UPPSC_PCS": "Cluster 3: State Public Service Commissions",
    "BPSC_CCE": "Cluster 3: State Public Service Commissions",
    "MPPSC_SSE": "Cluster 3: State Public Service Commissions",
    "RPSC_RAS": "Cluster 3: State Public Service Commissions",
    "TSPSC_GROUP_1": "Cluster 3: State Public Service Commissions",

    "PSU_ONGC_GT": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_IOCL_ET": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_NTPC_EET": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_BHEL_ET": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_PGCIL_ET": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_HPCL_OFFICER": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_BPCL_MT": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_SAIL_MTT": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_GAIL_ET": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_COAL_INDIA_MT": "Cluster 4: Maharatna & Navratna PSUs",
    "PSU_BARC_NPCIL_ET": "Cluster 4: Maharatna & Navratna PSUs",
}


def safe_json_loads(val: Any) -> Any:
    """Safely parses JSON strings or returns fallback."""
    if val is None:
        return None
    if isinstance(val, (dict, list)):
        return val
    try:
        return json.loads(val)
    except Exception:
        return None


def export_database_to_json(db_path: str, out_path: str, indent: int = 2) -> None:
    """Extracts master SQLite database into hierarchical JSON payload."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")

    conn = sqlite3.connect(f"file:{os.path.abspath(db_path)}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Fetch all eligibility criteria mapped by exam_id
    cursor.execute("SELECT * FROM eligibility_criteria;")
    elig_rows = {row["exam_id"]: row for row in cursor.fetchall()}

    # 2. Fetch all source audit records grouped by exam_id
    cursor.execute("SELECT * FROM source_audit_log ORDER BY fact_type, audit_id;")
    audit_rows: Dict[str, List[Dict[str, Any]]] = {}
    for row in cursor.fetchall():
        eid = row["exam_id"]
        audit_rows.setdefault(eid, []).append({
            "audit_id": row["audit_id"],
            "fact_type": row["fact_type"],
            "official_document_title": row["official_document_title"],
            "document_date": row["document_date"],
            "clause_or_page_number": row["clause_or_page_number"],
            "official_download_link": row["official_download_link"],
            "archive_link": row["archive_link"] if "archive_link" in row.keys() else None,
            "verifier_notes": row["verifier_notes"] if "verifier_notes" in row.keys() else None,
        })

    # 3. Fetch syllabus mappings if populated
    syllabus_map: Dict[str, List[Dict[str, Any]]] = {}
    try:
        cursor.execute("SELECT * FROM exam_syllabus_map ORDER BY stage_name, topic_id;")
        for row in cursor.fetchall():
            eid = row["exam_id"]
            syllabus_map.setdefault(eid, []).append({
                "stage_name": row["stage_name"],
                "topic_id": row["topic_id"],
                "depth_level": row["depth_level"],
                "is_optional": bool(row["is_optional"]),
                "weightage_pct_estimate": row["weightage_pct_estimate"] if "weightage_pct_estimate" in row.keys() else None,
                "source_clause_ref": row["source_clause_ref"] if "source_clause_ref" in row.keys() else None
            })
    except sqlite3.OperationalError:
        pass  # Table might be empty or missing in minimal scenarios

    # 4. Fetch all exams and build denormalized objects
    cursor.execute("SELECT * FROM exams ORDER BY category, exam_id;")
    exams_out = []
    category_counts: Dict[str, int] = {}
    cluster_counts: Dict[str, int] = {}

    for row in cursor.fetchall():
        eid = row["exam_id"]
        cat = row["category"]
        cluster_name = CLUSTER_MAP.get(eid, f"Other: {cat}")

        category_counts[cat] = category_counts.get(cat, 0) + 1
        cluster_counts[cluster_name] = cluster_counts.get(cluster_name, 0) + 1

        # Build eligibility sub-object
        elig_data = elig_rows.get(eid)
        elig_obj = None
        if elig_data:
            elig_obj = {
                "cutoff_reference_date_rule": elig_data["cutoff_reference_date_rule"],
                "min_age_gen": elig_data["min_age_gen"],
                "max_age_gen": elig_data["max_age_gen"],
                "relaxations": safe_json_loads(elig_data["relaxations_json"]),
                "min_education_level": elig_data["min_education_level"],
                "accepted_disciplines": safe_json_loads(elig_data["accepted_disciplines"]),
                "min_aggregate_percentage_gen": elig_data["min_aggregate_percentage_gen"],
                "min_aggregate_percentage_reserved": elig_data["min_aggregate_percentage_reserved"],
                "final_year_students_allowed": bool(elig_data["final_year_students_allowed"]),
                "attempt_limit_gen": elig_data["attempt_limit_gen"],
                "attempt_limit_obc": elig_data["attempt_limit_obc"],
                "attempt_limit_sc_st": elig_data["attempt_limit_sc_st"],
                "domicile_restrictions": safe_json_loads(elig_data["domicile_restrictions"]),
                "language_requirements": safe_json_loads(elig_data["language_requirements"]),
                "physical_standards": safe_json_loads(elig_data["physical_standards"]),
                "source_citation_clause": elig_data["source_citation_clause"]
            }

        exam_obj = {
            "exam_id": eid,
            "title": row["title"],
            "short_code": row["short_code"],
            "category": cat,
            "cluster": cluster_name,
            "administering_body": row["administering_body"],
            "frequency": row["frequency"],
            "official_website": row["official_website"],
            "latest_official_notification_url": row["latest_official_notification_url"],
            "latest_gazette_ref": row["latest_gazette_ref"] if "latest_gazette_ref" in row.keys() else None,
            "tentative_timeline_2027": safe_json_loads(row["tentative_timeline_2027"]),
            "description": row["description"] if "description" in row.keys() else None,
            "eligibility": elig_obj,
            "audit_trail": audit_rows.get(eid, []),
            "syllabus_stages": syllabus_map.get(eid, [])
        }
        exams_out.append(exam_obj)

    conn.close()

    # 5. Precompute D3 Set Visualization Index
    all_exam_ids = [e["exam_id"] for e in exams_out]
    visualization_index = {
        "all_exam_ids": all_exam_ids,
        "clusters": {
            "Cluster_1_Central_Uniformed": [eid for eid, cl in CLUSTER_MAP.items() if "Cluster 1" in cl],
            "Cluster_2_Regulatory_Financial": [eid for eid, cl in CLUSTER_MAP.items() if "Cluster 2" in cl],
            "Cluster_3_State_PSC": [eid for eid, cl in CLUSTER_MAP.items() if "Cluster 3" in cl],
            "Cluster_4_PSU": [eid for eid, cl in CLUSTER_MAP.items() if "Cluster 4" in cl]
        }
    }

    # 6. Assemble Full Master Payload
    master_payload = {
        "$schema": "https://raw.githubusercontent.com/grade-a/schema/v1/exam-export.json",
        "metadata": {
            "version": "1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "scripts/export_json.py",
            "database_source": os.path.relpath(db_path),
            "total_exams": len(exams_out),
            "cluster_distribution": cluster_counts,
            "category_distribution": category_counts
        },
        "exams": exams_out,
        "d3_visualization_index": visualization_index
    }

    # 7. Atomic Write via Temporary File
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    temp_path = f"{out_path}.tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=indent, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())

    # 8. Post-Write Syntax Validation Check
    with open(temp_path, "r", encoding="utf-8") as f:
        json.load(f)

    # Atomic Rename
    os.replace(temp_path, out_path)
    file_size_bytes = os.path.getsize(out_path)

    print(f"Export successful: {len(exams_out)} examinations exported to {out_path}")
    print(f"File size: {file_size_bytes:,} bytes")
    print(f"Clusters: {cluster_counts}")
    print(f"Categories: {category_counts}")


def main():
    parser = argparse.ArgumentParser(description="Export Grade A Exams Relational Database to JSON")
    parser.add_argument("--db", default="data/grade_a_exams.db", help="Path to source SQLite database")
    parser.add_argument("--out", default="data/grade_a_exams.json", help="Path to destination JSON file")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation level")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, args.db) if not os.path.isabs(args.db) else args.db
    out_path = os.path.join(project_root, args.out) if not os.path.isabs(args.out) else args.out

    try:
        export_database_to_json(db_path, out_path, indent=args.indent)
    except Exception as e:
        print(f"Error exporting database to JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
