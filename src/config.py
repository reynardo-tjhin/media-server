import os
import configparser

from pathlib import Path
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# initialise the configuration for the app
cfg = configparser.ConfigParser()
cfg_path = Path(__file__).parent.parent / 'config.ini'
cfg.read(cfg_path)

class Config:
    """Base configuration"""
    # os.getenv() takes in the key
    # if key does not exist, the second parameter will be returned
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev') # for session
    DEBUG = os.getenv('DEBUG', True)
    TESTING = os.getenv('TESTING', True)
    
    # media base path
    MEDIA_BASE_PATH = os.getenv('MEDIA_BASE_PATH')
    MOVIES_PATH = os.path.join(MEDIA_BASE_PATH, cfg['media']['movies_location'])
    POSTERS_PATH = os.path.join(MEDIA_BASE_PATH, cfg['media']['posters_location'])
    BANNERS_PATH = os.path.join(MEDIA_BASE_PATH, cfg['media']['banners_location'])
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    FLASK_ENV = 'production'
    
# configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}