# main.py

# Import necessary libraries
import os
import chainlit as cl
import requests
from langchain_openai import ChatOpenAI
from docx import Document
from bs4 import BeautifulSoup
# from config import OPENAI_API_KEY

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

# Fetch LinkedIn profile data (Dummy API for simulation)
def fetch_linkedin_profile(profile_url):
    # Simulating LinkedIn profile extraction
    response = f"""
    Extract key data from LinkedIn profile: {profile_url}
    - Name: John Doe
    - Experience: 5+ years in Data Science
    - Certifications: AWS Certified, PMP
    - Skills: Python, Machine Learning, NLP, SQL
    """
    return response

# Analyze job-resume match
def analyze_job_match(resume_text, job_posting):
    prompt = f"""
    Analyze the following resume against the job posting and provide:
    - Match percentage
    - Missing skills
    - Recommendations for improvement

    Resume:
    {resume_text}

    Job Posting:
    {job_posting}
    """
    return llm(prompt)

# Suggest resume keywords
def suggest_keywords(job_posting):
    prompt = f"""
    Extract 5-7 high-impact, ATS-friendly keywords to include in a resume for this job:
    {job_posting}
    """
    return llm(prompt)

# Provide insights on in-demand skills and roles
def provide_skill_insights(resume_text):
    prompt = f"""
    Based on this resume, suggest 3 in-demand skills, emerging roles, and salary ranges relevant to the user's experience.
    Resume:
    {resume_text}
    """
    return llm(prompt)

# Generate interview questions
def generate_interview_questions(resume_text, job_posting):
    prompt = f"""
    Generate 5-7 interview questions that combine technical knowledge and behavioral skills.
    Resume:
    {resume_text}
    Job Posting:
    {job_posting}
    """
    return llm(prompt)

# Get company insights
def get_company_insights(company_name):
    prompt = f"""
    Provide a summary of the company "{company_name}" including:
    - Mission and values
    - Recent news and trends
    - Insights on work culture and team environment
    """
    return llm(prompt)

def get_default(user_input, resume_text="no input provided", job_posting="no input provided"):


    prompt = f"""
    User provided an input that our job assistant app does not handle.  Our job assistant app can handle input with resume and job posting and provide feedback
    on user's resume according to the requirement in the job posting.  Please help with user input: "{user_input}"  This is user's resume "{resume_text}"
    and the job position they are referencing is "{job_posting}"
    """
    return llm(prompt)

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




@cl.on_message
async def main(message):
    if message.content == "start":
        await cl.Message("Welcome to the AI-Powered Job Application Assistant! 🎯").send()
        await cl.Message("Upload your resume, job posting, or LinkedIn profile URL to get started.").send()
    
    elif message.content.startswith("resume:"):
        file_path = message.content.replace("resume:", "").strip()
        resume_text = parse_resume(file_path)
        await cl.Message("✅ Resume uploaded and parsed successfully!").send()

        # Save resume for further use
        cl.user_session.set("resume_text", resume_text)
    
    elif message.content.startswith("job_posting:"):
        file_path = message.content.replace("job_posting:", "").strip()
        job_posting = parse_job_posting(file_path)
        await cl.Message("✅ Job posting uploaded successfully!").send()

        # Save job posting for further use
        cl.user_session.set("job_posting", job_posting)

    elif message.content.startswith("linkedin:"):
        profile_url = message.content.replace("linkedin:", "").strip()
        linkedin_data = fetch_linkedin_profile(profile_url)
        await cl.Message("✅ LinkedIn profile analyzed successfully!").send()

        # Save LinkedIn profile data
        cl.user_session.set("linkedin_data", linkedin_data)
    
    elif message.content == "analyze_match":
        resume_text = cl.user_session.get("resume_text")
        job_posting = cl.user_session.get("job_posting")
        if resume_text and job_posting:
            result = analyze_job_match(resume_text, job_posting)
            await cl.Message(f"📊 Match Analysis:\n{result.content}").send()
        else:
            await cl.Message("⚠️ Please upload both the resume and job posting before analyzing.").send()
    
    elif message.content == "suggest_keywords":
        job_posting = cl.user_session.get("job_posting")
        if job_posting:
            keywords = suggest_keywords(job_posting)
            await cl.Message(f"🔑 Suggested Keywords:\n{keywords.content}").send()
        else:
            await cl.Message("⚠️ Please upload the job posting before suggesting keywords.").send()

    elif message.content == "skill_insights":
        resume_text = cl.user_session.get("resume_text")
        if resume_text:
            insights = provide_skill_insights(resume_text)
            await cl.Message(f"📈 Skill Insights:\n{insights.content}").send()
        else:
            await cl.Message("⚠️ Please upload your resume before getting skill insights.").send()
    
    elif message.content == "interview_questions":
        resume_text = cl.user_session.get("resume_text")
        job_posting = cl.user_session.get("job_posting")
        if resume_text and job_posting:
            questions = generate_interview_questions(resume_text, job_posting)
            await cl.Message(f"🎙️ Sample Interview Questions:\n{questions.content}").send()
        else:
            await cl.Message("⚠️ Please upload both the resume and job posting before generating interview questions.").send()

    elif message.content.startswith("company:"):
        company_name = message.content.replace("company:", "").strip()
        insights = get_company_insights(company_name)
        await cl.Message(f"🏢 Company Insights:\n{insights.content}").send()

    elif message.content == "help":
        await cl.Message("""
        🤖 Available Commands:
        - `resume:<file_path>` -> Upload resume (DOCX format)
        - `job_posting:<file_path>` -> Upload job posting (TXT format)
        - `linkedin:<profile_url>` -> Analyze LinkedIn profile
        - `analyze_match` -> Analyze job match
        - `suggest_keywords` -> Get resume keyword suggestions
        - `skill_insights` -> Get in-demand skill insights
        - `interview_questions` -> Generate interview questions
        - `company:<company_name>` -> Get company insights
        - `help` -> List available commands
        """).send()
    
    else:
        await cl.Message("⚠️ No available command. Using default").send()

        user_input = message.content.strip()
        resume_text = cl.user_session.get("resume_text")
        job_posting = cl.user_session.get("job_posting")
        if resume_text or job_posting:
            user_input_handler = get_default(user_input, resume_text, job_posting)
        else:
            user_input_handler = get_default(user_input)
        await cl.Message(f"Here you go:\n{user_input_handler.content}").send()
