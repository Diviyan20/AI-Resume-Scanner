import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')


openai = OpenAI(api_key=openai_api_key)

#Uses GPT to provide score for a resume and provide feedback
def score_resume(resume_text: str, job_description: str):
    prompt =f"""
    You are an expert technical recruiter. Evaluate the resume against the job description
    and strictly follow the instructions:

    1. Compare the resume skills and experiences with the job description.
    2. Assign a numerical score (0–100) based on overlap:
        - 90–100 = Strong match (resume hits nearly all requirements).
        - 70–89 = Good match (many relevant skills, but missing some).
        - 50–69 = Partial match (some transferable skills, but gaps exist).
        - 0–49  = Weak match (resume misses most requirements).
    3. Clearly list missing skills (as bullet points).
    4. Summarize candidate strengths in a short paragraph.
    5. Output your result in **strict Markdown format** like this:

   # Score: 75
    
   # Missing Skills

    - Experience with quality assurance (QA) testing

    - Direct experience in responding to feedback from QA

    - Specific examples of liaising with game designers and developers for technical resources

    - Evidence of ensuring game performance and design realization

    - Experience with iterative design and performance optimization

   # Summary   
     The candidate, Diviyan Rajan, has a solid foundation in game development, with experience in multiple game 
     engines such as Unity, Unreal Engine, and Godot. The resume highlights hands-on experience in gameplay programming 
     and AI systems through internships, showcasing abilities in developing player control systems and modular AI 
     architectures. However, there are notable gaps in quality assurance experience, particularly in conducting QA 
     tests and providing feedback. While Diviyan demonstrates strong collaboration skills with game designers and 
     technical implementations, the resume lacks explicit examples of working with game designers to set up technical 
     resources or ensuring optimal game design performance. Overall, the candidate shows promise but would benefit from 
     more detailed experience related to QA processes and design maximization.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
"""
    
    response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    return result