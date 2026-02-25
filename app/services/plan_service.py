from datetime import datetime
from app.models import Task
from flask import current_app

class PlanService:
    @staticmethod
    def can_create_task(session_id: str) -> bool:
        today = datetime.utcnow().date()
        task_count = Task.query.filter_by(session_id=session_id, task_date=today).count()
        limit = current_app.config['FREE_PLAN_TASK_LIMIT']
        return task_count < limit