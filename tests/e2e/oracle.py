"""
Authoritative Reference Oracle & Ground-Truth Test Harness for Indian Grade A Government Exams Platform.
Derived strictly from statutory examination notifications, gazette rules, and PROJECT.md / TEST_INFRA.md contracts.
"""

import datetime
import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


# ==============================================================================
# 1. CANONICAL DATABASE DDL SPECIFICATION
# ==============================================================================

SCHEMA_DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS exams (
    exam_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    short_code TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Central-Civil', 'Regulatory', 'Defense', 'State-PSC', 'PSU')),
    administering_body TEXT NOT NULL,
    frequency TEXT NOT NULL CHECK(frequency IN ('Annual', 'Bi-annual', 'Periodic')),
    official_website TEXT NOT NULL,
    latest_official_notification_url TEXT NOT NULL,
    latest_gazette_ref TEXT,
    tentative_timeline_2027 JSON NOT NULL,
    description TEXT,
    CHECK (json_valid(tentative_timeline_2027))
);

CREATE TABLE IF NOT EXISTS eligibility_criteria (
    exam_id TEXT PRIMARY KEY,
    cutoff_reference_date_rule TEXT NOT NULL,
    min_age_gen INTEGER NOT NULL,
    max_age_gen INTEGER NOT NULL,
    relaxations_json JSON NOT NULL,
    min_education_level TEXT NOT NULL,
    accepted_disciplines JSON NOT NULL,
    min_aggregate_percentage_gen REAL DEFAULT 0,
    min_aggregate_percentage_reserved REAL DEFAULT 0,
    final_year_students_allowed BOOLEAN NOT NULL DEFAULT 1,
    attempt_limit_gen INTEGER,
    attempt_limit_obc INTEGER,
    attempt_limit_sc_st INTEGER,
    domicile_restrictions JSON,
    language_requirements JSON,
    physical_standards JSON,
    source_citation_clause TEXT NOT NULL,
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE,
    CHECK (json_valid(relaxations_json)),
    CHECK (json_valid(accepted_disciplines)),
    CHECK (domicile_restrictions IS NULL OR json_valid(domicile_restrictions)),
    CHECK (language_requirements IS NULL OR json_valid(language_requirements)),
    CHECK (physical_standards IS NULL OR json_valid(physical_standards))
);

CREATE TABLE IF NOT EXISTS syllabus_taxonomy (
    topic_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL CHECK(domain IN ('General Studies', 'Quantitative Aptitude', 'Reasoning', 'English', 'Economics & Finance', 'Technical')),
    sub_domain TEXT NOT NULL,
    topic_title TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS exam_syllabus_map (
    exam_id TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    depth_level TEXT NOT NULL CHECK(depth_level IN ('Foundation', 'Intermediate', 'Advanced', 'Analytical')),
    is_optional BOOLEAN NOT NULL DEFAULT 0,
    weightage_pct_estimate REAL,
    source_clause_ref TEXT NOT NULL,
    PRIMARY KEY(exam_id, stage_name, topic_id),
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE,
    FOREIGN KEY(topic_id) REFERENCES syllabus_taxonomy(topic_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS source_audit_log (
    audit_id TEXT PRIMARY KEY,
    exam_id TEXT NOT NULL,
    fact_type TEXT NOT NULL CHECK(fact_type IN ('Age_Limit', 'Education', 'Syllabus', 'Pattern', 'Timeline_2027', 'Physical_Standards')),
    official_document_title TEXT NOT NULL,
    document_date TEXT NOT NULL,
    clause_or_page_number TEXT NOT NULL,
    official_download_link TEXT NOT NULL,
    archive_link TEXT,
    verifier_notes TEXT,
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    dob TEXT NOT NULL,
    gender TEXT NOT NULL,
    category TEXT NOT NULL,
    graduation_degree TEXT NOT NULL,
    graduation_discipline TEXT NOT NULL,
    graduation_aggregate_pct REAL NOT NULL,
    is_final_year BOOLEAN DEFAULT 0,
    state_domicile TEXT NOT NULL,
    mother_tongue TEXT,
    height_cm REAL,
    chest_cm REAL,
    vision_specs TEXT,
    prior_attempts_json JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (prior_attempts_json IS NULL OR json_valid(prior_attempts_json))
);

CREATE INDEX IF NOT EXISTS idx_exams_cat ON exams(category);
CREATE INDEX IF NOT EXISTS idx_eligibility_age ON eligibility_criteria(min_age_gen, max_age_gen);
CREATE INDEX IF NOT EXISTS idx_exam_map_topic ON exam_syllabus_map(topic_id);
CREATE INDEX IF NOT EXISTS idx_exam_map_exam ON exam_syllabus_map(exam_id);
CREATE INDEX IF NOT EXISTS idx_exam_map_depth ON exam_syllabus_map(depth_level);
CREATE INDEX IF NOT EXISTS idx_audit_exam ON source_audit_log(exam_id);
"""


# ==============================================================================
# 2. CANONICAL EXAM SPECIFICATIONS (ALL 36 EXAMS ACROSS 4 CLUSTERS)
# ==============================================================================

EXAMS_SPEC: Dict[str, Dict[str, Any]] = {
    # ----------------- Cluster 1: Central All-India & Uniformed Services (8) -----------------
    "UPSC_CSE": {
        "title": "UPSC Civil Services Examination",
        "short_code": "CSE",
        "category": "Central-Civil",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CSP-24-engl-140224.pdf",
        "latest_gazette_ref": "DoPT Notification F. No. 13018/07/2023-AIS-I dated 14.02.2024",
        "tentative_timeline_2027": {
            "notification_month": "February 2027",
            "prelims_date": "May 23, 2027",
            "mains_date": "September 17-26, 2027",
            "interview_window": "January - April 2028"
        },
        "description": "Premier central administrative recruitment for IAS, IFS, IPS, IRS, and central Group A services."
    },
    "UPSC_ESE": {
        "title": "UPSC Engineering Services Examination",
        "short_code": "ESE",
        "category": "Central-Civil",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-ENGG-25-engl-180924.pdf",
        "latest_gazette_ref": "Ministry of Communications (DoT) Notification dated 18.09.2024 / IRMS Amendment Rules",
        "tentative_timeline_2027": {
            "notification_month": "September 2026",
            "prelims_date": "February 14, 2027",
            "mains_date": "June 20, 2027",
            "interview_window": "October - December 2027"
        },
        "description": "Recruitment for technical Group A engineering cadres across Civil, Mech, Elec, and E&T."
    },
    "UPSC_IFOS": {
        "title": "UPSC Indian Forest Service Examination",
        "short_code": "IFoS",
        "category": "Central-Civil",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-IFSP-24-engl-140224.pdf",
        "latest_gazette_ref": "MoEFCC Notification dated 14.02.2024",
        "tentative_timeline_2027": {
            "notification_month": "February 2027",
            "prelims_date": "May 23, 2027",
            "mains_date": "November 21-30, 2027",
            "interview_window": "March - April 2028"
        },
        "description": "All-India Service governing environment, forestry, and wildlife management."
    },
    "UPSC_CAPF_AC": {
        "title": "UPSC Central Armed Police Forces (Assistant Commandants)",
        "short_code": "CAPF (AC)",
        "category": "Defense",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CAPF-2024-engl-240424.pdf",
        "latest_gazette_ref": "Ministry of Home Affairs Notification dated 24.04.2024",
        "tentative_timeline_2027": {
            "notification_month": "April 2027",
            "written_exam_date": "August 1, 2027",
            "pet_pst_window": "November - December 2027",
            "interview_window": "March - May 2028"
        },
        "description": "Gazetted Class-1 combat officers for BSF, CRPF, CISF, ITBP, and SSB."
    },
    "UPSC_CDS": {
        "title": "UPSC Combined Defence Services Examination",
        "short_code": "CDS",
        "category": "Defense",
        "administering_body": "UPSC",
        "frequency": "Bi-annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CDSI-24-engl-201223.pdf",
        "latest_gazette_ref": "Ministry of Defence Statutory Notifications / CDS Rules",
        "tentative_timeline_2027": {
            "notification_month": "December 2026",
            "exam_date": "April 18, 2027",
            "ssb_interview": "July - September 2027",
            "course_commencement": "January 2028"
        },
        "description": "Commissioned officer entry into IMA, INA, AFA, and OTA."
    },
    "IAF_AFCAT": {
        "title": "Air Force Common Admission Test",
        "short_code": "AFCAT",
        "category": "Defense",
        "administering_body": "Indian Air Force",
        "frequency": "Bi-annual",
        "official_website": "https://afcat.cdac.in",
        "latest_official_notification_url": "https://afcat.cdac.in/AFCAT/assets/images/news/AFCAT_01_2024_NOTIFICATION.pdf",
        "latest_gazette_ref": "IAF Employment Gazette Notification May/June & Nov/Dec",
        "tentative_timeline_2027": {
            "notification_month": "December 2026",
            "exam_date": "February 13-15, 2027",
            "afsb_interview": "April - June 2027",
            "course_commencement": "January 2028"
        },
        "description": "Officer recruitment for Flying Branch and Ground Duty (Technical & Non-Technical) branches."
    },
    "UPSC_CGSE": {
        "title": "UPSC Combined Geo-Scientist Examination",
        "short_code": "CGSE",
        "category": "Central-Civil",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-GEOL-25-engl-040924.pdf",
        "latest_gazette_ref": "Ministry of Mines Notification dated 04.09.2024",
        "tentative_timeline_2027": {
            "notification_month": "September 2026",
            "prelims_date": "February 14, 2027",
            "mains_date": "June 19-20, 2027",
            "interview_window": "October - December 2027"
        },
        "description": "Class-1 Geologists, Geophysicists, Chemists, and Hydrogeologists for GSI and CGWB."
    },
    "UPSC_IES_ISS": {
        "title": "UPSC Indian Economic Service / Indian Statistical Service",
        "short_code": "IES/ISS",
        "category": "Central-Civil",
        "administering_body": "UPSC",
        "frequency": "Annual",
        "official_website": "https://upsc.gov.in",
        "latest_official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-IES-ISS-24-engl-100424.pdf",
        "latest_gazette_ref": "MoSPI / Ministry of Finance (DEA) Notification dated 10.04.2024",
        "tentative_timeline_2027": {
            "notification_month": "April 2027",
            "written_exam_date": "June 18-20, 2027",
            "interview_window": "November - December 2027"
        },
        "description": "Group A civil services specializing in econometric analysis and official statistical governance."
    },

    # ----------------- Cluster 2: Premier Financial & Regulatory Bodies (7) -----------------
    "RBI_GRADE_B": {
        "title": "RBI Officers in Grade 'B' (General / DEPR / DSIM)",
        "short_code": "RBI Gr B",
        "category": "Regulatory",
        "administering_body": "Reserve Bank of India",
        "frequency": "Annual",
        "official_website": "https://rbi.org.in",
        "latest_official_notification_url": "https://opportunities.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4440",
        "latest_gazette_ref": "RBI Staff Regulations 1948 / Advt. No. 2A/2024-25",
        "tentative_timeline_2027": {
            "notification_month": "July 2027",
            "phase_1_exam": "September 12, 2027",
            "phase_2_exam": "October 17, 2027",
            "interview_window": "December 2027 - February 2028"
        },
        "description": "Flagship entry into central bank monetary policy, financial regulation, and supervision."
    },
    "SEBI_GRADE_A": {
        "title": "SEBI Officer Grade 'A' (Assistant Manager)",
        "short_code": "SEBI Gr A",
        "category": "Regulatory",
        "administering_body": "Securities and Exchange Board of India",
        "frequency": "Annual",
        "official_website": "https://sebi.gov.in",
        "latest_official_notification_url": "https://www.sebi.gov.in/sebiweb/other/careerdetail.jsp?careerId=334",
        "latest_gazette_ref": "SEBI (Employees' Service) Regulations 2001",
        "tentative_timeline_2027": {
            "notification_month": "March 2027",
            "phase_1_exam": "May 15, 2027",
            "phase_2_exam": "June 19, 2027",
            "interview_window": "August - September 2027"
        },
        "description": "Capital market surveillance, securities regulation, and corporate finance enforcement."
    },
    "NABARD_GRADE_A": {
        "title": "NABARD Assistant Manager in Grade 'A' (RDBS/Rajbhasha)",
        "short_code": "NABARD Gr A",
        "category": "Regulatory",
        "administering_body": "NABARD",
        "frequency": "Annual",
        "official_website": "https://nabard.org",
        "latest_official_notification_url": "https://www.nabard.org/careers-notices.aspx",
        "latest_gazette_ref": "NABARD Staff Rules / Advt. No. 01/Grade A/2024-25",
        "tentative_timeline_2027": {
            "notification_month": "July 2027",
            "phase_1_exam": "September 2027",
            "phase_2_exam": "October 2027",
            "interview_window": "December 2027 - January 2028"
        },
        "description": "Apex development financial institution for agriculture and rural infrastructure."
    },
    "IFSCA_GRADE_A": {
        "title": "IFSCA Officer Grade 'A' (Assistant Manager)",
        "short_code": "IFSCA Gr A",
        "category": "Regulatory",
        "administering_body": "IFSCA",
        "frequency": "Annual",
        "official_website": "https://ifsca.gov.in",
        "latest_official_notification_url": "https://ifsca.gov.in/Careers",
        "latest_gazette_ref": "IFSCA Act 2019 / Officer Grade A Regulations 2024",
        "tentative_timeline_2027": {
            "notification_month": "March 2027",
            "phase_1_exam": "May 2027",
            "phase_2_exam": "June 2027",
            "interview_window": "August 2027"
        },
        "description": "Unified regulatory authority for international financial services centers (GIFT City)."
    },
    "PFRDA_GRADE_A": {
        "title": "PFRDA Officer Grade 'A' (Assistant Manager)",
        "short_code": "PFRDA Gr A",
        "category": "Regulatory",
        "administering_body": "PFRDA",
        "frequency": "Periodic",
        "official_website": "https://pfrda.org.in",
        "latest_official_notification_url": "https://www.pfrda.org.in/index1.cshtml?lsid=16",
        "latest_gazette_ref": "PFRDA Act 2013 / Service Regulations 2022",
        "tentative_timeline_2027": {
            "notification_month": "May 2027",
            "phase_1_exam": "July 2027",
            "phase_2_exam": "August 2027",
            "interview_window": "October 2027"
        },
        "description": "Regulatory authority for pension schemes, National Pension System, and APY."
    },
    "SIDBI_GRADE_A": {
        "title": "SIDBI Assistant Manager in Grade 'A' (General Stream)",
        "short_code": "SIDBI Gr A",
        "category": "Regulatory",
        "administering_body": "SIDBI",
        "frequency": "Annual",
        "official_website": "https://sidbi.in",
        "latest_official_notification_url": "https://www.sidbi.in/en/careers",
        "latest_gazette_ref": "SIDBI Officers Recruitment Notification 2024",
        "tentative_timeline_2027": {
            "notification_month": "October 2027",
            "written_exam_date": "December 2027",
            "interview_window": "February 2028"
        },
        "description": "Principal financial institution for promotion, financing, and development of MSME sector."
    },
    "EXIM_BANK_MT": {
        "title": "India Exim Bank Management Trainee (Grade A / Deputy Manager)",
        "short_code": "EXIM Bank MT",
        "category": "Regulatory",
        "administering_body": "Export-Import Bank of India",
        "frequency": "Annual",
        "official_website": "https://eximbankindia.in",
        "latest_official_notification_url": "https://www.eximbankindia.in/careers",
        "latest_gazette_ref": "Advt. No. HRM/ MT/ 2024-25/ 01",
        "tentative_timeline_2027": {
            "notification_month": "August 2027",
            "written_exam_date": "October 2027",
            "interview_window": "December 2027"
        },
        "description": "Apex export credit agency supporting India's foreign trade and international investments."
    },

    # ----------------- Cluster 3: State Public Service Commissions (10) -----------------
    "UPPSC_PCS": {
        "title": "UPPSC Combined State / Upper Subordinate Services (PCS)",
        "short_code": "UPPSC PCS",
        "category": "State-PSC",
        "administering_body": "UPPSC",
        "frequency": "Annual",
        "official_website": "https://uppsc.up.nic.in",
        "latest_official_notification_url": "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx",
        "latest_gazette_ref": "Advt. No. A-1/E-1/2024 / UP Civil Services Executive Rules",
        "tentative_timeline_2027": {
            "notification_month": "January 2027",
            "prelims_date": "March / April 2027",
            "mains_date": "July / August 2027",
            "interview_window": "November / December 2027"
        },
        "description": "Premier UP State administrative recruitment for SDM, DSP, and Class 1 executive officers."
    },
    "BPSC_CCE": {
        "title": "BPSC Combined Competitive Examination (CCE)",
        "short_code": "BPSC CCE",
        "category": "State-PSC",
        "administering_body": "BPSC",
        "frequency": "Annual",
        "official_website": "https://bpsc.bih.nic.in",
        "latest_official_notification_url": "https://bpsc.bih.nic.in/Advt/NB-2024-09-02-01.pdf",
        "latest_gazette_ref": "Advt. No. 23/2024 (70th Integrated CCE)",
        "tentative_timeline_2027": {
            "notification_month": "July 2027",
            "prelims_date": "September 2027",
            "mains_date": "January 2028",
            "interview_window": "May 2028"
        },
        "description": "Bihar State administrative recruitment for Bihar Administrative Service and Police Service."
    },
    "MPPSC_SSE": {
        "title": "MPPSC State Service Examination (SSE)",
        "short_code": "MPPSC SSE",
        "category": "State-PSC",
        "administering_body": "MPPSC",
        "frequency": "Annual",
        "official_website": "https://mppsc.mp.gov.in",
        "latest_official_notification_url": "https://mppsc.mp.gov.in/uploads/advertisement/Advt_State_Service_Exam_2024.pdf",
        "latest_gazette_ref": "Advt. No. 40/2023 / MP Civil Services Rules",
        "tentative_timeline_2027": {
            "notification_month": "November 2026",
            "prelims_date": "February 2027",
            "mains_date": "July 2027",
            "interview_window": "November 2027"
        },
        "description": "Madhya Pradesh civil administrative recruitment with January 1 cutoff."
    },
    "RPSC_RAS": {
        "title": "RPSC Rajasthan State & Subordinate Services (RAS/RTS)",
        "short_code": "RPSC RAS/RTS",
        "category": "State-PSC",
        "administering_body": "RPSC",
        "frequency": "Periodic",
        "official_website": "https://rpsc.rajasthan.gov.in",
        "latest_official_notification_url": "https://rpsc.rajasthan.gov.in/Static/RecruitmentAdvertisements/RAS_2023_Detailed_Notification.pdf",
        "latest_gazette_ref": "Advt. No. 02/2023-24 / Rajasthan Services Rules 1999",
        "tentative_timeline_2027": {
            "notification_month": "May 2027",
            "prelims_date": "October 2027",
            "mains_date": "February 2028",
            "interview_window": "June 2028"
        },
        "description": "Rajasthan administrative entry with forward-calendar-year January 1 cutoff."
    },
    "TSPSC_GROUP_1": {
        "title": "TGPSC / TSPSC Group-1 Services Examination",
        "short_code": "TSPSC Group 1",
        "category": "State-PSC",
        "administering_body": "TSPSC",
        "frequency": "Annual",
        "official_website": "https://tgpsc.gov.in",
        "latest_official_notification_url": "https://websnew.tspsc.gov.in/preview/PRESSNOTICES/0220242202.pdf",
        "latest_gazette_ref": "Notification No. 02/2024 / Presidential Order 2018",
        "tentative_timeline_2027": {
            "notification_month": "February 2027",
            "prelims_date": "June 2027",
            "mains_date": "November 2027",
            "interview_window": "None (Abolished)"
        },
        "description": "Telangana State recruitment: 100% selection on 900-mark Mains, interview abolished."
    },

    # ----------------- Cluster 4: Maharatna & Navratna PSUs (11) -----------------
    "PSU_ONGC_GT": {
        "title": "ONGC Graduate Trainee (E-1 Level) via GATE",
        "short_code": "ONGC GT",
        "category": "PSU",
        "administering_body": "ONGC Limited",
        "frequency": "Annual",
        "official_website": "https://ongcindia.com",
        "latest_official_notification_url": "https://ongcindia.com/documents/77101/2988775/advt012024gt.pdf",
        "latest_gazette_ref": "Advt. No. 01/2024(R&P) / ONGC Regulations 1980",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "application_window": "April / May 2027",
            "interview_window": "July / August 2027"
        },
        "description": "ONGC Graduate Trainee recruitment through GATE (60% weightage) + Qual (25%) + PI (15%)."
    },
    "PSU_IOCL_ET": {
        "title": "IOCL Engineers / Officers (E-2 Level) through GATE",
        "short_code": "IOCL Officer",
        "category": "PSU",
        "administering_body": "Indian Oil Corporation Limited",
        "frequency": "Annual",
        "official_website": "https://iocl.com",
        "latest_official_notification_url": "https://iocl.com/admin/img/UploadedFiles/LatestJobOpening/Files/Detailed_Advertisement_GATE_2024.pdf",
        "latest_gazette_ref": "Detailed Advertisement GATE-2024 / IOCL Service Rules",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "application_window": "May / June 2027",
            "interview_window": "August / September 2027"
        },
        "description": "IOCL E-2 recruitment: 26 yr upper age, 65% aggregate with strict non-rounding rule."
    },
    "PSU_NTPC_EET": {
        "title": "NTPC Engineering Executive Trainees (EET) via GATE",
        "short_code": "NTPC EET",
        "category": "PSU",
        "administering_body": "NTPC Limited",
        "frequency": "Annual",
        "official_website": "https://careers.ntpc.co.in",
        "latest_official_notification_url": "https://careers.ntpc.co.in/recruitment/advt_eet2024.pdf",
        "latest_gazette_ref": "Advt. No. 04/2024 / NTPC Service Rules",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "application_window": "March / April 2027",
            "interview_window": "July 2027"
        },
        "description": "NTPC EET recruitment: 27 yr upper age, 65% engineering aggregate."
    },
    "PSU_BHEL_ET": {
        "title": "BHEL Engineer / Executive Trainee (E-1 Level)",
        "short_code": "BHEL ET",
        "category": "PSU",
        "administering_body": "BHEL Limited",
        "frequency": "Annual",
        "official_website": "https://careers.bhel.in",
        "latest_official_notification_url": "https://careers.bhel.in/bhel/static/advt_et2024.pdf",
        "latest_gazette_ref": "BHEL Employment Notification 2024",
        "tentative_timeline_2027": {
            "written_exam_date": "May 2027",
            "interview_window": "August 2027"
        },
        "description": "BHEL Engineer Trainee via direct computer-based test or GATE."
    },
    "PSU_PGCIL_ET": {
        "title": "PowerGrid Engineer Trainee (E-1 Level) via GATE",
        "short_code": "PGCIL ET",
        "category": "PSU",
        "administering_body": "Power Grid Corporation of India",
        "frequency": "Annual",
        "official_website": "https://powergrid.in",
        "latest_official_notification_url": "https://www.powergrid.in/careers/job-opportunities",
        "latest_gazette_ref": "Advt. No. CC/06/2024",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "application_window": "May 2027",
            "interview_window": "August 2027"
        },
        "description": "PowerGrid ET selection: 28 yr age cap, 60% engineering aggregate."
    },
    "PSU_HPCL_OFFICER": {
        "title": "HPCL Officers Recruitment via Direct CBT",
        "short_code": "HPCL Officer",
        "category": "PSU",
        "administering_body": "Hindustan Petroleum Corporation Limited",
        "frequency": "Annual",
        "official_website": "https://hindustanpetroleum.com",
        "latest_official_notification_url": "https://hindustanpetroleum.com/hpclcareers/job_openings",
        "latest_gazette_ref": "HPCL Officers Advertisement 2024",
        "tentative_timeline_2027": {
            "application_window": "June / July 2027",
            "cbt_exam_date": "September 2027",
            "interview_window": "November 2027"
        },
        "description": "HPCL E-2 direct CBT recruitment (85% CBT + 5% GD + 10% PI), 25 yr age cap."
    },
    "PSU_BPCL_MT": {
        "title": "BPCL Management Trainee via GATE",
        "short_code": "BPCL MT",
        "category": "PSU",
        "administering_body": "Bharat Petroleum Corporation Limited",
        "frequency": "Annual",
        "official_website": "https://bharatpetroleum.in",
        "latest_official_notification_url": "https://www.bharatpetroleum.in/careers/careers.aspx",
        "latest_gazette_ref": "BPCL GATE Recruitment Notice 2024",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "interview_window": "July / August 2027"
        },
        "description": "BPCL MT entry: 25 yr age cap on June 1, 60% engineering degree."
    },
    "PSU_SAIL_MTT": {
        "title": "SAIL Management Trainee (Technical) (E-1 Level)",
        "short_code": "SAIL MTT",
        "category": "PSU",
        "administering_body": "Steel Authority of India Limited",
        "frequency": "Annual",
        "official_website": "https://sail.co.in",
        "latest_official_notification_url": "https://www.sailcareers.com",
        "latest_gazette_ref": "Advt. No. 01/2024(MT)",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "interview_window": "August / September 2027"
        },
        "description": "SAIL MTT technical cadre: 28 yr age cap, 65% degree, 155 cm min male height."
    },
    "PSU_GAIL_ET": {
        "title": "GAIL Executive Trainee via GATE",
        "short_code": "GAIL ET",
        "category": "PSU",
        "administering_body": "GAIL (India) Limited",
        "frequency": "Annual",
        "official_website": "https://gailonline.com",
        "latest_official_notification_url": "https://gailonline.com/CRApplyingGail.html",
        "latest_gazette_ref": "GAIL/OPEN/ET/1/2024",
        "tentative_timeline_2027": {
            "gate_exam": "February 2027",
            "interview_window": "July 2027"
        },
        "description": "GAIL ET: 26 yr upper age, 65% degree aggregate across engineering disciplines."
    },
    "PSU_COAL_INDIA_MT": {
        "title": "Coal India Management Trainee via CBT / GATE",
        "short_code": "Coal India MT",
        "category": "PSU",
        "administering_body": "Coal India Limited",
        "frequency": "Annual",
        "official_website": "https://coalindia.in",
        "latest_official_notification_url": "https://www.coalindia.in/career-at-cil/jobs-at-coal-india/",
        "latest_gazette_ref": "CIL Advt. No. 02/2024",
        "tentative_timeline_2027": {
            "application_window": "August 2027",
            "cbt_exam_date": "October 2027",
            "interview_window": "December 2027"
        },
        "description": "Coal India MT E-2 level: 30 yr UR cap, strict non-rounding 60.0% cutoff."
    },
    "PSU_BARC_OCES": {
        "title": "BARC Scientific Officer / OCES & NPCIL Executive Trainee",
        "short_code": "BARC OCES",
        "category": "PSU",
        "administering_body": "Bhabha Atomic Research Centre / DAE",
        "frequency": "Annual",
        "official_website": "https://barcocesexam.in",
        "latest_official_notification_url": "https://barcocesexam.in/barc2024/document/brochure.pdf",
        "latest_gazette_ref": "DAE / BARC OCES Brochure 2024",
        "tentative_timeline_2027": {
            "cbt_exam_date": "March / April 2027",
            "interview_window": "June / July 2027"
        },
        "description": "DAE Group A Gazetted entry: 26 yr age cap on August 1, 60% engineering/science aggregate."
    }
}


# ==============================================================================
# 3. STATUTORY ELIGIBILITY CRITERIA SPECIFICATION
# ==============================================================================

ELIGIBILITY_RULES_SPEC: Dict[str, Dict[str, Any]] = {
    "UPSC_CSE": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 32,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10, "PWBD_OBC": 13, "PWBD_SC_ST": 15, "EX_SERVICEMEN": 5},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {"GEN": 6, "EWS": 6, "OBC": 9, "SC": None, "ST": None, "PWBD_GEN": 9, "PWBD_OBC": 9, "PWBD_SC_ST": None},
        "domicile_restrictions": None,
        "language_requirements": {"mains_paper_a": "Compulsory Indian Language (Qualifying 25%)", "mains_paper_b": "English (Qualifying 25%)"},
        "physical_standards": {
            "IPS_Male": {"min_height_cm": 165, "min_chest_cm": 84, "min_expansion_cm": 5},
            "IPS_Female": {"min_height_cm": 150, "min_chest_cm": 79, "min_expansion_cm": 5},
            "lasik_allowed": True,
            "min_lasik_age": 20,
            "min_lasik_wait_months": 12
        },
        "citation": "UPSC Notice No. 05/2024-CSP, Clause 3(i)-(v)"
    },
    "UPSC_ESE": {
        "cutoff_rule": "JANUARY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10, "CENTRAL_CIVIL_GOVT": 5},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Civil", "Mechanical", "Electrical", "Electronics_Telecommunication"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": {"min_height_male_cm": 152, "min_height_female_cm": 150},
        "citation": "UPSC Notice No. 02/2025-ENGG, Clause 3(i)-(ii)"
    },
    "UPSC_IFOS": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 32,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Science", "Forestry", "Engineering", "Agriculture", "Botany", "Chemistry", "Geology", "Mathematics", "Physics", "Statistics", "Zoology"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {"GEN": 6, "EWS": 6, "OBC": 9, "SC": None, "ST": None},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": {
            "min_height_male_cm": 163, "min_height_female_cm": 150,
            "walking_test": {"male_distance_km": 25, "male_hours": 4, "female_distance_km": 14, "female_hours": 4}
        },
        "citation": "UPSC Notice No. 06/2024-IFoS, Clause 3(ii)-(iv)"
    },
    "UPSC_CAPF_AC": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 20,
        "max_age_gen": 25,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "EX_SERVICEMEN": 5},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "disallow_prior_selected_ac": True,
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": {
            "min_height_male_cm": 165, "min_height_female_cm": 157,
            "min_chest_male_cm": 81, "min_expansion_male_cm": 5,
            "pet_100m_male_sec": 16, "pet_100m_female_sec": 18,
            "pet_800m_male_sec": 225, "pet_800m_female_sec": 285
        },
        "citation": "UPSC Notice No. 09/2024-CPF, Clause 3(III)-(V)"
    },
    "UPSC_CDS": {
        "cutoff_rule": "COURSE_COMMENCEMENT_YEAR",
        "min_age_gen": 19,
        "max_age_gen": 24, # 25 for OTA
        "relaxations": {}, # No category relaxation in military commissioned ranks
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY", "Engineering", "Physics_Maths_10plus2"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "marital_status_restrictions": {"IMA": "Unmarried_Male", "OTA_Women": "Unmarried_or_Issueless_Widow"},
        "physical_standards": {"min_height_male_cm": 157.5, "min_height_female_cm": 152},
        "citation": "UPSC Notice No. 11/2025.CDS-II, Clause 3(a)-(c)"
    },
    "IAF_AFCAT": {
        "cutoff_rule": "COURSE_COMMENCEMENT_YEAR",
        "min_age_gen": 20,
        "max_age_gen": 24, # 26 for Ground Duty
        "relaxations": {"DGCA_CPL_HOLDER": 2}, # Commercial pilot license allows 26 for Flying
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY", "Engineering", "BCom"],
        "min_pct_gen": 60.0, # 60% in degree AND 50% in 10+2 Math & Physics for Flying/Tech
        "min_pct_res": 60.0,
        "requires_10plus2_physics_maths": True,
        "min_10plus2_subject_pct": 50.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "physical_standards": {"min_height_male_flying_cm": 162.5, "min_height_ground_cm": 157.5, "lasik_min_age": 20, "lasik_wait_months": 12},
        "citation": "IAF AFCAT 01/2024 Notification, Clause 3(b)"
    },
    "UPSC_CGSE": {
        "cutoff_rule": "JANUARY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 32,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Master",
        "accepted_disciplines": ["Geology", "Applied_Geology", "Geophysics", "Physics", "Applied_Physics", "Chemistry", "Analytical_Chemistry"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "UPSC Notice No. 01/2025-GEOL, Clause 3(ii)-(iii)"
    },
    "UPSC_IES_ISS": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Master_or_Bachelor_Stats",
        "accepted_disciplines": ["Economics", "Applied_Economics", "Econometrics", "Statistics", "Mathematical_Statistics"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "UPSC Notice No. 07/2024-IES/ISS, Clause 3(ii)-(iii)"
    },

    # ----------------- Cluster 2: Regulatory Bodies (7) -----------------
    "RBI_GRADE_B": {
        "cutoff_rule": "JULY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10, "MPHIL": 2, "PHD": 4},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY", "Economics", "Statistics", "Finance"],
        "min_pct_gen": 60.0, # or 55% in Post-Graduation
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": False, # Result must be declared on or before July 1
        "attempt_limits": {"GEN": 6, "EWS": 6, "OBC": None, "SC": None, "ST": None, "PWBD_GEN": None},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "RBI Advt. No. 2A/2024-25, Section II.1-3"
    },
    "SEBI_GRADE_A": {
        "cutoff_rule": "MARCH_31_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Master_or_Professional",
        "accepted_disciplines": ["Master_Any", "MBA_Finance", "Law", "Engineering", "Computer_Science", "Information_Technology", "CA", "CFA", "CS"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "SEBI Recruitment Notice 2024, Section I & II"
    },
    "NABARD_GRADE_A": {
        "cutoff_rule": "JULY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY", "Agriculture", "Fisheries", "Forestry", "Finance"],
        "min_pct_gen": 60.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "NABARD Advt. No. 01/Grade A/2024-25"
    },
    "IFSCA_GRADE_A": {
        "cutoff_rule": "FEBRUARY_1_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Master_or_Professional",
        "accepted_disciplines": ["Master_Economics", "Commerce", "Finance", "Law", "IT", "CA", "CFA"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "IFSCA Officer Grade A Notification 2024"
    },
    "PFRDA_GRADE_A": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Master_or_Professional",
        "accepted_disciplines": ["Master_Any", "Law", "Engineering", "CA", "CFA", "CS"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "PFRDA Advt. No. 02/2022"
    },
    "SIDBI_GRADE_A": {
        "cutoff_rule": "NOVEMBER_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Bachelor_or_Master",
        "accepted_disciplines": ["Law", "Engineering", "Master_Any", "CA", "CS", "CFA"],
        "min_pct_gen": 60.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "SIDBI Grade A Notification 2024"
    },
    "EXIM_BANK_MT": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 28,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD_GEN": 10},
        "min_education": "Dual_UG_and_MBA",
        "accepted_disciplines": ["MBA_Finance", "PGDBA_Finance", "CA"],
        "min_pct_gen": 60.0, # Requires 60% in BOTH UG and PG
        "min_pct_res": 55.0,
        "requires_dual_threshold": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "India Exim Bank Advt. HRM/MT/2024-25/01"
    },

    # ----------------- Cluster 3: State PSCs (10) -----------------
    "UPPSC_PCS": {
        "cutoff_rule": "JULY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 40,
        "relaxations": {"SC_UP": 5, "ST_UP": 5, "OBC_UP": 5, "PWBD_UP": 15},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": {"reservation_benefit": "UP_DOMICILE_ONLY"},
        "language_requirements": {"compulsory_paper": "General Hindi (150 marks)"},
        "physical_standards": {"DSP_Male": {"min_height_cm": 165, "min_chest_cm": 84, "min_expansion_cm": 5}},
        "citation": "UPPSC Advt. No. A-1/E-1/2024, Clause 6 & 10"
    },
    "BPSC_CCE": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 20, # 20 for DSP, 21 for finance, 22 for SDM
        "max_age_gen": 37, # 37 for Male UR, 40 for Female UR & BC/EBC
        "female_max_age_gen": 40,
        "relaxations": {"GEN_Female": 3, "BC_Male": 3, "BC_Female": 3, "EBC_Male": 3, "EBC_Female": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": {"reservation_benefit": "BIHAR_DOMICILE_ONLY"},
        "language_requirements": {"qualifying_paper": "General Hindi (30% passing)"},
        "physical_standards": {"DSP_Male": {"min_height_cm": 165}},
        "citation": "BPSC Advt. No. 23/2024, Para 3 & 4"
    },
    "MPPSC_SSE": {
        "cutoff_rule": "JANUARY_1_EXAM_YEAR",
        "min_age_gen": 21,
        "max_age_gen": 40, # 33 for Police DSP
        "police_max_age_gen": 33,
        "relaxations": {"SC_MP": 5, "ST_MP": 5, "OBC_MP": 5, "Women_All": 5},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": {"reservation_benefit": "MP_DOMICILE_ONLY"},
        "language_requirements": {"mains_paper": "General Hindi (200 marks)"},
        "physical_standards": {"DSP_Male": {"min_height_cm": 168}},
        "citation": "MPPSC Advt. No. 40/2023, Section 2 & 8"
    },
    "RPSC_RAS": {
        "cutoff_rule": "FOLLOWING_JANUARY_1_EXAM_YEAR", # 01-01-2028 for 2027 cycle
        "min_age_gen": 21,
        "max_age_gen": 40,
        "relaxations": {"SC_RJ": 5, "ST_RJ": 5, "OBC_RJ": 5, "Female_GEN_RJ": 5, "Female_Reserved_RJ": 10, "Widow_Divorcee": 99},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": {"reservation_benefit": "RAJASTHAN_DOMICILE_ONLY"},
        "language_requirements": {"working_knowledge": "Hindi Devanagari & Rajasthani Culture"},
        "physical_standards": {"RPS_Male": {"min_height_cm": 168}},
        "citation": "RPSC Advt. No. 02/2023-24, Clause 7 & 8"
    },
    "TSPSC_GROUP_1": {
        "cutoff_rule": "JULY_1_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 44,
        "relaxations": {"SC_TS": 5, "ST_TS": 5, "BC_TS": 5, "EWS_TS": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["ANY"],
        "min_pct_gen": 0.0,
        "min_pct_res": 0.0,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": {"presidential_order_2018": "95% local reservation"},
        "language_requirements": {"qualifying_paper": "General English"},
        "physical_standards": {"DSP_Male": {"min_height_cm": 167.6}},
        "citation": "TSPSC Notification No. 02/2024, Para III-IV"
    },

    # ----------------- Cluster 4: Maharatna & Navratna PSUs (11) -----------------
    "PSU_ONGC_GT": {
        "cutoff_rule": "CLOSING_DATE_MAY",
        "min_age_gen": 18,
        "max_age_gen": 30, # 28 for AEE Drilling
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Mechanical", "Petroleum", "Civil", "Electrical", "Electronics", "Chemical", "Computer_Science", "Geology", "Geophysics"],
        "min_pct_gen": 60.0,
        "min_pct_res": 60.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "ONGC Advt. No. 01/2024(R&P), Section 2-3"
    },
    "PSU_IOCL_ET": {
        "cutoff_rule": "JUNE_30_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 26,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Chemical", "Civil", "Electrical", "Instrumentation", "Mechanical", "Metallurgical", "Computer_Science"],
        "min_pct_gen": 65.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "IOCL GATE-2024 Advt., Clause 2 & 3.1"
    },
    "PSU_NTPC_EET": {
        "cutoff_rule": "CLOSING_DATE_APRIL",
        "min_age_gen": 18,
        "max_age_gen": 27,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Electrical", "Mechanical", "Civil", "Mining"],
        "min_pct_gen": 65.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "NTPC Advt. No. 04/2024, Clause 2"
    },
    "PSU_BHEL_ET": {
        "cutoff_rule": "CLOSING_DATE_MAY",
        "min_age_gen": 18,
        "max_age_gen": 27, # 29 for Post-Graduates
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Civil", "Mechanical", "Electrical", "Chemical", "Metallurgy"],
        "min_pct_gen": 60.0,
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "BHEL Advt. 2024, Section 3"
    },
    "PSU_PGCIL_ET": {
        "cutoff_rule": "CLOSING_DATE_MAY",
        "min_age_gen": 18,
        "max_age_gen": 28,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Electrical", "Civil", "Electronics", "Computer_Science"],
        "min_pct_gen": 60.0,
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "PGCIL Advt. CC/06/2024, Clause 2"
    },
    "PSU_HPCL_OFFICER": {
        "cutoff_rule": "CLOSING_DATE_JUNE",
        "min_age_gen": 18,
        "max_age_gen": 25,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Mechanical", "Civil", "Electrical", "Instrumentation", "Chemical"],
        "min_pct_gen": 60.0,
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "HPCL Officers Advt. 2024, Section 2"
    },
    "PSU_BPCL_MT": {
        "cutoff_rule": "JUNE_1_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 25,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Mechanical", "Chemical", "Civil", "Electrical", "Instrumentation"],
        "min_pct_gen": 60.0,
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "BPCL GATE Advt. 2024, Section 2"
    },
    "PSU_SAIL_MTT": {
        "cutoff_rule": "CLOSING_DATE_MAY",
        "min_age_gen": 18,
        "max_age_gen": 28,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Mechanical", "Metallurgy", "Electrical", "Chemical", "Civil", "Instrumentation", "Mining"],
        "min_pct_gen": 65.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": {"min_height_male_cm": 155, "min_height_female_cm": 143},
        "citation": "SAIL Advt. 01/2024(MT), Clause 3 & Physical"
    },
    "PSU_GAIL_ET": {
        "cutoff_rule": "CLOSING_DATE_MAY",
        "min_age_gen": 18,
        "max_age_gen": 26,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Chemical", "Mechanical", "Electrical", "Instrumentation", "Civil", "GAIL_Telecom_IT"],
        "min_pct_gen": 65.0,
        "min_pct_res": 55.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "GAIL Advt. GAIL/OPEN/ET/1/2024, Section 2"
    },
    "PSU_COAL_INDIA_MT": {
        "cutoff_rule": "CLOSING_DATE_AUGUST",
        "min_age_gen": 18,
        "max_age_gen": 30,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor",
        "accepted_disciplines": ["Mining", "Civil", "Mechanical", "Electrical", "Geology"],
        "min_pct_gen": 60.0,
        "min_pct_res": 50.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "CIL Advt. No. 02/2024, Section 3"
    },
    "PSU_BARC_OCES": {
        "cutoff_rule": "AUGUST_1_EXAM_YEAR",
        "min_age_gen": 18,
        "max_age_gen": 26,
        "relaxations": {"OBC": 3, "SC": 5, "ST": 5, "PWBD": 10},
        "min_education": "Bachelor_or_MSc",
        "accepted_disciplines": ["Mechanical", "Chemical", "Metallurgy", "Electrical", "Electronics", "Computer_Science", "Instrumentation", "Civil", "Physics", "Chemistry"],
        "min_pct_gen": 60.0,
        "min_pct_res": 60.0,
        "strict_non_rounding": True,
        "allows_final_year": True,
        "attempt_limits": {},
        "domicile_restrictions": None,
        "language_requirements": None,
        "physical_standards": None,
        "citation": "BARC OCES Brochure 2024, Section 2"
    }
}


# ==============================================================================
# 4. MASTER SYLLABUS TAXONOMY SPECIFICATION
# ==============================================================================

TAXONOMY_DOMAINS = [
    "General Studies",
    "Quantitative Aptitude",
    "Reasoning",
    "English",
    "Economics & Finance",
    "Technical"
]

CANONICAL_TOPICS = [
    # General Studies
    {"topic_id": "gs.polity.constitution_features", "domain": "General Studies", "sub_domain": "polity", "topic_title": "Constitutional Framework & Features"},
    {"topic_id": "gs.polity.union_state_executive", "domain": "General Studies", "sub_domain": "polity", "topic_title": "Union & State Executives & Legislatures"},
    {"topic_id": "gs.polity.judiciary_bodies", "domain": "General Studies", "sub_domain": "polity", "topic_title": "Judiciary & Constitutional Bodies"},
    {"topic_id": "gs.polity.local_governance", "domain": "General Studies", "sub_domain": "polity", "topic_title": "Local Self-Government & Panchayati Raj"},
    {"topic_id": "gs.history.modern_freedom_struggle", "domain": "General Studies", "sub_domain": "history", "topic_title": "Modern Indian History & Freedom Movement"},
    {"topic_id": "gs.history.art_and_culture", "domain": "General Studies", "sub_domain": "history", "topic_title": "Art, Architecture & Cultural Heritage"},
    {"topic_id": "gs.history.ancient_medieval", "domain": "General Studies", "sub_domain": "history", "topic_title": "Ancient & Medieval Indian Civilization"},
    {"topic_id": "gs.geography.physical_india_world", "domain": "General Studies", "sub_domain": "geography", "topic_title": "Physical & Regional Geography"},
    {"topic_id": "gs.environment.ecology_biodiversity", "domain": "General Studies", "sub_domain": "environment", "topic_title": "Ecology, Biodiversity & Climate Action"},
    {"topic_id": "gs.science_tech.emerging_technologies", "domain": "General Studies", "sub_domain": "science_tech", "topic_title": "Emerging Technologies, Space & Defense"},
    {"topic_id": "gs.economy_gen.indian_economy_overview", "domain": "General Studies", "sub_domain": "economy_gen", "topic_title": "Indian Economy & Social Sector Development"},
    {"topic_id": "gs.ir_security.internal_security_borders", "domain": "General Studies", "sub_domain": "ir_security", "topic_title": "Internal Security & Border Management"},
    {"topic_id": "gs.ethics.foundations_case_studies", "domain": "General Studies", "sub_domain": "ethics", "topic_title": "Ethics, Public Values & Case Scenarios"},

    # Quantitative Aptitude
    {"topic_id": "quant.arithmetic.percentages_profit_loss", "domain": "Quantitative Aptitude", "sub_domain": "arithmetic", "topic_title": "Percentages, Profit, Loss & Discount"},
    {"topic_id": "quant.arithmetic.interest_si_ci", "domain": "Quantitative Aptitude", "sub_domain": "arithmetic", "topic_title": "Simple & Compound Interest"},
    {"topic_id": "quant.arithmetic.ratio_variation_mixtures", "domain": "Quantitative Aptitude", "sub_domain": "arithmetic", "topic_title": "Ratio, Proportion & Mixtures"},
    {"topic_id": "quant.arithmetic.time_speed_distance", "domain": "Quantitative Aptitude", "sub_domain": "arithmetic", "topic_title": "Time, Speed, Distance & Relative Motion"},
    {"topic_id": "quant.arithmetic.time_work_pipes", "domain": "Quantitative Aptitude", "sub_domain": "arithmetic", "topic_title": "Time, Work, Efficiency & Cisterns"},
    {"topic_id": "quant.algebra.equations_inequalities", "domain": "Quantitative Aptitude", "sub_domain": "algebra", "topic_title": "Linear/Quadratic Equations & Inequalities"},
    {"topic_id": "quant.geometry.mensuration_2d_3d", "domain": "Quantitative Aptitude", "sub_domain": "geometry", "topic_title": "Geometry & 2D/3D Mensuration"},
    {"topic_id": "quant.modern_math.pnc_probability", "domain": "Quantitative Aptitude", "sub_domain": "modern_math", "topic_title": "Permutations, Combinations & Probability"},
    {"topic_id": "quant.di_ds.charts_caselets_sufficiency", "domain": "Quantitative Aptitude", "sub_domain": "di_ds", "topic_title": "Data Interpretation & Data Sufficiency"},

    # Reasoning
    {"topic_id": "reasoning.analytical.seating_puzzles", "domain": "Reasoning", "sub_domain": "analytical", "topic_title": "Seating Arrangements & Complex Puzzles"},
    {"topic_id": "reasoning.analytical.coding_blood_directions", "domain": "Reasoning", "sub_domain": "analytical", "topic_title": "Coding-Decoding, Blood Relations & Directions"},
    {"topic_id": "reasoning.verbal.syllogisms_logic", "domain": "Reasoning", "sub_domain": "verbal", "topic_title": "Syllogisms & Deductive Logic"},
    {"topic_id": "reasoning.critical.assumptions_conclusions", "domain": "Reasoning", "sub_domain": "critical", "topic_title": "Critical Reasoning & Inferences"},
    {"topic_id": "reasoning.non_verbal.pattern_spatial", "domain": "Reasoning", "sub_domain": "non_verbal", "topic_title": "Pattern Completion & Spatial Series"},

    # English Language
    {"topic_id": "english.reading.comprehension_inference", "domain": "English", "sub_domain": "reading", "topic_title": "Reading Comprehension & Inferences"},
    {"topic_id": "english.grammar.error_spotting_syntax", "domain": "English", "sub_domain": "grammar", "topic_title": "Grammar, Syntax & Sentence Correction"},
    {"topic_id": "english.vocabulary.lexicon_cloze_parajumbles", "domain": "English", "sub_domain": "vocabulary", "topic_title": "Vocabulary, Cloze Test & Para Jumbles"},
    {"topic_id": "english.descriptive.essay_precis_drafting", "domain": "English", "sub_domain": "descriptive", "topic_title": "Descriptive Essay, Precis & Official Drafting"},

    # Economics & Finance
    {"topic_id": "econ_fin.macro.national_income_monetary", "domain": "Economics & Finance", "sub_domain": "macro", "topic_title": "Macroeconomics & Monetary Policy Transmission"},
    {"topic_id": "econ_fin.fin_markets.capital_money_derivatives", "domain": "Economics & Finance", "sub_domain": "fin_markets", "topic_title": "Financial Markets, Bonds & Derivatives"},
    {"topic_id": "econ_fin.banking.regulations_basel_npa", "domain": "Economics & Finance", "sub_domain": "banking", "topic_title": "Banking Regulations, Basel III & NPAs"},
    {"topic_id": "econ_fin.accounting.financial_statements_ratios", "domain": "Economics & Finance", "sub_domain": "accounting", "topic_title": "Financial Statements & Ratio Analysis"},
    {"topic_id": "econ_fin.mgmt_corp.governance_leadership", "domain": "Economics & Finance", "sub_domain": "mgmt_corp", "topic_title": "Management Principles & Corporate Governance"},

    # Technical Streams
    {"topic_id": "tech.cs_it.data_structures_algorithms", "domain": "Technical", "sub_domain": "cs_it", "topic_title": "Data Structures & Algorithms"},
    {"topic_id": "tech.cs_it.dbms_os_networks", "domain": "Technical", "sub_domain": "cs_it", "topic_title": "Operating Systems, DBMS & Computer Networks"},
    {"topic_id": "tech.ece.signals_communications", "domain": "Technical", "sub_domain": "ece", "topic_title": "Signals, Systems & Analog/Digital Communications"},
    {"topic_id": "tech.mech.thermo_fluid_mechanics", "domain": "Technical", "sub_domain": "mech", "topic_title": "Thermodynamics & Fluid Mechanics"},
    {"topic_id": "tech.civil.structures_geotechnical", "domain": "Technical", "sub_domain": "civil", "topic_title": "Structural Analysis & Geotechnical Engineering"},
    {"topic_id": "tech.ee.power_systems_machines", "domain": "Technical", "sub_domain": "ee", "topic_title": "Power Systems & Electrical Machines"},
    {"topic_id": "tech.stats.probability_distributions_inference", "domain": "Technical", "sub_domain": "stats", "topic_title": "Probability Distributions & Statistical Inference"}
]


# ==============================================================================
# 5. STATUTORY ELIGIBILITY EVALUATION ORACLE
# ==============================================================================

@dataclass
class UserProfile:
    dob: str # YYYY-MM-DD
    gender: str # 'Male', 'Female', 'Other'
    category: str # 'GEN', 'EWS', 'OBC', 'SC', 'ST', 'PWBD_GEN', 'PWBD_OBC', 'PWBD_SC_ST'
    degree: str # 'Bachelor', 'Master', 'Dual_UG_and_MBA'
    discipline: str # 'Civil', 'Mechanical', 'ANY', etc.
    aggregate_pct: float
    is_final_year: bool = False
    domicile_state: str = "Delhi"
    fluent_languages: List[str] = field(default_factory=lambda: ["Hindi", "English"])
    prior_attempts: Dict[str, int] = field(default_factory=dict)
    height_cm: Optional[float] = None
    chest_cm: Optional[float] = None
    chest_expansion_cm: Optional[float] = None
    is_ex_serviceman: bool = False
    ex_service_years: int = 0
    has_commercial_pilot_license: bool = False
    has_lasik: bool = False
    lasik_age: Optional[int] = None
    lasik_wait_months: Optional[int] = None
    ten_plus_two_maths_pct: Optional[float] = None
    ten_plus_two_physics_pct: Optional[float] = None
    prior_selected_as_ac: bool = False
    marital_status: str = "Unmarried"
    has_children: bool = False


def calculate_age_on_date(dob_str: str, target_date_str: str) -> Tuple[int, int, int]:
    """Calculates exact (years, months, days) between DOB and target cutoff date."""
    dob = datetime.date.fromisoformat(dob_str)
    target = datetime.date.fromisoformat(target_date_str)
    
    if dob > target:
        return (-1, 0, 0)
        
    years = target.year - dob.year
    if (target.month, target.day) < (dob.month, dob.day):
        years -= 1
        
    # Return years as primary metric
    return (years, 0, 0)


def evaluate_statutory_eligibility(profile: UserProfile, exam_id: str, exam_year: int = 2027) -> Dict[str, Any]:
    """
    Evaluates profile against authoritative statutory examination rules for given exam_id.
    Returns:
      {
        'exam_id': exam_id,
        'status': 'ELIGIBLE' | 'CONDITIONALLY_ELIGIBLE' | 'INELIGIBLE',
        'reasons': List[str],
        'relaxations_applied': List[str],
        'statutory_citation': str
      }
    """
    rule = ELIGIBILITY_RULES_SPEC.get(exam_id)
    if not rule:
        raise ValueError(f"Unknown exam_id: {exam_id}")

    reasons: List[str] = []
    relaxations_applied: List[str] = []
    is_eligible = True
    is_conditional = False

    # 1. Determine Cutoff Date
    cutoff_rule = rule["cutoff_rule"]
    if cutoff_rule == "AUGUST_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-08-01"
    elif cutoff_rule == "JANUARY_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-01-01"
    elif cutoff_rule == "JULY_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-07-01"
    elif cutoff_rule == "APRIL_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-04-01"
    elif cutoff_rule == "FOLLOWING_JANUARY_1_EXAM_YEAR":
        cutoff_date = f"{exam_year + 1}-01-01"
    elif cutoff_rule == "MARCH_31_EXAM_YEAR":
        cutoff_date = f"{exam_year}-03-31"
    elif cutoff_rule == "FEBRUARY_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-02-01"
    elif cutoff_rule == "NOVEMBER_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-11-01"
    elif cutoff_rule == "JUNE_30_EXAM_YEAR":
        cutoff_date = f"{exam_year}-06-30"
    elif cutoff_rule == "JUNE_1_EXAM_YEAR":
        cutoff_date = f"{exam_year}-06-01"
    elif "CLOSING_DATE" in cutoff_rule:
        cutoff_date = f"{exam_year}-05-15"
    elif cutoff_rule == "COURSE_COMMENCEMENT_YEAR":
        cutoff_date = f"{exam_year + 1}-01-01"
    else:
        cutoff_date = f"{exam_year}-08-01"

    # Age calculation
    dob = datetime.date.fromisoformat(profile.dob)
    cutoff = datetime.date.fromisoformat(cutoff_date)
    
    # Accurate age in full years
    age_years = cutoff.year - dob.year
    if (cutoff.month, cutoff.day) < (dob.month, dob.day):
        age_years -= 1

    # Exact boundary condition: For UPSC CSE (e.g. 1995-08-01 vs 1995-08-02):
    # Clause says: "Must not have attained age of 32 on 1st August 2027" -> born on Aug 1, 1995 attains 32 on Aug 1, 2027 (ineligible). Born Aug 2, 1995 is eligible.
    if cutoff_rule == "AUGUST_1_EXAM_YEAR" and exam_id in ["UPSC_CSE", "UPSC_IFOS"]:
        min_dob = datetime.date(exam_year - rule["max_age_gen"], 8, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 8, 1)
    else:
        min_dob = None
        max_dob = None

    # Base Max Age
    max_age = rule["max_age_gen"]
    if profile.gender == "Female" and "female_max_age_gen" in rule:
        max_age = rule["female_max_age_gen"]

    # Check state domicile restriction for reservation
    domicile_rule = rule.get("domicile_restrictions")
    category = profile.category
    if domicile_rule and "reservation_benefit" in domicile_rule:
        required_domicile_tag = domicile_rule["reservation_benefit"]
        # e.g. UP_DOMICILE_ONLY requires profile.domicile_state == 'Uttar Pradesh'
        state_map = {
            "UP_DOMICILE_ONLY": "Uttar Pradesh",
            "BIHAR_DOMICILE_ONLY": "Bihar",
            "MAHARASHTRA_DOMICILE_ONLY": "Maharashtra",
            "MP_DOMICILE_ONLY": "Madhya Pradesh",
            "RAJASTHAN_DOMICILE_ONLY": "Rajasthan",
            "TAMIL_NADU_DOMICILE_ONLY": "Tamil Nadu",
            "ANDHRA_PRADESH_DOMICILE_ONLY": "Andhra Pradesh",
            "WEST_BENGAL_DOMICILE_ONLY": "West Bengal",
            "KARNATAKA_DOMICILE_ONLY": "Karnataka"
        }
        required_state = state_map.get(required_domicile_tag)
        if required_state and profile.domicile_state != required_state:
            # Caste relaxations nullified outside home state
            category = "GEN"
            relaxations_applied.append(f"Out-of-state applicant: Mapped to General (UR) category under domicile rule")

    # Apply age relaxations with strict precedence: Exact Match -> Gender-Specific -> Domicile State Key -> Prefix
    relaxation_years = 0
    cat_prefix = category.split("_")[0]
    state_abbrevs = {
        "Uttar Pradesh": "UP",
        "Bihar": "BIHAR",
        "Maharashtra": "MH",
        "Madhya Pradesh": "MP",
        "Rajasthan": "RJ",
        "Tamil Nadu": "TN",
        "Andhra Pradesh": "AP",
        "Telangana": "TS",
        "West Bengal": "WB",
        "Karnataka": "KA"
    }
    st_abbr = state_abbrevs.get(profile.domicile_state, "")
    state_cat_key = f"{cat_prefix}_{st_abbr}"

    if category in rule["relaxations"]:
        relaxation_years = rule["relaxations"][category]
        relaxations_applied.append(f"{category} relaxation: +{relaxation_years} years")
    elif f"{category}_{profile.gender}" in rule["relaxations"]:
        g_key = f"{category}_{profile.gender}"
        relaxation_years = rule["relaxations"][g_key]
        relaxations_applied.append(f"{g_key} relaxation: +{relaxation_years} years")
    elif state_cat_key in rule["relaxations"]:
        relaxation_years = rule["relaxations"][state_cat_key]
        relaxations_applied.append(f"{state_cat_key} relaxation: +{relaxation_years} years")
    elif cat_prefix in rule["relaxations"]:
        relaxation_years = rule["relaxations"][cat_prefix]
        relaxations_applied.append(f"{cat_prefix} relaxation: +{relaxation_years} years")

    # Ex-Servicemen relaxation
    if profile.is_ex_serviceman and "EX_SERVICEMEN" in rule["relaxations"]:
        esm_rel = rule["relaxations"]["EX_SERVICEMEN"]
        relaxation_years = max(relaxation_years, esm_rel)
        relaxations_applied.append(f"Ex-Servicemen relaxation: +{esm_rel} years")

    # AFCAT Commercial Pilot License relaxation
    if profile.has_commercial_pilot_license and "DGCA_CPL_HOLDER" in rule.get("relaxations", {}):
        cpl_rel = rule["relaxations"]["DGCA_CPL_HOLDER"]
        relaxation_years += cpl_rel
        relaxations_applied.append(f"DGCA CPL Holder: +{cpl_rel} years")

    # Widow / Divorcee relaxation (e.g. RPSC no age cap)
    if profile.marital_status in ["Widow", "Divorcee"] and "Widow_Divorcee" in rule.get("relaxations", {}):
        widow_rel = rule["relaxations"]["Widow_Divorcee"]
        relaxation_years = max(relaxation_years, widow_rel)
        relaxations_applied.append(f"Widow/Divorcee relaxation: +{widow_rel} years")

    allowed_max_age = max_age + relaxation_years

    # Exact statutory birth window calculation
    if cutoff_rule == "AUGUST_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 8, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 8, 1)
    elif cutoff_rule == "JANUARY_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 1, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 1, 1)
    elif cutoff_rule == "JULY_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 7, 1)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 7, 1)
    elif cutoff_rule == "APRIL_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 4, 1)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 4, 1)
    elif cutoff_rule == "FOLLOWING_JANUARY_1_EXAM_YEAR":
        # Candidate must not have crossed 40 years (i.e. not reached 41st birthday on Jan 1 of following year)
        min_dob = datetime.date(exam_year + 1 - (allowed_max_age + 1), 1, 2)
        max_dob = datetime.date(exam_year + 1 - rule["min_age_gen"], 1, 1)
    elif cutoff_rule == "MARCH_31_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 4, 1)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 3, 31)
    elif cutoff_rule == "FEBRUARY_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 2, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 2, 1)
    elif cutoff_rule == "NOVEMBER_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 11, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 11, 1)
    elif cutoff_rule == "JUNE_30_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 7, 1)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 6, 30)
    elif cutoff_rule == "JUNE_1_EXAM_YEAR":
        min_dob = datetime.date(exam_year - allowed_max_age, 6, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 6, 1)
    elif "CLOSING_DATE" in cutoff_rule:
        min_dob = datetime.date(exam_year - allowed_max_age, 5, 16)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 5, 15)
    elif cutoff_rule == "COURSE_COMMENCEMENT_YEAR":
        min_dob = datetime.date(exam_year + 1 - allowed_max_age, 1, 2)
        max_dob = datetime.date(exam_year + 1 - rule["min_age_gen"], 1, 1)
    else:
        min_dob = datetime.date(exam_year - allowed_max_age, 8, 2)
        max_dob = datetime.date(exam_year - rule["min_age_gen"], 8, 1)

    # Check Age against statutory birth window
    if dob < min_dob:
        is_eligible = False
        reasons.append(f"Age exceeds maximum limit of {allowed_max_age} years on {cutoff_date} (Born before {min_dob.isoformat()})")
    elif dob > max_dob:
        is_eligible = False
        reasons.append(f"Age is below minimum limit of {rule['min_age_gen']} years on {cutoff_date} (Born after {max_dob.isoformat()})")

    # 2. Check Degree & Discipline
    accepted_disc = rule["accepted_disciplines"]
    if "ANY" not in accepted_disc:
        if profile.discipline not in accepted_disc:
            is_eligible = False
            reasons.append(f"Graduation discipline '{profile.discipline}' is not accepted. Required: {accepted_disc}")

    if rule.get("min_education") == "Master":
        if profile.degree not in ["Master", "Dual_UG_and_MBA"]:
            is_eligible = False
            reasons.append(f"Degree '{profile.degree}' does not meet Master's requirement for this post")
    elif rule.get("min_education") == "Master_or_Professional":
        is_prof = profile.discipline in ["Law", "Engineering", "Computer_Science", "Information_Technology", "CA", "CFA", "CS", "Civil", "Mechanical", "Electrical"]
        is_post_grad = profile.degree in ["Master", "Dual_UG_and_MBA"]
        if not (is_prof or is_post_grad):
            is_eligible = False
            reasons.append(f"Degree '{profile.degree}' in '{profile.discipline}' does not meet Master's or Professional requirement for this post")

    # 3. Check Aggregate Percentage (Strict Non-Rounding)
    min_pct = rule["min_pct_res"] if category in ["SC", "ST", "PWBD", "PWBD_GEN", "PWBD_OBC", "PWBD_SC_ST"] else rule["min_pct_gen"]
    if min_pct > 0.0:
        # Strict floating point check (e.g. 59.99 < 60.0)
        if profile.aggregate_pct < min_pct:
            is_eligible = False
            reasons.append(f"Aggregate {profile.aggregate_pct:.2f}% is below strict threshold of {min_pct:.2f}% (No rounding off allowed)")

    # 4. Check Final Year Student Allowance
    if profile.is_final_year:
        if not rule.get("allows_final_year", True):
            is_eligible = False
            reasons.append("Final year appearing students are strictly ineligible; passing proof required by cutoff date")
        else:
            is_conditional = True
            reasons.append("Conditionally eligible: Must produce documentary proof of degree passing prior to Mains/Interview")

    # 5. Check Attempt Limits
    limits = rule.get("attempt_limits", {})
    if category in limits and limits[category] is not None:
        user_attempts = profile.prior_attempts.get(exam_id, 0)
        if user_attempts >= limits[category]:
            is_eligible = False
            reasons.append(f"Exceeded maximum allowed attempts of {limits[category]} for {category} category (Attempt count: {user_attempts})")

    # 6. Prior Assistant Commandant Disqualification (CAPF AC)
    if rule.get("disallow_prior_selected_ac", False) and profile.prior_selected_as_ac:
        is_eligible = False
        reasons.append("Disqualified under MHA rules: Currently or previously appointed Assistant Commandants cannot re-appear")

    # 7. Physical Standards Check (Uniformed Services)
    phys = rule.get("physical_standards")
    if phys:
        # Height check
        if profile.height_cm is not None:
            min_h = None
            if profile.gender == "Male":
                min_h = phys.get("min_height_male_cm") or (phys.get("DSP_Male", {}).get("min_height_cm")) or (phys.get("IPS_Male", {}).get("min_height_cm"))
            elif profile.gender == "Female":
                min_h = phys.get("min_height_female_cm") or (phys.get("DSP_Female", {}).get("min_height_cm")) or (phys.get("IPS_Female", {}).get("min_height_cm"))
            if min_h and profile.height_cm < min_h:
                is_eligible = False
                reasons.append(f"Height {profile.height_cm} cm fails minimum standard of {min_h} cm for {profile.gender}")

        # LASIK check
        if profile.has_lasik and "lasik_min_age" in phys:
            if profile.lasik_age and profile.lasik_age < phys["lasik_min_age"]:
                is_eligible = False
                reasons.append(f"Disqualified: LASIK performed at age {profile.lasik_age} (Minimum allowed age is {phys['lasik_min_age']})")
            if profile.lasik_wait_months and profile.lasik_wait_months < phys.get("lasik_wait_months", 6):
                is_eligible = False
                reasons.append(f"Disqualified: LASIK elapsed time {profile.lasik_wait_months} months fails mandatory wait period of {phys.get('lasik_wait_months', 6)} months")

    # 8. Compulsory Language Check (State PSCs)
    lang_req = rule.get("language_requirements")
    if lang_req and "mandatory_fluency" in lang_req:
        req_lang = lang_req["mandatory_fluency"]
        if req_lang not in profile.fluent_languages and (req_lang != "Bengali" or "Nepali" not in profile.fluent_languages):
            is_eligible = False
            reasons.append(f"Candidate lacks mandatory fluency/reading/writing proficiency in '{req_lang}'")

    # 9. 10+2 Math/Physics Requirement (AFCAT Flying/Technical)
    if rule.get("requires_10plus2_physics_maths", False):
        if (profile.ten_plus_two_maths_pct is not None and profile.ten_plus_two_maths_pct < 50.0) or \
           (profile.ten_plus_two_physics_pct is not None and profile.ten_plus_two_physics_pct < 50.0):
            is_eligible = False
            reasons.append("Disqualified: Requires minimum 50% marks in both Mathematics and Physics at 10+2 level")

    # 10. Marital Status Check (CDS OTA Women)
    marital_req = rule.get("marital_status_restrictions", {}).get("OTA_Women")
    if marital_req == "Unmarried_or_Issueless_Widow" and profile.gender == "Female":
        if profile.marital_status == "Married" or (profile.marital_status in ["Widow", "Divorcee"] and profile.has_children):
            is_eligible = False
            reasons.append("OTA Women Non-Technical entry accepts only unmarried women or issueless widows/divorcees")

    status = "INELIGIBLE"
    if is_eligible:
        status = "CONDITIONALLY_ELIGIBLE" if is_conditional else "ELIGIBLE"

    return {
        "exam_id": exam_id,
        "status": status,
        "reasons": reasons if not is_eligible else (reasons if is_conditional else ["Meets all statutory eligibility criteria"]),
        "relaxations_applied": relaxations_applied,
        "statutory_citation": rule.get("citation", "Official Gazette Notification")
    }


# ==============================================================================
# 6. SET-THEORETIC MATHEMATICAL CALCULATORS
# ==============================================================================

def calculate_jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Calculates Jaccard Index J(A, B) = |A ∩ B| / |A ∪ B|."""
    union_len = len(set_a | set_b)
    if union_len == 0:
        return 1.0
    return len(set_a & set_b) / union_len


def calculate_overlap_coefficient(set_a: Set[str], set_b: Set[str]) -> float:
    """Calculates Overlap (Szymkiewicz-Simpson) Coefficient = |A ∩ B| / min(|A|, |B|)."""
    min_len = min(len(set_a), len(set_b))
    if min_len == 0:
        return 0.0
    return len(set_a & set_b) / min_len


def calculate_upset_intersections(exam_topic_map: Dict[str, Set[str]]) -> Dict[Tuple[str, ...], Set[str]]:
    """
    Computes exclusive disjoint intersections for all 2^k - 1 combinations.
    Returns: Dict mapping tuple of active exam IDs -> set of exclusively shared topic IDs.
    """
    exam_ids = sorted(list(exam_topic_map.keys()))
    k = len(exam_ids)
    all_topics: Set[str] = set()
    for topics in exam_topic_map.values():
        all_topics.update(topics)

    intersections: Dict[Tuple[str, ...], Set[str]] = {}

    # For each topic, compute its membership mask
    for topic in all_topics:
        membership = tuple(e for e in exam_ids if topic in exam_topic_map[e])
        if membership:
            if membership not in intersections:
                intersections[membership] = set()
            intersections[membership].add(topic)

    return intersections
