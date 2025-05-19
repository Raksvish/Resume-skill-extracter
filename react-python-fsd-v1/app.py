from flask import Flask, request, render_template
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
SKILLS = ["Python", "Java", "React", "SQL", "Machine Learning", "Docker", "Agile"]

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_skills(text, skill_list):
    found = []
    for skill in skill_list:
        if skill.lower() in text.lower():
            found.append(skill)
    return found

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        text = extract_text(filepath)
        matched_skills = extract_skills(text, SKILLS)
        for skill in matched_skills:
            text = text.replace(skill, f"<mark>{skill}</mark>")
        return render_template("result.html", text=text, skills=matched_skills)
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
