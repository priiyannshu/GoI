-- ============================================================================
-- Add hidden items JSON columns to user_profiles table
-- Target Engine: Cloudflare D1 Serverless SQLite
-- File: worker/migrations/0004_hidden_items.sql
-- ============================================================================

ALTER TABLE user_profiles ADD COLUMN hidden_exams_json JSON DEFAULT '[]';
ALTER TABLE user_profiles ADD COLUMN hidden_posts_json JSON DEFAULT '[]';
