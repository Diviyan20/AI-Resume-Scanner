import gradio as gr
import os
from utils.parser import parse_resume
from utils.scorer import score_resume
from utils.cleaner import clean_text
from utils.ats_score import ats_score

def process_resume(resume_files, job_desc):
    if resume_files is None or job_desc.strip() == "":
        return "Please provide resume or enter a job description"

    results = []

    for resume_file in(resume_files if isinstance(resume_files, list) else[resume_files]):

        resume = resume_file.name

        raw_text = parse_resume(resume)
        cleaned_text = clean_text(raw_text)
    
        resume_score = score_resume(cleaned_text, job_desc)

        ats_match = ats_score(resume_file, job_desc)

        results.append({
            "name": os.path.basename(resume_file.name),
            "ats": ats_match,
            "gpt":resume_score
        })

    results_sorted = sorted(results, key=lambda x: x["ats"], reverse=True)

    if len(results_sorted) > 1:
        markdown_output = "# 📊 Resume Ranking\n\n"
        for idx, res in enumerate(results_sorted, 1):
            markdown_output += f"**{idx}.{res['name']}**  - ATS: {res['ats']}%\n\n"

    else:
       res = results_sorted[0]
       markdown_output = f"""
# Resume Analysis

## ATS Match Score
**{res['ats']}%**

## GPT Recruiter Analysis
{res['gpt']}
"""

    return "", markdown_output

with gr.Blocks() as demo:
    gr.Markdown("# 📄 AI-Powered Resume Scanner")
    with gr.Row():
        with gr.Column(scale=1):
            resume_input = gr.File(label="Upload File", type="filepath", file_types=[".pdf"], file_count="multiple")
            jd_input = gr.Textbox(label="Enter Job Description", lines=6, placeholder="Job Description....")
            btn = gr.Button("Scan Resume")

        with gr.Column(scale=2):
            status = gr.Markdown()
            output = gr.Markdown("# Resume Analysis / Ranking")

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