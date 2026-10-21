export interface SyllabusTopic {
  topic_id: string;
  title: string;
  description: string;
  sub_points?: string[];
  weightage_estimate?: string;
  source_clause?: string;
  gazette_link?: string;
}

export interface SchemePaper {
  paper_id: string;
  paper_name: string;
  marks: number;
  duration_hours: number;
  question_type: string;
  negative_marking: string;
  is_qualifying: boolean;
  qualifying_threshold_pct?: number;
  merit_status: string;
  source_clause?: string;
  stream_id?: string;
  topics: SyllabusTopic[];
}

export interface SchemeStage {
  stage_id: string;
  stage_name: string;
  stage_type: string;
  total_stage_marks?: number;
  description?: string;
  papers: SchemePaper[];
}

export interface DisciplineOption {
  code: string;
  name: string;
}

export interface ExaminationScheme {
  exam_id: string;
  exam_title: string;
  short_code: string;
  total_marks: number;
  negative_marking_rule: string;
  official_notification_clause?: string;
  official_notification_url?: string;
  is_psu_recruitment?: boolean;
  parent_exam_id?: string;
  disciplines?: DisciplineOption[];
  stages: SchemeStage[];
}

export interface CurriculumDataset {
  $schema?: string;
  metadata?: {
    version: string;
    updated_at: string;
    total_exams_schemed: number;
    description: string;
  };
  schemes: Record<string, ExaminationScheme>;
}

export interface ProgressMetric {
  completed: number;
  total: number;
  pct: number;
}
