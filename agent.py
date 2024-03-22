from langchain.tools import tool
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
import os
from typing import List, Optional
import csv

prompt= """ Your a helpful assistant with csv file tools, use the tool to search the CSV file to get the answer related to the data in the CSV file.
"""

# Step 1: Define the CSV Reading Function
@tool
def read_csv_file():
    """
    Tool to use and Read the most recent CSV file in the temp directory
    """
    directory_path = "temp"
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    if not csv_files:
        return "No CSV files found."
    
    # Sort files by modification time and pick the most recent
    latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
    path = os.path.join(directory_path, latest_file)

    data = []
    with open(path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Main Agent Function
def execute_agent(message):

    # Define tools
    tools = [read_csv_file]
    
    llm_chat = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Bind tools to chat model
    llm_with_tools = llm_chat.bind(functions=[convert_to_openai_function(t) for t in tools])

    # Define agent
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])
            
        }
        | prompt_template
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    try:
        
        response = agent_executor.invoke({"input": message})
        

        return response["output"]
    
    except AttributeError as ae:
        error_message = str(ae)
        print('AttributeError in execute_agent', error_message)
        return error_message
    