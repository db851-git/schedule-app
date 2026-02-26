import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.services.task_service import TaskService
from app.services.plan_service import PlanService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('welcome.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_name = session.get('user_name', 'User')
    
    can_create = PlanService.can_create_task(user_id)

    if request.method == 'POST' and can_create:
        TaskService.create_task(user_id, request.form)
        return redirect(url_for('main.dashboard'))
    elif request.method == 'POST' and not can_create:
        flash("You've reached your free tier limit for today.", "warning")

    tasks = TaskService.get_tasks_for_session(user_id)
    
    today = datetime.utcnow().date()
    todays_tasks = [t for t in tasks if t.task_date == today]
    
    stats = {
        'total': len(todays_tasks),
        'completed': sum(1 for t in todays_tasks if t.status == 'Completed'),
        'pending': sum(1 for t in todays_tasks if t.status != 'Completed')
    }
    stats['percent'] = int((stats['completed'] / stats['total'] * 100)) if stats['total'] > 0 else 0

    return render_template('dashboard.html', tasks=tasks, user_name=user_name, can_create=can_create, stats=stats)

# --- NEW OPTIMIZED TOGGLE ROUTE ---
@main_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    task = TaskService.toggle_status(task_id, user_id)
    
    # Recalculate today's stats to send back to the frontend instantly
    tasks = TaskService.get_tasks_for_session(user_id)
    today = datetime.utcnow().date()
    todays_tasks = [t for t in tasks if t.task_date == today]
    
    total = len(todays_tasks)
    completed = sum(1 for t in todays_tasks if t.status == 'Completed')
    pending = total - completed
    percent = int((completed / total * 100)) if total > 0 else 0

    # Return raw data instead of refreshing the page
    return jsonify({
        'success': True,
        'new_status': task.status,
        'stats': {
            'percent': percent,
            'pending': pending
        }
    })