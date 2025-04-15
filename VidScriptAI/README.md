# YouTube Script Generator

A Streamlit application that generates YouTube video scripts using Azure OpenAI GPT-4.5.

## Features

- Generate engaging YouTube video scripts from any topic
- Clean and intuitive user interface
- Download generated scripts as text files
- Tips for creating better scripts

## Setup

1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Azure OpenAI credentials:
     ```
     AZURE_OPENAI_API_KEY=your_api_key_here
     AZURE_OPENAI_ENDPOINT=your_endpoint_here
     AZURE_OPENAI_DEPLOYMENT=your_deployment_name_here
     ```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys and credentials secure
- The `.env` file is already in `.gitignore`
- If you accidentally commit sensitive information, immediately rotate your credentials

## Running the Application

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Open your browser and go to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Enter your video topic in the text input field
2. Click "Generate Script"
3. Wait for the AI to generate your script
4. View the generated script and download it if needed

## Requirements

- Python 3.7+
- Streamlit
- Azure OpenAI
- python-dotenv
