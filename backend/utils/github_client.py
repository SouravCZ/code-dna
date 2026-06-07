import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter
import json

logger = logging.getLogger(__name__)

class GitHubClient:
    """GitHub API Client for fetching user data"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and update rate limit info"""
        self.rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
        self.rate_limit_reset = response.headers.get('X-RateLimit-Reset')
        
        if response.status_code == 404:
            raise ValueError(f"User or resource not found: {response.text}")
        elif response.status_code == 403:
            raise ValueError(f"Rate limit exceeded or access denied: {response.text}")
        elif response.status_code >= 400:
            raise ValueError(f"API Error ({response.status_code}): {response.text}")
        
        return response.json()
    
    def get_user_profile(self, username: str) -> Dict:
        """Fetch user profile data"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(url, headers=self.headers)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            raise
    
    def get_user_repos(self, username: str, max_repos: int = 50) -> List[Dict]:
        """Fetch user's public repositories"""
        try:
            repos = []
            page = 1
            per_page = 100
            
            while len(repos) < max_repos:
                url = f"{self.base_url}/users/{username}/repos"
                params = {
                    "sort": "stars",
                    "direction": "desc",
                    "per_page": per_page,
                    "page": page,
                    "type": "owner"
                }
                response = requests.get(url, headers=self.headers, params=params)
                data = self._handle_response(response)
                
                if not data:
                    break
                
                repos.extend(data)
                page += 1
                
                if len(data) < per_page:
                    break
            
            return repos[:max_repos]
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            raise
    
    def get_repo_commits(self, username: str, repo: str, max_commits: int = 100) -> List[Dict]:
        """Fetch recent commits from a repository"""
        try:
            commits = []
            page = 1
            per_page = 100
            
            while len(commits) < max_commits:
                url = f"{self.base_url}/repos/{username}/{repo}/commits"
                params = {
                    "per_page": per_page,
                    "page": page
                }
                response = requests.get(url, headers=self.headers, params=params)
                data = self._handle_response(response)
                
                if not data:
                    break
                
                commits.extend(data)
                page += 1
                
                if len(data) < per_page:
                    break
            
            return commits[:max_commits]
        except Exception as e:
            logger.error(f"Error fetching commits: {e}")
            return []
    
    def get_repo_readme(self, username: str, repo: str) -> Optional[str]:
        """Fetch README content from a repository"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo}/readme"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 404:
                return None
            
            data = self._handle_response(response)
            
            # The API returns base64 encoded content
            import base64
            if isinstance(data, dict) and 'content' in data:
                return base64.b64decode(data['content']).decode('utf-8')
            
            return None
        except Exception as e:
            logger.error(f"Error fetching README: {e}")
            return None

def extract_developer_profile(username: str, github_token: str) -> Dict:
    """Extract comprehensive developer profile from GitHub"""
    
    client = GitHubClient(github_token)
    
    try:
        # Fetch user profile
        logger.info(f"Fetching profile for {username}")
        user_data = client.get_user_profile(username)
        
        # Fetch repositories
        logger.info(f"Fetching repositories for {username}")
        repos = client.get_user_repos(username)
        
        # Analyze languages and repositories
        languages = Counter()
        readme_count = 0
        total_stars = 0
        commit_messages = []
        repo_descriptions = []
        
        for repo in repos[:20]:  # Analyze top 20 repos
            # Count languages
            if repo.get('language'):
                languages[repo['language']] += 1
            
            # Check for README
            readme_content = client.get_repo_readme(username, repo['name'])
            if readme_content:
                readme_count += 1
            
            # Sum stars
            total_stars += repo.get('stargazers_count', 0)
            
            # Add repo description
            if repo.get('description'):
                repo_descriptions.append(repo['description'])
            
            # Fetch commits
            logger.info(f"Fetching commits for {repo['name']}")
            commits = client.get_repo_commits(username, repo['name'])
            
            for commit in commits[:50]:  # Get commit messages
                if commit.get('commit', {}).get('message'):
                    message = commit['commit']['message'].split('\n')[0]  # First line only
                    commit_messages.append(message)
        
        # Build profile data
        profile = {
            'username': username,
            'name': user_data.get('name'),
            'bio': user_data.get('bio'),
            'location': user_data.get('location'),
            'company': user_data.get('company'),
            'blog': user_data.get('blog'),
            'public_repos': user_data.get('public_repos'),
            'followers': user_data.get('followers'),
            'following': user_data.get('following'),
            'account_created': user_data.get('created_at'),
            'last_updated': user_data.get('updated_at'),
            'avatar_url': user_data.get('avatar_url'),
            'profile_url': user_data.get('html_url'),
            
            # Analytics
            'top_languages': dict(languages.most_common(5)),
            'readme_ratio': readme_count / len(repos) if repos else 0,
            'total_repos': len(repos),
            'total_stars': total_stars,
            'avg_stars_per_repo': total_stars / len(repos) if repos else 0,
            'commit_messages_sample': commit_messages[:100],
            'repo_descriptions': repo_descriptions,
            
            # Metadata
            'rate_limit_remaining': client.rate_limit_remaining,
            'rate_limit_reset': client.rate_limit_reset
        }
        
        logger.info(f"Successfully extracted profile for {username}")
        return profile
    
    except Exception as e:
        logger.error(f"Error extracting developer profile: {e}")
        raise
