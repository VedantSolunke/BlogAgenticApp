# BlogAgenticApp

BlogAgenticApp is a small LangGraph-powered blog generation service. It uses a Groq-hosted language model to create a blog title and article from a topic, and can translate the generated article into Hindi or Spanish.

## Features

- Generate a Markdown blog title and article from a topic.
- Translate generated blog content into Hindi or Spanish.
- Expose the workflow through a FastAPI endpoint.
- Run the graph in LangGraph Studio through the included `langgraph.json` configuration.

## Requirements

- Python 3.14 or newer
- A Groq API key
- `uv` or `pip` for installing dependencies

## Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd BlogAgenticApp
```

Create and activate a virtual environment:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies with either method:

```bash
# uv
uv sync

# or pip
pip install -e .
```

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your-groq-api-key
```

To enable LangSmith tracing, also add your LangChain API key:

```dotenv
LANGCHAIN_API_KEY=your-langchain-api-key
```

Do not commit `.env` or expose either key in client-side code.

## Run The API

Start the development server:

```bash
python app.py
```

The API is available at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

### Create A Blog

Send a topic to generate a blog in the default language:

```bash
curl -X POST http://localhost:8000/blogs \
	-H "Content-Type: application/json" \
	-d '{"topic":"The future of renewable energy"}'
```

To translate the generated blog, include `language` with the value `hindi` or `spanish`:

```bash
curl -X POST http://localhost:8000/blogs \
	-H "Content-Type: application/json" \
	-d '{"topic":"The future of renewable energy","language":"spanish"}'
```

The response contains the final graph state. The generated post is available under `data.blog`:

```json
{
	"data": {
		"topic": "The future of renewable energy",
		"blog": {
			"title": "...",
			"content": "..."
		},
		"current_language": "spanish"
	}
}
```

## Run With LangGraph Studio

With the virtual environment active and the dependencies installed, run:

```bash
langgraph dev
```

The graph is configured as `blog_generator_agent` in `langgraph.json`. The Studio input should include a `topic`; for translation, include `current_language` with `hindi` or `spanish`.

## Project Structure

```text
.
├── app.py                         # FastAPI application
├── langgraph.json                 # LangGraph Studio configuration
└── src/
		├── graphs/graph_builder.py   # Topic and translation graph definitions
		├── llms/groqllm.py            # Groq Chat model configuration
		├── nodes/blog_node.py         # Blog generation and translation nodes
		└── states/blogstate.py        # Blog state and validation models
```

## Workflow

The topic workflow runs these nodes in order:

```text
START -> title_creation -> content_creation -> END
```

The language workflow adds a routing step and a language-specific translation node:

```text
START -> title_creation -> content_creation -> route
																			├── hindi_translation -> END
																			└── spanish_translation -> END
```

## Development

Run a syntax check for the source tree:

```bash
python -m compileall app.py src
```

The application currently does not include an automated test suite. Because generation uses a remote Groq model, integration checks require a valid `GROQ_API_KEY`.
