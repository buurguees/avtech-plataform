"""Add database indexes

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add indexes for better performance
    
    # Clients table indexes
    op.create_index('idx_clients_email', 'clients', ['contact_email'])
    op.create_index('idx_clients_api_key', 'clients', ['api_key'])
    op.create_index('idx_clients_active', 'clients', ['is_active'])
    
    # Users table indexes
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_client_id', 'users', ['client_id'])
    op.create_index('idx_users_active', 'users', ['is_active'])
    
    # Videos table indexes
    op.create_index('idx_videos_client_id', 'videos', ['client_id'])
    op.create_index('idx_videos_status', 'videos', ['status'])
    op.create_index('idx_videos_created_at', 'videos', ['created_at'])
    op.create_index('idx_videos_hash', 'videos', ['hash_sha256'])
    
    # Screens table indexes
    op.create_index('idx_screens_client_id', 'screens', ['client_id'])
    op.create_index('idx_screens_status', 'screens', ['status'])
    op.create_index('idx_screens_code', 'screens', ['screen_code'])
    op.create_index('idx_screens_heartbeat', 'screens', ['last_heartbeat'])
    
    # Schedule rules table indexes
    op.create_index('idx_schedule_rules_client_id', 'schedule_rules', ['client_id'])
    op.create_index('idx_schedule_rules_type', 'schedule_rules', ['rule_type'])
    op.create_index('idx_schedule_rules_active_from', 'schedule_rules', ['active_from'])
    op.create_index('idx_schedule_rules_active_until', 'schedule_rules', ['active_until'])
    
    # Time slots table indexes
    op.create_index('idx_time_slots_video_id', 'time_slots', ['video_id'])
    op.create_index('idx_time_slots_screen_id', 'time_slots', ['screen_id'])
    op.create_index('idx_time_slots_schedule_rule_id', 'time_slots', ['schedule_rule_id'])
    op.create_index('idx_time_slots_day_of_week', 'time_slots', ['day_of_week'])
    op.create_index('idx_time_slots_start_time', 'time_slots', ['start_time'])
    
    # Player sync status table indexes
    op.create_index('idx_player_sync_screen_code', 'player_sync_status', ['screen_code'])
    op.create_index('idx_player_sync_status', 'player_sync_status', ['sync_status'])
    op.create_index('idx_player_sync_heartbeat', 'player_sync_status', ['last_heartbeat'])
    
    # Audit logs table indexes
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_table_name', 'audit_logs', ['table_name'])
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'])


def downgrade() -> None:
    # Drop indexes in reverse order
    
    # Audit logs indexes
    op.drop_index('idx_audit_logs_created_at', 'audit_logs')
    op.drop_index('idx_audit_logs_table_name', 'audit_logs')
    op.drop_index('idx_audit_logs_action', 'audit_logs')
    op.drop_index('idx_audit_logs_user_id', 'audit_logs')
    
    # Player sync status indexes
    op.drop_index('idx_player_sync_heartbeat', 'player_sync_status')
    op.drop_index('idx_player_sync_status', 'player_sync_status')
    op.drop_index('idx_player_sync_screen_code', 'player_sync_status')
    
    # Time slots indexes
    op.drop_index('idx_time_slots_start_time', 'time_slots')
    op.drop_index('idx_time_slots_day_of_week', 'time_slots')
    op.drop_index('idx_time_slots_schedule_rule_id', 'time_slots')
    op.drop_index('idx_time_slots_screen_id', 'time_slots')
    op.drop_index('idx_time_slots_video_id', 'time_slots')
    
    # Schedule rules indexes
    op.drop_index('idx_schedule_rules_active_until', 'schedule_rules')
    op.drop_index('idx_schedule_rules_active_from', 'schedule_rules')
    op.drop_index('idx_schedule_rules_type', 'schedule_rules')
    op.drop_index('idx_schedule_rules_client_id', 'schedule_rules')
    
    # Screens indexes
    op.drop_index('idx_screens_heartbeat', 'screens')
    op.drop_index('idx_screens_code', 'screens')
    op.drop_index('idx_screens_status', 'screens')
    op.drop_index('idx_screens_client_id', 'screens')
    
    # Videos indexes
    op.drop_index('idx_videos_hash', 'videos')
    op.drop_index('idx_videos_created_at', 'videos')
    op.drop_index('idx_videos_status', 'videos')
    op.drop_index('idx_videos_client_id', 'videos')
    
    # Users indexes
    op.drop_index('idx_users_active', 'users')
    op.drop_index('idx_users_client_id', 'users')
    op.drop_index('idx_users_email', 'users')
    op.drop_index('idx_users_username', 'users')
    
    # Clients indexes
    op.drop_index('idx_clients_active', 'clients')
    op.drop_index('idx_clients_api_key', 'clients')
    op.drop_index('idx_clients_email', 'clients')
