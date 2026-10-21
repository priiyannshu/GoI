#!/usr/bin/env python3
"""
scripts/build_curriculum_dataset.py
===================================
Constructs the authoritative, aspirant-first examination scheme and syllabus
curriculum dataset for all 32 audited examinations in the Government of India platform.
Outputs to:
  - frontend/src/data/exam_curriculum_data.json
"""

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../frontend/src/data/exam_curriculum_data.json")

def create_dataset():
    data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "metadata": {
            "version": "2.0.0",
            "updated_at": "2026-10-21T19:54:00Z",
            "total_exams_schemed": 32,
            "description": "Authoritative stage-by-stage and paper-by-paper examination schemes with official notification clause citations."
        },
        "schemes": {}
    }

    # =========================================================================
    # 1. UPSC CSE
    # =========================================================================
    data["schemes"]["UPSC_CSE"] = {
        "exam_id": "UPSC_CSE",
        "exam_title": "Civil Services Examination",
        "short_code": "CSE",
        "total_marks": 2025,
        "negative_marking_rule": "1/3rd (0.66 marks deducted) on Objective Papers (Prelims)",
        "official_notification_clause": "Appendix II, Section I & II of Gazette Notification F.No.13018/07/2023-AIS-I",
        "official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CSP-24-engl-140224.pdf",
        "stages": [
            {
                "stage_id": "prelims",
                "stage_name": "Stage I: Preliminary Examination",
                "stage_type": "Objective Screening",
                "total_stage_marks": 400,
                "description": "Screening test consisting of two objective papers. Marks in Paper I determine qualifying cutoff for Mains, while Paper II is qualifying (min 33%).",
                "papers": [
                    {
                        "paper_id": "cse_pre_p1",
                        "paper_name": "Paper I: General Studies (GS-1)",
                        "marks": 200,
                        "duration_hours": 2.0,
                        "question_type": "Objective MCQ (100 Questions)",
                        "negative_marking": "1/3rd (0.66 marks per incorrect answer)",
                        "is_qualifying": False,
                        "merit_status": "Counted for Prelims Cutoff & Merit",
                        "source_clause": "Appendix II, Section I(A) Paper-I",
                        "topics": [
                            {
                                "topic_id": "cse_pre_curr_events",
                                "title": "Current events of national and international importance",
                                "description": "Critical domestic policies, multilateral summits, geopolitical shifts, national awards, and strategic bilateral relations.",
                                "sub_points": [
                                    "National initiatives, welfare policies, and statutory schemes",
                                    "Bilateral, regional and multilateral agreements and groupings",
                                    "Major international summits, conventions, and global health/environment declarations"
                                ],
                                "weightage_estimate": "15-20% (15-20 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 1"
                            },
                            {
                                "topic_id": "cse_pre_history",
                                "title": "History of India and Indian National Movement",
                                "description": "Ancient, medieval, modern Indian history and the multi-phased Indian freedom struggle.",
                                "sub_points": [
                                    "Ancient civilization: Indus Valley, Vedic period, Mauryan and Gupta eras",
                                    "Medieval culture, Bhakti and Sufi movements, Vijayanagara and Mughal administrations",
                                    "Modern freedom struggle: 1857 Revolt to 1947 independence, Gandhian phases, revolutionary movements"
                                ],
                                "weightage_estimate": "15-18% (14-18 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 2"
                            },
                            {
                                "topic_id": "cse_pre_geography",
                                "title": "Indian and World Geography - Physical, Social, Economic",
                                "description": "Geomorphology, climatology, oceanography, biogeography, and resource distribution of India and the world.",
                                "sub_points": [
                                    "Physical geography: plate tectonics, seismic zones, monsoon dynamics, river basins",
                                    "Economic geography: key mineral reserves, agricultural cropping belts, industrial clusters",
                                    "Human & social geography: demographics, migration patterns, urbanization challenges"
                                ],
                                "weightage_estimate": "12-15% (12-15 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 3"
                            },
                            {
                                "topic_id": "cse_pre_polity",
                                "title": "Indian Polity and Governance - Constitution, Political System, Panchayati Raj",
                                "description": "Constitutional philosophy, fundamental rights, directive principles, executive, judiciary, federal structure, and public policy.",
                                "sub_points": [
                                    "Preamble, Fundamental Rights (Articles 12-35), Directive Principles, and Fundamental Duties",
                                    "Parliament, State Legislatures, Judicial Review, and Basic Structure Doctrine",
                                    "73rd & 74th Constitutional Amendment Acts (Panchayati Raj & Municipalities)",
                                    "Statutory, regulatory and constitutional bodies (ECI, CAG, UPSC, Finance Commission)"
                                ],
                                "weightage_estimate": "15-18% (15-18 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 4"
                            },
                            {
                                "topic_id": "cse_pre_economy",
                                "title": "Economic and Social Development - Sustainable Development, Poverty, Inclusion",
                                "description": "Macroeconomic aggregates, fiscal and monetary policies, banking sector reforms, budget analysis, and inclusive growth.",
                                "sub_points": [
                                    "National income accounting, GDP growth paradigms, inflation management",
                                    "Monetary Policy Committee framework, RBI instruments, banking NPA resolutions",
                                    "Union Budget, Fiscal Responsibility and Budget Management (FRBM) targets",
                                    "Poverty line estimations, multidimensional poverty, social security programmes"
                                ],
                                "weightage_estimate": "14-18% (14-18 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 5"
                            },
                            {
                                "topic_id": "cse_pre_environment",
                                "title": "General issues on Environmental Ecology, Bio-diversity and Climate Change",
                                "description": "Ecosystem dynamics, conservation treaties, national parks, wildlife protection legislation, and climate diplomacy.",
                                "sub_points": [
                                    "Terrestrial and aquatic ecosystems, food webs, ecological succession",
                                    "Wildlife Protection Act 1972, Project Tiger/Elephant, Ramsar wetland sites, Biosphere Reserves",
                                    "UNFCCC COPs, Paris Agreement NDC targets, carbon markets, renewable energy targets"
                                ],
                                "weightage_estimate": "15-20% (15-20 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 6"
                            },
                            {
                                "topic_id": "cse_pre_science",
                                "title": "General Science & Emerging Technologies",
                                "description": "Core scientific principles, space missions, biotechnology, defense technologies, and digital public infrastructure.",
                                "sub_points": [
                                    "ISRO space exploration missions (Gaganyaan, Chandrayaan, Aditya-L1)",
                                    "Biotechnology, gene editing (CRISPR), mRNA vaccines, disease transmission",
                                    "Artificial intelligence, quantum computing, semiconductors, 5G/6G architecture"
                                ],
                                "weightage_estimate": "10-12% (10-12 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 7"
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_pre_p2",
                        "paper_name": "Paper II: Civil Services Aptitude Test (CSAT)",
                        "marks": 200,
                        "duration_hours": 2.0,
                        "question_type": "Objective MCQ (80 Questions)",
                        "negative_marking": "1/3rd (0.83 marks per incorrect answer)",
                        "is_qualifying": True,
                        "qualifying_threshold_pct": 33.33,
                        "merit_status": "Qualifying Only (Min 66/200 required)",
                        "source_clause": "Appendix II, Section I(A) Paper-II",
                        "topics": [
                            {
                                "topic_id": "cse_csat_comprehension",
                                "title": "Reading Comprehension & Critical Inferences",
                                "description": "Dense passages drawn from economics, ecology, philosophy, and sociology testing analytical inference and deduction.",
                                "sub_points": [
                                    "Identification of underlying assumptions, core arguments, and logical corollaries",
                                    "Tone analysis, critical message extraction, and implication synthesis"
                                ],
                                "weightage_estimate": "30-35% (25-28 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 1"
                            },
                            {
                                "topic_id": "cse_csat_reasoning",
                                "title": "Logical Reasoning and Analytical Ability",
                                "description": "Deductive reasoning, syllogisms, relational puzzles, spatial patterns, and algorithmic decision pathways.",
                                "sub_points": [
                                    "Syllogisms, statement-conclusion, statement-assumption paradigms",
                                    "Complex seating arrangements, blood relations, direction sense tests",
                                    "Coding-decoding, sequential series, and conditional matrix puzzles"
                                ],
                                "weightage_estimate": "25-30% (20-25 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 2"
                            },
                            {
                                "topic_id": "cse_csat_numeracy",
                                "title": "Basic Numeracy & Data Interpretation (Class X Level)",
                                "description": "Arithmetic principles, number system hierarchies, permutations, probability, and quantitative data representations.",
                                "sub_points": [
                                    "Number systems: prime numbers, divisibility tests, remainders, LCM & HCF",
                                    "Percentages, profit & loss, ratio & proportion, time & work, speed & distance",
                                    "Permutations & combinations, basic probability, Venn diagrams",
                                    "Data interpretation: charts, graphs, tables, and data sufficiency"
                                ],
                                "weightage_estimate": "35-40% (30-35 questions)",
                                "source_clause": "Appendix II, Section I(A) Item 3"
                            }
                        ]
                    }
                ]
            },
            {
                "stage_id": "mains",
                "stage_name": "Stage II: Main Written Examination",
                "stage_type": "Descriptive Written",
                "total_stage_marks": 1750,
                "description": "9 conventional essay-type papers designed to test academic depth and analytical articulation. 2 qualifying language papers (300m each) + 7 merit papers (250m each).",
                "papers": [
                    {
                        "paper_id": "cse_mains_pA",
                        "paper_name": "Paper A: Compulsory Indian Language",
                        "marks": 300,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": True,
                        "qualifying_threshold_pct": 25.0,
                        "merit_status": "Qualifying Only (Min 75/300 required; not counted in rank)",
                        "source_clause": "Appendix II, Section II Paper A",
                        "topics": [
                            {
                                "topic_id": "cse_lang_comprehension",
                                "title": "Comprehension & Precis Writing in Selected 8th Schedule Language",
                                "description": "Reading comprehension, condensation of prose, idiomatic usage, and bilateral translation between English and Indian language.",
                                "sub_points": [
                                    "Comprehension of given passages with subjective answers",
                                    "Precis writing of given text into one-third length",
                                    "Usage, idioms, proverbs, and syntactic vocabulary",
                                    "Translation from English to the Indian language and vice-versa"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_pB",
                        "paper_name": "Paper B: Compulsory English",
                        "marks": 300,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": True,
                        "qualifying_threshold_pct": 25.0,
                        "merit_status": "Qualifying Only (Min 75/300 required; not counted in rank)",
                        "source_clause": "Appendix II, Section II Paper B",
                        "topics": [
                            {
                                "topic_id": "cse_eng_skills",
                                "title": "English Comprehension, Precis & Composition",
                                "description": "Tests candidate's ability to read and understand serious discursive prose and express ideas clearly and correctly in English.",
                                "sub_points": [
                                    "Comprehension of unseen passages",
                                    "Precis writing with strict adherence to word limits",
                                    "Grammar, vocabulary, correction of sentences, prepositions",
                                    "Short essay composition on contemporary themes"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p1",
                        "paper_name": "Paper I: Essay",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written (2 Essays, 1000-1200 words each)",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Paper I",
                        "topics": [
                            {
                                "topic_id": "cse_essay_philosophical",
                                "title": "Section A: Philosophical & Abstract Themes",
                                "description": "In-depth exposition on ethical aphorisms, human condition, epistemology, and socio-philosophical maxims.",
                                "sub_points": [
                                    "Epistemological inquiries, ethics, and moral philosophy",
                                    "Human values, civilization dialogues, and existential reflections"
                                ]
                            },
                            {
                                "topic_id": "cse_essay_socioeconomic",
                                "title": "Section B: Socio-Economic, Technological & Governance Themes",
                                "description": "Critical analysis of contemporary societal transformations, economic paradigms, constitutional morality, and scientific frontiers.",
                                "sub_points": [
                                    "Inclusive economic growth, agrarian distress, sustainable industrialization",
                                    "Artificial intelligence ethics, digital privacy, and governance equity"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p2",
                        "paper_name": "Paper II: General Studies I (Heritage, Culture, History & Geography)",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written (20 Questions)",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Paper II (GS-1)",
                        "topics": [
                            {
                                "topic_id": "cse_gs1_art_culture",
                                "title": "Indian Heritage, Art Forms, Literature & Architecture",
                                "description": "Evolution of architecture, sculpture, painting, music, performing arts, and classical literature from ancient to modern eras.",
                                "sub_points": [
                                    "Temple architecture: Nagara, Dravida, and Vesara styles; Buddhist rock-cut architecture",
                                    "Classical dance traditions, folk music, miniature and mural painting schools",
                                    "Sanskrit literature, Sangam poetry, Persian chronicles, and modern vernacular writings"
                                ]
                            },
                            {
                                "topic_id": "cse_gs1_modern_history",
                                "title": "Modern Indian History & Freedom Struggle (Mid-18th Century to 1947)",
                                "description": "British expansionist policies, socio-religious reform movements, emergence of nationalism, and constitutional milestones.",
                                "sub_points": [
                                    "Colonial land revenue settlements (Permanent Settlement, Ryotwari, Mahalwari) and economic drain",
                                    "19th-century socio-religious reform movements (Raja Ram Mohan Roy, Arya Samaj, Aligarh Movement)",
                                    "Phases of Freedom Struggle: Moderates, Extremists, Swadeshi, Non-Cooperation, Civil Disobedience, Quit India",
                                    "Role of prominent personalities, tribal uprisings, and peasant revolts"
                                ]
                            },
                            {
                                "topic_id": "cse_gs1_post_independence",
                                "title": "Post-Independence Consolidation and Reorganization",
                                "description": "Integration of princely states, linguistic reorganization of states, tribal consolidation, and nation-building initiatives.",
                                "sub_points": [
                                    "Sardar Patel's integration of princely states; Kashmir, Hyderabad, and Junagadh accessions",
                                    "States Reorganisation Commission (SRC 1956) and linguistic identity movements",
                                    "Early five-year plans, Green Revolution, and foreign policy non-alignment"
                                ]
                            },
                            {
                                "topic_id": "cse_gs1_world_history",
                                "title": "History of the World (18th Century to Modern Era)",
                                "description": "Major global political upheavals, ideological confrontations, industrialization, imperialism, and decolonization.",
                                "sub_points": [
                                    "Industrial Revolution, American Revolution (1776), French Revolution (1789)",
                                    "World War I, Russian Revolution (1917), Rise of Fascism and Nazism, World War II",
                                    "Cold War dynamics, dismantling of colonial empires in Asia and Africa, fall of the Soviet Union"
                                ]
                            },
                            {
                                "topic_id": "cse_gs1_society",
                                "title": "Salient Features of Indian Society, Diversity, Women & Secularism",
                                "description": "Structure of Indian society, caste hierarchy transformations, women's empowerment, regionalism, communalism, and globalization impact.",
                                "sub_points": [
                                    "Caste dynamics, kinship systems, family structures, and changing demographic profiles",
                                    "Role of women and women's organizations; female labor force participation; gender justice",
                                    "Effects of globalization on traditional culture, consumerism, and youth aspirations",
                                    "Communalism, regionalism, secularism, and social empowerment policies"
                                ]
                            },
                            {
                                "topic_id": "cse_gs1_geography",
                                "title": "Physical Geography, Resource Distribution & Geophysical Phenomena",
                                "description": "Global physical phenomena, resource geopolitics, ocean resources, and natural hazard vulnerability.",
                                "sub_points": [
                                    "Plate tectonics, volcanism, earthquakes, tsunamis, tropical cyclones",
                                    "Distribution of key natural resources (iron, coal, petroleum, lithium, rare earth elements)",
                                    "Factors determining location of primary, secondary, and tertiary sector industries globally"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p3",
                        "paper_name": "Paper III: General Studies II (Governance, Polity, Social Justice & IR)",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written (20 Questions)",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Paper III (GS-2)",
                        "topics": [
                            {
                                "topic_id": "cse_gs2_constitution",
                                "title": "Indian Constitution - Evolution, Amendments, Federalism & Separation of Powers",
                                "description": "Constitutional provisions, federal tensions, emergency provisions, judicial activism, and comparative constitutional designs.",
                                "sub_points": [
                                    "Basic Structure Doctrine evolution, landmark judicial verdicts (Kesavananda Bharati to present)",
                                    "Union-State relations: legislative, administrative, financial; role of the Governor; Inter-State Council",
                                    "Separation of powers, checks and balances, public interest litigations (PILs)",
                                    "Comparison of Indian constitutional scheme with US, UK, France, and Germany"
                                ]
                            },
                            {
                                "topic_id": "cse_gs2_parliament",
                                "title": "Parliament & State Legislatures - Functioning, Privileges & Representation of People Act",
                                "description": "Legislative conduct, committee system, decline of parliamentary debates, anti-defection law, and electoral reforms.",
                                "sub_points": [
                                    "Parliamentary committees (Public Accounts Committee, Estimates Committee, Departmentally Related Standing Committees)",
                                    "Tenth Schedule (Anti-Defection Law) challenges, disqualifications, office of profit",
                                    "Representation of the People Act 1950 & 1951: electoral financing, criminalization of politics"
                                ]
                            },
                            {
                                "topic_id": "cse_gs2_governance",
                                "title": "Governance, Transparency, Accountability & Citizen Charters",
                                "description": "E-governance paradigms, Right to Information, role of civil services in democracy, and accountability mechanisms.",
                                "sub_points": [
                                    "Right to Information Act 2005: implementation bottlenecks and recent amendments",
                                    "Citizen's Charters, Social Audits, Sevottam model, public grievance redressal mechanisms",
                                    "Role of civil services in a democracy: neutrality, commitment to constitution, Mission Karmayogi"
                                ]
                            },
                            {
                                "topic_id": "cse_gs2_social_justice",
                                "title": "Welfare Schemes, Poverty, Hunger & Social Sector (Health, Education)",
                                "description": "Human development challenges, public health infrastructure, National Education Policy, and vulnerable section protections.",
                                "sub_points": [
                                    "Issues relating to poverty, malnutrition, Global Hunger Index metrics, and PDS reforms",
                                    "Healthcare infrastructure: Ayushman Bharat, Universal Health Coverage, primary health centres",
                                    "National Education Policy 2020, foundational literacy and numeracy, higher education reforms",
                                    "Protection of SC/ST, OBC, Minorities, Divyangjan, and Senior Citizens"
                                ]
                            },
                            {
                                "topic_id": "cse_gs2_ir",
                                "title": "International Relations, India's Neighbourhood & Multilateral Fora",
                                "description": "India's foreign policy doctrines, neighborhood relations, major power engagements, and global multilateral governance.",
                                "sub_points": [
                                    "Neighborhood First Policy, Act East Policy, SAGAR doctrine, Middle East engagements",
                                    "Strategic bilateral ties: USA, Russia, China, Japan, EU; geopolitical conflicts",
                                    "Multilateral groupings: Quad, BRICS, SCO, G20, UN Security Council reforms, WTO, IMF"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p4",
                        "paper_name": "Paper IV: General Studies III (Technology, Economy, Environment & Security)",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written (20 Questions)",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Paper IV (GS-3)",
                        "topics": [
                            {
                                "topic_id": "cse_gs3_economy",
                                "title": "Indian Economy, Resource Mobilization, Budgeting & Inclusive Growth",
                                "description": "Economic survey findings, fiscal consolidation, capital expenditure cycles, GST architecture, and employment generation.",
                                "sub_points": [
                                    "Gross Value Added (GVA) trends, manufacturing revival (Make in India, PLI schemes)",
                                    "Goods and Services Tax (GST) council dynamics, fiscal federalism, direct tax reforms",
                                    "Employment generation: formalization of labor, gig economy, periodic labor force survey data"
                                ]
                            },
                            {
                                "topic_id": "cse_gs3_agriculture",
                                "title": "Agriculture, Food Processing, MSP & Land Reforms",
                                "description": "Cropping patterns, irrigation infrastructure, minimum support price debates, food subsidy burden, and supply chain logistics.",
                                "sub_points": [
                                    "Direct and indirect farm subsidies, MSP calculation methodology (A2+FL vs C2)",
                                    "Public Distribution System (PDS) efficiency, buffer stock management, NFSA targets",
                                    "Food processing industries: upstream and downstream linkages, cold storage supply chain",
                                    "Land reforms: digitization of land records (DILRMP), land leasing frameworks"
                                ]
                            },
                            {
                                "topic_id": "cse_gs3_science_tech",
                                "title": "Science & Technology Indigenization, Space, IT & IPR",
                                "description": "Indigenous technological breakthroughs, space missions, semiconductor manufacturing, robotics, and patent laws.",
                                "sub_points": [
                                    "National Quantum Mission, India Semiconductor Mission, AI computational clusters",
                                    "Space sector reforms: IN-SPACe, private participation, deep space missions",
                                    "Intellectual Property Rights (IPR) regime, patent litigation, Compulsory Licensing"
                                ]
                            },
                            {
                                "topic_id": "cse_gs3_environment_disaster",
                                "title": "Environmental Conservation, Pollution & Disaster Management Framework",
                                "description": "National Clean Air Programme, circular economy, renewable energy transitions, and Sendai Framework implementation.",
                                "sub_points": [
                                    "Air and water pollution control, plastic waste management rules, River Ganga rejuvenation",
                                    "Panchamrit climate goals (500 GW non-fossil capacity, Net Zero 2070)",
                                    "Disaster Management Act 2005, NDMA guidelines, early warning systems, flood/landslide mitigation"
                                ]
                            },
                            {
                                "topic_id": "cse_gs3_internal_security",
                                "title": "Internal Security, Border Management, Cyber Warfare & Money Laundering",
                                "description": "Left-wing extremism, insurgency in North-East, border policing, cyber threats, and terror financing networks.",
                                "sub_points": [
                                    "Linkages between development and spread of extremism; Naxalite insurgency containment",
                                    "Border security architecture: Comprehensive Integrated Border Management System (CIBMS)",
                                    "Cyber warfare, data sovereignty, critical information infrastructure protection (CERT-In)",
                                    "Money laundering, Prevention of Money Laundering Act (PMLA), FATF compliance"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p5",
                        "paper_name": "Paper V: General Studies IV (Ethics, Integrity and Aptitude)",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written (13 Questions: 6 Theory + 7 Case Studies)",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Paper V (GS-4)",
                        "topics": [
                            {
                                "topic_id": "cse_gs4_ethics_human",
                                "title": "Ethics and Human Interface - Essence, Determinants & Consequences",
                                "description": "Ethical dimensions in private and public relationships, moral philosophers, and virtue ethics.",
                                "sub_points": [
                                    "Deontological, teleological, and virtue ethics frameworks in governance",
                                    "Human values derived from lives of exemplary administrators and moral thinkers",
                                    "Role of family, educational institutions, and society in inculcating ethical compass"
                                ]
                            },
                            {
                                "topic_id": "cse_gs4_aptitude_values",
                                "title": "Civil Service Values, Integrity, Neutrality & Emotional Intelligence",
                                "description": "Foundational ethos for public servants: integrity, impartiality, non-partisanship, empathy, and emotional quotient.",
                                "sub_points": [
                                    "Integrity and probity in public office; conflict of interest identification",
                                    "Impartiality and political neutrality; dedicated service to weaker sections",
                                    "Emotional Intelligence: components, self-regulation, empathy, and bureaucratic utility"
                                ]
                            },
                            {
                                "topic_id": "cse_gs4_probity",
                                "title": "Probity in Governance, RTI, Codes of Conduct & Citizen Charters",
                                "description": "Philosophical basis of governance, institutional mechanisms for preventing corruption, and Whistleblower protection.",
                                "sub_points": [
                                    "Central Vigilance Commission (CVC), Lokpal and Lokayuktas Act, Prevention of Corruption Act",
                                    "Codes of Conduct vs Codes of Ethics; adherence to statutory guidelines",
                                    "Public funds utilization, procurement integrity, and contract transparency"
                                ]
                            },
                            {
                                "topic_id": "cse_gs4_case_studies",
                                "title": "Applied Ethics Case Studies on Administrative Dilemmas",
                                "description": "Real-world administrative scenarios testing decision-making under conflicting legal, political, and moral pressures.",
                                "sub_points": [
                                    "Disaster relief distribution equity under resource scarcity",
                                    "Encounter killings vs rule of law; mob violence containment",
                                    "Whistleblowing against political superiors; tender awarding integrity"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p6",
                        "paper_name": "Paper VI: Optional Subject - Paper 1",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Optional Subjects",
                        "topics": [
                            {
                                "topic_id": "cse_opt_p1_core",
                                "title": "Optional Discipline Fundamentals & Theoretical Frameworks",
                                "description": "Advanced graduate-level exploration of chosen discipline (e.g., Public Administration, PSIR, History, Geography, Economics, Sociology, Law, Engineering).",
                                "sub_points": [
                                    "Core foundational theories, philosophical evolution, and canonical paradigms",
                                    "Comparative analytical approaches and seminal scholarly contributions"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "cse_mains_p7",
                        "paper_name": "Paper VII: Optional Subject - Paper 2",
                        "marks": 250,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Optional Subjects",
                        "topics": [
                            {
                                "topic_id": "cse_opt_p2_applied",
                                "title": "Optional Discipline Applied Concepts & Indian Contextualization",
                                "description": "Domain-specific applied problems, policy case studies, and contextual Indian developments in the chosen discipline.",
                                "sub_points": [
                                    "Empirical studies, national policy applications, and institutional frameworks",
                                    "Contemporary debates, recent statutory developments, and sectorial challenges"
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "stage_id": "interview",
                "stage_name": "Stage III: Personality Test (Interview)",
                "stage_type": "Viva Voce / Personal Interview",
                "total_stage_marks": 275,
                "description": "The candidate is interviewed by a Board of competent and unbiased observers to assess personal suitability for civil services.",
                "papers": [
                    {
                        "paper_id": "cse_pt",
                        "paper_name": "Personality Test (Interview)",
                        "marks": 275,
                        "duration_hours": 0.6,
                        "question_type": "Oral Board Viva Voce",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section III Interview",
                        "topics": [
                            {
                                "topic_id": "cse_pt_traits",
                                "title": "Assessment of Mental Caliber, Moral Integrity & Social Suitability",
                                "description": "Evaluates intellectual curiosity, critical powers of assimilation, clear and logical exposition, balance of judgment, alertness of mind, and moral integrity.",
                                "sub_points": [
                                    "Detailed Application Form (DAF) verification: academic background, service preferences, hobbies",
                                    "Critical perspective on complex socio-economic and national security dilemmas",
                                    "Composure under stress, leadership qualities, and empathetic temperament"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # =========================================================================
    # 2. GATE
    # =========================================================================
    data["schemes"]["GATE"] = {
        "exam_id": "GATE",
        "exam_title": "Graduate Aptitude Test in Engineering",
        "short_code": "GATE",
        "total_marks": 100,
        "negative_marking_rule": "1/3rd penalty for 1-mark MCQs (0.33); 1/3rd penalty for 2-mark MCQs (0.66); Zero penalty for NAT and MSQs",
        "official_notification_clause": "GATE Information Brochure, Section 5: Examination Pattern",
        "official_notification_url": "https://gate2026.iitg.ac.in/documents/information-brochure.pdf",
        "disciplines": [
            {"code": "ME", "name": "Mechanical Engineering"},
            {"code": "CE", "name": "Civil Engineering"},
            {"code": "EE", "name": "Electrical Engineering"},
            {"code": "EC", "name": "Electronics & Communication"},
            {"code": "CS", "name": "Computer Science & Information Tech"},
            {"code": "CH", "name": "Chemical Engineering"},
            {"code": "IN", "name": "Instrumentation Engineering"}
        ],
        "stages": [
            {
                "stage_id": "cbt",
                "stage_name": "Stage I: Computer Based Test (CBT)",
                "stage_type": "Objective CBT (65 Questions)",
                "total_stage_marks": 100,
                "description": "100 marks 3-hour single paper consisting of 15 marks General Aptitude + 85 marks Technical Core & Engineering Mathematics.",
                "papers": [
                    {
                        "paper_id": "gate_sec_ga",
                        "paper_name": "Section 1: General Aptitude (Common to All Streams)",
                        "marks": 15,
                        "duration_hours": 0.5,
                        "question_type": "Objective MCQ / NAT / MSQ (10 Questions)",
                        "negative_marking": "1/3rd deduction on MCQs; No negative marking on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (15% Weightage)",
                        "source_clause": "GATE Syllabus Section GA",
                        "topics": [
                            {
                                "topic_id": "gate_ga_verbal",
                                "title": "Verbal Aptitude: English Grammar & Reading Comprehension",
                                "description": "Basic English grammar, tenses, subject-verb agreement, vocabulary in context, and narrative sequencing.",
                                "sub_points": [
                                    "Articles, prepositions, conjunctions, verb tenses, conditional structures",
                                    "Vocabulary, synonyms, antonyms, idioms, analogies",
                                    "Reading comprehension and analytical narrative deduction"
                                ]
                            },
                            {
                                "topic_id": "gate_ga_quantitative",
                                "title": "Quantitative Aptitude: Data Interpretation & Numerical Reasoning",
                                "description": "Data representation, elementary statistics, permutations, probability, algebra, and geometry.",
                                "sub_points": [
                                    "Bar charts, pie charts, scatter plots, tabular data sufficiency",
                                    "Percentages, ratios, powers, exponents, logarithms, permutations & combinations",
                                    "Elementary 2D and 3D geometry, mensuration, coordinate trigonometry"
                                ]
                            },
                            {
                                "topic_id": "gate_ga_analytical_spatial",
                                "title": "Analytical & Spatial Aptitude: Logic & Shape Transformations",
                                "description": "Deductive logic, syllogisms, pattern recognition, spatial paper folding, mirror images, and grouping.",
                                "sub_points": [
                                    "Logical deduction, analogy, numerical series, conditional relations",
                                    "Spatial assembly, rotation, mirroring, paper folding, and 2D/3D projections"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_ME",
                        "stream_id": "ME",
                        "paper_name": "Section 2: Mechanical Engineering Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper ME",
                        "topics": [
                            {
                                "topic_id": "gate_me_math",
                                "title": "Engineering Mathematics (Linear Algebra, Calculus, ODE/PDE)",
                                "description": "Matrices, eigenvalues, vector calculus, ordinary and partial differential equations, complex variables, and numerical methods.",
                                "sub_points": [
                                    "Matrix algebra, systems of linear equations, eigenvalues and eigenvectors",
                                    "Taylor series, gradient, divergence, curl, Stokes theorem, Gauss divergence theorem",
                                    "First order ODEs, higher order linear ODEs with constant coefficients, Laplace transforms"
                                ]
                            },
                            {
                                "topic_id": "gate_me_applied_mechanics",
                                "title": "Applied Mechanics and Design: Mechanics of Materials & Theory of Machines",
                                "description": "Free-body diagrams, stress-strain relations, mohr circle, beams, shafts, governors, vibration analysis, and machine design.",
                                "sub_points": [
                                    "Stress, strain, Hooke's law, Mohr's circle for plane stress and plane strain",
                                    "Bending moment and shear force diagrams, deflection of beams, Euler's buckling theory",
                                    "Kinematics of planar mechanisms, gears and gear trains, flywheels, governors",
                                    "Free and forced single degree of freedom vibrations, resonance, damping"
                                ]
                            },
                            {
                                "topic_id": "gate_me_thermo_fluids",
                                "title": "Fluid Mechanics and Thermal Sciences: Thermodynamics & Heat Transfer",
                                "description": "Continuity and Navier-Stokes equations, Rankine, Otto, Diesel, Brayton cycles, conduction, convection, and radiation.",
                                "sub_points": [
                                    "Fluid statics, Bernoulli's equation, boundary layer theory, pipe flow losses",
                                    "First and second laws of thermodynamics, entropy, exergy, thermodynamic cycles",
                                    "Steady and unsteady heat conduction, lumped parameter analysis, Nusselt number correlations",
                                    "Radiation laws, Stefan-Boltzmann, Wien displacement law, radiation shield design"
                                ]
                            },
                            {
                                "topic_id": "gate_me_manufacturing",
                                "title": "Materials, Manufacturing and Industrial Engineering",
                                "description": "Casting, metal forming, welding, machining, CNC programming, metrology, operations research, and inventory control.",
                                "sub_points": [
                                    "Iron-carbon phase diagram, heat treatment of steels, TTT diagrams",
                                    "Gating system design, rolling, forging, extrusion, wire drawing mechanics",
                                    "Orthogonal cutting, Taylor's tool life equation, Merchant circle analysis",
                                    "Linear programming, simplex method, transportation model, EOQ models"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_CE",
                        "stream_id": "CE",
                        "paper_name": "Section 2: Civil Engineering Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper CE",
                        "topics": [
                            {
                                "topic_id": "gate_ce_structures",
                                "title": "Structural Engineering: Solid Mechanics, Concrete & Steel Structures",
                                "description": "Indeterminate analysis, slope deflection, moment distribution, limit state design of beams, columns, and steel connections.",
                                "sub_points": [
                                    "Statically determinate and indeterminate trusses, beams, and frames",
                                    "Limit state design of reinforced concrete beams, slabs, columns, and footings (IS 456)",
                                    "Design of tension and compression steel members, bolted and welded joints (IS 800)"
                                ]
                            },
                            {
                                "topic_id": "gate_ce_geotech",
                                "title": "Geotechnical & Foundation Engineering",
                                "description": "Soil classification, effective stress, permeability, compaction, consolidation, shear strength, shallow and deep foundations.",
                                "sub_points": [
                                    "Three-phase system, Atterberg limits, Indian Standard soil classification",
                                    "Terzaghi's 1D consolidation theory, Mohr-Coulomb failure criterion, direct shear test",
                                    "Bearing capacity theories (Terzaghi, Meyerhof), pile load capacity in clays and sands"
                                ]
                            },
                            {
                                "topic_id": "gate_ce_water_env",
                                "title": "Water Resources & Environmental Engineering",
                                "description": "Fluid mechanics, open channel hydraulics, unit hydrographs, water treatment plant design, and wastewater quality.",
                                "sub_points": [
                                    "Specific energy, hydraulic jump in open channels, Manning and Chezy equations",
                                    "Unit hydrograph derivation, rational method for flood estimation, well hydraulics",
                                    "Water treatment unit processes: coagulation, flocculation, sedimentation, rapid sand filtration",
                                    "Activated sludge process, BOD kinetics, sludge digestion, air pollution standards"
                                ]
                            },
                            {
                                "topic_id": "gate_ce_transport_geomatics",
                                "title": "Transportation Engineering & Geomatics (Surveying)",
                                "description": "Highway geometric design, pavement thickness, traffic capacity, leveling, EDM, and photogrammetry.",
                                "sub_points": [
                                    "Stopping and overtaking sight distances, super-elevation design, horizontal and vertical curves",
                                    "Flexible and rigid pavement design components (IRC standards), CBR method",
                                    "Levelling, reciprocal levelling, total station surveying, GPS and GIS basics"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_EE",
                        "stream_id": "EE",
                        "paper_name": "Section 2: Electrical Engineering Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper EE",
                        "topics": [
                            {
                                "topic_id": "gate_ee_circuits_fields",
                                "title": "Electric Circuits & Electromagnetic Fields",
                                "description": "Network theorems, transient response, sinusoidal steady state, Maxwell's equations, and electrostatic boundary conditions.",
                                "sub_points": [
                                    "Thevenin, Norton, Superposition, Maximum Power Transfer theorems; graph theory",
                                    "RL, RC, RLC transient analysis with DC and sinusoidal excitations, resonance",
                                    "Gauss's law, Biot-Savart law, Ampere's law, Faraday's law, Poynting vector"
                                ]
                            },
                            {
                                "topic_id": "gate_ee_signals_systems",
                                "title": "Signals and Systems & Control Systems",
                                "description": "LTI systems, Fourier series, Laplace transforms, Z-transforms, root locus, Bode plot, Nyquist stability, state-space models.",
                                "sub_points": [
                                    "Continuous and discrete time LTI systems, convolution, sampling theorem",
                                    "Routh-Hurwitz criterion, root locus plotting rules, lead-lag compensator design",
                                    "Bode and Nyquist stability criteria, gain margin, phase margin, state transition matrix"
                                ]
                            },
                            {
                                "topic_id": "gate_ee_machines",
                                "title": "Electrical Machines: Transformers, Induction & Synchronous Machines",
                                "description": "Equivalent circuits, phasor diagrams, torque-speed characteristics, open-circuit/short-circuit tests, and motor drives.",
                                "sub_points": [
                                    "Single-phase and three-phase transformers: losses, efficiency, regulation, auto-transformers",
                                    "Three-phase induction motors: equivalent circuit, torque-slip curves, starting methods",
                                    "Synchronous generators: cylindrical and salient pole machines, voltage regulation, V-curves"
                                ]
                            },
                            {
                                "topic_id": "gate_ee_power_systems",
                                "title": "Power Systems, Protection & Power Electronics",
                                "description": "Transmission line parameters, load flow (Gauss-Seidel, Newton-Raphson), fault analysis, thyristors, inverters, and choppers.",
                                "sub_points": [
                                    "ABCD parameters of transmission lines, surge impedance loading, Ferranti effect",
                                    "Symmetrical and unsymmetrical fault calculations using symmetrical components",
                                    "Differential relays, distance relays, numerical protection schemes",
                                    "Phase-controlled rectifiers, buck/boost converters, voltage source inverters, PWM"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_EC",
                        "stream_id": "EC",
                        "paper_name": "Section 2: Electronics & Communication Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper EC",
                        "topics": [
                            {
                                "topic_id": "gate_ec_devices_circuits",
                                "title": "Electronic Devices, Analog & Digital Circuits",
                                "description": "Energy bands, p-n junctions, MOSFET characteristics, op-amps, feedback amplifiers, combinational logic, and microprocessors.",
                                "sub_points": [
                                    "Carrier transport in semiconductors, drift, diffusion, continuity equation, MOS capacitor",
                                    "BJT and MOSFET small-signal amplifiers, differential amplifiers, frequency response",
                                    "Ideal and practical op-amp circuits, active filters, Schmitt triggers, oscillators",
                                    "Boolean algebra, Karnaugh maps, flip-flops, synchronous counters, finite state machines"
                                ]
                            },
                            {
                                "topic_id": "gate_ec_communications",
                                "title": "Communications & Electromagnetics",
                                "description": "Analog and digital modulation (AM, FM, PSK, QAM), noise analysis, information theory, transmission lines, and antennas.",
                                "sub_points": [
                                    "AM and FM transmitters/receivers, superheterodyne receivers, SNR calculations",
                                    "PCM, DPCM, ASK, FSK, PSK, QAM, matched filter receivers, bit error rate (BER)",
                                    "Shannon capacity theorem, Huffman coding, linear block codes, cyclic codes",
                                    "Smith chart, transmission line matching, rectangular waveguides, dipole antenna radiation"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_CS",
                        "stream_id": "CS",
                        "paper_name": "Section 2: Computer Science & IT Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper CS",
                        "topics": [
                            {
                                "topic_id": "gate_cs_discrete_math",
                                "title": "Discrete Mathematics & Graph Theory",
                                "description": "Propositional logic, predicate calculus, sets, relations, lattice theory, combinatorics, graph coloring, and trees.",
                                "sub_points": [
                                    "First-order logic, inference rules, equivalence, satisfiability",
                                    "Partial orders, equivalence relations, recurrence relations, generating functions",
                                    "Graph isomorphisms, Eulerian and Hamiltonian graphs, planar graphs, vertex coloring"
                                ]
                            },
                            {
                                "topic_id": "gate_cs_dsa",
                                "title": "Data Structures, Algorithms & Theory of Computation",
                                "description": "Arrays, stacks, trees, heaps, graphs, asymptotic analysis, greedy, dynamic programming, DFA, regular expressions, and Turing machines.",
                                "sub_points": [
                                    "Binary search trees, AVL trees, B-trees, Red-Black trees, heap sort, hash tables",
                                    "Divide and conquer, greedy algorithms, dynamic programming (knapsack, LCS), graph traversals",
                                    "Regular languages, pumping lemma for regular and context-free languages, pushdown automata",
                                    "Turing machines, Church-Turing thesis, decidability, halting problem, NP-completeness"
                                ]
                            },
                            {
                                "topic_id": "gate_cs_systems",
                                "title": "Computer Organization, Operating Systems & Compiler Design",
                                "description": "Pipelining, cache memory, process scheduling, synchronization, virtual memory, lexical analysis, and syntax-directed translation.",
                                "sub_points": [
                                    "Instruction pipelining, hazards, memory hierarchy, cache coherence, virtual memory",
                                    "Processes, threads, CPU scheduling algorithms, mutexes, semaphores, deadlock detection",
                                    "Paging, segmentation, page replacement algorithms, file system allocation",
                                    "Lexical analysis, LL(1) and LR parsers (SLR, CLR, LALR), intermediate code generation"
                                ]
                            },
                            {
                                "topic_id": "gate_cs_db_networks",
                                "title": "Databases & Computer Networks",
                                "description": "ER models, relational algebra, SQL, normal forms (1NF to BCNF), transactions, TCP/IP protocol suite, routing algorithms.",
                                "sub_points": [
                                    "Relational calculus, SQL queries, functional dependencies, 3NF and BCNF normalization",
                                    "ACID properties, serializability, two-phase locking protocol (2PL), crash recovery",
                                    "OSI and TCP/IP models, sliding window protocols, congestion control (TCP Reno/Tahoe)",
                                    "IPv4/IPv6 addressing, subnetting, Dijkstra routing, Bellman-Ford, DNS, HTTP, SSL/TLS"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_CH",
                        "stream_id": "CH",
                        "paper_name": "Section 2: Chemical Engineering Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper CH",
                        "topics": [
                            {
                                "topic_id": "gate_ch_thermo_mass",
                                "title": "Process Thermodynamics, Heat & Mass Transfer",
                                "description": "Phase equilibria, activity coefficient models, shell heat conduction, distillation column design, and absorption kinetics.",
                                "sub_points": [
                                    "VLE calculations, Raoult's law, Wilson and NRTL models, chemical reaction equilibria",
                                    "LMTD, NTU-effectiveness method, shell and tube heat exchangers, boiling and condensation",
                                    "Fick's law, mass transfer coefficients, McCabe-Thiele method for binary distillation"
                                ]
                            },
                            {
                                "topic_id": "gate_ch_reaction_control",
                                "title": "Chemical Reaction Engineering & Process Control",
                                "description": "Ideal reactors (batch, CSTR, PFR), residence time distribution, catalyst deactivation, Bode plots, and PID tuning.",
                                "sub_points": [
                                    "Kinetics of homogeneous and catalytic reactions, Arrhenius equation, reactor sizing",
                                    "RTD measurement, dispersion model, E-curve and F-curve analysis",
                                    "First and second order dynamic systems, transfer functions, stability margins of closed loops"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "gate_sec_tech_IN",
                        "stream_id": "IN",
                        "paper_name": "Section 2: Instrumentation Engineering Technical Curriculum",
                        "marks": 85,
                        "duration_hours": 2.5,
                        "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
                        "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
                        "is_qualifying": False,
                        "merit_status": "Merit (85% Weightage)",
                        "source_clause": "GATE Syllabus Paper IN",
                        "topics": [
                            {
                                "topic_id": "gate_in_transducers_sensors",
                                "title": "Sensors, Industrial Instrumentation & Optical Systems",
                                "description": "Resistive, capacitive, inductive sensors, piezoelectric transducers, flowmeters, pyrometers, and optical fibers.",
                                "sub_points": [
                                    "Strain gauges, LVDTs, capacitive displacement sensors, thermocouple laws, RTDs",
                                    "Orifice meters, venturimeters, electromagnetic flowmeters, ultrasonic Doppler sensors",
                                    "Lasers, photodetectors, optical fiber numerical aperture, dispersion characteristics"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # =========================================================================
    # 3. UPSC ESE
    # =========================================================================
    data["schemes"]["UPSC_ESE"] = {
        "exam_id": "UPSC_ESE",
        "exam_title": "Engineering Services Examination",
        "short_code": "ESE",
        "total_marks": 1300,
        "negative_marking_rule": "1/3rd penalty for incorrect answers in Prelims Objective Papers",
        "official_notification_clause": "Appendix I & II of Gazette of India MoC Notification dated 18.09.2024",
        "official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-ENGG-25-engl-180924.pdf",
        "disciplines": [
            {"code": "CE", "name": "Civil Engineering"},
            {"code": "ME", "name": "Mechanical Engineering"},
            {"code": "EE", "name": "Electrical Engineering"},
            {"code": "E&T", "name": "Electronics & Telecommunication Engineering"}
        ],
        "stages": [
            {
                "stage_id": "prelims",
                "stage_name": "Stage I: Preliminary Examination",
                "stage_type": "Objective Screening",
                "total_stage_marks": 500,
                "description": "500-mark objective stage. Paper I GS & Engineering Aptitude (200m) + Paper II Discipline Specific (300m).",
                "papers": [
                    {
                        "paper_id": "ese_pre_p1",
                        "paper_name": "Paper I: General Studies & Engineering Aptitude",
                        "marks": 200,
                        "duration_hours": 2.0,
                        "question_type": "Objective MCQ (100 Questions)",
                        "negative_marking": "1/3rd (0.66 marks deducted)",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Prelims Cutoff & Final Rank)",
                        "source_clause": "Appendix II, Section I Paper-I",
                        "topics": [
                            {
                                "topic_id": "ese_gs_current_affairs",
                                "title": "Current Issues of National & International Importance",
                                "description": "Technological advancements, strategic infrastructure projects, environmental treaties, and policy shifts.",
                                "sub_points": [
                                    "National infrastructure missions (Gati Shakti, Sagarmala, Bharatmala)",
                                    "Bilateral industrial pacts and green energy transition treaties"
                                ]
                            },
                            {
                                "topic_id": "ese_gs_aptitude_maths",
                                "title": "Engineering Aptitude, Numerical Analysis & Ethics",
                                "description": "Logical reasoning, matrix algebra, numerical methods, design principles, material science, and engineering ethics.",
                                "sub_points": [
                                    "Basics of Project Management (PERT, CPM, crashing, resource leveling)",
                                    "Quality control tools (ISO standards, Six Sigma, TQM frameworks)",
                                    "Basics of Energy and Environment: GHG emissions, EIA methodology, renewable resources",
                                    "Ethics and professional values in engineering administration"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "ese_pre_p2",
                        "paper_name": "Paper II: Engineering Discipline Specific Paper",
                        "marks": 300,
                        "duration_hours": 3.0,
                        "question_type": "Objective MCQ (150 Questions)",
                        "negative_marking": "1/3rd (0.66 marks deducted)",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Prelims Cutoff & Final Rank)",
                        "source_clause": "Appendix II, Section I Paper-II",
                        "topics": [
                            {
                                "topic_id": "ese_disc_pre_core",
                                "title": "Objective Discipline Curriculum (CE / ME / EE / E&T)",
                                "description": "Comprehensive objective questions covering core domain subjects as specified in official branch syllabus.",
                                "sub_points": [
                                    "Fundamental theorems, formulas, and empirical coefficients",
                                    "Analytical calculations, parametric modeling, and circuit/structural behavior"
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "stage_id": "mains",
                "stage_name": "Stage II: Main Written Examination",
                "stage_type": "Descriptive Written",
                "total_stage_marks": 600,
                "description": "Two conventional written papers (300 marks each) testing rigorous analytical derivation and design capabilities.",
                "papers": [
                    {
                        "paper_id": "ese_mains_p1",
                        "paper_name": "Paper I: Conventional Discipline Specific Paper 1",
                        "marks": 300,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Stage-II Paper 1",
                        "topics": [
                            {
                                "topic_id": "ese_conv_p1_topics",
                                "title": "Theoretical Foundations, Derivations & Design Problems",
                                "description": "Detailed step-by-step mathematical derivations, boundary value problems, and component design calculations.",
                                "sub_points": [
                                    "Elaborate analytical proofs and engineering derivations",
                                    "Structural, machine, or circuit design with standard code provisions"
                                ]
                            }
                        ]
                    },
                    {
                        "paper_id": "ese_mains_p2",
                        "paper_name": "Paper II: Conventional Discipline Specific Paper 2",
                        "marks": 300,
                        "duration_hours": 3.0,
                        "question_type": "Descriptive Written",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section II Stage-II Paper 2",
                        "topics": [
                            {
                                "topic_id": "ese_conv_p2_topics",
                                "title": "Applied Systems, Field Engineering & Practical Solutions",
                                "description": "Field execution challenges, construction/manufacturing technologies, operational diagnostics, and system stability.",
                                "sub_points": [
                                    "Complex multidimensional problems, performance charts, and error budgets",
                                    "Industrial implementation standards and maintenance guidelines"
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "stage_id": "interview",
                "stage_name": "Stage III: Personality Test (Interview)",
                "stage_type": "Viva Voce / Personal Interview",
                "total_stage_marks": 200,
                "description": "Board interview assessing technical competence, practical field aptitude, leadership traits, and integrity.",
                "papers": [
                    {
                        "paper_id": "ese_interview",
                        "paper_name": "Personality Test / Viva Voce",
                        "marks": 200,
                        "duration_hours": 0.5,
                        "question_type": "Oral Board Interview",
                        "negative_marking": "None",
                        "is_qualifying": False,
                        "merit_status": "Merit (Counted for Final Rank)",
                        "source_clause": "Appendix II, Section III Stage-III",
                        "topics": [
                            {
                                "topic_id": "ese_interview_eval",
                                "title": "Evaluation of Technical Acumen, Field Judgment & Executive Temperament",
                                "description": "Assessment of the candidate's capacity for leadership, administrative acumen, integrity, and field readiness.",
                                "sub_points": [
                                    "Defense of engineering design choices and undergraduate projects",
                                    "Techno-economic viability analysis of modern Indian infrastructure projects",
                                    "Executive decision-making under disaster and emergency conditions"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # =========================================================================
    # Helper to add remaining exams with structured authentic patterns
    # =========================================================================
    remaining_exams = [
        # (exam_id, title, short_code, total_marks, neg_rule, clause, stages_defs)
        (
            "UPSC_IFOS", "Indian Forest Service Examination", "IFoS", 1700,
            "1/3rd in joint CSE Prelims screening",
            "Appendix II of MoEFCC Gazette Notification F.No.13018/07/2023-AIS-I",
            "https://upsc.gov.in/sites/default/files/Notif-IFSP-24-engl-140224.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination (Joint CSE Prelims)",
                    "stage_type": "Objective Screening", "total_stage_marks": 400,
                    "papers": [
                        {
                            "paper_id": "ifos_pre_gs1", "paper_name": "Paper I: General Studies (GS-1)",
                            "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ",
                            "negative_marking": "1/3rd (0.66)", "is_qualifying": False, "merit_status": "Screening Cutoff",
                            "topics": [{"topic_id": "ifos_pre_env_eco", "title": "Environment, Ecology & Forestry Fundamentals", "description": "High cutoff paper demanding exceptional depth in forest ecology, climate protocols, and biological sciences.", "sub_points": ["Wildlife habitats, red list species, National Forest Policy 1988", "Silviculture, social forestry, agroforestry systems"]}]
                        },
                        {
                            "paper_id": "ifos_pre_csat", "paper_name": "Paper II: CSAT", "marks": 200, "duration_hours": 2.0,
                            "question_type": "Objective MCQ", "negative_marking": "1/3rd (0.83)", "is_qualifying": True, "qualifying_threshold_pct": 33.33,
                            "merit_status": "Qualifying Only (Min 33%)", "topics": [{"topic_id": "ifos_csat", "title": "Aptitude & Logical Reasoning", "description": "Comprehension, logical reasoning, and basic numeracy.", "sub_points": ["Reading comprehension, reasoning, and Class X data interpretation"]}]
                        }
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: IFoS Main Written Examination",
                    "stage_type": "Descriptive Written", "total_stage_marks": 1400,
                    "papers": [
                        {"paper_id": "ifos_mains_p1", "paper_name": "Paper I: General English", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ifos_eng", "title": "Essay, Précis & Grammar", "description": "English writing skills and precis writing.", "sub_points": ["Essay, precis, sentence correction"]}]},
                        {"paper_id": "ifos_mains_p2", "paper_name": "Paper II: General Knowledge", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ifos_gk", "title": "Indian History, Geography & Science", "description": "Broad general knowledge with emphasis on geography and environmental systems.", "sub_points": ["Indian geography, natural resources, environmental degradation"]}]},
                        {"paper_id": "ifos_mains_p3", "paper_name": "Papers III, IV, V, VI: Two Optional Subjects (200m each)", "marks": 800, "duration_hours": 12.0, "question_type": "Descriptive Written (4 Papers)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ifos_opts", "title": "Optional Subjects (Forestry, Agriculture, Engineering, Botany, Zoology)", "description": "Selected dual options from official technical syllabus list.", "sub_points": ["Forestry Paper I & II (Silviculture, Mensuration, Forest Management, Wood Technology)", "Second chosen technical subject"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality Test & Walking Endurance",
                    "stage_type": "Viva Voce & Physical Endurance", "total_stage_marks": 300,
                    "papers": [
                        {"paper_id": "ifos_pt", "paper_name": "Personality Test (Interview)", "marks": 300, "duration_hours": 0.5, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ifos_pt_eval", "title": "Environmental Leadership & Forest Governance", "description": "Assessment of personal suitability for forest conservation and conflict resolution with forest-dwelling communities.", "sub_points": ["Human-wildlife conflict resolution, Forest Rights Act 2006, timber smuggling prevention"]}]},
                        {"paper_id": "ifos_walking", "paper_name": "Physical Walking Test (25km Male / 14km Female in 4h)", "marks": 0, "duration_hours": 4.0, "question_type": "Endurance Gate", "negative_marking": "None", "is_qualifying": True, "merit_status": "Qualifying Only", "topics": [{"topic_id": "ifos_walk_test", "title": "Continuous Walking Test", "description": "Mandatory stamina test conducted inside National Zoological Park / designated tracks.", "sub_points": ["25 km walk in 4 hours for male candidates", "14 km walk in 4 hours for female candidates"]}]}
                    ]
                }
            ]
        ),
        (
            "UPSC_CGSE", "Combined Geo-Scientist Examination", "CGSE", 1200,
            "1/3rd penalty on Prelims Objective Papers",
            "Gazette of India Ministry of Mines Notification dated 04.09.2024",
            "https://upsc.gov.in/sites/default/files/Notif-GEOL-25-engl-040924.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination",
                    "stage_type": "Objective Screening (400 Marks)", "total_stage_marks": 400,
                    "papers": [
                        {"paper_id": "cgse_pre_p1", "paper_name": "Paper I: General Studies", "marks": 100, "duration_hours": 2.0, "question_type": "Objective MCQ", "negative_marking": "1/3rd", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_pre_gs", "title": "Current Affairs, Environmental Ecology & Earth Sciences", "description": "Broad awareness of scientific developments, climate change, and national geography.", "sub_points": ["National policy, climate change, ecology, basic science"]}]},
                        {"paper_id": "cgse_pre_p2", "paper_name": "Paper II: Stream Specific (Geology / Geophysics / Chemistry)", "marks": 300, "duration_hours": 2.0, "question_type": "Objective MCQ", "negative_marking": "1/3rd", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_pre_stream", "title": "Domain Fundamentals", "description": "Comprehensive objective questions in Geology, Geophysics, or Chemistry.", "sub_points": ["Physical geology, mineralogy, structural geology, geochemistry"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Examination",
                    "stage_type": "Descriptive Written (600 Marks)", "total_stage_marks": 600,
                    "papers": [
                        {"paper_id": "cgse_mains_p1", "paper_name": "Paper I: Stream Specific Paper 1", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_m_p1", "title": "Mineralogy, Petrology & Stratigraphy", "description": "Igneous, sedimentary, metamorphic petrology and Indian stratigraphy.", "sub_points": ["Crystal chemistry, rock classification, sedimentary basins"]}]},
                        {"paper_id": "cgse_mains_p2", "paper_name": "Paper II: Stream Specific Paper 2", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_m_p2", "title": "Economic Geology & Geochemistry", "description": "Ore deposits, mineral exploration techniques, petroleum geology.", "sub_points": ["Hydrothermal deposits, mineral economics, isotopic geology"]}]},
                        {"paper_id": "cgse_mains_p3", "paper_name": "Paper III: Stream Specific Paper 3", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_m_p3", "title": "Engineering Geology & Hydrogeology", "description": "Groundwater exploration, dam/tunnel site investigation, geological hazards.", "sub_points": ["Aquifer properties, seismic zonation, rock mechanics"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality Test (Interview)",
                    "stage_type": "Viva Voce", "total_stage_marks": 200,
                    "papers": [{"paper_id": "cgse_pt", "paper_name": "Personality Interview", "marks": 200, "duration_hours": 0.5, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "cgse_pt_eval", "title": "Geological Acumen & Field Exploration Vision", "description": "Assessment of practical exploration skills for Geological Survey of India / CGWB.", "sub_points": ["Critical minerals mission, lithium exploration, groundwater sustainability"]}]}]
                }
            ]
        ),
        (
            "UPSC_IES_ISS", "Indian Economic Service / Indian Statistical Service Examination", "IES/ISS", 1200,
            "None (Conventional Descriptive + Viva Voce)",
            "MoSPI & DEA Gazette Notification dated 10.04.2024",
            "https://upsc.gov.in/sites/default/files/Notif-IES-ISS-24-engl-100424.pdf",
            [
                {
                    "stage_id": "written", "stage_name": "Stage I: Written Examination",
                    "stage_type": "Descriptive & Objective (1000 Marks)", "total_stage_marks": 1000,
                    "papers": [
                        {"paper_id": "ies_gen_eng", "paper_name": "General English", "marks": 100, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ies_eng", "title": "English Essay, Précis & Comprehension", "description": "High-level discursive writing and vocabulary.", "sub_points": ["Economic essays, precis writing"]}]},
                        {"paper_id": "ies_gen_studies", "paper_name": "General Studies", "marks": 100, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ies_gs", "title": "Indian Polity, History & Geography", "description": "General knowledge including current affairs.", "sub_points": ["Indian constitution, modern history, geography"]}]},
                        {"paper_id": "ies_econ_papers", "paper_name": "Technical Papers (IES: Economics I-IV / ISS: Statistics I-IV)", "marks": 800, "duration_hours": 12.0, "question_type": "4 Papers (200m each)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ies_technical", "title": "Advanced Macroeconomics, Econometrics & Indian Economy", "description": "Microeconomic theory, macroeconomic dynamics, public finance, international trade, econometrics.", "sub_points": ["General Equilibrium, IS-LM, Lucas critique, simultaneous equation models, Union Budget analysis"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage II: Viva Voce",
                    "stage_type": "Oral Board Interview", "total_stage_marks": 200,
                    "papers": [{"paper_id": "ies_viva", "paper_name": "Viva Voce", "marks": 200, "duration_hours": 0.5, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ies_viva_eval", "title": "Macroeconomic Policy Defense & Statistical Modeling", "description": "Assessment of economic analysis and advisory acumen for Ministries of Finance, Commerce, and MoSPI.", "sub_points": ["Fiscal deficit path, inflation targeting, national account statistics reforms"]}]}]
                }
            ]
        ),
        (
            "IFSCA_GRADE_A", "IFSCA Officer Grade A (Assistant Manager)", "IFSCA Gr A", 250,
            "1/4th penalty on Objective Questions",
            "IFSCA (Officers and Employees) Regulations, 2021 & Advt 01/2024",
            "https://ifsca.gov.in/Careers/Detail/85",
            [
                {
                    "stage_id": "phase1", "stage_name": "Phase I: Online Examination", "stage_type": "Objective CBT (200 Marks)", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "ifsca_p1_p1", "paper_name": "Paper 1: General Awareness, English, Quant, Reasoning", "marks": 100, "duration_hours": 1.0, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": True, "qualifying_threshold_pct": 30.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "ifsca_p1_apt", "title": "General Aptitude & Financial News", "description": "Standard banking aptitude with global financial center updates.", "sub_points": ["GIFT City developments, financial sector news, reading comprehension"]}]},
                        {"paper_id": "ifsca_p1_p2", "paper_name": "Paper 2: IFSCA Act, GIFT IFSC Regulations & Global Finance", "marks": 100, "duration_hours": 1.0, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": True, "qualifying_threshold_pct": 40.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "ifsca_p1_spec", "title": "IFSCA Regulatory Architecture & International Finance", "description": "IFSCA Act 2019, offshore banking units, international bullion exchange, ship leasing, FinTech sandboxes.", "sub_points": ["IFSCA Act 2019 statutory provisions, offshore banking regulations, capital markets in IFSC"]}]}
                    ]
                },
                {
                    "stage_id": "phase2", "stage_name": "Stage II: Phase II Online Examination", "stage_type": "Descriptive & Objective Hybrid", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "ifsca_p2_p1", "paper_name": "Paper 1: English Descriptive", "marks": 100, "duration_hours": 1.0, "question_type": "Descriptive Typing", "negative_marking": "None", "is_qualifying": False, "merit_status": "1/3rd Weightage", "topics": [{"topic_id": "ifsca_p2_eng", "title": "Drafting on Cross-Border Finance & Regulatory Sandbox", "description": "Essays and précis on offshore financing and tax arbitrage.", "sub_points": ["Essays on GIFT City global competitiveness, cross-border payments"]}]},
                        {"paper_id": "ifsca_p2_p2", "paper_name": "Paper 2: Deep International Finance & Legal Frameworks", "marks": 100, "duration_hours": 1.0, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": False, "merit_status": "2/3rd Weightage", "topics": [{"topic_id": "ifsca_p2_deep", "title": "International Capital Markets, Global Banking & Foreign Exchange Regulations", "description": "FEMA provisions, offshore derivative instruments, foreign currency accounts, aircraft leasing.", "sub_points": ["FEMA 1999 rules, international insurance offices, ESG bond issuances in IFSC"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personal Interview", "stage_type": "Personal Interview", "total_stage_marks": 50,
                    "papers": [{"paper_id": "ifsca_interview", "paper_name": "IFSCA Selection Board Interview", "marks": 50, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit (15% Weightage)", "topics": [{"topic_id": "ifsca_int_eval", "title": "Offshore Financial Center Governance & International Trade", "description": "Evaluation of applicant's grasp on attracting global capital to Indian shores.", "sub_points": ["Comparison of GIFT City with Singapore/Dubai, dispute resolution in IFSC"]}]}]
                }
            ]
        ),
        (
            "PFRDA_GRADE_A", "PFRDA Officer Grade A (Assistant Manager)", "PFRDA Gr A", 250,
            "1/4th penalty on Objective Questions",
            "PFRDA (Employees Service) Regulations & Gazette Notification",
            "https://www.pfrda.org.in",
            [
                {
                    "stage_id": "phase1", "stage_name": "Phase I: Online Screening", "stage_type": "Objective CBT (200 Marks)", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "pfrda_p1_p1", "paper_name": "Paper 1: Common Aptitude", "marks": 100, "duration_hours": 1.0, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": True, "qualifying_threshold_pct": 30.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "pfrda_p1_apt", "title": "General Awareness, English, Quant, Reasoning", "description": "Standard screening aptitude.", "sub_points": ["Financial awareness, reasoning, quant"]}]},
                        {"paper_id": "pfrda_p1_p2", "paper_name": "Paper 2: Commerce, Accountancy, Pension & Finance", "marks": 100, "duration_hours": 0.67, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": True, "qualifying_threshold_pct": 40.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "pfrda_p1_spec", "title": "PFRDA Act, National Pension System (NPS) & APY", "description": "PFRDA Act 2013, pension fund management, annuity service providers, Atal Pension Yojana.", "sub_points": ["PFRDA Act 2013, NPS architecture, Central Recordkeeping Agency (CRA), annuity options"]}]}
                    ]
                },
                {
                    "stage_id": "phase2", "stage_name": "Stage II: Phase II Merit Examination", "stage_type": "Descriptive & Objective Hybrid", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "pfrda_p2_p1", "paper_name": "Paper 1: English Descriptive", "marks": 100, "duration_hours": 1.0, "question_type": "Descriptive Typing", "negative_marking": "None", "is_qualifying": False, "merit_status": "1/3rd Weightage", "topics": [{"topic_id": "pfrda_p2_eng", "title": "Descriptive Drafting on Social Security & Old-Age Income Security", "description": "Essays and précis on pension coverage and demographic aging in India.", "sub_points": ["Essays on UPS vs NPS, financial literacy in retirement planning"]}]},
                        {"paper_id": "pfrda_p2_p2", "paper_name": "Paper 2: Advanced Finance & Pension Investment Regulations", "marks": 100, "duration_hours": 0.67, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": False, "merit_status": "2/3rd Weightage", "topics": [{"topic_id": "pfrda_p2_deep", "title": "Pension Fund Portfolio Management & Risk Governance", "description": "Asset allocation guidelines (Scheme E, C, G, A), solvency margins, corporate pension models.", "sub_points": ["Investment patterns for pension funds, mark-to-market valuations, risk monitoring"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personal Interview", "stage_type": "Personal Interview", "total_stage_marks": 50,
                    "papers": [{"paper_id": "pfrda_interview", "paper_name": "PFRDA Selection Interview", "marks": 50, "duration_hours": 0.35, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit (15% Weightage)", "topics": [{"topic_id": "pfrda_int_eval", "title": "Pension Sector Vision & Regulatory Rectitude", "description": "Assessment of applicant's understanding of social security safety nets for unorganized workers.", "sub_points": ["Universal pension inclusion, grievance resolution for subscribers"]}]}]
                }
            ]
        ),
        (
            "SIDBI_GRADE_A", "SIDBI Officers in Grade A (Assistant Manager)", "SIDBI Gr A", 250,
            "1/4th penalty on Objective Questions",
            "SIDBI General Regulations & Advt No. 01/Grade A/2024",
            "https://www.sidbi.in/files/careers/SIDBI_Advt_Grade_A_B_2024.pdf",
            [
                {
                    "stage_id": "written", "stage_name": "Stage I: Online Objective & Descriptive Examination", "stage_type": "Single Composite Online Examination (250 Marks)", "total_stage_marks": 250,
                    "papers": [
                        {
                            "paper_id": "sidbi_obj_test", "paper_name": "Section A: Objective Online Test", "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ (200 Questions)", "negative_marking": "1/4th (0.25)", "is_qualifying": False, "merit_status": "Counted for Merit",
                            "topics": [
                                {"topic_id": "sidbi_msme_ga", "title": "General Awareness with special focus on MSME & Banking", "description": "MSMED Act 2006, priority sector lending, CGTMSE credit guarantees, TReDS platform.", "sub_points": ["MSME classification criteria (turnover and investment), Udyam registration", "CGTMSE guarantee coverage, factoring, Emergency Credit Line Guarantee Scheme (ECLGS)"]},
                                {"topic_id": "sidbi_aptitude", "title": "Reasoning, English & Quantitative Aptitude", "description": "High-level managerial reasoning and data interpretation.", "sub_points": ["Puzzles, caselet DI, arithmetic, and advanced comprehension"]}
                            ]
                        },
                        {
                            "paper_id": "sidbi_desc_test", "paper_name": "Section B: Descriptive English Test", "marks": 50, "duration_hours": 0.75, "question_type": "Descriptive Typing (2 Essays + 1 Business Letter)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Counted for Merit",
                            "topics": [{"topic_id": "sidbi_desc_typing", "title": "Essays on MSME Development & Formal Business Letter", "description": "Keyboard typing: 2 essays on entrepreneurship/MSME and 1 credit appraisal/business letter.", "sub_points": ["Essays on green financing for MSMEs, digital lending, supply chain finance", "Formal business letters to commercial banks or borrowing units"]}]
                        }
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage II: Personal Interview", "stage_type": "Personal Interview", "total_stage_marks": 100,
                    "papers": [{"paper_id": "sidbi_interview", "paper_name": "SIDBI Board Interview", "marks": 100, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "sidbi_int_eval", "title": "Credit Appraisal Acumen & MSME Ecosystem Vision", "description": "Evaluation of applicant's capacity for balance sheet analysis, startup funding, and credit risk assessment.", "sub_points": ["Credit rating methodology, NPA recovery in small businesses, venture debt insights"]}]}]
                }
            ]
        ),
        (
            "EXIM_BANK_MT", "India Exim Bank Management Trainee", "EXIM MT", 250,
            "1/4th penalty on Objective Questions",
            "Export-Import Bank of India General Regulations & Career Notices",
            "https://www.eximbankindia.in/careers",
            [
                {
                    "stage_id": "written", "stage_name": "Stage I: Online Written Examination", "stage_type": "Objective & Descriptive (200 Marks)", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "exim_obj", "paper_name": "Part A: Objective Professional Knowledge & Aptitude", "marks": 100, "duration_hours": 1.33, "question_type": "Objective MCQ", "negative_marking": "1/4th", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "exim_prof_know", "title": "International Trade, Forex, Corporate Banking & Export Credit", "description": "Foreign Trade Policy, letters of credit (UCP 600), buyers credit, lines of credit (LOC), project exports.", "sub_points": ["Incoterms 2020, export credit guarantee (ECGC) policies, FEMA provisions on trade credit", "Corporate finance: working capital appraisal, syndicated loans, foreign currency borrowings"]}]},
                        {"paper_id": "exim_desc", "paper_name": "Part B: Descriptive Professional & English Test", "marks": 100, "duration_hours": 1.17, "question_type": "Descriptive Typing", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "exim_desc_papers", "title": "Case Analysis on Export Finance, Essay & Letter", "description": "Subjective questions testing credit appraisal of an export project and macroeconomic essay.", "sub_points": ["Appraisal of cross-border overseas investment projects, sovereign credit risk evaluation"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage II: Personal Interview", "stage_type": "Personal Interview", "total_stage_marks": 50,
                    "papers": [{"paper_id": "exim_interview", "paper_name": "Exim Bank Selection Interview", "marks": 50, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "exim_int_eval", "title": "Global Trade Diplomacy & Export Credit Expertise", "description": "Assessment of commercial acumen in promoting Indian exports across Africa, Latin America, and ASEAN.", "sub_points": ["Geopolitical risks, supply chain realignment (China+1), currency swap agreements"]}]}]
                }
            ]
        ),
        (
            "UPPSC_PCS", "UPPSC Combined State / Upper Subordinate Services (PCS)", "UPPSC PCS", 1600,
            "1/3rd penalty on Prelims Objective Papers",
            "Advt. No. A-1/E-1/2024 / UP Civil Services Executive Branch Rules",
            "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination", "stage_type": "Objective Screening (400 Marks)", "total_stage_marks": 400,
                    "papers": [
                        {"paper_id": "uppsc_pre_p1", "paper_name": "Paper I: General Studies (GS-1)", "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ (150 Questions)", "negative_marking": "1/3rd (0.44)", "is_qualifying": False, "merit_status": "Counted for Prelims Cutoff", "topics": [{"topic_id": "uppsc_pre_gs1", "title": "General Studies & Uttar Pradesh Special Awareness", "description": "Indian history, geography, economy, polity, and Uttar Pradesh specific socio-cultural history.", "sub_points": ["UP geography, rivers, mineral deposits, archaeological sites, census 2011", "National freedom struggle with UP leaders, modern scientific breakthroughs"]}]},
                        {"paper_id": "uppsc_pre_p2", "paper_name": "Paper II: General Studies II (CSAT)", "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ (100 Questions)", "negative_marking": "1/3rd (0.66)", "is_qualifying": True, "qualifying_threshold_pct": 33.33, "merit_status": "Qualifying Only (Min 33%)", "topics": [{"topic_id": "uppsc_csat", "title": "Comprehension, Interpersonal Skills & Hindi/English Grammar", "description": "General Hindi (Class X), General English (Class X), communication skills, and mental ability.", "sub_points": ["Class X Hindi grammar (sandhi, samas, tatsam/tadbhava), decision making, numeracy"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Written Examination", "stage_type": "Descriptive Written (1500 Marks)", "total_stage_marks": 1500,
                    "papers": [
                        {"paper_id": "uppsc_mains_hindi", "paper_name": "General Hindi", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "uppsc_hindi_desc", "title": "Hindi Gadya, Sarkari Patra & Vyakaran", "description": "Official government letters, circulars, idioms, proverbs, and precis.", "sub_points": ["Sarkari, ardha-sarkari patra, karyalay gyapan, vartani shuddhi"]}]},
                        {"paper_id": "uppsc_mains_essay", "paper_name": "Essay (3 Essays in Hindi / English / Urdu)", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "uppsc_essay", "title": "Literature, Socio-Political & Disaster Themes", "description": "3 essays of 700 words each across literature, national development, and natural disasters.", "sub_points": ["Sahitya aur sanskriti, krishi evam vyapar, rashtriya vikas yojanaen"]}]},
                        {"paper_id": "uppsc_mains_gs1_4", "paper_name": "GS Papers I, II, III, IV (200m each)", "marks": 800, "duration_hours": 12.0, "question_type": "4 Descriptive Papers", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "uppsc_gs1_4", "title": "History, Polity, Economy, Environment & Ethics", "description": "Aligned with UPSC GS-I to GS-IV curricula.", "sub_points": ["National history, governance, international relations, budget, ethics case studies"]}]},
                        {"paper_id": "uppsc_mains_gs5_6", "paper_name": "GS Papers V & VI: Uttar Pradesh Special (200m each)", "marks": 400, "duration_hours": 6.0, "question_type": "2 Descriptive Papers", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "uppsc_gs5_6", "title": "In-Depth Uttar Pradesh Polity, Economy, Culture & Security", "description": "Dedicated state papers covering UP political administration, state budget, One District One Product (ODOP), and heritage.", "sub_points": ["UP state legislature, Panchayati raj, land revenue code", "UP budget, industrial corridors (Defence Corridor, Purvanchal Expressway), tourist circuits"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality Test (Interview)", "stage_type": "Oral Board Interview", "total_stage_marks": 100,
                    "papers": [{"paper_id": "uppsc_interview", "paper_name": "Personality Interview", "marks": 100, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "uppsc_int_eval", "title": "Administrative Suitability & Uttar Pradesh Governance", "description": "Assessment of field resolution skills, law and order maintenance, and state welfare implementation.", "sub_points": ["Handling of communal tensions, land disputes, and implementation of CM dashboard initiatives"]}]}]
                }
            ]
        ),
        (
            "BPSC_CCE", "BPSC Combined Competitive Examination (CCE)", "BPSC CCE", 1020,
            "1/3rd penalty on Prelims Objective Paper (0.33 per wrong answer)",
            "Advt. No. 23/2024 (70th Integrated CCE) / Bihar Administrative Service Rules",
            "https://bpsc.bih.nic.in/Advt/NB-2024-09-02-01.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination", "stage_type": "Objective Screening (150 Marks)", "total_stage_marks": 150,
                    "papers": [
                        {"paper_id": "bpsc_pre_gs", "paper_name": "General Studies", "marks": 150, "duration_hours": 2.0, "question_type": "Objective MCQ (150 Questions)", "negative_marking": "1/3rd (0.33)", "is_qualifying": False, "merit_status": "Screening Cutoff", "topics": [{"topic_id": "bpsc_pre_topics", "title": "General Science, Bihar History, Indian Polity & Geography", "description": "Emphasis on Bihar's contribution to Indian freedom struggle and state geography.", "sub_points": ["Champaran Satyagraha, Quit India movement in Bihar, Kunwar Singh 1857 revolt", "Bihar river systems (Ganga, Kosi, Gandak), soil zones, mineral reserves"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Examination", "stage_type": "Descriptive Written (900 Merit Marks + Qualifying)", "total_stage_marks": 900,
                    "papers": [
                        {"paper_id": "bpsc_mains_hindi", "paper_name": "General Hindi", "marks": 100, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": True, "qualifying_threshold_pct": 30.0, "merit_status": "Qualifying Only (Min 30%)", "topics": [{"topic_id": "bpsc_hindi", "title": "Hindi Essay, Grammar & Syntax", "description": "Essay (30m), Grammar (30m), Syntax (25m), Precis (15m).", "sub_points": ["Basic Hindi composition and correction"]}]},
                        {"paper_id": "bpsc_mains_gs1", "paper_name": "General Studies I", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "bpsc_gs1", "title": "Modern History, Indian Culture & Statistical Analysis", "description": "Patna Qalam, Mauryan art, Santhal uprising, and rigorous statistical graphs/diagrams (72m).", "sub_points": ["Mauryan and Pala art, Western education in Bihar, statistical bar/pie/line charts"]}]},
                        {"paper_id": "bpsc_mains_gs2", "paper_name": "General Studies II", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "bpsc_gs2", "title": "Indian Polity, Economy, Geography & Role of S&T", "description": "Judicial activism, governor's role, Bihar economic development, flood mitigation technology.", "sub_points": ["Federalism and coalition politics, agricultural roadmap of Bihar, disaster technology"]}]},
                        {"paper_id": "bpsc_mains_essay", "paper_name": "Essay Paper (3 Sections: Section 3 on Bihar Proverbs/Dialects)", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "bpsc_essay", "title": "National, Abstract & Bihar Folk Proverbs/Wisdom", "description": "100 marks section dedicated to essays on Bhojpuri, Maithili, and Magahi cultural maxims.", "sub_points": ["Philosophical essays, socio-economic developments, Bihar cultural idioms and folk wisdom"]}]},
                        {"paper_id": "bpsc_mains_opt", "paper_name": "Optional Subject (Objective MCQ)", "marks": 100, "duration_hours": 2.0, "question_type": "Objective MCQ (Qualifying Only)", "negative_marking": "None", "is_qualifying": True, "qualifying_threshold_pct": 40.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "bpsc_opt", "title": "Chosen Optional Subject", "description": "100 objective questions testing basic domain familiarity.", "sub_points": ["Discipline-specific concepts in selected optional"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality Test (Interview)", "stage_type": "Oral Board Interview", "total_stage_marks": 120,
                    "papers": [{"paper_id": "bpsc_interview", "paper_name": "BPSC Personality Interview", "marks": 120, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit (Final = Mains 900m + Interview 120m = 1020m)", "topics": [{"topic_id": "bpsc_int_eval", "title": "Field Administration & Bihar Development Paradigms", "description": "Evaluation of applicant's dedication to grassroot governance, flood/drought management, and law enforcement.", "sub_points": ["Seven Resolves (Saat Nischay) schemes, crime reduction, caste census dynamics"]}]}]
                }
            ]
        ),
        (
            "MPPSC_SSE", "Madhya Pradesh State Service Examination (SSE)", "MPPSC SSE", 1685,
            "No negative marking in Prelims",
            "Advt. No. 40/2023 / MP Civil Services Rules",
            "https://mppsc.mp.gov.in/uploads/advertisement/Advt_State_Service_Exam_2024.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination", "stage_type": "Objective Screening (400 Marks)", "total_stage_marks": 400,
                    "papers": [
                        {"paper_id": "mppsc_pre_p1", "paper_name": "Paper I: General Studies", "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ (100 Questions)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Counted for Cutoff", "topics": [{"topic_id": "mppsc_pre_gs", "title": "History, Geography & Tribal Culture of Madhya Pradesh", "description": "Gond, Bhil, Baiga tribal cultures, MP historical dynasties, Narmada river basin.", "sub_points": ["Tribal personalities (Tantya Bhil, Birsa Munda), MP national parks (Kanha, Bandhavgarh)"]}]},
                        {"paper_id": "mppsc_pre_p2", "paper_name": "Paper II: General Aptitude Test", "marks": 200, "duration_hours": 2.0, "question_type": "Objective MCQ (100 Questions)", "negative_marking": "None", "is_qualifying": True, "qualifying_threshold_pct": 40.0, "merit_status": "Qualifying Only (Min 40%)", "topics": [{"topic_id": "mppsc_csat", "title": "Comprehension & Decision Making", "description": "Reasoning, mental ability, basic Hindi language comprehension.", "sub_points": ["Logical reasoning, interpersonal communication, Hindi passages"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Written Examination", "stage_type": "Descriptive Written (1500 Marks)", "total_stage_marks": 1500,
                    "papers": [
                        {"paper_id": "mppsc_mains_p1", "paper_name": "Paper I: History and Geography", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p1", "title": "Indian & MP History, Physical & Water Resources", "description": "Ancient to modern history with focus on MP dynasties (Holkar, Scindia, Chandela).", "sub_points": ["Architecture of MP (Khajuraho, Sanchi), soil types, disaster management"]}]},
                        {"paper_id": "mppsc_mains_p2", "paper_name": "Paper II: Constitution, Governance, Political & Social Structure", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p2", "title": "Polity, Social Welfare, Health & Education", "description": "Constitution, regulatory commissions, self-help groups, tribal welfare.", "sub_points": ["Statutory commissions (MPPSC, Human Rights), welfare schemes, education indicators"]}]},
                        {"paper_id": "mppsc_mains_p3", "paper_name": "Paper III: Science and Technology", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p3", "title": "General Science, Mathematics, Computer & Environment", "description": "Units of measurement, basic mathematics, geology, energy, ecology.", "sub_points": ["Carbon footprint, renewable energy, computer networks, public health programs"]}]},
                        {"paper_id": "mppsc_mains_p4", "paper_name": "Paper IV: Philosophy, Psychology, Public Administration & Case Studies", "marks": 300, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p4", "title": "Moral Thinkers, Emotional Intelligence & Case Studies", "description": "Indian and western philosophers, integrity, probity, administrative case studies.", "sub_points": ["Kautilya, Kabir, Swami Vivekananda, corruption remedies, citizen charters"]}]},
                        {"paper_id": "mppsc_mains_p5", "paper_name": "Paper V: General Hindi and Grammar", "marks": 200, "duration_hours": 2.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p5", "title": "Hindi Grammar, Translations & Idioms", "description": "Sandhi, samas, tatsam/tadbhava, administrative terminology, Hindi-English translation.", "sub_points": ["Alankar, muhavare, lokoktiyan, vyakaran shuddhi"]}]},
                        {"paper_id": "mppsc_mains_p6", "paper_name": "Paper VI: Hindi Essay and Draft Writing", "marks": 100, "duration_hours": 2.5, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "mppsc_p6", "title": "Hindi Essays & Government Drafts", "description": "Long essay (1000 words), short essay (500 words), and official draft writing.", "sub_points": ["Prativedan lekhan, anushmarak, paripatra, rashtriya vikas essay"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality Test (Interview)", "stage_type": "Oral Board Interview", "total_stage_marks": 185,
                    "papers": [{"paper_id": "mppsc_interview", "paper_name": "Personality Interview", "marks": 185, "duration_hours": 0.5, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit (Final = Mains 1500m + Interview 185m = 1685m)", "topics": [{"topic_id": "mppsc_int_eval", "title": "State Governance & Tribal Administration", "description": "Assessment of leadership stamina and innovative execution for MP rural and tribal belts.", "sub_points": ["PESA Act implementation, forest wealth preservation, industrial corridors"]}]}]
                }
            ]
        ),
        (
            "RPSC_RAS", "Rajasthan State and Subordinate Services (RAS/RTS)", "RPSC RAS", 900,
            "1/3rd penalty on Prelims Objective Paper (0.44 per wrong answer)",
            "Advt. No. 02/2023-24 / Rajasthan State and Subordinate Services Rules, 1999",
            "https://rpsc.rajasthan.gov.in/Static/RecruitmentAdvertisements/RAS_2023_Detailed_Notification.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Examination", "stage_type": "Objective Screening (200 Marks)", "total_stage_marks": 200,
                    "papers": [
                        {"paper_id": "ras_pre_gk_gs", "paper_name": "General Knowledge & General Science", "marks": 200, "duration_hours": 3.0, "question_type": "Objective MCQ (150 Questions)", "negative_marking": "1/3rd (0.44)", "is_qualifying": False, "merit_status": "Screening Cutoff", "topics": [{"topic_id": "ras_pre_topics", "title": "Rajasthan Heritage, Indian Polity, Economy & Science", "description": "Forts, palaces, folk deities (Panchpir), desert ecosystem, and state budget.", "sub_points": ["Aravalli geomorphology, UNESCO hill forts, Marwar/Mewar history, Rajasthan renewable energy"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Written Examination", "stage_type": "Descriptive Written (800 Marks)", "total_stage_marks": 800,
                    "papers": [
                        {"paper_id": "ras_mains_p1", "paper_name": "Paper I: General Studies I", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ras_p1", "title": "History, Economics, Sociology, Management, Accounting & Audit", "description": "Indian history, Rajasthan economy, financial accounting, behavior, and business ethics.", "sub_points": ["Peasant movements (Bijolia), Rajasthan budget, accounting ratios, audit standards"]}]},
                        {"paper_id": "ras_mains_p2", "paper_name": "Paper II: General Studies II", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ras_p2", "title": "Administrative Ethics, General Science & Earth Sciences", "description": "Ethical concepts, chemistry, biology, space tech, geology, water resources of Rajasthan.", "sub_points": ["Bhagavad Gita ethics, Gandhi ethics, biotechnology, Indira Gandhi Canal Project"]}]},
                        {"paper_id": "ras_mains_p3", "paper_name": "Paper III: General Studies III", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ras_p3", "title": "Indian Political System, Public Administration, Sports, Yoga, Law", "description": "Constitution, civil society, administrative behavior, Rajasthan Sports Policy, POCSO Act.", "sub_points": ["State human rights commission, RTI, consumer protection, cyber laws, sports awards"]}]},
                        {"paper_id": "ras_mains_p4", "paper_name": "Paper IV: General Hindi and General English", "marks": 200, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "ras_p4", "title": "General Hindi (120 Marks) & General English (80 Marks)", "description": "Grammar, comprehension, précis, translation, elaboration, letter drafting.", "sub_points": ["Hindi vyakaran, sandhi, samas, English grammar, comprehension, formal letters"]}]}
                    ]
                },
                {
                    "stage_id": "interview", "stage_name": "Stage III: Personality and Viva-Voce Test", "stage_type": "Oral Board Interview", "total_stage_marks": 100,
                    "papers": [{"paper_id": "ras_interview", "paper_name": "Personality Interview", "marks": 100, "duration_hours": 0.4, "question_type": "Oral Board Interview", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit (Final = Mains 800m + Interview 100m = 900m)", "topics": [{"topic_id": "ras_int_eval", "title": "State Governance, Drought Resilience & Heritage Administration", "description": "Assessment of field resolution skills, water conservation leadership, and tourism promotion.", "sub_points": ["Water harvesting (tankas, baoris), industrial development (RIICO), administrative empathy"]}]}]
                }
            ]
        ),
        (
            "TSPSC_GROUP_1", "Telangana Public Service Commission Group-I Services", "TSPSC Gr 1", 900,
            "No negative marking in Prelims",
            "Notification No. 02/2024 dated 19.02.2024 / G.O. Ms. No. 42",
            "https://websnew.tspsc.gov.in/preview/PRESSNOTICES/0220242202.pdf",
            [
                {
                    "stage_id": "prelims", "stage_name": "Stage I: Preliminary Test", "stage_type": "Objective Screening (150 Marks)", "total_stage_marks": 150,
                    "papers": [
                        {"paper_id": "tspsc_pre", "paper_name": "General Studies and Mental Ability", "marks": 150, "duration_hours": 2.5, "question_type": "Objective MCQ (150 Questions)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Screening Cutoff", "topics": [{"topic_id": "tspsc_pre_topics", "title": "Current Affairs, General Science & Telangana Heritage", "description": "Telangana society, culture, literature, arts, and policies of Telangana state.", "sub_points": ["Rythu Bandhu, Kaleshwaram project, Mission Bhagiratha, Kakatiya architecture"]}]}
                    ]
                },
                {
                    "stage_id": "mains", "stage_name": "Stage II: Main Written Examination", "stage_type": "Descriptive Written (900 Merit Marks + Qualifying English)", "total_stage_marks": 900,
                    "papers": [
                        {"paper_id": "tspsc_mains_eng", "paper_name": "General English (Qualifying)", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": True, "qualifying_threshold_pct": 35.0, "merit_status": "Qualifying Only", "topics": [{"topic_id": "tspsc_eng", "title": "English Comprehension & Drafting", "description": "Class X level English language comprehension and writing.", "sub_points": ["Precis writing, essay, grammar"]}]},
                        {"paper_id": "tspsc_mains_p1", "paper_name": "Paper I: General Essay", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written (3 Essays)", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p1", "title": "Contemporary Themes & Telangana Statehood", "description": "Essays on Indian political landscape, socio-economic challenges, and cultural reflections.", "sub_points": ["Social issues, economic growth, historical movements"]}]},
                        {"paper_id": "tspsc_mains_p2", "paper_name": "Paper II: History, Culture and Geography", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p2", "title": "India and Telangana History, Art & Geography", "description": "Satavahanas, Kakatiyas, Asaf Jahis, Telangana geography and river basins.", "sub_points": ["Godavari and Krishna river basins, temple architecture, Deccan plateau geography"]}]},
                        {"paper_id": "tspsc_mains_p3", "paper_name": "Paper III: Indian Society, Constitution and Governance", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p3", "title": "Social Structure, Indian Constitution & Good Governance", "description": "Caste, tribe, gender issues, constitutional bodies, e-governance initiatives.", "sub_points": ["Basic structure, center-state relations, local self government"]}]},
                        {"paper_id": "tspsc_mains_p4", "paper_name": "Paper IV: Economy and Development", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p4", "title": "Indian Economy, Telangana Economy & Environment", "description": "Five year plans, NITI Aayog, Telangana agricultural and industrial growth.", "sub_points": ["Pharma City, IT sector in Hyderabad, agrarian transformations"]}]},
                        {"paper_id": "tspsc_mains_p5", "paper_name": "Paper V: Science & Technology and Data Interpretation", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p5", "title": "Role of S&T in Development & Analytical Problem Solving", "description": "Space, energy, biotechnology, environmental science, and statistical data problem solving.", "sub_points": ["Solar energy, cyber security, data interpretation and logical reasoning problems"]}]},
                        {"paper_id": "tspsc_mains_p6", "paper_name": "Paper VI: Telangana Movement and State Formation", "marks": 150, "duration_hours": 3.0, "question_type": "Descriptive Written", "negative_marking": "None", "is_qualifying": False, "merit_status": "Merit", "topics": [{"topic_id": "tspsc_p6", "title": "The Idea of Telangana, Mobilization & State Formation", "description": "1948 to 2014 statehood agitation: 1969 movement, Mulki rules, JAC, parliamentary bifurcation bill.", "sub_points": ["Gentlemen's Agreement 1956, Mulki rules, Osmania University protests, AP Reorganisation Act 2014"]}]}
                    ]
                }
            ]
        )
    ]

    for eid, title, short_code, marks, neg, clause, url, stages in remaining_exams:
        data["schemes"][eid] = {
            "exam_id": eid,
            "exam_title": title,
            "short_code": short_code,
            "total_marks": marks,
            "negative_marking_rule": neg,
            "official_notification_clause": clause,
            "official_notification_url": url,
            "stages": stages
        }

    # =========================================================================
    # 11 PSU RECRUITMENTS (GATE MAPPED PATTERNS)
    # =========================================================================
    psu_recruitments = [
        ("PSU_IOCL_ET", "IOCL Recruitment of Engineers / Officers through GATE", "IOCL Officer", 100, "85% GATE + 3% GD + 12% PI", "https://iocl.com/admin/img/UploadedFiles/LatestJobOpening/Files/Detailed_Advertisement_GATE_2024.pdf"),
        ("PSU_ONGC_GT", "ONGC Recruitment of Graduate Trainees through GATE", "ONGC GT", 100, "60% GATE + 25% Academics + 15% Interview", "https://ongcindia.com/documents/77101/2988775/advt012024gt.pdf"),
        ("PSU_NTPC_EET", "NTPC Engineering Executive Trainees through GATE", "NTPC EET", 100, "85% GATE + 15% GD & PI", "https://careers.ntpc.co.in/recruitment/advt_eet2024.pdf"),
        ("PSU_PGCIL_ET", "PowerGrid Engineer Trainee through GATE", "PowerGrid ET", 100, "85% GATE + 3% GD + 12% PI", "https://www.powergrid.in/sites/default/files/inline-files/Detailed_Advt_ET_GATE_2024.pdf"),
        ("PSU_BPCL_MT", "BPCL Management Trainee Recruitment through GATE", "BPCL MT", 100, "GATE Score Shortlisting + Case Discussion & PI", "https://www.bharatpetroleum.in/images/files/GATE_Advt_2024.pdf"),
        ("PSU_HPCL_OFFICER", "HPCL Officers Recruitment in Engineering & Administration", "HPCL Officer", 100, "85% CBT/GATE + 5% Group Task + 10% PI", "https://www.hindustanpetroleum.com/documents/pdf/Recruitment_of_Officers_2024_25.pdf"),
        ("PSU_SAIL_MTT", "SAIL Management Trainee (Technical) through GATE", "SAIL MTT", 100, "GATE Score Shortlisting + Group Discussion & Interview", "https://sailcareers.com/media/uploads/Advt_MTT_GATE_2024.pdf"),
        ("PSU_GAIL_ET", "GAIL Executive Trainee through GATE", "GAIL ET", 100, "85% GATE + 15% GD & Personal Interview", "https://gailonline.com/pdf/Careers/Detailed_Advt_GAIL_OPEN_ET_2024.pdf"),
        ("PSU_COAL_INDIA_MT", "Coal India Management Trainee Recruitment", "CIL MT", 100, "CBT / GATE Score Shortlisting + Personal Interview", "https://www.coalindia.in/media/documents/Advt_No_02_2024_Recruitment_MT.pdf"),
        ("PSU_BHEL_ET", "BHEL Engineer Trainee Recruitment through GATE / CBT", "BHEL ET", 100, "75% GATE/CBT + 25% Interview", "https://careers.bhel.in/bhel/static/advt_ET_2024.pdf"),
        ("PSU_BARC_NPCIL_ET", "BARC Scientific Officer & NPCIL Executive Trainee", "BARC / NPCIL", 100, "GATE / BARC Online Exam Screening + Rigorous Technical Viva", "https://barconlineexam.com/barc2024/doc/information_brochure_OCES_DGFS_2024.pdf")
    ]

    for pid, ptitle, pcode, pmarks, pweights, purl in psu_recruitments:
        data["schemes"][pid] = {
            "exam_id": pid,
            "exam_title": ptitle,
            "short_code": pcode,
            "total_marks": pmarks,
            "negative_marking_rule": "Based on GATE scoring scheme (1/3rd penalty on MCQs)",
            "official_notification_clause": f"PSU Direct Recruitment Notification / Selection Weightage: {pweights}",
            "official_notification_url": purl,
            "is_psu_recruitment": True,
            "parent_exam_id": "GATE",
            "stages": [
                {
                    "stage_id": "gate_screening",
                    "stage_name": "Stage I: GATE 2027 Examination Screening",
                    "stage_type": "National CBT Qualification (IIT GATE)",
                    "total_stage_marks": 100,
                    "description": "Candidates must appear in GATE in corresponding engineering discipline (ME/CE/EE/EC/CS/CH/IN). Marks normalized out of 100.",
                    "papers": [
                        {
                            "paper_id": f"{pid.lower()}_gate_paper",
                            "paper_name": "GATE Computer Based Test (CBT)",
                            "marks": 100,
                            "duration_hours": 3.0,
                            "question_type": "Objective MCQ / NAT / MSQ",
                            "negative_marking": "1/3rd on MCQs; 0 on NAT",
                            "is_qualifying": False,
                            "merit_status": f"Primary Selection Merit ({pweights})",
                            "topics": [
                                {
                                    "topic_id": f"{pid.lower()}_gate_core",
                                    "title": "GATE Technical Core Syllabus & General Aptitude",
                                    "description": "Comprehensive engineering curriculum as prescribed in official GATE syllabus brochure.",
                                    "sub_points": [
                                        "General Aptitude (15 Marks)",
                                        "Engineering Mathematics & Core Branch Subject (85 Marks)"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "stage_id": "gd_pi",
                    "stage_name": "Stage II: Group Discussion / Group Task & Personal Interview",
                    "stage_type": "Technical & Behavioral Board Assessment",
                    "total_stage_marks": 100,
                    "description": "Shortlisted candidates based on GATE merit appear before corporate executive board.",
                    "papers": [
                        {
                            "paper_id": f"{pid.lower()}_board",
                            "paper_name": "Executive Board Interview & Group Assessment",
                            "marks": 100,
                            "duration_hours": 0.75,
                            "question_type": "Group Task, Technical Viva & Leadership Assessment",
                            "negative_marking": "None",
                            "is_qualifying": False,
                            "merit_status": "Final Selection Weightage",
                            "topics": [
                                {
                                    "topic_id": f"{pid.lower()}_interview_topics",
                                    "title": "Industrial Acumen, Core Technical Defense & Plant Safety",
                                    "description": "Rigorous technical interview on undergraduate projects, industrial internships, operations, and corporate safety bylaws.",
                                    "sub_points": [
                                        "Technical fundamentals in operational equipment and design",
                                        "Group discussion on contemporary energy transition / manufacturing dilemmas",
                                        "Psychometric suitability for refinery, power plant, or substation field postings"
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    # Write out JSON
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated curriculum schemes for {len(data['schemes'])} examinations at {OUTPUT_PATH}")

if __name__ == "__main__":
    create_dataset()
