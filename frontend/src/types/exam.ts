export type ExamCategory =
  | 'Central-Civil'
  | 'Regulatory'
  | 'Defense'
  | 'State-PSC'
  | 'PSU';

export interface ExamRecord {
  exam_id: string;
  title: string;
  short_code: string;
  category: ExamCategory;
  administering_body: string;
  frequency: string;
  official_website: string;
  latest_official_notification_url: string;
  latest_gazette_ref?: string;
  tentative_timeline_2027: Record<string, any>;
  description?: string;
  eligibility?: Record<string, any>;
}
