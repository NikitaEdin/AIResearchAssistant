from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, arxiv_tool

# Load environment variables from .env file
load_dotenv()

# Define Pydantic model for research response
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]
    
# Initialise LLM with Claude 4
llm = ChatAnthropic(model="claude-opus-4-20250514",
        max_tokens=250,
        # temp of 1 = more randomness and potentially longer responses.
        temperature=0.3)


parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Define prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools to gather information.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())
    
# Define tools to be used by agent
tools = [search_tool, wiki_tool, arxiv_tool, save_tool]


# Create agent with LLM and prompt
agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)

# Ask user for input query
query = input("Enter your research query: ")

# Example query to the agent
raw_response = agent_executor.invoke({
    "query": query,
    "name": "Research Assistant"
})

# Print the raw response from the agent
# Uncomment the next line to see the raw response
### print(raw_response)

# Parse the raw response using the Pydantic parser
try:
    structured_response = parser.parse(raw_response['output'][0]["text"])
    print(structured_response)
except Exception as e:
    print(f"Error parsing response: {e}, raw response: {raw_response}")
    






#response = llm.invoke("What is the capital of Scotland?")
#print(response)