/**
 * SkillSathi Core TypeScript Types
 * Smart India Hackathon 2026 - Problem Statement 26241
 */

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
  error?: string | null;
  timestamp: string;
  meta?: Record<string, any>;
}

export interface AppHealth {
  status: "healthy" | "degraded" | "unhealthy";
  app_name: string;
  tagline: string;
  version: string;
  environment: string;
  uptime_seconds: number;
  timestamp: string;
}

export interface DatabaseHealth {
  status: "healthy" | "degraded" | "unhealthy";
  connected: boolean;
  latency_ms: number;
  database_engine: string;
  database_version?: string;
  host?: string;
  database?: string;
  error?: string;
}

export interface VersionInfo {
  app_name: string;
  version: string;
  api_version: string;
  problem_statement: string;
  ai_provider: string;
  ai_model: string;
  build_time: string;
  supported_locales: string[];
}

export interface EvidenceSource {
  id: number;
  source_name: string;
  publisher: string;
  url?: string;
  source_type: string;
  geographic_scope: string;
  data_period?: string;
  publication_date?: string;
  retrieval_timestamp: string;
  verification_status: "OFFICIAL_VERIFIED" | "PROVISIONALLY_VERIFIED" | "UNVERIFIED" | "REJECTED";
  freshness_status: "LIVE" | "FRESH" | "STALE" | "FAILED" | "MANUAL_REVIEW";
  last_synced_at?: string;
  next_recommended_sync?: string;
  is_demo: boolean;
}

export interface LocationInfo {
  id: number;
  state: string;
  district: string;
  pincode?: string;
  region_type: string;
  industrial_cluster_name?: string;
  is_demo: boolean;
}

export interface TradeCategory {
  id: number;
  code: string;
  name: string;
  description?: string;
  icon_name: string;
}

export interface ProgressionOption {
  id: number;
  pathway_step_id: number;
  destination_type: string;
  title: string;
  eligibility_criteria?: string;
  recognizing_body: string;
  source_id?: number;
  source?: EvidenceSource;
}

export interface CareerPathwayStep {
  id: number;
  pathway_id: number;
  step_order: number;
  role_title: string;
  experience_required_months: number;
  certifications_required?: string;
  expected_monthly_inr_min?: number;
  expected_monthly_inr_max?: number;
  education_ladder_option?: string;
  description?: string;
  progression_options?: ProgressionOption[];
}

export interface CareerPathway {
  id: number;
  trade_id: number;
  title: string;
  overview?: string;
  entry_qualification: string;
  total_progression_years: number;
  is_demo: boolean;
  steps: CareerPathwayStep[];
}

export interface TrainingProvider {
  id: number;
  name: string;
  code: string;
  provider_type: string;
  location_id?: number;
  affiliation_body: string;
  website_url?: string;
  is_verified: boolean;
  is_demo: boolean;
  location?: LocationInfo;
}

export interface Trade {
  id: number;
  category_id?: number;
  code: string;
  title: string;
  sector: string;
  nsqf_level: number;
  duration_months: number;
  min_qualification: string;
  description?: string;
  is_active: boolean;
  is_demo: boolean;
  category?: TradeCategory;
  career_pathways?: CareerPathway[];
  providers?: TrainingProvider[];
}

export interface EmploymentData {
  id: number;
  outcome_id?: number;
  trade_id: number;
  location_id?: number;
  top_hiring_sectors?: string[];
  top_employer_names?: string[];
  retention_rate_1yr?: number;
  formal_contract_pct?: number;
  source_id: number;
  is_demo: boolean;
}

export interface EarningsData {
  id: number;
  outcome_id?: number;
  trade_id: number;
  location_id?: number;
  median_starting_monthly_inr: number;
  mid_career_monthly_inr?: number;
  p10_inr?: number;
  p90_inr?: number;
  stipend_during_training_inr: number;
  source_id: number;
  is_demo: boolean;
}

export interface OutcomeData {
  id: number;
  trade_id: number;
  provider_id?: number;
  location_id?: number;
  placement_rate: number;
  earnings_min: number;
  earnings_max: number;
  earnings_period: string;
  employment_type: string;
  data_year: number;
  sample_size?: number;
  source_id: number;
  verification_status: string;
  last_verified_at: string;
  last_synced_at: string;
  is_demo: boolean;
  trade?: Trade;
  provider?: TrainingProvider;
  location?: LocationInfo;
  source?: EvidenceSource;
  employment_records?: EmploymentData[];
  earnings_records?: EarningsData[];
}

export interface DataSyncRun {
  id: number;
  source_id: number;
  start_time: string;
  end_time?: string;
  records_found: number;
  records_inserted: number;
  records_updated: number;
  records_rejected: number;
  status: string;
  error_log?: string;
  triggered_by: string;
  source?: EvidenceSource;
}

export interface DataQualityCheck {
  id: number;
  source_id?: number;
  sync_run_id?: number;
  entity_type: string;
  record_identifier?: string;
  issue_type: string;
  details: string;
  status: string;
  created_at: string;
}

export interface AdminMonitoringSummary {
  total_sources: number;
  total_trades: number;
  total_providers: number;
  total_outcomes: number;
  total_sync_runs: number;
  total_quality_checks: number;
  sources_by_freshness: Record<string, number>;
  sources_by_verification: Record<string, number>;
  recent_sync_runs: DataSyncRun[];
  recent_quality_alerts: DataQualityCheck[];
}

export interface EvidenceCitation {
  title: string;
  source_name: string;
  publisher: string;
  verification_status: string;
  freshness_status: string;
  data_year?: number;
  placement_rate?: number;
  starting_salary_min?: number;
  starting_salary_max?: number;
  mid_career_salary?: number;
  formal_contract_pct?: number;
  retention_rate_1yr?: number;
  education_ladder?: string;
  citation_snippet: string;
  trade_title?: string;
}

export interface CounsellingDialogueResponse {
  session_id: string;
  detected_language: string;
  detected_intent: string;
  detected_concern?: string;
  concern_severity?: string;
  strategy_mode: string;
  empathy_framing?: string;
  response_text: string;
  explanation_points: string[];
  suggested_next_actions: string[];
  suggested_question_chips: string[];
  is_evidence_available: boolean;
  evidence_citations: EvidenceCitation[];
  escalation_recommended: boolean;
  escalation_reason?: string;
  family_alignment_score?: number;
  trade?: Trade;
  timestamp: string;
}

export interface CounsellingMessageItem {
  id?: number;
  speaker: "LEARNER" | "PARENT" | "COUNSELLOR" | "SYSTEM";
  message: string;
  language: string;
  intent?: string;
  concern?: string;
  timestamp: string;
  evidence_refs?: EvidenceCitation[];
  explanation_points?: string[];
  suggested_chips?: string[];
  escalation_recommended?: boolean;
}

export interface CounsellingSessionData {
  session_id: string;
  family_id?: number;
  learner_id?: number;
  parent_id?: number;
  trade_id?: number;
  trade_title?: string;
  message_count: number;
  escalation_flag: boolean;
  escalation_reason?: string;
  created_at: string;
  updated_at: string;
  messages: CounsellingMessageItem[];
}

export interface QuestionStarter {
  text: string;
  intent: string;
  label: string;
}

export interface SuggestedStartersData {
  trade_id?: number;
  trade_title?: string;
  parent_starters: QuestionStarter[];
  learner_starters: QuestionStarter[];
  trade_specific_starters: QuestionStarter[];
}

export interface CounsellorNote {
  id: number;
  case_id: number;
  author_id?: number;
  author_name?: string;
  note_text: string;
  visibility: "COUNSELLOR_PRIVATE" | "FAMILY_SHARED";
  is_action_item: boolean;
  created_at: string;
  updated_at: string;
}

export interface CounsellorCase {
  id: number;
  family_id: number;
  family_code?: string;
  family_name?: string;
  location_label?: string;
  learner_id?: number;
  learner_name?: string;
  trade_id?: number;
  trade_title?: string;
  assigned_counsellor_id?: number;
  assigned_counsellor_name?: string;
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  case_status: "OPEN" | "ASSIGNED" | "IN_PROGRESS" | "RESOLVED" | "FOLLOW_UP_NEEDED";
  escalation_reason: string;
  parent_concerns?: string[];
  ai_summary?: string;
  evidence_shown?: any[];
  unresolved_questions?: string[];
  recommended_resources?: Array<{
    resource_type: string;
    title: string;
    description: string;
    url?: string;
    source_name?: string;
  }>;
  resolution_summary?: string;
  preferred_contact_method: string;
  contact_details?: string;
  scheduled_at?: string;
  resolved_at?: string;
  created_at: string;
  updated_at: string;
  notes_count: number;
  notes?: CounsellorNote[];
}

export interface CounsellorDashboardSummary {
  total_cases: number;
  new_cases: number;
  active_cases: number;
  priority_cases: number;
  resolved_cases: number;
  recent_cases: CounsellorCase[];
}

export interface FamilyDecisionRoomSnapshot {
  family_id: number;
  family_code: string;
  family_name?: string;
  location_label?: string;
  alignment_score: number;
  decision_status: "EXPLORING" | "DISCUSSING" | "COMPARING" | "NEEDS_COUNSELLING" | "INFORMED" | "DECISION_MADE";
  learner_perspective: {
    name: string;
    education_level: string;
    interests: string[];
    academic_strengths: string[];
    work_env: string;
    expected_salary_monthly_inr: number;
    further_education_goal: string;
    is_complete: boolean;
  };
  parent_perspective: {
    name: string;
    relationship: string;
    top_priorities: string[];
    raw_concerns_text: string;
    is_complete: boolean;
  };
  shared_priorities: string[];
  discussion_topics: string[];
  reported_concerns: Array<{
    id: number;
    category: string;
    concern_text: string;
    severity_level: number;
    confidence_score: number;
    is_addressed: boolean;
    created_at: string;
  }>;
  resolved_concerns_count: number;
  open_concerns_count: number;
  selected_trade?: {
    id: number;
    code: string;
    title: string;
    sector: string;
    nsqf_level: number;
    duration_months: number;
    min_qualification: string;
    description?: string;
  };
  saved_trades: Array<{
    id: number;
    title: string;
    sector: string;
    nsqf_level: number;
    duration_months: number;
  }>;
  evidence_citations: EvidenceCitation[];
  active_counsellor_case?: {
    id: number;
    status: string;
    priority: string;
    assigned_counsellor_name?: string;
    escalation_reason: string;
    scheduled_at?: string;
    resolution_summary?: string;
  };
  shared_counsellor_notes: Array<{
    id: number;
    author_name: string;
    note_text: string;
    is_action_item: boolean;
    created_at: string;
  }>;
  learner_agreed: boolean;
  parent_agreed: boolean;
  updated_at: string;
}

export interface AdminOverviewMetrics {
  families_counselled: number;
  active_sessions: number;
  high_concern_cases: number;
  counsellor_escalations: number;
  resolved_sessions: number;
  unresolved_cases: number;
  average_family_alignment: number;
  total_trades_cataloged: number;
  total_providers_mapped: number;
}

export interface ConcernCategoryStat {
  category: string;
  count: number;
  percentage: number;
  avg_severity: number;
  unresolved_count: number;
  top_associated_trades: string[];
  top_districts: string[];
}

export interface FamilyResistanceIndexItem {
  family_id: number;
  family_code: string;
  district?: string;
  state?: string;
  concern_score: number;
  unresolved_concerns: number;
  decision_state: string;
  counsellor_requested: boolean;
  primary_concern?: string;
  resistance_level: "LOW" | "MODERATE" | "HIGH" | "ACUTE";
}

export interface GeographicConcernHotspot {
  state: string;
  district: string;
  total_families: number;
  total_concerns: number;
  avg_resistance_score: number;
  primary_concern_category: string;
  top_explored_trade?: string;
  escalation_rate: number;
}

export interface TradeAnalyticsItem {
  trade_id: number;
  trade_title: string;
  sector: string;
  nsqf_level: number;
  exploration_count: number;
  comparison_count: number;
  top_concern_category?: string;
  escalations_count: number;
  average_alignment: number;
}

export interface CounsellingFunnelStage {
  stage_key: string;
  stage_label: string;
  count: number;
  conversion_pct: number;
  drop_off_pct: number;
}

export interface ProgrammeAnalyticsResponse {
  overview: AdminOverviewMetrics;
  concerns_breakdown: ConcernCategoryStat[];
  resistance_index: FamilyResistanceIndexItem[];
  resistance_methodology: string;
  geographic_hotspots: GeographicConcernHotspot[];
  trade_analytics: TradeAnalyticsItem[];
  counselling_funnel: CounsellingFunnelStage[];
  filter_context: Record<string, any>;
  generated_at: string;
}

export interface UserRead {

  id?: number;
  full_name: string;
  role: "LEARNER" | "PARENT" | "GUARDIAN" | "COUNSELLOR" | "ADMIN" | string;
  phone_number?: string | null;
  email?: string | null;
  preferred_language?: string;
  avatar_url?: string | null;
  family_id?: number | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserRead;
  family_code?: string | null;
  family_id?: number | null;
}

export interface UserRegisterRequest {
  full_name: string;
  email?: string;
  phone_number?: string;
  password: string;
  role: "LEARNER" | "PARENT" | "GUARDIAN" | "COUNSELLOR" | "ADMIN" | string;
  preferred_language?: string;
  family_code?: string;
}

export interface UserLoginRequest {
  email_or_phone: string;
  password: string;
  role?: "LEARNER" | "PARENT" | "GUARDIAN" | "COUNSELLOR" | "ADMIN" | string;
}





