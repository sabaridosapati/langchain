# LangChain Learning Playground

Hands-on LangChain examples covering models, prompt templates, structured outputs, output parsers, chains, RAG basics, and agents.

This repository is organized as runnable Python scripts (plus a few notebooks) under `langchainenv/`.

## What This Project Contains

- `01_Models/`: LLM, chat model, and embedding examples (OpenAI, Gemini, Anthropic, Hugging Face)
- `02_Prompts/`: prompt template and chat prompt template examples
- `03_StructuredOutput/`: TypedDict, Pydantic, and JSON structured outputs
- `04_OutputParsers/`: `StrOutputParser`, JSON parser, structured parser, Pydantic parser
- `05_Chains/`: simple, sequential, parallel, and conditional chain patterns
- `06_RAG/`: document loaders, text splitters, retriever/vector DB notebooks
- `Tools/`: tool calling patterns
- `08_Agents.py`: agent example with web search and local tools
- `gemini_llm_server_tools.py`: FastAPI app demonstrating Gemini + function tools

## Prerequisites

- Python 3.11+
- Windows PowerShell (commands below assume Windows; adapt for macOS/Linux if needed)
- API keys depending on which scripts you run

## Setup

1. Clone and enter the repo:
```powershell
git clone <your-repo-url>
cd c:\langchain
```
2. Create and activate a virtual environment (recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3. Install dependencies:
```powershell
pip install -r .\langchainenv\01_Models\requirements.txt
pip install streamlit fastapi uvicorn pypdf beautifulsoup4 duckduckgo-search grandalf
```

## Environment Variables

Create a `.env` file (for example at repo root) with keys for the providers you use:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

Notes:
- Most scripts call `load_dotenv()`, so they will load from a nearby/root `.env`.
- You only need keys for the scripts you plan to run.

## Run Examples

From `\langchain`, run any script directly:

```powershell
python .\langchainenv\01_Models\LLMs\llm_demo.py
python .\langchainenv\01_Models\ChatModels\chatmodel_google.py
python .\langchainenv\02_Prompts\PromptTemplate\prompt_template.py
python .\langchainenv\05_Chains\simple_chain.py
python .\langchainenv\04_OutputParsers\01_StrOutputParser_HF_endpnt_chain.py
python .\langchainenv\08_Agents.py
```

Run the Streamlit UI:

```powershell
streamlit run .\langchainenv\02_Prompts\PromptTemplate\streamlit_PromptTemplate_ui.py
```

Run the FastAPI tool-calling server:

```powershell
python .\langchainenv\gemini_llm_server_tools.py
```

Then open `http:URL`.

## Recommended Learning Order

1. `01_Models`
2. `02_Prompts`
3. `03_StructuredOutput`
4. `04_OutputParsers`
5. `05_Chains`
6. `06_RAG`
7. `Tools` and `08_Agents.py`

## Important Security Note

Some files currently contain hardcoded API keys (for example in `08_Agents.py`, `gemini_llm_server_tools.py`, and `Tools/tool_calling.py`).  
You should rotate those keys and replace hardcoded values with environment variables before sharing or deploying.

## Troubleshooting

- If a Hugging Face endpoint script fails, confirm `HUGGINGFACEHUB_API_TOKEN` is valid and has inference access.
- If web loader scripts fail, keep a valid `USER_AGENT` set.
- If `chain.get_graph().print_ascii()` fails, install `grandalf`.

## Next Improvements

Add a Per-Module Requirements table
Map folders to required keys and extra packages (example: 04_OutputParsers needs HF token).

Improve Run Examples into grouped tracks
Group commands by Models, Prompts, Chains, RAG, Agents instead of one mixed list.

Add API/Server Usage example for FastAPI
Include a sample curl/PowerShell request body for /geminiask.

Add Known Issues / Limitations
Mention duplicated prompt folders and that some scripts are learning demos, not production-ready.

Add Security Checklist section
Explicitly say: never commit keys, rotate exposed keys, use .env.example, add .gitignore.

Add Contributing + License sections
Even short placeholders make the project complete and shareable.

