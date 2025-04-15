import streamlit as st
import requests
import json
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="VidScript AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    /* Main App Styling */
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #ffffff;
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* Script output styling */
    .script-output {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin: 1.5rem 0;
        font-size: 1rem;
        line-height: 1.6;
        color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
    
    /* Tips section styling */
    .tips-section {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        color: #ffffff;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom header styling */
    .css-1d391kg h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle styling */
    .css-1d391kg p {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
    }
    
    /* Section headers */
    h3 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Remove extra padding */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #3b82f6;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 10px;
        margin-top: 3rem;
    }

    /* Error and Warning Styling */
    .stAlert {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .stAlert[data-baseweb="notification"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
    }

    .stAlert[data-baseweb="notification"] > div {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    }

    /* Error message styling */
    .stAlert[data-baseweb="notification"] > div > div {
        color: #f87171;
    }

    /* Warning message styling */
    .stAlert[data-baseweb="notification"] > div > div[data-testid="stMarkdownContainer"] {
        color: #fbbf24;
    }

    /* Success message styling */
    .stAlert[data-baseweb="notification"] > div > div[data-testid="stMarkdownContainer"] {
        color: #34d399;
    }
    </style>
""", unsafe_allow_html=True)

# Main title and subtitle with custom HTML for modern header
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #ffffff; font-size: 3.0rem; font-weight: 700; margin-bottom: 0.5rem;'>🎥 VidScript AI</h1>
        <p style='color: #94a3b8; font-size: 1.2rem;'>   Transform your ideas into engaging content with AI</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for customization toggle
if 'show_customize' not in st.session_state:
    st.session_state.show_customize = False

# Create Your Content section with customization button
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        
            <h3 style='color: #ffffff; margin: 0;'>✨ Create Your Content</h3>
        
    """, unsafe_allow_html=True)
with col2:
    if st.button("⚙️ Customize", use_container_width=True):
        st.session_state.show_customize = not st.session_state.show_customize

# Customization options section
if st.session_state.show_customize:
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            # Tone Selection
            tone = st.selectbox(
                "🎭 Tone",
                ["Professional", "Casual", "Humorous", "Inspirational", "Educational", "Conversational", "Technical"],
                help="Choose the tone for your content"
            )
            
            # Niche Selection
            niche = st.selectbox(
                "🎯 Niche",
                ["Technology", "Business", "Education", "Entertainment", "Health & Wellness", "Lifestyle", "Gaming", "Sports", "Science", "Finance"],
                help="Select your content niche"
            )
            
            # Video Length Selection
            video_length = st.slider(
                "⏱️ Video Length (minutes)",
                min_value=1,
                max_value=30,
                value=5,
                help="Select the desired length of your video"
            )
        
        with col2:
            # Target Audience
            audience = st.selectbox(
                "👥 Target Audience",
                ["General Audience", "Beginners", "Experts", "Professionals", "Students", "Kids", "Entrepreneurs", "Creators"],
                help="Choose your target audience"
            )
            
            # Content Type
            content_type = st.selectbox(
                "📝 Content Type",
                ["YouTube Video", "Blog Post", "Social Media Post", "Podcast Script", "News Article", "Product Description"],
                help="Select the type of content you want to create"
            )
            
            # Language Selection
            language = st.selectbox(
                "🌐 Language",
                ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Japanese", "Korean", "Chinese", "Hindi", "Arabic"],
                help="Select the language for your content"
            )
else:
    # Set default values when customization is hidden
    tone = "Professional"
    niche = "Technology"
    audience = "General Audience"
    content_type = "YouTube Video"
    video_length = 5
    language = "English"

# Input field
topic = st.text_input("Enter your topic:", placeholder="e.g., The Future of Artificial Intelligence", key="topic_input")

# Generate button
if st.button("✨ Generate Content", key="generate_script"):
    if topic:
        with st.spinner("✨ Generating your content..."):
            try:
                # Make API request to Flask backend with customization options
                response = requests.post(
                    'http://localhost:5000/generate-script',
                    json={
                        'topic': topic,
                        'settings': {
                            'tone': tone,
                            'niche': niche,
                            'target_audience': audience,
                            'content_type': content_type,
                            'video_length': video_length,
                            'language': language
                        }
                    }
                )
                
                if response.status_code == 200:
                    script = response.json()['script']
                    
                    # Display the script in a nice format
                    st.markdown("### 📝 Your Generated Content")
                    st.markdown(f"""
                        <div class='script-output'>
                            {script}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a download button
                    st.download_button(
                        label="📥 Download Content",
                        data=script,
                        file_name=f"content_{topic[:30]}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Error: {response.json().get('error', 'Failed to generate content')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic first!")

# Tips section with custom styling
with st.expander("💡 Tips for Better Content", expanded=False):
    st.markdown("""
        <div class='tips-section'>
            <h4>How to get the best results:</h4>
            <ul>
                <li>Be specific with your topic</li>
                <li>Include key points you want to cover</li>
                <li>Mention your target audience</li>
                <li>Specify the content length if needed</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style='color: #94a3b8; font-size: 1.1rem;'>Powered by Azure OpenAI GPT-4.5 | Created with ❤️</p>
    <p style='color: #64748b; font-size: 0.9rem;'>© 2024 VidScript AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True) 