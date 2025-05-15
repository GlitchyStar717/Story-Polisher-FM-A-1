# StoryPolisher

A FastAPI application that helps improve stories by generating insightful questions about potential plot holes and areas for improvement.

## Features

- Submit stories for analysis
- Get AI-generated questions to improve your writing
- Simple web interface

## Local Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/storypolisher.git
   cd storypolisher
   ```

2. Create a `.env` file with your Gemini API key:
   ```
   API_KEY=your_gemini_api_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Navigate to http://localhost:8000 in your browser.

## Docker Setup

### Running with Docker Compose

1. Build and start the container:
   ```bash
   docker-compose up
   ```

2. Run tests:
   ```bash
   docker-compose run test
   ```

### Running with Docker CLI

1. Build the Docker image:
   ```bash
   docker build -t storypolisher .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env storypolisher
   ```

## Testing

Run tests using pytest:
```bash
pytest -v
```

## License

[MIT](LICENSE)
