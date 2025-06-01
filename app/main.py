from flask import Flask, render_template, request
from prometheus_client import Counter, Histogram, generate_latest
import time

from .data import project_map, company_map, subjects_list, skills_list

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('app_request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.path).inc()
    REQUEST_LATENCY.labels(request.path).observe(request_latency)
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/')
def login():
    return render_template('login.html')  # keep your original login page

@app.route('/home', methods=['POST'])
def index():
    name = request.form['name']
    dob = request.form['dob']
    semester = request.form['semester']
    selected_subjects = request.form.getlist('subjects')
    selected_skills = request.form.getlist('skills')

    recommended_projects = set()
    recommended_companies = set()

    for skill in selected_skills:
        recommended_projects.update(project_map.get(skill, []))
        recommended_companies.update(company_map.get(skill, []))

    return render_template('main.html',
                           name=name,
                           dob=dob,
                           semester=semester,
                           selected_subjects=selected_subjects,
                           selected_skills=selected_skills,
                           recommended_projects=recommended_projects,
                           recommended_companies=recommended_companies)

if __name__ == '__main__':
    app.run(debug=True)
