

#################### Prompt Template Declaration ######################
analyze_match_prompt="""
    Analyze the following resume against the job posting and provide:
    - Match percentage
    - Missing skills
    - Recommendations for improvement

    Resume:
    {resume_text}

    Job Posting:
    {job_posting}
    """


suggest_keyword_prompt = """
    Extract 5-7 high-impact, ATS-friendly keywords to include in a resume for this job:
    {job_posting}
    """

provide_skillset_prompt = """
    Based on this resume, suggest 3 in-demand skills, emerging roles, and salary ranges relevant to the user's experience.
    Resume:
    {resume_text}
    """


generate_interview_prompt = """
    Generate 5-7 interview questions that combine technical knowledge and behavioral skills.
    Resume:
    {resume_text}
    Job Posting:
    {job_posting}
    """

get_company_insight_promopt = """
    Provide a summary of the company "{company_name}" including:
    - Mission and values
    - Recent news and trends
    - Insights on work culture and team environment
    """

job_assist_default_prompt = """
    User provided an input that our job assistant app does not handle.  Our job assistant app can handle input with resume and job posting and provide feedback
    on user's resume according to the requirement in the job posting.  Please help with user input: "{user_input}"  This is user's resume "{resume_text}"
    and the job position they are referencing is "{job_posting}"
    """


PROMPT_INFO = [
    {
        "name": "analyze_match", 
        "description": "nalyze_match resume against job posting", 
        "prompt_template": analyze_match_prompt
    },
    {
        "name": "suggest_keyword", 
        "description": "extract keyword from job posting", 
        "prompt_template": suggest_keyword_prompt
    },
    {
        "name": "provide_skillset", 
        "description": "provide insight on in-demand skill and role", 
        "prompt_template": provide_skillset_prompt
    },
    {
        "name": "generate_interview", 
        "description": "generate interview question", 
        "prompt_template": generate_interview_prompt
    },
    {
        "name": "get_company_insight", 
        "description": "provide a summary for a company", 
        "prompt_template": get_company_insight_promopt
    },
    {
        "name": "job assist default", 
        "description": "app default prompt", 
        "prompt_template": job_assist_default_prompt
    }
]

MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{
    "destination": string, // name of prompt to use or "DEFAULT" 
    "next_inputs": {{"input": string, "resume_text": string,job_posting": string,company_name: string}}
}}
```

REMEMBER: The value of “destination” MUST match one of \
the candidate prompts listed below.\
If “destination” does not fit any of the specified prompts, set it to “DEFAULT.”
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}


<< OUTPUT (remember to include the ```json)>>"""