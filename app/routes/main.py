import uuid
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.task_service import TaskService
from app.services.plan_service import PlanService

main_bp = Blueprint('main', __name__)

@main_bp.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['user_name'] = request.form.get('name', 'User')
        return redirect(url_for('main.dashboard'))
    return render_template('welcome.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_name = session.get('user_name', 'Guest')
    session_id = session['session_id']
    
    can_create = PlanService.can_create_task(session_id)

    if request.method == 'POST' and can_create:
        TaskService.create_task(session_id, request.form)
        return redirect(url_for('main.dashboard'))
    elif request.method == 'POST' and not can_create:
        flash("You've reached your free tier limit for today. Upgrade to Pro!", "warning")

    tasks = TaskService.get_tasks_for_session(session_id)
    
    stats = {
        'total': len(tasks),
        'completed': sum(1 for t in tasks if t.status == 'Completed'),
        'pending': sum(1 for t in tasks if t.status != 'Completed')
    }
    stats['percent'] = int((stats['completed'] / stats['total'] * 100)) if stats['total'] > 0 else 0

    return render_template('dashboard.html', tasks=tasks, user_name=user_name, can_create=can_create, stats=stats)

@main_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    TaskService.toggle_status(task_id, session['session_id'])
    return redirect(url_for('main.dashboard'))
    
@main_bp.route('/analytics')
def analytics():
    return render_template('analytics.html')