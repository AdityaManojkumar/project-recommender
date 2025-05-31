from flask import Flask, render_template, request, redirect, url_for, session
from app.data import project_map, company_map, subjects_list, skills_list

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with your secret key

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        collegeid = request.form.get('collegeid')

        # Accept any non-empty inputs as valid login
        if username and email and collegeid:
            session['user'] = username
            session['email'] = email
            session['collegeid'] = collegeid
            return redirect(url_for('main_page'))
        else:
            error = "Please fill all fields."
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        dob = request.form.get('dob')
        semester = request.form.get('semester')
        college = request.form.get('college')
        rollno = request.form.get('rollno')
        subjects = request.form.getlist('subjects')
        skills = request.form.getlist('skills')

        projects = []
        companies = []
        for skill in skills:
            projects.extend(project_map.get(skill, []))
            companies.extend(company_map.get(skill, []))

        projects = sorted(set(projects))
        companies = sorted(set(companies))

        return render_template('recommendations.html',
                               fullname=fullname,
                               dob=dob,
                               semester=semester,
                               college=college,
                               rollno=rollno,
                               subjects=subjects,
                               skills=skills,
                               projects=projects,
                               companies=companies,
                               user=session['user'],
                               email=session['email'],
                               collegeid=session['collegeid'])

    return render_template('main.html', subjects=subjects_list, skills=skills_list,
                           user=session['user'], email=session['email'], collegeid=session['collegeid'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
