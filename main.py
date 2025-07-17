from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor


load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]
    

llm = ChatAnthropic(model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=1)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

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
    
agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools=[]
)

agent_executor = AgentExecutor(agent=agent, tools=[],verbose=True)

raw_response = agent_executor.invoke({
    "query": "What is the capital of Scotland?",
    "name": "Research Assistant"
})

#print(raw_response)

# Parse the raw response using the Pydantic parser
try:
    structured_response = parser.parse(raw_response['output'][0]["text"])
except Exception as e:
    structured_response = f"Error parsing response: {e}, raw response: {raw_response}"
    
print(structured_response)





#response = llm.invoke("What is the capital of Scotland?")
#print(response)