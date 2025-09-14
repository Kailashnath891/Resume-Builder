import streamlit as st
from jinja2 import Template
from datetime import datetime

# ---------------- CSS ----------------
CSS = """
body {
  font-family: -apple-system, Roboto, 'Segoe UI', Arial, sans-serif;
  margin: 0;
  padding: 0;
  color: #222;
}
.container {
  display: flex;
  width: 100%;
  min-height: 100vh;
}
.sidebar {
  width: 30%;
  background: #0056A0;
  color: white;
  padding: 20px;
}
.sidebar h2 {
  border-bottom: 1px solid rgba(255,255,255,0.3);
  padding-bottom: 6px;
  font-size: 16px;
}
.sidebar ul {
  list-style: none;
  padding-left: 10px;
}
.sidebar ul li::before {
  content: "➤ ";
  color: #fff;
  font-weight: bold;
}
.main {
  width: 70%;
  background: #fff;
  padding: 28px;
}
.main h2 {
  font-size: 16px;
  border-bottom: 1px solid #eee;
  margin-bottom: 8px;
  padding-bottom: 6px;
}
.main ul {
  list-style: none;
  padding-left: 16px;
}
.main ul li::before {
  content: "➤ ";
  color: #0056A0;
  font-weight: bold;
}
.title {
  font-weight: bold;
}
"""

# ---------------- Jinja2 Template ----------------
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
  <!-- Sidebar -->
  <div class="sidebar">
    <h2>Contact</h2>
    {% if email %}<div>{{ email }}</div>{% endif %}
    {% if phone %}<div>{{ phone }}</div>{% endif %}
    {% if location %}<div>{{ location }}</div>{% endif %}
    {% if linkedin %}<div>LinkedIn: {{ linkedin }}</div>{% endif %}
    {% if github %}<div>GitHub: {{ github }}</div>{% endif %}

    {% if skills %}
    <h2>Skills</h2>
    <ul>
      {% for skill in skills %}
        <li>{{ skill }}</li>
      {% endfor %}
    </ul>
    {% endif %}

    {% if strengths %}
    <h2>Strengths</h2>
    <ul>
      {% for s in strengths %}
      <li>{{ s }}</li>
      {% endfor %}
    </ul>
    {% endif %}

    {% if education %}
    <h2>Education</h2>
    {% for e in education %}
      <div><b>{{ e.degree }}</b><br>{{ e.institution }}<br>{{ e.start_date }} - {{ e.end_date }}</div>
    {% endfor %}
    {% endif %}
  </div>

  <!-- Main Content -->
  <div class="main">
    <h1 class="name">{{ name }}</h1>
    {% if tagline %}<p>{{ tagline }}</p>{% endif %}

    {% if summary %}
    <h2>Summary</h2>
    <p>{{ summary }}</p>
    {% endif %}

    {% if experience %}
    <h2>Experience</h2>
    {% for job in experience %}
      <div>
        <div class="title">{{ job.title }}</div>
        <div>{{ job.company }} · {{ job.start_date }} — {{ job.end_date or 'Present' }}</div>
        <ul>
        {% for r in job.responsibilities %}
          <li>{{ r }}</li>
        {% endfor %}
        </ul>
      </div>
    {% endfor %}
    {% endif %}

    {% if projects %}
    <h2>Projects</h2>
    {% for p in projects %}
      <div>
        <div class="title">{{ p.name }}</div>
        {% if p.description %}<p>{{ p.description }}</p>{% endif %}
        <ul>
        {% for pt in p.points %}
          <li>{{ pt }}</li>
        {% endfor %}
        </ul>
      </div>
    {% endfor %}
    {% endif %}
  </div>
</div>
</body>
</html>
"""

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Resume Generator", layout="wide")
st.title("📄 Resume Generator")

# Sidebar input fields
st.sidebar.header("Basic Information")
name = st.sidebar.text_input("Full Name", key="name")
tagline = st.sidebar.text_input("Tagline", key="tagline")
email = st.sidebar.text_input("Email", key="email")
phone = st.sidebar.text_input("Phone", key="phone")
location = st.sidebar.text_input("Location", key="location")
linkedin = st.sidebar.text_input("LinkedIn", key="linkedin")
github = st.sidebar.text_input("GitHub", key="github")
summary = st.sidebar.text_area("Summary", key="summary")

# Experience
st.sidebar.header("Experience")
exp_count = st.sidebar.number_input("Number of experiences", min_value=0, max_value=10, value=1, step=1, key="exp_count")
experience = []
for i in range(exp_count):
    with st.expander(f"Experience {i+1}"):
        title = st.text_input(f"Job Title {i+1}", key=f"title_{i}")
        company = st.text_input(f"Company {i+1}", key=f"company_{i}")
        start = st.text_input(f"Start Date {i+1}", key=f"start_{i}")
        end = st.text_input(f"End Date {i+1}", key=f"end_{i}")
        loc = st.text_input(f"Location {i+1}", key=f"loc_{i}")
        resps = st.text_area(f"Responsibilities (one per line) {i+1}", key=f"resps_{i}")
        experience.append({
            "title": title, "company": company, "start_date": start,
            "end_date": end, "location": loc,
            "responsibilities": resps.split("\n") if resps else []
        })

# Education
st.sidebar.header("Education")
edu_count = st.sidebar.number_input("Number of education entries", min_value=0, max_value=5, value=1, step=1, key="edu_count")
education = []
for i in range(edu_count):
    with st.expander(f"Education {i+1}"):
        degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
        institution = st.text_input(f"Institution {i+1}", key=f"institution_{i}")
        start = st.text_input(f"Start Date {i+1}", key=f"edu_start_{i}")
        end = st.text_input(f"End Date {i+1}", key=f"edu_end_{i}")
        loc = st.text_input(f"Location {i+1}", key=f"edu_loc_{i}")
        details = st.text_input(f"Details {i+1}", key=f"edu_details_{i}")
        education.append({
            "degree": degree, "institution": institution, "start_date": start,
            "end_date": end, "location": loc, "details": details
        })

# Projects
st.sidebar.header("Projects")
proj_count = st.sidebar.number_input("Number of projects", min_value=0, max_value=10, value=1, step=1, key="proj_count")
projects = []
for i in range(proj_count):
    with st.expander(f"Project {i+1}"):
        pname = st.text_input(f"Project Name {i+1}", key=f"proj_name_{i}")
        plink = st.text_input(f"Project Link {i+1}", key=f"proj_link_{i}")
        pdesc = st.text_area(f"Description {i+1}", key=f"proj_desc_{i}")
        points = st.text_area(f"Highlights (one per line) {i+1}", key=f"proj_points_{i}")
        projects.append({
            "name": pname, "link": plink, "description": pdesc,
            "points": points.split("\n") if points else []
        })

# Skills
st.sidebar.header("Skills")
skills = []
skills_count = st.sidebar.number_input("Number of skill categories", min_value=0, max_value=10, value=1, step=1, key="skills_count")
for i in range(skills_count):
    main_skill = st.text_input(f"Main Skill {i+1}", key=f"skill_main_{i}")
    subs = st.text_input(f"Sub-skills (comma separated) {i+1}", key=f"skill_sub_{i}")
    if main_skill:
        if subs:
            skills.append(f"{main_skill}: {subs}")
        else:
            skills.append(main_skill)

# Strengths
st.sidebar.header("Strengths")
strengths_text = st.sidebar.text_area("Strengths (one per line)", key="strengths")
strengths = strengths_text.split("\n") if strengths_text else []

# Render HTML
tpl = Template(TEMPLATE)
data = {
    "name": name, "tagline": tagline, "email": email, "phone": phone,
    "location": location, "linkedin": linkedin, "github": github,
    "summary": summary, "experience": experience, "education": education,
    "projects": projects, "skills": skills, "strengths": strengths
}
html = tpl.render(css=CSS, **data)

st.header("📄 Resume Preview")
st.components.v1.html(html, height=1000, scrolling=True)

st.download_button("⬇️ Download HTML", html, file_name="resume.html")
