# standard library
from datetime import datetime

# third party libraries
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
import google.genai.types as types
from vertexai import rag

from .prompts import (
    RAG_AGENT_PROMPT,
    ROOT_AGENT_PROMPT,
    GOOGLE_SEARCH_PROMPT
)

# load the .env environment variables
load_dotenv()

class Hotel(BaseModel):
    """Defines the schema for a single hotel."""
    hotel_name: str = Field(description="The name of the hotel.")
    hotel_photo: str = Field(description="A URL string of the hotel exterior.")
    address: str = Field(description="The street address of the hotel.")
    city: str = Field(description="The hotel's address city.")
    state: str = Field(description="The hotel's address state.")
    zip_code: str = Field(description="The hotel's zip code.")
    brand_code: str = Field(description="The 2-letter brand code for the hotel.")
    brand_name: str = Field(description="The name of the hotel brand.")

class HotelList(BaseModel):
    """Defines the schema for a list of hotels."""
    hotels: list[Hotel] = Field(description="A list of hotels.")

json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            # please fill in your own rag corpus
            # here is a sample rag corpus for testing purpose
            # e.g. projects/123/locations/us-central1/ragCorpora/456
            rag_corpus='projects/canonical-pipeline-demo/locations/us-central1/ragCorpora/7991637538768945152'
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

hotel_search_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_search_agent',
    instruction=RAG_AGENT_PROMPT,
    tools=[
        ask_vertex_retrieval,
    ]
)

hotel_formatting_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_formatting_agent',
    instruction=(
        'You are a data formatting expert. You will receive unstructured text '
        'containing information about hotels. Your sole responsibility is to '
        'extract this information and format it precisely into the required '
        'JSON structure. Do not add any conversational text.'
    ),
    tools=[],  # <-- IMPORTANT: Tools list is empty
    generate_content_config=json_response_config,
    output_schema=HotelList,
)

hotel_search_orchestrator = Agent(
    model='gemini-2.5-flash',
    name='hotel_search_orchestrator',
    instruction=(
        'You are a hotel search coordinator. To fulfill the user request, '
        'you must follow these two steps in order: '
        '1. First, use the `hotel_search_agent` to find relevant hotel information. '
        '2. Second, take the output from the retrieval and use the `hotel_formatting_agent` '
        'to structure the information into the final JSON format.'
    ),
    tools=[
        AgentTool(hotel_search_agent),
        AgentTool(hotel_formatting_agent),
    ]
)

google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    global_instruction=f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}",
    instruction=GOOGLE_SEARCH_PROMPT,
    tools=[
        google_search
    ],
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        AgentTool(hotel_search_orchestrator),
        AgentTool(google_search_agent)
    ]
)
