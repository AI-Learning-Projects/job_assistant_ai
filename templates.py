from langchain.chains.router.multi_prompt import MULTI_PROMPT_ROUTER_TEMPLATE


fetch_linkedin_profile = """Stimulate an ATS (Application Tracking System) system to extract data from LinkedIn profile.
    For example it should return the following:
    - Name: Name of the person
    - Experience: Number of years in the field
    - Certifications: List of certifications
    - Skills: List of skills
    - Education: Degree and institution
    - Location: City and state
    - Contact: Email and phone number (Optional, if found warn the user about privacy)
    - Summary: A brief summary of the profile
    and other ATS friendly data that can be extracted from LinkedIn profile.

    Here is the user input:
    {input}
    """

analyze_job_match = """
    Analyze the following resume against the job posting and provide:
    - Match percentage: How well does the resume match the job posting?
    - Missing skills: What skills are missing from the resume that are required in the job posting?
    - Recommendations for improvement: What can be improved in the resume to better match the job posting?

    Here is the user input:
    {input}
    """

extract_job_keywords = """
    Extract 5-7 high-impact, ATS-friendly keywords to include in a resume for this job posting:
    
    Here is the user input:
    {input}
    """

provide_resume_insights = """
    Based on this resume, suggest:
    - Any imporovements to be made in the resume.
    - 3 in-demand skills: skills that are relevant to the user's experience but not mentioned in the resume.
    - emerging roles: roles that the user might consider based on their experience.
    - salary ranges: give a list of salary ranges based on the emerging roles listed above 
                    and it should be relevant to the user's experience and zip code location from user's resume.
    
    Here is the user input:
    {input}
    """

generate_interview_questions = """
    Generate 5-7 interview questions that combine technical knowledge and behavioral skills based on the resume and job posting.
    
    Here is the user input:
    {input}
    """

get_company_insights = """
    Provide a summary of the company in the job posting including:
    - Mission and values
    - Recent news and trends
    - Insights on work culture and team environment

    Here is the user input:
    {input}
    """

default_template = """
    User provided an input that our job assistant app does not handle. 
    Our job assistant app can handle input with resume and job posting and provide feedback
    on user's resume according to the requirement in the job posting.  
    
    Here is the user input:
    {input}
    """

destinations = """
"fetch_linkedin_profile": Extract data from LinkedIn profile
"analyze_job_match": Analyze resume against job posting
"extract_job_keywords": Extract keywords from job posting
"provide_resume_insights": Provide insights based on resume
"generate_interview_questions": Generate interview questions
"get_company_insights": Get company insights
"default_template": Handle unrecognized input
"""
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations)

# router_template = """
# You are an AI assistant that routes user queries to the appropriate function.

# Based on the user input, determine:
# 1. The **chain name** from the following options: 
#    - "fetch_linkedin_profile": Extract data from LinkedIn profile
#    - "analyze_job_match": Analyze resume against job posting
#    - "extract_job_keywords": Extract keywords from job posting
#    - "provide_resume_insights": Provide insights based on resume
#    - "generate_interview_questions": Generate interview questions
#    - "get_company_insights": Get company insights
#    - "default_template": Handle unrecognized input
# 2. The **required variables** for that chain.

# Return your response as a JSON object with two keys:
# - "chain_name": The correct chain name.
# - "variables": A dictionary of extracted variables.

# User Input: {input}
# """

chain_templates = {
    "fetch_linkedin_profile": fetch_linkedin_profile,
    "analyze_job_match": analyze_job_match,
    "extract_job_keywords": extract_job_keywords,
    "provide_resume_insights": provide_resume_insights,
    "generate_interview_questions": generate_interview_questions,
    "get_company_insights": get_company_insights,
    "default_template": default_template
}
