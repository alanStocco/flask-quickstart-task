import json
from markupsafe import escape
from collections import namedtuple
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask ,url_for ,request ,render_template ,abort, redirect, url_for ,make_response ,session ,flash

# Set the secret key to some random bytes. Keep this really secret!
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

## YT https://www.youtube.com/watch?v=Z1RJmh_OqeA&list=PLh-WlvZK_vMXfsR4DW0wpaEoujkgqNfea&index=1
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/todo/', methods=['POST', 'GET'])
def todo_index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo_index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo/')
    except:
        return 'There was a problem deleting that task'

""" Delete a todo item """
@app.route('/todo/delete/<int:id>')
def todo_delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/todo/')
    except:
        return 'There was a problem deleting that task'

""" Update a todo item """
@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/todo/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('todo_update.html', task=task)




def valid_login(username, password):
    return True

def log_the_user_in(username):
    return f'User {escape(username)} logged in successfully'

@app.route('/')
def index():
    # return 'Index Page'
    # if 'username' in session:
    #     return f'Logged in as {session["username"]}'
    # return 'You are not logged in'    
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return render_template('index.html', user=session.get('username'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
            # return log_the_user_in(request.form['username'])
        else:            
            error = 'Invalid username/password'
            
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# @app.route("/<name>")
# def hello(name):
#     return f"Hello, {escape(name)}!"

@app.route('/show_user_profile/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'
    
@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    url_for('static', filename='style.css')
    
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp    


User = namedtuple("User", ["username", "theme", "image"])

def get_current_user():
    return User(username="test", theme="black", image="default.png")


class User(namedtuple("User", ["username", "theme", "image"])):
    def to_json(self):
        return json.dumps({
            "username": self.username,
            "theme": self.theme,
            "image": self.image,
        })
        
def get_all_users():
    users = [
        User(username="user1", theme="black", image="default.png"),
        User(username="user2", theme="white", image="default.png"),
        User(username="user3", theme="black", image="default.png"),
    ]
    return users

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        # "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]