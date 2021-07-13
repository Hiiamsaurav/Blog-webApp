from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Todo(db.Model):
    uid =db.Column(db.Integer,primary_key=True)
    PostTitle =db.Column(db.String(200),nullable=False)
    PostAContent=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.Date,default=datetime.utcnow)
    def _repr_(self) ->str:
        return f"{self.sno} - {self.PostTitle}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        PostTitle=request.form['PostTitle']  
        PostAContent=request.form['PostAContent']

        # print(request.form['title'])
        todo = Todo(PostTitle=PostTitle ,PostAContent=PostAContent)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
# @app.route('/products')

# def products():
#     allTodo=Todo.query.all()
#     # print(allTodo)

#     return 'this is my project'

@app.route('/update/<int:uid>',methods=['GET','POST'])
def update(uid):
    if request.method =='POST':
       PostTitle=request.form['PostTitle']
       PostAContent=request.form['PostAContent']
       todo=Todo.query.filter_by(uid=uid).first()
       todo.PostTitle=PostTitle
       todo.PostAContent=PostAContent
       
       db.session.add(todo)
       db.session.commit()
       return redirect("/")

    
    todo=Todo.query.filter_by(uid=uid).first()
    return render_template('update.html',todo=todo)
    

#     return 'this is my project'

@app.route('/delete/<int:uid>')
def delete(uid):
    todo=Todo.query.filter_by(uid=uid).first()
    db.session.delete(todo)
    db.session.commit()

    # print(allTodo)

    return redirect('/')

if(__name__ =="__main__"):
    app.run(debug=True,port=8000)