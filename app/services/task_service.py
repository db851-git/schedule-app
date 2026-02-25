from datetime import datetime
from app.models import Task
from app import db

class TaskService:
    @staticmethod
    def get_tasks_for_session(user_id: int, date_filter=None):
        query = Task.query.filter_by(user_id=user_id)
        if date_filter:
            query = query.filter_by(task_date=date_filter)
        return query.order_by(Task.task_date, Task.start_time).all()

    @staticmethod
    def create_task(user_id, data):
        new_task = Task(
            user_id=user_id,
            title=data['title'],
            category=data['category'],
            task_date=datetime.strptime(data['task_date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium')
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def toggle_status(task_id, user_id):
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        task.status = 'Completed' if task.status != 'Completed' else 'Pending'
        db.session.commit()
        return task