from flask import Flask, render_template, request, redirect, url_for, session, make_response
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
        'joined_classes': []
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
                'description': 'Prepare a presentation about BioTechnology'
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
                'description': 'Prepare a presentation about Covalent Bonds'
            }
        ]
    },
    {
        'id':'333',
        'classcode':'3333',
        'name':'Physics',
        'instructor':'Isac Newton',
        'members': [],
        'assignments':[]
    }

]



@app.route('/users')
def userss():
    return [users, classes]

#====================== Signup/Login form =============================

@app.route('/form', methods=['GET', 'POST'])
def form():
    print('its hosted on ')
    print(request.host)
    status_pass = ''
    status_user = ''
    if request.method == 'POST':

        if request.form['submit'] == 'Login':
            for user in users:
                if user['username'] == request.form['username'] and user['password'] == request.form['password']:
                    session['logged_user'] = user
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
            
            user_id = str(uuid.uuid4())
            user['id'] = user_id

            users.append(user)
            session['logged_user'] = user
            return redirect('/home')
    else:
        return render_template('index.html', status_pass=status_pass)

# ====================== End Signup/login form ===================================

# ====================== Home Page ===================================

@app.route('/home')
def home():
    logged_user = session['logged_user']
    if logged_user:
        return render_template('dashboard/homepage.html', user=logged_user)
    else:
        return redirect('/form')

# ======= Join Class ======
@app.route('/home/join', methods=['POST', 'GET'])
def joinclass():
    print('request recived')
    if request.method == 'POST':
        logged_user = session['logged_user']
        code = request.form['classCodee']
        for c in classes:
            if c['classcode'] == code:
                for user in users:
                    if logged_user['id'] == user['id']:
                        if c not in user['joined_classes']:
                            user['joined_classes'].append(c)
                            c['members'].append(user['id'])
                        session['logged_user'] = user
                        return redirect('/home')
            
        return redirect('/home')


# ======= End Join Class ==

# ====================== End Home Page ===============================

# ============ Todo Page ===========================

@app.route('/todos', methods=['GET', 'POST'])
def todo():
    logged_user = session['logged_user']
    if request.method == 'GET':
        if logged_user:
            return render_template('todo/todo.html', user=logged_user)
        else:
            return redirect('/form')
    elif request.method == 'POST':
        added_todo = request.form['title']
        for user in users:
            if user == logged_user:
                user['todos'].insert(0, {'title': added_todo, 'completed': 'false'})
                session['logged_user'] = user
                return redirect('/todos')

@app.route('/delete/<int:title_index>')
def todo_delete(title_index):
    logged_user = session['logged_user']
    index = users.index(logged_user)
    users[index]['todos'].remove(users[index]['todos'][title_index])
    session['logged_user'] = users[index]
    return redirect('/todos')

@app.route('/todo_status/<int:title_index>/<stat>', methods=['POST'])
def todo_status(title_index, stat):
    logged_user = session['logged_user']
    index = users.index(logged_user)
    users[index]['todos'][title_index]['completed'] = stat;session
    session['logged_user'] = users[index]
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
    logged_user = session['logged_user']
    if request.method == 'GET':
            for c in classes:
                if c['id'] == class_id:
                    return render_template('/class_room/class_room.html', user=logged_user, classroom=c)
    # ------------Chat room ------

    # ------------end chatroom ---
    

# ================== End Class room ===============================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
