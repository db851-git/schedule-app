from datetime import datetime
from app.models import Task
from flask import current_app

class PlanService:
    @staticmethod
    def can_create_task(user_id: int) -> bool:
        today = datetime.utcnow().date()
        task_count = Task.query.filter_by(user_id=user_id, task_date=today).count()
        limit = current_app.config['FREE_PLAN_TASK_LIMIT']
        return task_count < limit