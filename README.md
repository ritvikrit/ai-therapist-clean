# AI Voice Therapist

An AI-powered voice therapy application built with FastAPI and OpenAI's API.

## Features

- Voice input via web interface
- AI-powered responses using OpenAI's models
- Real-time audio processing
- Supportive and empathetic responses

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: HTML, JavaScript
- **API**: OpenAI GPT

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd voiceagent_manual
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

6. Open your browser and navigate to `http://localhost:8000`

## Usage

- Click "Start Recording" to record your voice
- The AI will process your input and provide a supportive response
- Audio will be played automatically

## License

MIT
