from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.task_service import TaskService
from app.services.plan_service import PlanService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # If they are already logged in, send them straight to the dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('welcome.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Security check: If not logged in, kick them to the login page
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_name = session.get('user_name', 'User')
    
    can_create = PlanService.can_create_task(user_id)

    if request.method == 'POST' and can_create:
        TaskService.create_task(user_id, request.form)
        return redirect(url_for('main.dashboard'))
    elif request.method == 'POST' and not can_create:
        flash("You've reached your free tier limit for today. Upgrade to Pro!", "warning")

    tasks = TaskService.get_tasks_for_session(user_id)
    
    stats = {
        'total': len(tasks),
        'completed': sum(1 for t in tasks if t.status == 'Completed'),
        'pending': sum(1 for t in tasks if t.status != 'Completed')
    }
    stats['percent'] = int((stats['completed'] / stats['total'] * 100)) if stats['total'] > 0 else 0

    return render_template('dashboard.html', tasks=tasks, user_name=user_name, can_create=can_create, stats=stats)

@main_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    if 'user_id' in session:
        TaskService.toggle_status(task_id, session['user_id'])
    return redirect(url_for('main.dashboard'))
    
@main_bp.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('analytics.html')