from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import os

app = Flask(__name__)

generated_resume_text = ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    global generated_resume_text

    name = request.form["name"]
    education = request.form["education"]
    skills = request.form["skills"]
    projects = request.form["projects"]
    experience = request.form["experience"]

    generated_resume_text = f"""
{name.upper()}

EDUCATION
{education}

SKILLS
{skills}

PROJECTS
{projects}

EXPERIENCE
{experience if experience else "Fresher"}

Professional Summary:
Motivated and detail-oriented student with strong technical skills and problem-solving abilities.
"""

    return render_template("result.html", resume=generated_resume_text)

@app.route("/download")
def download():
    file_path = "resume.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    for line in generated_resume_text.split("\n"):
        elements.append(Paragraph(line, style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)