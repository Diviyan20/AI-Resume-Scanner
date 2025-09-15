import gradio as gr
import time
from utils.parser import parse_resume
from utils.scorer import score_resume
from utils.cleaner import clean_text
from utils.ats_score import ats_score

def process_resume(resume_file, job_desc):
    if resume_file is None or job_desc.strip() == "":
        return "Please provide resume or enter a job description"

    resume = resume_file.name

    raw_text = parse_resume(resume)
    cleaned_text = clean_text(raw_text)
    resume_score = score_resume(cleaned_text, job_desc)

    ats_match = ats_score(resume_file, job_desc)

    time.sleep(2)

    formatted_output = f"""
# Resume Analysis

## ATS Match Score
**{ats_match}%**

## GPT Recruiter Analysis
{resume_score}
"""
    return "", formatted_output

with gr.Blocks() as demo:
    gr.Markdown("# 📄 AI-Powered Resume Scanner")
    with gr.Row():
        with gr.Column(scale=1):
            resume_input = gr.File(label="Upload File", type="filepath")
            jd_input = gr.Textbox(label="Enter Job Description", lines=6, placeholder="Job Description....")
            btn = gr.Button("Scan Resume")

        with gr.Column(scale=2):
            status = gr.Markdown()
            output = gr.Markdown("# Resume Analysis")

    def set_status(resume_file, job_desc):
        return "Analyzing Resume....."

    btn.click(
            fn=set_status,
            inputs=[resume_input, jd_input],
            outputs=status
        ).then(
            fn=process_resume,
            inputs=[resume_input,jd_input],
            outputs=[status,output]
        )

demo.launch()