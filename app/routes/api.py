from flask import Blueprint, jsonify, session, Response
from app.services.task_service import TaskService
import csv
from io import StringIO

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks/export')
def export_tasks():
    tasks = TaskService.get_tasks_for_session(session.get('session_id'))
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Title', 'Category', 'Date', 'Start Time', 'End Time', 'Status', 'Priority'])
    for task in tasks:
        cw.writerow([task.title, task.category, task.task_date, task.start_time, task.end_time, task.status, task.priority])
    
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=schedule_export.csv"}
    )
    
@api_bp.route('/analytics/data')
def analytics_data():
    tasks = TaskService.get_tasks_for_session(session.get('session_id'))
    categories = {}
    for task in tasks:
        categories[task.category] = categories.get(task.category, 0) + 1
    return jsonify(categories)