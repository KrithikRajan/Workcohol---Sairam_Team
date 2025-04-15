from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from typing import List
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Azure OpenAI configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4-5-preview")
API_VERSION = "2024-12-01-preview"

# Debug logging for Azure OpenAI configuration
print("Azure OpenAI Configuration:")
print(f"API Key: {'*' * len(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else 'Not set'}")
print(f"Endpoint: {AZURE_OPENAI_ENDPOINT}")
print(f"Deployment: {AZURE_OPENAI_DEPLOYMENT}")
print(f"API Version: {API_VERSION}")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    default_headers={"api-key": AZURE_OPENAI_API_KEY}
)

# Define the output structure
class ScriptSection(BaseModel):
    title: str = Field(description="The title of the section")
    content: str = Field(description="The content of the section")
    duration: str = Field(description="The approximate duration of this section")
    word_count: int = Field(description="Approximate number of words in this section")

class YouTubeScript(BaseModel):
    introduction: ScriptSection = Field(description="The introduction section")
    main_sections: List[ScriptSection] = Field(description="The main content sections")
    conclusion: ScriptSection = Field(description="The conclusion section")
    total_duration: str = Field(description="The total duration of the script")
    total_word_count: int = Field(description="The total word count of the script")

def generate_youtube_script(topic, settings):
    try:
        # Calculate time allocations
        video_length = settings.get('video_length', 5)
        intro_time = round(video_length * 0.15, 1)
        main_time = round(video_length * 0.7, 1)
        conclusion_time = round(video_length * 0.15, 1)
        
        # Get language from settings or default to English
        language = settings.get('language', 'English')
        
        # Create the system message
        system_message = f"""You are a professional content creator specializing in {settings.get('content_type', 'YouTube Video')} writing.
Your expertise lies in creating engaging content for the {settings.get('niche', 'Technology')} niche, targeting {settings.get('target_audience', 'General Audience')}.
Maintain a {settings.get('tone', 'Professional')} tone throughout the content.
Write in {language} language.
The content should be structured to fit within {video_length} minutes, considering:
- Average speaking rate of 150 words per minute
- Time for transitions and visual elements
- Appropriate pacing for the target audience
- Cultural context and language-specific nuances for {language}

Generate the content in JSON format with the following structure:
{{
    "introduction": {{
        "title": "Introduction",
        "content": "Introduction content here",
        "duration": "0:00-{intro_time}:00",
        "word_count": 150
    }},
    "main_sections": [
        {{
            "title": "Section 1",
            "content": "Section 1 content here",
            "duration": "{intro_time}:00-{intro_time + main_time/2}:00",
            "word_count": 150
        }},
        {{
            "title": "Section 2",
            "content": "Section 2 content here",
            "duration": "{intro_time + main_time/2}:00-{intro_time + main_time}:00",
            "word_count": 150
        }}
    ],
    "conclusion": {{
        "title": "Conclusion",
        "content": "Conclusion content here",
        "duration": "{intro_time + main_time}:00-{video_length}:00",
        "word_count": 150
    }},
    "total_duration": "{video_length}:00",
    "total_word_count": 450
}}"""

        # Create the user message
        user_message = f"""Create a detailed {settings.get('content_type', 'YouTube Video')} about {topic}.
Make sure to include:
1. An engaging introduction (approximately {intro_time} minutes)
2. 3-4 main content sections (approximately {main_time} minutes total)
3. Clear transitions between sections
4. A strong conclusion with a call to action (approximately {conclusion_time} minutes)

Format the content in a natural, spoken style that resonates with {settings.get('target_audience', 'General Audience')}.
Include approximate timestamps for each section to help with pacing.
Use appropriate cultural references and language-specific expressions for {language}."""

        # Generate the script using Azure OpenAI
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model=AZURE_OPENAI_DEPLOYMENT,
            temperature=0.7,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Parse the response
        script_data = YouTubeScript.parse_raw(response.choices[0].message.content)
        
        # Format the script for display
        script = f"""# {topic}

## Introduction [{script_data.introduction.duration}]
{script_data.introduction.content}

## Main Content"""
        
        for section in script_data.main_sections:
            script += f"""

### {section.title} [{section.duration}]
{section.content}"""
        
        script += f"""

## Conclusion [{script_data.conclusion.duration}]
{script_data.conclusion.content}

---
Total Duration: {script_data.total_duration}
Total Word Count: {script_data.total_word_count} words"""
        
        return script
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/generate-script', methods=['POST'])
def generate_script():
    try:
        data = request.get_json()
        topic = data.get('topic')
        settings = data.get('settings', {})
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
            
        # Generate the script
        script = generate_youtube_script(topic, settings)
        
        if script.startswith("❌ Error:"):
            return jsonify({'error': script}), 500
            
        return jsonify({'script': script})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 