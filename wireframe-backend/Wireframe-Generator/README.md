
# Wireframe Generator API

A FastAPI backend for generating wireframes from natural language descriptions using LLMs and LangGraph.

## Features

- Generate wireframes from natural language descriptions
- Multi-agent system with specialized agents for different tasks:
  - Requirements gathering agent
  - Wireframe planning agent
  - SVG generation agent
- FastAPI backend with proper documentation
- Docker support for easy deployment

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)

### Environment Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file with your API keys

### Running Locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the API documentation

### Running with Docker

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the API documentation

## API Usage

### Generate a Wireframe

**Endpoint**: `POST /api/v1/wireframe/generate`

**Request Body**:
```json
{
  "user_query": "Design a low-fidelity, responsive desktop + mobile checkout experience for a fashion e-commerce site."
}
```

**Response**:
```json
{
  "svg_code": "...",
  "detailed_requirements": {...},
  "wireframe_plan": {...},
  "errors": null
}
```

## Development

### Project Structure

- `app/`: Main application package
  - `api/`: API routes and endpoints
  - `models/`: Pydantic models
  - `services/`: Business logic services
  - `core/`: Core application components
  - `utils/`: Utility functions
- `tests/`: Test cases

### Running Tests

```bash
pytest
```

## License

MIT
