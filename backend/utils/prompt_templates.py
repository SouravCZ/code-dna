def get_personality_analysis_prompt() -> str:
    """Get the main prompt for personality analysis"""
    return """
You are a creative developer personality analyzer. Based on the GitHub profile data provided, 
generate a fun and insightful "Developer DNA Card" in JSON format.

Your response must be a valid JSON object with the following structure:
{
  "personality_type": "A catchy archetype name (e.g., 'The Chaotic Architect', 'The Silent Perfectionist')",
  "archetype": "Developer archetype category (Creator, Architect, Maintainer, Experimenter, Minimalist, Collaborator)",
  "headline": "A 1-2 sentence summary of their developer personality",
  "top_languages_analysis": {
    "primary": "Main language with personality insight",
    "insight": "What their language choices say about them"
  },
  "commit_style_analysis": {
    "style_name": "Their commit message style (e.g., 'Poetic', 'Technical', 'Concise', 'Verbose')",
    "rating": "Rating 1-10",
    "description": "Brief description of their commit style"
  },
  "readme_quality": {
    "score": "0-10",
    "description": "Assessment of their documentation habits"
  },
  "strengths": [
    "First developer strength based on their profile",
    "Second developer strength based on their profile"
  ],
  "brutal_truths": [
    "First insight about their development patterns",
    "Second insight about their development patterns"
  ],
  "quirks": [
    "Interesting finding about their coding style"
  ],
  "dev_dna_sequence": "A playful DNA-like sequence representing their profile (e.g., 'PYTHON-STAR-COMMIT-FORK-COLLAB')",
  "energy_level": "High/Medium/Low (based on activity)",
  "collaboration_score": "0-10",
  "perfectionism_score": "0-10",
  "fun_fact": "One fun observation about their coding behavior"
}

Make it fun, insightful, and based on the data provided. Be creative but accurate to the profile.
"""

def get_languages_insight_prompt(languages: dict) -> str:
    """Get prompt for language-based insights"""
    return f"""
Based on these languages used by the developer: {languages}

Provide insights about what these language choices reveal about:
1. Their problem-solving approach
2. Their career focus
3. Their personality traits

Keep it concise and fun.
"""

def get_commit_message_analysis_prompt(messages: list) -> str:
    """Get prompt for commit message analysis"""
    sample_messages = messages[:20] if messages else []
    return f"""
Analyze these commit messages from the developer and describe their style:
{sample_messages}

Describe their commit message style in terms of:
1. Clarity and detail level
2. Personality (formal, casual, creative, etc.)
3. Consistency
4. How it reflects their development approach

Keep it fun and insightful, 2-3 sentences max.
"""

def get_repo_description_analysis_prompt(descriptions: list) -> str:
    """Get prompt for repository description analysis"""
    return f"""
Based on these repository descriptions: {descriptions}

What do they tell us about:
1. The developer's interests
2. Their project priorities
3. Their communication style

Be brief and fun.
"""

def get_developer_archetype_prompt(profile_data: dict) -> str:
    """Get prompt for determining developer archetype"""
    return f"""
Based on this developer's profile:
- Public repos: {profile_data.get('public_repos', 0)}
- Followers: {profile_data.get('followers', 0)}
- Top languages: {profile_data.get('top_languages', {})}
- README ratio: {profile_data.get('readme_ratio', 0):.2%}
- Average stars per repo: {profile_data.get('avg_stars_per_repo', 0):.1f}

Determine their developer archetype and explain why.

Archetypes:
- Creator: Building original projects with high stars
- Architect: Well-documented, planned systems
- Maintainer: Focus on reliability and community contributions
- Experimenter: Diverse language mix, exploratory projects
- Minimalist: Focused on quality over quantity
- Collaborator: High followers, community engagement
"""

# All templates as a dictionary
PROMPT_TEMPLATES = {
    "personality_analysis": get_personality_analysis_prompt(),
    "languages_insight": get_languages_insight_prompt,
    "commit_message_analysis": get_commit_message_analysis_prompt,
    "repo_description_analysis": get_repo_description_analysis_prompt,
    "developer_archetype": get_developer_archetype_prompt
}
