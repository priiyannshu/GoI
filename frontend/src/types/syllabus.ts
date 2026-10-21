export type DepthLevel = 'Foundation' | 'Intermediate' | 'Advanced' | 'Analytical';

export interface TopicRecord {
  topic_id: string;
  domain: string;
  sub_domain: string;
  topic_title: string;
  description: string;
}

export interface DomainRecord {
  domain: string;
  sub_domain_count: number;
  total_topics: number;
  sub_domains: SubDomainRecord[];
}

export interface SubDomainRecord {
  sub_domain: string;
  topic_count: number;
  topics: TopicRecord[];
}

export interface ExamTopicMapping {
  exam_id: string;
  topic_id?: string;
  stage_name: string;
  depth_level: DepthLevel;
  is_optional: boolean;
  weightage_pct_estimate?: number;
  source_clause_ref?: string;
}

export interface ExamSyllabusMapping {
  exam_id: string;
  topic_id: string;
  stage_name: string;
  depth_level: DepthLevel;
  is_optional: boolean;
  weightage_pct_estimate?: number;
  source_clause_ref?: string;
}

export interface TopicTaxonomyDetail extends TopicRecord {
  mapped_exams: ExamTopicMapping[];
  mapped_exams_count: number;
  total_stage_appearances?: number;
  depth_distribution?: Record<DepthLevel, number>;
}

export interface UpSetCombination {
  key: string;
  examIds: string[];
  topicIds: string[];
  topics: TopicRecord[];
  cardinality: number;
  degree: number;
}

export interface VennRegion {
  mask: number;
  participatingExamIds: string[];
  topicIds: string[];
  topics: TopicRecord[];
  cardinality: number;
  degree: number;
  centroid: { x: number; y: number };
  label: string;
}

export interface PairwiseMetric {
  examA: string;
  examB: string;
  intersectionCount: number;
  jaccardSimilarity: number;
  overlapCoefficient: number;
  uniqueToA: number;
  uniqueToB: number;
}

export interface BipartiteGraphNode {
  id: string;
  type: 'exam' | 'topic';
  name: string;
  cluster?: string;
  category?: string;
  short_code?: string;
  sub_domain?: string;
  domain?: string;
  description?: string;
  r: number;
  degree: number;
  color?: string;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;
  index?: number;
}

export interface BipartiteGraphLink {
  source: string | BipartiteGraphNode;
  target: string | BipartiteGraphNode;
  stage_name?: string;
  depth_level: DepthLevel;
  weight?: number;
  stroke_width: number;
  is_optional: boolean;
  weightage_pct_estimate?: number;
  source_clause_ref?: string;
}

export interface BipartiteGraphData {
  nodes: BipartiteGraphNode[];
  links: BipartiteGraphLink[];
}
