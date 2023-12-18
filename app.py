from flask import Flask, g, render_template, request, redirect, url_for, session, make_response
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = '123robel123robel789'

users = [
    {
        'id':'1',
        'name':'Robel Wondimu',
        'username':'robel',
        'email':'robpalus75@gmail.com',
        'password':'123',
        'todos':[
                {'title':'Do Biology HomeWork', 'completed':'false'},
                {'title':'Do you Project', 'completed':'true'}
        ],
        'joined_classes': [],
        'occupation':'student',
        'notifications': []
    },
    {
        'id':'2',
        'name':'Inst Solomon Wondimu',
        'username':'sele',
        'email':'seleminds75@gmail.com',
        'password':'123',
        'todos':[
                {'title':'Give assignments to class B', 'completed':'false'},
                {'title':'Give them exams to class D', 'completed':'true'}
        ],
        'joined_classes': [],
        'occupation':'teacher',
        'notifications': []
    }
]

classes = [
    {
        'id':'111',
        'classcode':'1111',
        'name':'Biology',
        'instructor':'Dr. Yosef Abera',
        'members': [],
        'assignments': [
            {
                'title': 'BioTechnology',
                'description': 'Prepare a presentation about BioTechnology',
                'date': 'christmass eve'
            }
        ],
        'exams': [
            {
                'title': 'Genetics',
                'description': 'Contains multiple choices ...',
                'date': '2 January 2024'
            }
        ]
    },
    {
        'id':'222',
        'classcode':'2222',
        'name':'Chemistry',
        'instructor':'Albert Eienstien',
        'members': [],
        'assignments':[
            {
                'title': 'Covalent Bonds',
                'description': 'Prepare a presentation about Covalent Bonds',
                'date': 'for the last day'
            }
        ],
        'exams': [
            {
                'title': 'Ionic Bonds',
                'description': 'Contains multiple choices and workout...',
                'date': '12 January 2024'
            }
        ]
    },
    {
        'id':'333',
        'classcode':'3333',
        'name':'Physics',
        'instructor':'Isac Newton',
        'members': [],
        'assignments': [],
        'exams': []
    }

]

import random
import string

def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_uppercase, k=6))
    return random_string


@app.before_request
def before_request():
    g.logged_user = None
    if 'logged_user' in session:
        g.logged_user = session['logged_user']
    print(f"logged user is {g.logged_user}")

@app.route('/users')
def userss():
    return [users, classes]

#====================== Signup/Login form =============================

@app.route('/')
def landingpage():
    return redirect('/form')


@app.route('/form', methods=['GET', 'POST'])
def form():
    status_pass = ''
    status_user = ''
    session.pop('logged_user', None)
    if request.method == 'POST':

        if request.form['submit'] == 'Login':
            session.pop('logged_user', None)
            for user in users:
                if user['username'] == request.form['username'] and user['password'] == request.form['password']:
                    session['logged_user'] = user['id']
                    return redirect('/home')
            status_pass = """
             <div style="color:red;">
                  Username or Password is not Correct
            </div>
            """
            return render_template('index.html', status_pass=status_pass)
        elif request.form['submit'] == 'Signup':
            for user in users:
                if user['username'] == request.form['username']:
                    status_user = """
                    <center><div style="color:red;padding:15px;border:1px solid red;width:300px;display:flex;justify-content:center;align-items:center;">
                         Username Already exists
                    </div></center>
                    """
                    return render_template('index.html', status_user=status_user)

            user = request.form.to_dict()
            user.pop('submit')
            user['todos'] = []
            user['joined_classes'] = []
            user['notifications'] = []
            user['occupation'] = request.form['occupation']   
            if (user['occupation'] == 'teacher'):
                user['name'] = f"Inst {user['name']}"         
            
            user_id = str(uuid.uuid4())
            user['id'] = user_id

            users.append(user)
            session['logged_user'] = user['id']
            return redirect('/home')
    else:
        return render_template('index.html', status_pass=status_pass)

# ====================== End Signup/login form ===================================

# ====================== Home Page ===================================

@app.route('/home')
def home():
    if not g.logged_user:
        return redirect('/form')
    logged_user = None
    for user in users:
        if session['logged_user'] == user['id']:
            logged_user = user
    if logged_user:
        return render_template('dashboard/homepage.html', user=logged_user, classes=classes)
    else:
        return redirect('/form')

# ======= Join Class ======
@app.route('/home/join', methods=['POST', 'GET'])
def joinclass():
    if not g.logged_user:
        return redirect('/form')
    if request.method == 'POST':
        code = request.form['classCodee']
        for c in classes:
            if c['classcode'] == code:
                for user in users:
                    if session['logged_user'] == user['id']:
                        if c['id'] not in user['joined_classes']:
                            user['joined_classes'].append(c['id'])
                            c['members'].append(user['id'])
                        return redirect('/home')
            
        return redirect('/home')

# ======= End Join Class ==
# ======= Create Class ====
@app.route('/home/create', methods=['POST'])
def createclass():
    logged_user_id = session['logged_user']
    class_name = request.form['class_name']
    inst_username = request.form['inst_username']
    for user in users:
        if user['username'] == inst_username:
            class_id = str(uuid.uuid4())
            new_class = {
            'id': class_id,
            'classcode':generate_random_string(),
            'name':class_name,
            'instructor': user['name'],
            'members': [logged_user_id],
            'assignments': [],
            'exams': []
            }
            for u in users:
                if (u['id'] == logged_user_id):
                    u['joined_classes'].append(new_class['id'])
            classes.append(new_class)
            if new_class['id'] not in user['joined_classes']:
                user['joined_classes'].append(new_class['id'])
            print('class created successfully')
            return redirect('/home')
    return redirect('/home')


# ======= End Create Class ======

# ====================== End Home Page ===============================

# ============ Todo Page ===========================

@app.route('/todos', methods=['GET', 'POST'])
def todo():
    if not g.logged_user:
        return redirect('/form')
    logged_user_id = session['logged_user']
    logged_user = None
    for user in users:
        if user['id'] == logged_user_id:
            logged_user = user
    if request.method == 'GET':
        if logged_user:
            return render_template('todo/todo.html', user=logged_user)
        else:
            return redirect('/form')
    elif request.method == 'POST':
        added_todo = request.form['title']
        for user in users:
            if user['id'] == logged_user_id:
                user['todos'].insert(0, {'title': added_todo, 'completed': 'false'})
                return redirect('/todos')

@app.route('/delete/<todo_title>')
def todo_delete(todo_title):
    logged_user_id = session['logged_user']
    logged_user = None
    for user in users:
        if user['id'] == logged_user_id:
            logged_user = user
            for todo in user['todos']:
                if todo['title'] == todo_title:
                    user['todos'].remove(todo)
    return redirect('/todos')

@app.route('/todo_status/<int:title_index>/<stat>', methods=['POST'])
def todo_status(title_index, stat):
    logged_user_id = session['logged_user']
    logged_user = None
    for user in users:
        if user['id'] == logged_user_id:
            logged_user = user
    index = users.index(logged_user)
    users[index]['todos'][title_index]['completed'] = stat;session
    response = make_response()
    response.status_code = 200
    return response

# ==================== TodoPage end ===============================

# ==================== GPA Calculator ============================

@app.route('/gpa_calculator')
def calculator():
    logged_user = session['logged_user']
    return render_template('/gpa_calculator/gpa_calculator.html', user=logged_user)

# ==================== End GPA Calculator ========================

# ================== Class room ===================================
@app.route('/class/<class_id>')
def class_room(class_id):
    if not g.logged_user:
        return redirect('/form')
    for user in users:
        if user['id'] == session['logged_user']:
            logged_user = user
    if request.method == 'GET':
            for c in classes:
                if c['id'] == class_id:
                    return render_template('/class_room/class_room.html', user=logged_user, classroom=c)

# ------------exambox------

@app.route('/class/add_exam/<class_id>', methods=['POST'])
def addexam(class_id):
    for c in classes:
        if c['id'] == class_id:
            new_exam = {
                        'title': request.form.get('add_exam_title'),
                        'description': request.form.get('add_exam_description'),
                        'date': request.form.get('add_exam_date')
                        }
            c['exams'].append(new_exam)
            for member in c['members']:
                for user in users:
                    if user['id'] == member:
                        notification = {
                            'class_id': c['id'],
                            'name': c['name'],
                            'type': 'Exam'
                        }
                        user['notifications'].append(notification)
            return redirect(f'/class/{class_id}')

# ------------end exambox ---

# ------------assignmentbox------

@app.route('/class/add_assignment/<class_id>', methods=['POST'])
def addassignment(class_id):
    for c in classes:
        if c['id'] == class_id:
            new_assignment = {
                        'title': request.form.get('add_exam_title'),
                        'description': request.form.get('add_exam_description'),
                        'date': request.form.get('add_exam_date')
                    }
            c['assignments'].append(new_assignment)
            for member in c['members']:
                for user in users:
                    if user['id'] == member:
                        notification = {
                            'class_id': c['id'],
                            'name': c['name'],
                            'type': 'Assignment'
                        }
                        user['notifications'].append(notification)
            return redirect(f'/class/{class_id}')

# ------------end exambox ---
    

# ================== End Class room ===============================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
