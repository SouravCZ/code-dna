import logging
from flask import Blueprint, request, jsonify
from typing import Dict
import os

# Import utilities
from utils.github_client import extract_developer_profile
from utils.ai_client import AIClient
from utils.prompt_templates import get_personality_analysis_prompt
from utils.dna_processor import parse_ai_response, enrich_dna_card, calculate_developer_score
from utils.validators import validate_github_username, format_error_response, sanitize_text

logger = logging.getLogger(__name__)

# Create blueprint
analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

@analyze_bp.route('/analyze', methods=['POST'])
def analyze_developer():
    """
    Main endpoint to analyze a GitHub developer and generate DNA card
    
    Request body:
    {
        "username": "github_username"
    }
    
    Response:
    {
        "success": true,
        "data": {
            "dna_card": {...},
            "profile": {...},
            "scores": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data:
            return format_error_response("Username is required", 400)
        
        username = sanitize_text(data['username']).lower()
        
        if not validate_github_username(username):
            return format_error_response(f"Invalid GitHub username: {username}", 400)
        
        logger.info(f"Starting analysis for {username}")
        
        # Get GitHub token from environment
        github_token = os.getenv('GITHUB_API_TOKEN')
        if not github_token:
            logger.error("GITHUB_API_TOKEN not set")
            return format_error_response("Server configuration error", 500)
        
        # Extract developer profile
        logger.info(f"Extracting profile for {username}")
        profile_data = extract_developer_profile(username, github_token)
        
        # Get AI provider
        ai_provider = os.getenv('AI_PROVIDER', 'openai')
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if ai_provider == 'openai' and not openai_key:
            return format_error_response("OpenAI API key not configured", 500)
        elif ai_provider == 'anthropic' and not anthropic_key:
            return format_error_response("Anthropic API key not configured", 500)
        
        # Initialize AI client
        ai_client = AIClient(
            provider=ai_provider,
            openai_key=openai_key,
            anthropic_key=anthropic_key
        )
        
        # Get analysis prompt
        prompt = get_personality_analysis_prompt()
        
        # Generate analysis
        logger.info(f"Generating AI analysis for {username}")
        ai_response = ai_client.analyze_developer(profile_data, prompt)
        
        # Parse AI response
        dna_card = parse_ai_response(ai_response['analysis'])
        
        # Enrich DNA card with profile data
        enriched_dna_card = enrich_dna_card(dna_card, profile_data)
        
        # Calculate scores
        scores = calculate_developer_score(profile_data)
        
        logger.info(f"Analysis complete for {username}")
        
        return jsonify({
            'success': True,
            'data': {
                'dna_card': enriched_dna_card,
                'profile': {
                    'username': profile_data['username'],
                    'name': profile_data.get('name'),
                    'avatar_url': profile_data.get('avatar_url'),
                    'profile_url': profile_data.get('profile_url'),
                    'bio': profile_data.get('bio'),
                    'location': profile_data.get('location'),
                    'public_repos': profile_data.get('public_repos'),
                    'followers': profile_data.get('followers'),
                    'top_languages': profile_data.get('top_languages'),
                },
                'scores': scores,
                'ai_provider': ai_response['provider'],
                'tokens_used': ai_response.get('tokens_used', 0)
            }
        }), 200
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return format_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error analyzing developer: {e}")
        return format_error_response(f"Error analyzing developer: {str(e)}", 500)

@analyze_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Code DNA API'
    }), 200

@analyze_bp.route('/config', methods=['GET'])
def get_config():
    """Get API configuration"""
    return jsonify({
        'ai_provider': os.getenv('AI_PROVIDER', 'openai'),
        'max_repos': int(os.getenv('MAX_REPOS_TO_ANALYZE', 50)),
        'max_commits': int(os.getenv('MAX_COMMITS_PER_REPO', 100)),
        'frontend_url': os.getenv('FRONTEND_URL', 'http://localhost:3000')
    }), 200
