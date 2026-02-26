import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///schedule.db'
    FREE_PLAN_TASK_LIMIT = 5
    
    # NEW: Database connection pooling to prevent 500 Errors after server sleep
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Checks if the connection is alive before using it
        "pool_recycle": 300,    # Recycles connections older than 5 minutes (300 seconds)
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)