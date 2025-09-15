from simple_ats import ATS
from utils.parser import parse_resume


def ats_score(resume_file, job_desc):
    resume_text = parse_resume(resume_file.name)
    resume_text = " ".join(resume_text.split())

    ats = ATS()
    ats.load_resume(resume_text)
    ats.load_job_description(job_desc)

    experience = ats.extract_experience()
    ats.clean_experience(experience)

    skills = ats.extract_skills()
    skills_str = " ".join(skills)
    ats.clean_skills(skills_str)

    similarity_score = ats.compute_similarity()
    return round(similarity_score.item() * 100, 2)