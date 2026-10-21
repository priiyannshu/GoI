#!/usr/bin/env python3
"""
scripts/generate_curriculum_data.py
===================================
Generates the authoritative, aspirant-first examination scheme and syllabus
curriculum dataset for all audited examinations in the Government of India platform.
Output: frontend/src/data/exam_curriculum_data.json
"""

import json
import os

CURRICULUM_DATA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "metadata": {
    "version": "2.0.0",
    "updated_at": "2026-10-21T19:54:00Z",
    "total_exams_schemed": 32,
    "description": "Authoritative stage-by-stage and paper-by-paper examination schemes with official notification clause citations."
  },
  "schemes": {}
}

# 1. UPSC CSE
CURRICULUM_DATA["schemes"]["UPSC_CSE"] = {
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
          "is_qualifying": false,
          "merit_status": "Counted for Prelims Cutoff & Merit",
          "source_clause": "Appendix II, Section I(A) Paper-I",
          "topics": [
            {
              "topic_id": "cse_pre_curr_events",
              "title": "Current Events of National and International Importance",
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
              "title": "General Issues on Environmental Ecology, Bio-diversity and Climate Change",
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
          "is_qualifying": true,
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
          "is_qualifying": true,
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
          "is_qualifying": true,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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

# 2. GATE (Graduate Aptitude Test in Engineering)
CURRICULUM_DATA["schemes"]["GATE"] = {
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
          "is_qualifying": false,
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
        # Engineering Discipline Papers (Filtered by active discipline)
        {
          "paper_id": "gate_sec_tech_ME",
          "stream_id": "ME",
          "paper_name": "Section 2: Mechanical Engineering Technical Curriculum",
          "marks": 85,
          "duration_hours": 2.5,
          "question_type": "Objective MCQ / NAT / MSQ (55 Questions)",
          "negative_marking": "1/3rd on MCQs; 0 on NAT/MSQ",
          "is_qualifying": false,
          "merit_status": "Merit (85% Weightage)",
          "source_clause": "GATE Syllabus Paper ME",
          "topics": [
            {
              "topic_id": "gate_me_math",
              "title": "Engineering Mathematics (Linear Algebra, Calculus, Differential Equations)",
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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

# 3. UPSC ESE (Engineering Services Examination)
CURRICULUM_DATA["schemes"]["UPSC_ESE"] = {
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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
          "is_qualifying": false,
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

# 4. RBI GRADE B (Officers in Grade B General)
CURRICULUM_DATA["schemes"]["RBI_GRADE_B"] = {
  "exam_id": "RBI_GRADE_B",
  "exam_title": "RBI Officers in Grade B (General)",
  "short_code": "RBI Gr B",
  "total_marks": 375,
  "negative_marking_rule": "1/4th (0.25 marks deducted) on all Objective Questions",
  "official_notification_clause": "Scheme of Selection, Reserve Bank of India Staff Regulations, 1948",
  "official_notification_url": "https://opportunities.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4440",
  "stages": [
    {
      "stage_id": "phase1",
      "stage_name": "Phase I: Online Examination",
      "stage_type": "Objective Screening (200 Questions)",
      "total_stage_marks": 200,
      "description": "200 marks online test with individual sectional timings: GA (80m, 25m), Reasoning (60m, 45m), English (30m, 25m), Quant (30m, 25m).",
      "papers": [
        {
          "paper_id": "rbi_p1_composite",
          "paper_name": "Phase I Composite Test (GA, Reasoning, English, Quant)",
          "marks": 200,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (200 Questions, Sectional Timed)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": true,
          "merit_status": "Qualifying Screening for Phase II",
          "source_clause": "RBI Notification Appendix I Phase I",
          "topics": [
            {
              "topic_id": "rbi_p1_ga",
              "title": "General Awareness & Banking/Financial Current Affairs",
              "description": "RBI circulars, Monetary Policy Committee resolutions, Union Budget, Economic Survey, banking regulations, and global finance.",
              "sub_points": [
                "RBI notifications, repo rate trajectories, foreign exchange reserves",
                "Government flagship social schemes, financial inclusion index, priority sector lending",
                "National & international summits, sports, awards, reports (World Bank, IMF, BIS)"
              ],
              "weightage_estimate": "40% (80 Questions / 80 Marks)"
            },
            {
              "topic_id": "rbi_p1_reasoning",
              "title": "Analytical & High-Level Reasoning Ability",
              "description": "Advanced floor/box puzzles, scheduling matrices, machine input-output, data sufficiency, and critical argumentation.",
              "sub_points": [
                "Multi-variable seating arrangements and circular/linear logic puzzles",
                "Syllogisms (only a few / reverse syllogisms), direction sense, coded blood relations",
                "Critical reasoning: strengthening/weakening arguments, cause and effect"
              ],
              "weightage_estimate": "30% (60 Questions / 60 Marks)"
            },
            {
              "topic_id": "rbi_p1_quant",
              "title": "Quantitative Aptitude & Advanced Data Interpretation",
              "description": "Missing/wrong number series, quadratic equations, arithmetic applications, caselet DI, radar charts.",
              "sub_points": [
                "Profit & loss, partnership, time & work, pipe & cistern, mixture & alligation",
                "Probability, permutations & combinations, mensuration 2D/3D",
                "High-level DI: caselets, tabular, cumulative, and double bar charts"
              ],
              "weightage_estimate": "15% (30 Questions / 30 Marks)"
            },
            {
              "topic_id": "rbi_p1_english",
              "title": "English Language Proficiency",
              "description": "Reading comprehension, cloze test, sentence improvement, para jumbles, and error detection.",
              "sub_points": [
                "Financial and macroeconomic passages testing contextual vocabulary and tone",
                "Advanced cloze test, fillers, and phrase replacements"
              ],
              "weightage_estimate": "15% (30 Questions / 30 Marks)"
            }
          ]
        }
      ]
    },
    {
      "stage_id": "phase2",
      "stage_name": "Stage II: Phase II Online Examination",
      "stage_type": "Objective & Descriptive Hybrid",
      "total_stage_marks": 300,
      "description": "3 papers of 100 marks each. Paper I (ESI) & Paper III (FM) are 50% Objective + 50% Descriptive; Paper II is Descriptive English.",
      "papers": [
        {
          "paper_id": "rbi_p2_esi",
          "paper_name": "Paper I: Economic and Social Issues (ESI)",
          "marks": 100,
          "duration_hours": 2.0,
          "question_type": "50% Objective (30 Qs) + 50% Descriptive (4 Qs typed)",
          "negative_marking": "1/4th on Objective portion; None on Descriptive",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for Final Rank)",
          "source_clause": "RBI Notification Annexure II ESI",
          "topics": [
            {
              "topic_id": "rbi_esi_growth",
              "title": "Growth & Development: National Income, Poverty, Sustainable Development",
              "description": "Macroeconomic measurement, structural unemployment, sustainable development goals (SDGs), and social sector initiatives.",
              "sub_points": [
                "Measurement of growth: GDP, GNI, per capita income, green GDP accounting",
                "Poverty alleviation programs, demographic dividend, skill development missions",
                "Millennium Development Goals, SDG targets, climate change finance"
              ]
            },
            {
              "topic_id": "rbi_esi_indian_economy",
              "title": "Indian Economy: Monetary & Fiscal Policy, Banking Sector Reforms",
              "description": "Inflation targeting framework, monetary transmission, FRBM Act, public debt management, and IBC resolution.",
              "sub_points": [
                "Monetary Policy Framework Agreement, flexible inflation targeting (4% +/- 2%)",
                "Insolvency and Bankruptcy Code (IBC 2016), Bad Bank (NARCL), Prompt Corrective Action (PCA)",
                "Disinvestment policy, foreign trade policy, balance of payments, convertibility"
              ]
            },
            {
              "topic_id": "rbi_esi_social_structure",
              "title": "Social Structure in India: Multiculturalism, Urbanization & Migration",
              "description": "Demographic trends, gender empowerment, health & education infrastructure, and labor reforms.",
              "sub_points": [
                "Four New Labor Codes (Wages, Social Security, Industrial Relations, OSH)",
                "National Health Mission, Ayushman Bharat, NEP 2020 implementations"
              ]
            }
          ]
        },
        {
          "paper_id": "rbi_p2_english",
          "paper_name": "Paper II: English (Writing Skills)",
          "marks": 100,
          "duration_hours": 1.5,
          "question_type": "Descriptive Typing (Essay, Précis, Business Comprehension)",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for Final Rank)",
          "source_clause": "RBI Notification Annexure II English",
          "topics": [
            {
              "topic_id": "rbi_eng_composition",
              "title": "Descriptive Composition: Macroeconomic Essay, Précis & Comprehension",
              "description": "Typing on computer keyboard: 1 Essay (400 words), 1 Précis (170 words), and 1 Reading Comprehension question set.",
              "sub_points": [
                "Essay on central banking, financial stability, digital currency (CBDC), or ESG",
                "Précis writing strictly adhering to 1/3rd word limit without personal commentary",
                "Direct and inferential answers to discursive passages"
              ]
            }
          ]
        },
        {
          "paper_id": "rbi_p2_fm",
          "paper_name": "Paper III: General Finance and Management (FM)",
          "marks": 100,
          "duration_hours": 2.0,
          "question_type": "50% Objective (30 Qs) + 50% Descriptive (4 Qs typed)",
          "negative_marking": "1/4th on Objective portion; None on Descriptive",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for Final Rank)",
          "source_clause": "RBI Notification Annexure II FM",
          "topics": [
            {
              "topic_id": "rbi_fm_financial_system",
              "title": "Financial System: Markets, Regulatory Bodies & Global FinTech",
              "description": "Structure of Indian financial system, money markets, capital markets, FOREX market, FinTech innovations, and financial inclusion.",
              "sub_points": [
                "Call money, treasury bills, commercial papers, certificate of deposits, repos",
                "Primary vs secondary markets, SEBI regulations, mutual funds, credit rating agencies",
                "FinTech disruptions: UPI, account aggregators, central bank digital currency (e-Rupee)"
              ]
            },
            {
              "topic_id": "rbi_fm_risk_corporate_gov",
              "title": "Risk Management & Corporate Governance in Banks",
              "description": "Basel III capital accords, credit risk, market risk, operational risk, and corporate governance norms.",
              "sub_points": [
                "Basel III framework: Pillar 1, 2, 3; Capital Adequacy Ratio (CAR), CET-1, LCR, NSFR",
                "Corporate governance principles: board composition, audit committees, Uday Kotak committee"
              ]
            },
            {
              "topic_id": "rbi_fm_management_org_behavior",
              "title": "Management Principles & Organizational Behaviour (OB)",
              "description": "Leadership theories, motivation models, emotional intelligence, organizational culture, and conflict resolution.",
              "sub_points": [
                "Motivation theories: Maslow, Herzberg, McGregor, Vroom, Adam's Equity theory",
                "Leadership paradigms: Trait, behavioral, contingency, transformational, servant leadership",
                "Communication barriers, interpersonal feedback, transactional analysis, conflict handling"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "interview",
      "stage_name": "Stage III: Personality Test (Interview)",
      "stage_type": "Personal Interview",
      "total_stage_marks": 75,
      "description": "Interview conducted by RBI board assessing candidate's temperament, regulatory insight, and central banking acumen.",
      "papers": [
        {
          "paper_id": "rbi_interview",
          "paper_name": "Personality Interview",
          "marks": 75,
          "duration_hours": 0.4,
          "question_type": "Oral Board Interview",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (Final rank = Phase II 300m + Interview 75m = 375m)",
          "source_clause": "RBI Notification Phase III",
          "topics": [
            {
              "topic_id": "rbi_int_eval",
              "title": "Central Banking Perspective, Regulatory Vision & Ethical Judgment",
              "description": "Evaluation of applicant's grasp on current monetary dynamics, macro-prudential policies, and moral rectitude.",
              "sub_points": [
                "Defense of candidate bio-data, academic pedigree, and prior professional exposure",
                "Practical response to financial panic, systemic risk containment, and customer grievances",
                "Commitment to public interest and central bank independence"
              ]
            }
          ]
        }
      ]
    }
  ]
}

# 5. SEBI GRADE A (Assistant Manager)
CURRICULUM_DATA["schemes"]["SEBI_GRADE_A"] = {
  "exam_id": "SEBI_GRADE_A",
  "exam_title": "SEBI Assistant Manager (Officer Grade A - General Stream)",
  "short_code": "SEBI Gr A",
  "total_marks": 300,
  "negative_marking_rule": "1/4th (0.25 marks deducted) on all Objective Questions",
  "official_notification_clause": "SEBI (Employees Service) Regulations, 2001 & Gazette Advt No. 01/2024",
  "official_notification_url": "https://www.sebi.gov.in/sebiweb/other/careerdetail.jsp?careerId=334",
  "stages": [
    {
      "stage_id": "phase1",
      "stage_name": "Phase I: Online Screening Examination",
      "stage_type": "Objective CBT (2 Papers)",
      "total_stage_marks": 200,
      "description": "Paper 1 (Common GA, English, Quant, Reasoning; 100m, cutoff 30%) + Paper 2 (Specialized Commerce, Finance, Law, Costing; 100m, cutoff 40%). Aggregate cutoff: 40%.",
      "papers": [
        {
          "paper_id": "sebi_p1_p1",
          "paper_name": "Paper 1: Common Aptitude & Awareness",
          "marks": 100,
          "duration_hours": 1.0,
          "question_type": "Objective MCQ (80 Questions)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": true,
          "qualifying_threshold_pct": 30.0,
          "merit_status": "Qualifying Only (Min 30% required)",
          "source_clause": "SEBI Notification Phase I Paper 1",
          "topics": [
            {
              "topic_id": "sebi_p1_aptitude",
              "title": "General Awareness, English, Quantitative Aptitude & Test of Reasoning",
              "description": "General awareness focusing on financial sector news, reading comprehension, arithmetic reasoning, and puzzles.",
              "sub_points": [
                "Financial sector news, SEBI regulatory circulars, market movements",
                "Reading comprehension passages, grammar, cloze test",
                "Data interpretation, number series, arithmetic percentages and ratios",
                "Logical reasoning: seating arrangements, syllogisms, blood relations"
              ]
            }
          ]
        },
        {
          "paper_id": "sebi_p1_p2",
          "paper_name": "Paper 2: General Stream Specialized Subjects",
          "marks": 100,
          "duration_hours": 0.67,
          "question_type": "Objective MCQ (50 Questions, 40 Minutes)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": true,
          "qualifying_threshold_pct": 40.0,
          "merit_status": "Qualifying Only (Min 40% required; aggregate 40% needed for Phase II)",
          "source_clause": "SEBI Notification Phase I Paper 2",
          "topics": [
            {
              "topic_id": "sebi_p1_commerce_accounts",
              "title": "Commerce & Accountancy: Accounting Standards & Financial Statements",
              "description": "Accounting as a financial information system, Ind AS, inventory valuation, cash flow statements, and share capital accounting.",
              "sub_points": [
                "Ind AS 1, 2, 7, 16, 18, 38 principles and definitions",
                "Accounting for bonus and rights shares, buy-back of securities, employee stock options",
                "Preparation of company balance sheets and profit & loss accounts under Companies Act 2013"
              ]
            },
            {
              "topic_id": "sebi_p1_management",
              "title": "Management: Motivation, Leadership, Communication & HR",
              "description": "Foundational management theories, leadership models, corporate communication, and HR practices.",
              "sub_points": [
                "Leadership paradigms, situational leadership, Blake-Mouton managerial grid",
                "Motivational theories (Maslow, Herzberg, Alderfer ERG), emotional intelligence",
                "Communication channels, barriers to communication, active listening"
              ]
            },
            {
              "topic_id": "sebi_p1_finance",
              "title": "Finance: Financial System, Markets, Derivations & Alternative Investments",
              "description": "Role of financial intermediaries, primary & secondary markets, derivatives (forwards, futures, options), and REITs/InvITs.",
              "sub_points": [
                "SEBI mandate, capital markets ecosystem, IPO process, Book Building mechanism",
                "Derivatives: call and put options, Black-Scholes model basics, futures contracts, swaps",
                "Alternative Investment Funds (AIFs Category I, II, III), REITs, InvITs"
              ]
            },
            {
              "topic_id": "sebi_p1_costing",
              "title": "Costing: Marginal Costing, Standard Costing, Budgets & Lean Methods",
              "description": "Direct and indirect cost allocation, break-even analysis, standard costing variances, ABC costing, and JIT.",
              "sub_points": [
                "Cost-Volume-Profit (CVP) analysis, contribution margin, margin of safety",
                "Standard costing: material, labor, and overhead variance calculations",
                "Activity Based Costing (ABC), Just-in-Time (JIT), Kaizen costing"
              ]
            },
            {
              "topic_id": "sebi_p1_companies_act",
              "title": "Companies Act 2013: Corporate Governance & Statutory Compliances",
              "description": "Incorporation, prospectus, share capital, debentures, management & administration, directors, meetings, and audit.",
              "sub_points": [
                "Chapter III (Prospectus & Allotment), Chapter IV (Share Capital & Debentures)",
                "Chapter IX (Accounts of Companies), Chapter X (Audit and Auditors)",
                "Chapter XI (Appointment and Qualifications of Directors), Independent Directors"
              ]
            },
            {
              "topic_id": "sebi_p1_economics",
              "title": "Economics: Demand & Supply, National Income, Inflation & Balance of Payments",
              "description": "Microeconomic equilibria, market structures, Keynesian IS-LM framework, inflation indices, and balance of payments.",
              "sub_points": [
                "Price elasticity, indifference curve analysis, consumer surplus",
                "Monopoly, oligopoly, Cournot model, monopolistic competition",
                "IS-LM model, fiscal and monetary policy multipliers, foreign exchange regimes"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "phase2",
      "stage_name": "Stage II: Phase II Online Examination",
      "stage_type": "Descriptive & Objective Merit Examination",
      "total_stage_marks": 200,
      "description": "Paper 1 English Descriptive (100m, 1/3rd weightage) + Paper 2 Specialized Subjects (100m, 2/3rd weightage). Determines final merit list (85% weightage).",
      "papers": [
        {
          "paper_id": "sebi_p2_p1",
          "paper_name": "Paper 1: English Descriptive Test",
          "marks": 100,
          "duration_hours": 1.0,
          "question_type": "Descriptive Typing (Essay, Précis, Comprehension)",
          "negative_marking": "None",
          "is_qualifying": false,
          "qualifying_threshold_pct": 30.0,
          "merit_status": "Merit (1/3rd Weightage in Phase II score)",
          "source_clause": "SEBI Notification Phase II Paper 1",
          "topics": [
            {
              "topic_id": "sebi_p2_eng_typing",
              "title": "Descriptive Drafting on Capital Markets, ESG & Economy",
              "description": "Expressive writing: 1 Essay (30m), 1 Précis (30m), and 1 Reading Comprehension (40m) typed directly on terminal.",
              "sub_points": [
                "Structured essays on capital markets, algorithmic trading, insider trading, and FinTech",
                "Crisp précis writing adhering strictly to word count limits"
              ]
            }
          ]
        },
        {
          "paper_id": "sebi_p2_p2",
          "paper_name": "Paper 2: Advanced Specialized Subjects (Commerce, Finance, Law)",
          "marks": 100,
          "duration_hours": 0.67,
          "question_type": "Objective MCQ (50 High-Complexity Questions, 40 mins)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": false,
          "qualifying_threshold_pct": 40.0,
          "merit_status": "Merit (2/3rd Weightage in Phase II score)",
          "source_clause": "SEBI Notification Phase II Paper 2",
          "topics": [
            {
              "topic_id": "sebi_p2_advanced_commerce_law",
              "title": "In-Depth Securities Law, Financial Engineering & Advanced Accounting",
              "description": "Challenging numericals and statutory case-law applications across all 6 specialized domains.",
              "sub_points": [
                "SEBI Act 1992, Securities Contracts (Regulation) Act 1956 (SCRA), Depositories Act 1996",
                "Advanced variance analysis, marginal costing decision trees, transfer pricing",
                "Consolidated financial statements, corporate restructuring, merger valuations"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "interview",
      "stage_name": "Stage III: Personal Interview",
      "stage_type": "Personal Interview",
      "total_stage_marks": 100,
      "description": "Personal interview contributing 15% weightage towards the final selection, while Phase II marks contribute 85%.",
      "papers": [
        {
          "paper_id": "sebi_interview",
          "paper_name": "SEBI Board Personal Interview",
          "marks": 100,
          "duration_hours": 0.4,
          "question_type": "Oral Board Interview",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (15% Weightage towards Final Rank)",
          "source_clause": "SEBI Notification Phase III",
          "topics": [
            {
              "topic_id": "sebi_int_market_governance",
              "title": "Market Integrity, Investor Protection & Surveillance Acumen",
              "description": "Evaluation of applicant's technical domain competence, awareness of market scams, and regulatory resolve.",
              "sub_points": [
                "Surveillance against pump-and-dump schemes, front-running, and circular trading",
                "Investor grievance mechanisms (SCORES 2.0, Online Dispute Resolution portal)",
                "Applicant's motivation, ethical stamina, and adaptability to Mumbai headquarters"
              ]
            }
          ]
        }
      ]
    }
  ]
}

print(f"Base schemes generated: {len(CURRICULUM_DATA['schemes'])}")

# 6. NABARD GRADE A
CURRICULUM_DATA["schemes"]["NABARD_GRADE_A"] = {
  "exam_id": "NABARD_GRADE_A",
  "exam_title": "NABARD Assistant Manager in Grade A (RDBS)",
  "short_code": "NABARD Gr A",
  "total_marks": 250,
  "negative_marking_rule": "1/4th (0.25 marks deducted) on all Objective Questions",
  "official_notification_clause": "NABARD (Staff) Rules, 1982 & Advt No. 01/Grade A/2024-25",
  "official_notification_url": "https://www.nabard.org/careers-notices1.aspx?cid=552&id=32",
  "stages": [
    {
      "stage_id": "phase1",
      "stage_name": "Phase I: Preliminary Online Examination",
      "stage_type": "Objective Screening (200 Questions, 120 Minutes)",
      "total_stage_marks": 200,
      "description": "Composite test of 8 sections: 5 Qualifying sections (Reasoning 20m, English 30m, Computer 20m, Quant 20m, Decision Making 10m) + 3 Merit sections (GA 20m, ESI 40m, ARD 40m = 100m).",
      "papers": [
        {
          "paper_id": "nabard_p1_qualifying",
          "paper_name": "Paper 1A: Qualifying Aptitude Sections",
          "marks": 100,
          "duration_hours": 1.0,
          "question_type": "Objective MCQ (Reasoning, English, Computer, Quant, Decision Making)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": true,
          "qualifying_threshold_pct": 35.0,
          "merit_status": "Qualifying Only (Must clear sectional and composite cutoff)",
          "source_clause": "NABARD Notification Phase I Table 1",
          "topics": [
            {
              "topic_id": "nabard_p1_aptitude",
              "title": "Reasoning, English, Quant, Computer Knowledge & Decision Making",
              "description": "Standard banking aptitude questions with managerial decision-making scenarios.",
              "sub_points": [
                "Decision Making: ethical dilemmas, managerial triage, cost-benefit trade-offs",
                "Computer Knowledge: hardware, networking, cybersecurity, MS Office, cloud computing",
                "Reasoning & Quantitative Aptitude: high-level syllogisms, puzzles, and data interpretation"
              ]
            }
          ]
        },
        {
          "paper_id": "nabard_p1_merit",
          "paper_name": "Paper 1B: Merit Sections (GA, ESI, ARD)",
          "marks": 100,
          "duration_hours": 1.0,
          "question_type": "Objective MCQ (GA 20m, ESI 40m, ARD 40m)",
          "negative_marking": "1/4th (0.25 marks deducted)",
          "is_qualifying": false,
          "merit_status": "Counted for Phase II Shortlisting Merit",
          "source_clause": "NABARD Notification Phase I Table 2",
          "topics": [
            {
              "topic_id": "nabard_p1_ard",
              "title": "Agriculture & Rural Development (ARD): Agronomy, Horticulture, Animal Husbandry",
              "description": "Agronomic practices, soil and water conservation, irrigation water management, poultry/dairy husbandry, and rural economy.",
              "sub_points": [
                "Cropping patterns, organic farming, precision agriculture, micro-irrigation schemes",
                "Soil classification, nutrient management, fertilizer calculation (NPK)",
                "Rural credit institutions: NABARD refinance, RRBs, StCBs, PACS, Kisan Credit Card"
              ]
            },
            {
              "topic_id": "nabard_p1_esi",
              "title": "Economic and Social Issues (ESI) with Focus on Rural India",
              "description": "Rural poverty alleviation programs, SHG-Bank linkage, rural infrastructure development fund (RIDF), and rural livelihoods.",
              "sub_points": [
                "Deendayal Antyodaya Yojana (DAY-NRLM), PM Awas Yojana-Gramin, Jal Jeevan Mission",
                "Microfinance institutions, Priority Sector Lending (PSL) targets for agriculture"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "phase2",
      "stage_name": "Stage II: Phase II Main Examination",
      "stage_type": "Descriptive & Objective Hybrid",
      "total_stage_marks": 200,
      "description": "Paper 1 General English Descriptive (100m, 90 mins) + Paper 2 ESI & ARD (50% Objective + 50% Descriptive, 100m, 90 mins).",
      "papers": [
        {
          "paper_id": "nabard_p2_p1",
          "paper_name": "Paper I: General English Descriptive Test",
          "marks": 100,
          "duration_hours": 1.5,
          "question_type": "Descriptive Typing (Essay, Précis, Letter/Report Writing)",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for Final Rank)",
          "source_clause": "NABARD Notification Phase II Paper 1",
          "topics": [
            {
              "topic_id": "nabard_p2_eng",
              "title": "Descriptive English Composition on Rural & Agrarian Economy",
              "description": "Keyboard-typed essay, précis, and formal business letters or committee report drafting.",
              "sub_points": [
                "Analytical essay on climate-smart agriculture, rural banking, or agribusiness startups",
                "Precis writing of agricultural research excerpts",
                "Official correspondence: representation letter to RBI/MoA, branch inspection reports"
              ]
            }
          ]
        },
        {
          "paper_id": "nabard_p2_p2",
          "paper_name": "Paper II: Economic & Social Issues and Agriculture & Rural Development",
          "marks": 100,
          "duration_hours": 1.5,
          "question_type": "50% Objective (30 Qs) + 50% Descriptive (4 typed answers)",
          "negative_marking": "1/4th on Objective portion; None on Descriptive",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for Final Rank)",
          "source_clause": "NABARD Notification Phase II Paper 2",
          "topics": [
            {
              "topic_id": "nabard_p2_esi_ard_deep",
              "title": "Advanced Agrarian Policies, Rural Infrastructure & Social Development",
              "description": "Deep statutory analysis of rural development financing, FPOs, Agri-infrastructure fund, and tribal development.",
              "sub_points": [
                "Farmer Producer Organizations (FPOs), e-NAM integration, agricultural warehousing",
                "Watershed development, tribal development programs, microfinance regulation",
                "NABARD statutory mandate under NABARD Act 1981"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "interview",
      "stage_name": "Stage III: Personal Interview",
      "stage_type": "Personal Interview",
      "total_stage_marks": 50,
      "description": "Personal interview before NABARD selection committee assessing field aptitude and developmental vision.",
      "papers": [
        {
          "paper_id": "nabard_interview",
          "paper_name": "NABARD Selection Interview",
          "marks": 50,
          "duration_hours": 0.35,
          "question_type": "Oral Board Interview",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (Final Rank = Phase II 200m + Interview 50m = 250m)",
          "source_clause": "NABARD Notification Phase III",
          "topics": [
            {
              "topic_id": "nabard_int_eval",
              "title": "Rural Development Vision, Empathy & Leadership Temperament",
              "description": "Assessment of candidate's willingness for rural postings, developmental enthusiasm, and credit management insights.",
              "sub_points": [
                "Awareness of ground reality in rural farming communities and SHG ecosystems",
                "Innovative solutions for rural non-farm employment and agro-processing clusters"
              ]
            }
          ]
        }
      ]
    }
  ]
}

# 7. UPSC CAPF (AC)
CURRICULUM_DATA["schemes"]["UPSC_CAPF_AC"] = {
  "exam_id": "UPSC_CAPF_AC",
  "exam_title": "Central Armed Police Forces (Assistant Commandants) Examination",
  "short_code": "CAPF (AC)",
  "total_marks": 600,
  "negative_marking_rule": "1/3rd (0.83 marks deducted) on Paper I Objective Questions",
  "official_notification_clause": "Appendix I & II of MHA Gazette Notification dated 24.04.2024",
  "official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CAPF-2024-engl-240424.pdf",
  "stages": [
    {
      "stage_id": "written",
      "stage_name": "Stage I: Written Examination",
      "stage_type": "Objective & Descriptive (450 Marks)",
      "total_stage_marks": 450,
      "description": "Two papers conducted on a single day. Paper I General Ability and Intelligence (250m) + Paper II General Studies, Essay and Comprehension (200m).",
      "papers": [
        {
          "paper_id": "capf_p1",
          "paper_name": "Paper I: General Ability and Intelligence",
          "marks": 250,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (125 Questions)",
          "negative_marking": "1/3rd (0.66 marks deducted)",
          "is_qualifying": false,
          "merit_status": "Counted for Written Cutoff & Final Rank",
          "source_clause": "Appendix II, Section I Paper-I",
          "topics": [
            {
              "topic_id": "capf_p1_gma_science",
              "title": "General Mental Ability & General Science",
              "description": "Numerical ability, logical reasoning, data interpretation, everyday science, scientific temper, and modern technologies.",
              "sub_points": [
                "Quantitative aptitude, arithmetic, data sufficiency, analogy, series",
                "Physics, Chemistry, Biology of everyday observation; science in defense"
              ]
            },
            {
              "topic_id": "capf_p1_polity_economy",
              "title": "Indian Polity, Economy & Current Affairs",
              "description": "Constitution of India, security agencies, public administration, macroeconomic indicators, and border issues.",
              "sub_points": [
                "Fundamental Rights, Parliament, Emergency provisions, Police reforms",
                "Internal security challenges, border management mechanisms (BSF, CRPF, CISF, ITBP, SSB)"
              ]
            }
          ]
        },
        {
          "paper_id": "capf_p2",
          "paper_name": "Paper II: General Studies, Essay and Comprehension",
          "marks": 200,
          "duration_hours": 3.0,
          "question_type": "Descriptive Written (Part A: 4 Essays in English/Hindi; Part B: Counter-arguments, Reports, Précis in English)",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Counted for Written Cutoff & Final Rank",
          "source_clause": "Appendix II, Section I Paper-II",
          "topics": [
            {
              "topic_id": "capf_p2_essay",
              "title": "Part A: Essay Writing on Security, Polity & Society (80 Marks)",
              "description": "4 analytical essays (out of 6 options) of about 300 words each on internal security, foreign policy, and socio-economic themes.",
              "sub_points": [
                "Border security dilemmas, cyber terrorism, left-wing extremism, human rights in combat areas"
              ]
            },
            {
              "topic_id": "capf_p2_counter_arg_report",
              "title": "Part B: Arguments, Report Writing, Précis & Comprehension (120 Marks)",
              "description": "Arguments for and against a proposition, official report writing on security incidents, précis, and grammatical mechanics.",
              "sub_points": [
                "Debate formulations: Arguments for and against contemporary controversial propositions",
                "Formal incident reports: riot containment, industrial security breaches, disaster relief operations",
                "Precis writing, reading comprehension, active/passive voice, direct/indirect narration"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "pet_pst",
      "stage_name": "Stage II: Physical Standards / Physical Efficiency Tests (PET) & Medical Review",
      "stage_type": "Qualifying Physical & Medical Tests",
      "description": "Rigorous qualifying physical efficiency benchmarks enforced uniformly across all CAPF forces.",
      "papers": [
        {
          "paper_id": "capf_pet",
          "paper_name": "Physical Efficiency Test (PET) Protocol",
          "marks": 0,
          "duration_hours": 1.0,
          "question_type": "Physical Performance Gate",
          "negative_marking": "None",
          "is_qualifying": true,
          "merit_status": "Qualifying Only (Mandatory pass in all events)",
          "source_clause": "Appendix II, Section II PET Standards",
          "topics": [
            {
              "topic_id": "capf_pet_events",
              "title": "PET Events: 100m Race, 800m Race, Long Jump & Shot Put",
              "description": "Statutory physical events timed electronically under supervisory board.",
              "sub_points": [
                "100 Metres Sprint: 16 seconds (Male) / 18 seconds (Female)",
                "800 Metres Run: 3 minutes 45 seconds (Male) / 4 minutes 45 seconds (Female)",
                "Long Jump: 3.50 Metres (3 chances for Male) / 3.00 Metres (3 chances for Female)",
                "Shot Put (7.26 Kgs): 4.50 Metres (Male only, 3 chances)"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "interview",
      "stage_name": "Stage III: Interview / Personality Test",
      "stage_type": "Oral Board Interview",
      "total_stage_marks": 150,
      "description": "Interview conducted by UPSC board assessing leadership caliber, tactical fortitude, and armed police aptitude.",
      "papers": [
        {
          "paper_id": "capf_interview",
          "paper_name": "UPSC Armed Police Personality Test",
          "marks": 150,
          "duration_hours": 0.5,
          "question_type": "Oral Board Interview",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (Final Rank = Written 450m + Interview 150m = 600m)",
          "source_clause": "Appendix II, Section III Interview",
          "topics": [
            {
              "topic_id": "capf_int_eval",
              "title": "Leadership Caliber, Border Security Doctrine & Force Leadership",
              "description": "Assessment of tactical judgment, crisis management, troop leadership, and constitutional values.",
              "sub_points": [
                "Force preferences (CISF vs BSF vs CRPF vs ITBP vs SSB) and operational rationale",
                "Handling of civil unrest, counter-insurgency tactics, and humanitarian relief"
              ]
            }
          ]
        }
      ]
    }
  ]
}

# 8. UPSC CDS (Combined Defence Services)
CURRICULUM_DATA["schemes"]["UPSC_CDS"] = {
  "exam_id": "UPSC_CDS",
  "exam_title": "Combined Defence Services Examination",
  "short_code": "CDS",
  "total_marks": 600,
  "negative_marking_rule": "1/3rd (0.33 marks deducted) on all Objective Questions",
  "official_notification_clause": "Appendix I & II of MoD Gazette of India Notification",
  "official_notification_url": "https://upsc.gov.in/sites/default/files/Notif-CDSI-24-engl-201223.pdf",
  "stages": [
    {
      "stage_id": "written",
      "stage_name": "Stage I: Written Examination",
      "stage_type": "Objective Screening",
      "total_stage_marks": 300,
      "description": "IMA/INA/AFA: 3 papers (English 100m, GK 100m, Elementary Maths 100m = 300m). OTA: 2 papers (English 100m, GK 100m = 200m).",
      "papers": [
        {
          "paper_id": "cds_written_english",
          "paper_name": "Paper I: English",
          "marks": 100,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (120 Questions)",
          "negative_marking": "1/3rd (0.27 marks deducted)",
          "is_qualifying": false,
          "merit_status": "Counted for Written Cutoff & Final Merit",
          "source_clause": "Appendix II Standard and Syllabus Paper 1",
          "topics": [
            {
              "topic_id": "cds_eng_usage",
              "title": "English Grammar, Reading Comprehension & Usage",
              "description": "Testing workmanlike understanding of language: spotting errors, ordering of words, idioms, and passages.",
              "sub_points": [
                "Spotting errors, sentence rearrangement, order of sentences in a paragraph",
                "Synonyms, antonyms, idioms and phrases, comprehension of unseen passages"
              ]
            }
          ]
        },
        {
          "paper_id": "cds_written_gk",
          "paper_name": "Paper II: General Knowledge",
          "marks": 100,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (120 Questions)",
          "negative_marking": "1/3rd (0.27 marks deducted)",
          "is_qualifying": false,
          "merit_status": "Counted for Written Cutoff & Final Merit",
          "source_clause": "Appendix II Standard and Syllabus Paper 2",
          "topics": [
            {
              "topic_id": "cds_gk_comprehensive",
              "title": "General Knowledge: Everyday Science, History, Geography & Defence",
              "description": "Scientific observations, Indian history, physical geography of India and world, and military affairs.",
              "sub_points": [
                "Physics, chemistry, biology principles tested through everyday observation",
                "Indian National Movement, ancient and medieval Indian heritage",
                "Defence forces structure, military exercises, missile tests, and naval fleet assets"
              ]
            }
          ]
        },
        {
          "paper_id": "cds_written_maths",
          "paper_name": "Paper III: Elementary Mathematics (IMA / INA / AFA Only)",
          "marks": 100,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (100 Questions; Not applicable for OTA)",
          "negative_marking": "1/3rd (0.33 marks deducted)",
          "is_qualifying": false,
          "merit_status": "Merit (Counted for IMA, INA, AFA Merit)",
          "source_clause": "Appendix II Standard and Syllabus Paper 3",
          "topics": [
            {
              "topic_id": "cds_maths_curriculum",
              "title": "Arithmetic, Algebra, Trigonometry, Geometry & Mensuration",
              "description": "High-standard Class X mathematics: number theory, polynomials, trigonometric identities, circle theorems, and 3D volumes.",
              "sub_points": [
                "Arithmetic: prime numbers, logarithms, percentages, profit & loss, ratio, work & time",
                "Algebra: basic operations, remainder theorem, theory of quadratics, linear equations",
                "Trigonometry: simple trigonometric identities, use of trigonometric tables, heights & distances",
                "Geometry: congruence of triangles, similarity, circles and tangents, locus of points",
                "Mensuration: areas of plane figures, surface areas and volumes of cuboids, cylinders, cones, spheres"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "ssb",
      "stage_name": "Stage II: SSB Interview & Intelligence/Personality Test",
      "stage_type": "5-Day Services Selection Board (SSB)",
      "total_stage_marks": 300,
      "description": "5-day psychological, obstacle, and interview process. Stage 1 Screening (OIR + PPDT) followed by Stage 2 (Psych Tests, GTO, Personal Interview, Conference).",
      "papers": [
        {
          "paper_id": "cds_ssb_board",
          "paper_name": "SSB 5-Day Assessment Battery",
          "marks": 300,
          "duration_hours": 120.0,
          "question_type": "Psychological Battery, GTO Obstacles & Board Interview",
          "negative_marking": "None",
          "is_qualifying": false,
          "merit_status": "Merit (300m for IMA/INA/AFA; 200m for OTA)",
          "source_clause": "Appendix II SSB Selection System",
          "topics": [
            {
              "topic_id": "cds_ssb_olqs",
              "title": "Assessment of 15 Officer Like Qualities (OLQs)",
              "description": "Evaluates planning and organizing ability, social adaptability, social effectiveness, dynamic qualities, and courage.",
              "sub_points": [
                "Stage 1: Officer Intelligence Rating (OIR) test & Picture Perception and Discussion Test (PPDT)",
                "Stage 2 Psychological Battery: Thematic Apperception Test (TAT), Word Association Test (WAT), Situation Reaction Test (SRT), Self Description (SD)",
                "Group Testing Officer (GTO) Tasks: Group Discussion, Military Planning Exercise, Progressive Group Task, Snake Race, Command Task, Individual Obstacles",
                "Personal Interview with Interviewing Officer & Final Board Conference"
              ]
            }
          ]
        }
      ]
    }
  ]
}

# 9. IAF AFCAT (Air Force Common Admission Test)
CURRICULUM_DATA["schemes"]["IAF_AFCAT"] = {
  "exam_id": "IAF_AFCAT",
  "exam_title": "Air Force Common Admission Test",
  "short_code": "AFCAT",
  "total_marks": 300,
  "negative_marking_rule": "+3 marks for correct answer, -1 mark deducted for incorrect answer",
  "official_notification_clause": "AFCAT Information Notification, Scheme of Online Examination",
  "official_notification_url": "https://afcat.cdac.in/AFCAT/assets/images/news/AFCAT_01_2024_NOTIFICATION.pdf",
  "stages": [
    {
      "stage_id": "cbt",
      "stage_name": "Stage I: Online CBT Examination",
      "stage_type": "Objective CBT (100 Questions, 300 Marks)",
      "total_stage_marks": 300,
      "description": "2 hours online test containing 100 questions (+3, -1) across General Awareness, Verbal Ability, Numerical Ability, and Reasoning.",
      "papers": [
        {
          "paper_id": "afcat_cbt_composite",
          "paper_name": "AFCAT Online Test",
          "marks": 300,
          "duration_hours": 2.0,
          "question_type": "Objective MCQ (100 Questions: +3 correct, -1 wrong)",
          "negative_marking": "1 mark deducted per incorrect answer (-1.00)",
          "is_qualifying": true,
          "merit_status": "Qualifying Screening for AFSB Interview",
          "source_clause": "AFCAT Syllabus Paragraph 7",
          "topics": [
            {
              "topic_id": "afcat_ga",
              "title": "General Awareness: History, Geography, Defense, Sports, Civics",
              "description": "Modern defense exercises, aerospace advances, sports championships, national symbols, and environmental summits.",
              "sub_points": [
                "Indian Air Force fleet, squadrons, fighter aircraft, missiles, radar systems",
                "National sports events, Olympic medals, awards, and bilateral military drills"
              ]
            },
            {
              "topic_id": "afcat_verbal",
              "title": "Verbal Ability in English",
              "description": "Comprehension passages, error detection, sentence completion, synonyms, antonyms, idioms and phrases.",
              "sub_points": [
                "Vocabulary tests, one-word substitutions, analogy, and sentence correction"
              ]
            },
            {
              "topic_id": "afcat_numerical",
              "title": "Numerical Ability",
              "description": "Decimal fractions, time & work, average, profit & loss, ratio & proportion, simple interest, speed & distance.",
              "sub_points": [
                "Problems on trains, boats and streams, percentage, mixtures and alligations"
              ]
            },
            {
              "topic_id": "afcat_reasoning",
              "title": "Reasoning and Military Aptitude",
              "description": "Verbal and non-verbal spatial reasoning, pattern completion, embedded figures, odd one out, and analogy.",
              "sub_points": [
                "Rotational figure series, paper cutting, Venn diagrams, dot situation puzzles"
              ]
            }
          ]
        }
      ]
    },
    {
      "stage_id": "afsb",
      "stage_name": "Stage II: Air Force Selection Board (AFSB) Testing",
      "stage_type": "5-Day AFSB Assessment + CPSS (for Flying Branch)",
      "description": "5-day military selection board. Flying branch candidates also undergo Computerised Pilot Selection System (CPSS) once in a lifetime.",
      "papers": [
        {
          "paper_id": "afcat_afsb_process",
          "paper_name": "AFSB Interview & CPSS Testing",
          "marks": 0,
          "duration_hours": 120.0,
          "question_type": "Screening, Psych, GTO, PI & Flight Simulator",
          "negative_marking": "None",
          "is_qualifying": true,
          "merit_status": "Mandatory Recommendation for Commissioning",
          "source_clause": "AFCAT AFSB Selection Guidelines",
          "topics": [
            {
              "topic_id": "afcat_cpss",
              "title": "CPSS: Cognitive & Psychomotor Cockpit Simulation",
              "description": "Rigorous electronic testing of sensory-motor and multi-attribute cockpit decision capacity. Conducted only once per candidate.",
              "sub_points": [
                "Instrument battery test assessing flight display interpretation",
                "Sensory-motor apparatus test assessing hand-eye-foot coordination under acceleration"
              ]
            }
          ]
        }
      ]
    }
  ]
}

