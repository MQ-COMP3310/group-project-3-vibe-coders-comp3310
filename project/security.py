#Additional Feature 2 - Activity Log
from flask import request
from datetime import datetime, timedelta
from .models import ActivityLog, db
from sqlalchemy import func

def log_activity(user_id, activity_type, details=None):
    #log user activity into database
    log = ActivityLog(
        user_id=user_id,
        activity_type=activity_type,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        details=details
        #never logs passwords/security answers
    )
    db.session.add(log)
    db.session.commit()

#check for any suspicious activit
def check_login_anomalies(username):
    #Rate Limiting to prevent brute force attack
    threshold = 5
    time_window = timedelta(minutes=5)
    
    recent_failures = ActivityLog.query.filter(
        ActivityLog.activity_type == 'login_failed',
        ActivityLog.details.like(f'%username:{username}%'),
        ActivityLog.created_at > datetime.utcnow() - time_window
    ).count()
    

def get_recent_activities(user_id=None, limit=20):
    #get recent activities for admin to view
    query = ActivityLog.query.order_by(ActivityLog.created_at.desc())
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.limit(limit).all()
