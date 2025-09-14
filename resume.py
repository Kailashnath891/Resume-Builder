"""
High-level Resume Generator (Python) - HTML Only

Features:
- Accepts user data via interactive prompts
- Renders a clean HTML resume using an embedded Jinja2 template
- Outputs: resume.html (open in browser and Save as PDF if needed)

Usage:
- Install dependencies: pip install Jinja2
- Run: python resume_generator.py
"""

from jinja2 import Template
import argparse
import os
import sys
from datetime import datetime

# Minimal CSS
CSS = """
body { font-family: -apple-system, Roboto, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; color: #222 }
.container { max-width: 800px; margin: auto; background: #fff; padding: 28px; box-shadow: 0 2px 6px rgba(0,0,0,0.06) }
.header { display: flex; justify-content: space-between; align-items: center }
.name { font-size: 28px; font-weight: 700 }
.contact { text-align: right; font-size: 14px }
.section { margin-top: 18px }
.section h2 { font-size: 16px; margin-bottom: 8px; border-bottom: 1px solid #eee; padding-bottom: 6px }
.skill, .strength { display: block; margin-bottom: 6px; font-size: 14px }
.job, .education, .project { margin-bottom: 12px }
.job .title, .project .title { font-weight: 600 }
.job .meta, .project .meta { color: #666; font-size: 13px }
.summary { white-space: pre-wrap }
"""

# Jinja2 Template
TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ name }} - Resume</title>
  <style>{{ css }}</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <div class="name">{{ name }}</div>
        {% if tagline %}<div>{{ tagline }}</div>{% endif %}
      </div>
      <div class="contact">
        {% if email %}{{ email }}<br>{% endif %}
        {% if phone %}{{ phone }}<br>{% endif %}
        {% if location %}{{ location }}<br>{% endif %}
        {% if linkedin %}LinkedIn: {{ linkedin }}<br>{% endif %}
        {% if github %}GitHub: {{ github }}{% endif %}
      </div>
    </div>

    {% if summary %}
    <div class="section">
      <h2>Summary</h2>
      <div class="summary">{{ summary }}</div>
    </div>
    {% endif %}

    {% if experience %}
    <div class="section">
      <h2>Experience</h2>
      {% for job in experience %}
      <div class="job">
        <div class="title">{{ job.title }} — {{ job.company }}</div>
        <div class="meta">{{ job.start_date }} — {{ job.end_date or 'Present' }} · {{ job.location or '' }}</div>
        {% if job.responsibilities %}
        <ul>
          {% for r in job.responsibilities %}
          <li>{{ r }}</li>
          {% endfor %}
        </ul>
        {% endif %}
      </div>
      {% endfor %}
    </div>
    {% endif %}

    {% if education %}
    <div class="section">
      <h2>Education</h2>
      {% for e in education %}
      <div class="education">
        <div class="title">{{ e.degree }} — {{ e.institution }}</div>
        <div class="meta">{{ e.start_date }} — {{ e.end_date or '' }} · {{ e.location or '' }}</div>
        {% if e.details %}<div>{{ e.details }}</div>{% endif %}
      </div>
      {% endfor %}
    </div>
    {% endif %}

    {% if projects %}
    <div class="section">
      <h2>Projects</h2>
      {% for p in projects %}
      <div class="project">
        <div class="title">{{ p.name }}</div>
        {% if p.link %}<div class="meta">{{ p.link }}</div>{% endif %}
        {% if p.description %}<div>{{ p.description }}</div>{% endif %}
        {% if p.points %}
        <ul>
          {% for pt in p.points %}
          <li>{{ pt }}</li>
          {% endfor %}
        </ul>
        {% endif %}
      </div>
      {% endfor %}
    </div>
    {% endif %}

    {% if skills %}
    <div class="section">
      <h2>Skills</h2>
      <ul>
      {% for skill in skills %}
        <li>{{ skill }}</li>
      {% endfor %}
      </ul>
    </div>
    {% endif %}

    {% if strengths %}
    <div class="section">
      <h2>Strengths</h2>
      <ul>
        {% for s in strengths %}
        <li>{{ s }}</li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}

    <div style="margin-top:20px; font-size:12px; color:#888">Generated on {{ generated_on }}</div>
  </div>
</body>
</html>
"""

def interactive_fill():
    data = {}

    print("We'll ask a few quick questions. Leave blank to skip.\n")
    data['name'] = input("Name: ")
    data['tagline'] = input("Tagline: ")
    data['email'] = input("Email: ")
    data['phone'] = input("Phone: ")
    data['location'] = input("Location: ")
    data['linkedin'] = input("LinkedIn: ")
    data['github'] = input("GitHub: ")

    summary = input("Summary / Objective: ")
    data['summary'] = summary if summary.strip() else ""

    # Experience
    experience = []
    print("\nAdd your experiences (press Enter with no title to stop):")
    while True:
        title = input("Job title: ")
        if not title.strip():
            break
        company = input("Company: ")
        start = input("Start date: ")
        end = input("End date (leave blank if Present): ")
        loc = input("Location: ")
        resp_lines = []
        print("Enter responsibilities (blank line to finish):")
        while True:
            r = input("- ")
            if not r.strip():
                break
            resp_lines.append(r.strip())
        experience.append({
            'title': title, 'company': company, 'start_date': start,
            'end_date': end, 'location': loc, 'responsibilities': resp_lines
        })
    data['experience'] = experience

    # Education
    education = []
    print("\nAdd your education (press Enter with no degree to stop):")
    while True:
        degree = input("Degree: ")
        if not degree.strip():
            break
        inst = input("Institution: ")
        start = input("Start date: ")
        end = input("End date: ")
        loc = input("Location: ")
        details = input("Details (GPA, specialization, etc.): ")
        education.append({
            'degree': degree, 'institution': inst, 'start_date': start,
            'end_date': end, 'location': loc, 'details': details
        })
    data['education'] = education

    # Projects
    projects = []
    print("\nAdd your projects (press Enter with no name to stop):")
    while True:
        pname = input("Project name: ")
        if not pname.strip():
            break
        plink = input("Project link (optional): ")
        pdesc = input("Short description: ")
        subpoints = []
        print("Enter project highlights (blank line to finish):")
        while True:
            sp = input("- ")
            if not sp.strip():
                break
            subpoints.append(sp.strip())
        projects.append({'name': pname, 'link': plink, 'description': pdesc, 'points': subpoints})
    data['projects'] = projects

    # Skills (Main skill + sub-skills inline)
    skills = []
    print("\nAdd your skills (main skill + sub-skills). Leave main skill empty to stop.")
    while True:
        main = input("Main skill: ")
        if not main.strip():
            break
        subskills = []
        while True:
            sub = input(f"  Sub-skill for {main}: ")
            if not sub.strip():
                break
            subskills.append(sub.strip())
        if subskills:
            skills.append(f"{main}: {', '.join(subskills)}")
        else:
            skills.append(main)
    data['skills'] = skills

    # Strengths
    strengths = []
    print("\nAdd your strengths (leave blank to stop):")
    while True:
        s = input("- ")
        if not s.strip():
            break
        strengths.append(s.strip())
    data['strengths'] = strengths

    return data

def render_html(data, css=CSS):
    tpl = Template(TEMPLATE)
    return tpl.render(css=css, generated_on=datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'), **data)

def main():
    parser = argparse.ArgumentParser(description='High-level Resume Generator (HTML only)')
    parser.add_argument('--output', '-o', help='Base name for output file (default: resume)', default='resume')
    args = parser.parse_args()

    data = interactive_fill()
    html = render_html(data)
    html_file = f"{args.output}.html"

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ Saved HTML resume to', html_file)
    print('👉 Open it in your browser and use "Print → Save as PDF" for a PDF copy.')

if __name__ == '__main__':
    main()
