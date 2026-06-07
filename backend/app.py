import os
import logging
from flask import Flask
from flask_cors import CORS
from config import get_config
from routes.analyze import analyze_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(get_config())
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('FRONTEND_URL', 'http://localhost:3000'),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(analyze_bp)
    
    logger.info("Flask app created successfully")
    
    return app

# Create app instance
app = create_app()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {
        'error': 'Not found',
        'status': 404
    }, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return {
        'error': 'Internal server error',
        'status': 500
    }, 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Code DNA API on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
