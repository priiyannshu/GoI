export interface CandidateAccount {
  user_id: string;
  candidate_name: string;
  created_at?: string;
}

export interface AuthResponse {
  success: boolean;
  user_id?: string;
  candidate_name?: string;
  profile?: any;
  message?: string;
  error?: string;
  not_found?: boolean;
  multiple_accounts?: boolean;
  accounts?: CandidateAccount[];
}
