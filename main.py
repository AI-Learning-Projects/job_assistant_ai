# main.py

# Import necessary libraries
import os
import re
import chainlit as cl
import requests
import json
from langchain_openai import ChatOpenAI
from docx import Document
from bs4 import BeautifulSoup
# from config import OPENAI_API_KEY
from templates import router_template, chain_templates
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain

#get API token from system environment variable
OPENAI_API_KEY = os.environ.get("OPEAI_API_KEY")

# Initialize GPT-4o-mini with LangChain
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

# ---- Utility Functions ----

# Parse resume content from a DOCX file
def parse_resume(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Parse job posting from a text file
def parse_job_posting(file_path):
    with open(file_path, "r") as file:
        return file.read()

# create router chain from the imported router template in templates.py
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

chains = {}
for name, template in chain_templates.items():
    # Create a prompt template for each chain
    # input_variables = re.findall(r"\{(.*?)\}", template)
    # print(f"\nInput variables for {name}: {input_variables}\n")
    template = PromptTemplate.from_template(template=template)#, input_variables=input_variables)
    
    chains[name] = LLMChain(llm=llm, prompt=template)

# # Create sub-chains dynamically
# chains = {
#     name: LLMChain(llm=llm, prompt=PromptTemplate(input_variables=list(template.format("").split("{")[1:]), template=template))
#     for name, template in chain_templates.items()
# }

default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=llm, prompt=default_prompt)

chain = MultiPromptChain(router_chain=router_chain, 
                         destination_chains=chains, 
                         default_chain=default_chain, verbose=True
                        )

# def run_router_chain(user_input):
#     # Get the routing decision from the LLM
#     router_response = router_chain.invoke(user_input)

#     # Parse the response as JSON
#     router_decision = json.loads(router_response)
#     chain_name = router_decision["chain_name"]
#     variables = router_decision["variables"]

#     # Run the selected chain with extracted variables
#     return chains[chain_name].invoke(**variables)


# ---- Chainlit Event Handlers ----


@cl.on_chat_start
async def start():
    job = None

    # Wait for the user to upload a file
    while job == None:
        job = await cl.AskFileMessage(
            content="Please upload a job posting file to begin!", accept=["text/plain"]
        ).send()

    text_file = job[0]

    with open(text_file.path, "r", encoding="utf-8") as f:
        job_posting = f.read()

    cl.user_session.set("job_posting", job_posting)


    resume = None

    # Wait for the user to upload a file
    while resume == None:
        resume = await cl.AskFileMessage(
            content="Please upload a resume file with .docx extension to begin!", accept=["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        ).send()

    text_file = resume[0]
    resume_text = parse_resume(text_file.path)

    cl.user_session.set("resume_text", resume_text)

    await cl.Message("""
    Example Questions to ask:
    - `analyze job match`: Check how well the resume matches the job posting and give suggestions.
    - `generate interview questions`: Generate interview questions based on the job posting.
    - `get company insights`: Get any background information about the company in the job posting
    - `fetch linkedin profile`: Stimulate an ATS (Application Tracking System) system to extract data from LinkedIn profile.
    - `extract job keywords`: Extract keywords from the job posting.
    - `provide resume insights`: Give career planning advice based on the resume.
    - `/restart`: Restart the conversation.
    """).send()


@cl.on_message
async def main(message):
    if message.content == "restart":
        await cl.Message("Restarting the conversation...").send()
        await start()
        return

    await cl.Message("... waiting for response").send()
    job_posting = cl.user_session.get("job_posting")
    resume_text = cl.user_session.get("resume_text")

    response = chain.invoke(f"user input: {message.content}, \
                            Keep the following data in the chain:\
                            \njob_posting: {job_posting}\n \
                            \nresume: {resume_text}")
    await cl.Message(f"Here you go:\n{response['text']}").send()
