from fastapi import FastAPI
from pydantic import BaseModel
import google.genai as genai
from google.genai import types

app = FastAPI()

# -------------------------------------------------------
# Request schema: expects a 'prompt' string from the client
# 'max_length' is accepted but not currently used by Gemini API
# -------------------------------------------------------
class RequestData(BaseModel):
    prompt: str
    max_length: int = 20


# -------------------------------------------------------
# Local tool implementation
# In production, this would call a real weather API
# -------------------------------------------------------
def get_weather(city: str):
    return f"The weather in {city} is 32°C and sunny."


# -------------------------------------------------------
# Tool schema definition using Gemini's types
# This tells the LLM what tools are available, their purpose,
# and what arguments they accept — so the model knows when/how to call them
# -------------------------------------------------------
weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get current weather for a given city",
            parameters=types.Schema(
                type="object",
                properties={
                    "city": types.Schema(
                        type="string",
                        description="Name of the city"
                    )
                },
                required=["city"]
            )
        )
    ]
)

# -------------------------------------------------------
# Tool dispatcher map
# Maps tool names (returned by LLM) to actual Python functions
# Makes it easy to add new tools without changing the routing logic
# -------------------------------------------------------
TOOL_MAP = {
    "get_weather": get_weather
}


@app.post("/geminiask")
async def generate_ans(data: RequestData):

    client = genai.Client(api_key="AIzaSyAuKkH44_dvmH7dPqRBaUYvHvCy5kJG0oc")

    # -------------------------------------------------------
    # STEP 1: First LLM call — send user prompt with tool definitions
    # The system instruction ensures the model answers general questions
    # directly and only invokes tools when the query is tool-relevant
    # -------------------------------------------------------
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=data.prompt,
        config=types.GenerateContentConfig(
            tools=[weather_tool],
            system_instruction=(
                "You are a helpful assistant. Answer general questions directly "
                "using your knowledge. Only use the tools when the user specifically "
                "asks queries related to tools."
            )
        )
    )

    candidate = response.candidates[0]
    # Extract the first part of the response (could be text or a function call)
    part = candidate.content.parts[0] if candidate.content.parts else None

    # -------------------------------------------------------
    # STEP 2: Check if the LLM decided to call a tool
    # - hasattr check ensures the attribute exists on the part
    # - 'is not None' guard prevents AttributeError when function_call exists but is empty
    # - .name check confirms an actual tool was requested
    # -------------------------------------------------------
    if part and hasattr(part, "function_call") and part.function_call is not None and part.function_call.name:

        function_call = part.function_call
        function_name = function_call.name          # e.g., "get_weather"
        function_args = dict(function_call.args)    # e.g., {"city": "New York"}

        # Look up the corresponding Python function
        tool_fn = TOOL_MAP.get(function_name)
        if not tool_fn:
            return {"error": f"Unknown tool: {function_name}"}

        # Execute the tool locally with the args provided by the LLM
        result = tool_fn(**function_args)

        # -------------------------------------------------------
        # STEP 3: Second LLM call — send the tool result back
        # Full conversation history is passed so the model has context:
        #   [user prompt] → [model's tool call] → [tool result]
        # The model then generates a natural language response from the result
        # -------------------------------------------------------
        second_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                # Original user message
                types.Content(role="user", parts=[types.Part(text=data.prompt)]),
                # Model's decision to call the tool
                types.Content(role="model", parts=[types.Part(function_call=function_call)]),
                # Tool execution result returned to the model
                types.Content(
                    role="user",
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=function_name,
                            response={"result": result}
                        )
                    )]
                )
            ],
            config=types.GenerateContentConfig(tools=[weather_tool])
        )

        return {"generated_text": second_response.text}

    # -------------------------------------------------------
    # STEP 4: No tool call — return the direct text response
    # This handles all general knowledge questions
    # -------------------------------------------------------
    if response.text:
        return {"generated_text": response.text}

    # Fallback if the model returned neither text nor a tool call
    return {"error": "No response generated"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)