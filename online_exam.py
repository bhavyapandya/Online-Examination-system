from flask import *
import datetime
import sqlite3
app = Flask(__name__)
app.secret_key = 'some secret key'
@app.route('/')
def login():
    if 'eno' in session:
      return redirect(url_for('login_successfull'))
    return render_template("login.html")
@app.route('/login_successfull',methods=['GET','POST'])
def login_successfull():
   if request.method=='POST':
      con=sqlite3.connect('online_examination.db')
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute('select * from admins where eno=? AND password=? ',(request.form['eno'],request.form['pass']))
      row = cur.fetchone()
      if row == None:
         cur.execute('select * from student where eno=? AND password=? ', (request.form['eno'], request.form['pass']))
         row = cur.fetchone()
         if row == None :
            flash('invalid Enrollment number or password')
            return redirect(url_for('login'))
         else:
            session['eno'] = request.form['eno']
            cur.execute('select * from examination where department=?',(row['department'],))
            rows=cur.fetchall()
            return render_template("student_login.html", name=row['name'],rows=rows)
      else:
         session['eno'] = request.form['eno']
         return render_template("admin_login.html", name=row['eno'])
   if 'eno' in session:
      eno=session['eno']
      con = sqlite3.connect('online_examination.db')
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute('select * from student where eno=?', (eno,))
      row = cur.fetchone()
      if row==None:
         cur.execute('select * from admins where eno=?', (eno,))
         row = cur.fetchone()
         return render_template("admin_login.html", name=row['eno'])
      return render_template("student_login.html", name=row['name'])
   else:
      return redirect(url_for('login'))
@app.route('/register')
def register():
   try:
      with sqlite3.connect('online_examination.db') as con:
         con.row_factory = sqlite3.Row
         cur = con.cursor()
         cur.execute('select * from departments')
         rows = cur.fetchall()
   except:
      return "error"
   return render_template("registration.html",rows=rows)
@app.route('/registration_sucessfull',methods=['GET','POST'])
def reistration_successfull():
   if request.method=='POST':
      try:
         nm = request.form['username']
         eno = request.form['eno']
         dept = request.form['department']
         pin = request.form['pass']

         with sqlite3.connect('online_examination.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO student VALUES(?, ?, ?, ?)',(nm,eno,dept,pin))
            con.commit()
      except:
         return """Enter Enrollment number already exist if you have not contact owner"""
      name = request.form['username']
      return render_template("successfull_registration.html", name=name)
@app.route('/view_student',methods=['GET','POST'])
def view_student():
   if 'eno' in session:
      if request.method=='POST' or request.method=='GET':
         try:
            with sqlite3.connect('online_examination.db') as con:
               con.row_factory = sqlite3.Row
               cur = con.cursor()
               cur.execute('select * from student')
               rows = cur.fetchall()
         except:
            return "error"
         return render_template("view_student.html",rows=rows)
   else:
      return redirect(url_for('login'))
@app.route('/search_student',methods=['GET','POST'])
def search_student():
   if 'eno' in session:
      if request.method == 'POST' or request.method == 'GET':
         field=request.form['field']
         try:
            with sqlite3.connect('online_examination.db') as con:
               con.row_factory = sqlite3.Row
               cur = con.cursor()
               cur.execute('select * from student where eno=? OR name=? OR department=?',(field,field,field))
               rows = cur.fetchall()
         except:
            return "error"
         return render_template("view_student.html", rows=rows)
   else:
      return redirect(url_for('login'))
@app.route('/edit_student',methods=['GET','POST'])
def edit_student():
   if request.method == 'POST' or request.method == 'GET':
      eno=request.form['eno']
      name=request.form['name']
      department=request.form['department']
      password= request.form['password']
      with sqlite3.connect('online_examination.db') as con:
         con.row_factory = sqlite3.Row
         cur = con.cursor()
         cur.execute('update student set eno=?,name=?,department=?,password=? where eno=?', (eno, name, department,password,eno))
   return redirect(url_for('view_student'))
@app.route("/departments",methods=['GET','POST'])
def departments():
   if 'eno' in session:
      if request.method == 'POST' or request.method == 'GET':
         try:
            with sqlite3.connect('online_examination.db') as con:
               con.row_factory = sqlite3.Row
               cur = con.cursor()
               cur.execute('select * from departments')
               rows = cur.fetchall()
         except:
            return "error"
         return render_template("view_departments.html", rows=rows)
   else:
      return redirect(url_for('login'))
@app.route('/edit_department',methods=['GET','POST'])
def edit_department():
   if request.method == 'POST' or request.method == 'GET':
      button=request.form['edit']
      id=request.form['id']
      name=request.form['department']
      try:
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            if button == 'Edit':
               cur.execute('update departments set name=? where id=?',(name,id))
            else:
               cur.execute('delete from departments where id=?',(id))
      except:
         return 'error'
   return redirect(url_for('departments'))
@app.route('/add_department',methods=['GET','POST'])
def add_department():
   if request.method == 'POST' or request.method == 'GET':
      id=request.form['id']
      name=request.form['department']
      try:
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('insert into departments values(?,?)',(id,name))
      except:
         return redirect(url_for('departments'))
   return redirect(url_for('departments'))
@app.route("/logout",methods=['GET','POST'])
def logout():
   if request.method == 'POST' or request.method == 'GET':
      session.pop('eno',None)
      return redirect(url_for('login'))
@app.route("/examination",methods=['GET','POST'])
def examination():
   if 'eno' in session:
      if request.method == 'POST' or request.method=='GET':
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from examination')
            rows = cur.fetchall()
         return render_template("examination.html",rows=rows)
   else:
      return redirect(url_for('login'))
@app.route("/exam_paper",methods=['GET','POST'])
def exam_paper():
   if request.method == 'POST' or request.method == 'GET':
      date=request.form['date']
      id=request.form['id']
      name=request.form['subject_name']
      department=request.form['department']
      button=request.form['edit']
      s_time=request.form['start_time']
      e_time=request.form['end_time']
      with sqlite3.connect('online_examination.db') as con:
         con.row_factory = sqlite3.Row
         cur = con.cursor()
         if button=='view':
            cur.execute('select * from {}'.format(name))
            rows=cur.fetchall()
            return render_template("set_paper.html",rows=rows,name=name)
         elif button == 'Edit':
            cur.execute('update examination set subject_name=?,date_of_exam=?,department=?,start_time=?,end_time=? where id=?', (name,date,department,s_time,e_time,id))
         elif button=='Delete':
            query='''DROP TABLE {}'''.format(name)
            query1 = '''DROP TABLE {}student'''.format(name)
            query2 = '''DROP TABLE {}result'''.format(name)
            cur.execute('delete from examination where id=?', (id))
            cur.execute(query)
            cur.execute(query1)
            cur.execute(query2)
         else:
            pass
      return redirect(url_for('examination'))
@app.route("/add_examination",methods=['GET','POST'])
def add_examination():
   if request.method == 'POST' or request.method == 'GET':
      date=request.form['date']
      id=request.form['id']
      name=request.form['subject_name']
      department=request.form['department']
      s_time = request.form['start_time']
      e_time = request.form['end_time']
      query='''CREATE TABLE {}(sr_no NUMERIC,question TEXT NOT NULL,A TEXT NOT NULL,B TEXT NOT NULL,C TEXT NOT NULL,D TEXT NOT NULL,Ans TEXT NOT NULL,PRIMARY KEY("sr_no"))'''.format(name)
      query1='''CREATE TABLE {}student(eno TEXT NOT NULL)'''.format(name)
      query2='''CREATE TABLE {}result(eno TEXT NOT NULL,result NUMERIC,total Numeric)'''.format(name)
      with sqlite3.connect('online_examination.db') as con:
         con.row_factory = sqlite3.Row
         cur = con.cursor()
         cur.execute(query)
         cur.execute(query1)
         cur.execute(query2)
         cur.execute('insert into examination values (?,?,?,?,?,?)',(id,name,department,date,s_time,e_time))
      return redirect(url_for('examination'))
@app.route('/add_question',methods=['GET','POST'])
def add_question():
   if 'eno' in session:
      if request.method == 'POST' or request.method=='GET':
         name=request.form['name']
         sno=request.form["sr_no"]
         que=request.form['question']
         a=request.form['a']
         b = request.form['b']
         c = request.form['c']
         d = request.form['d']
         ans=request.form['ans']
         query='ALTER TABLE {}student ADD no{} TEXT'.format(name,sno)
         with sqlite3.connect('online_examination.db') as conn:
            conn.row_factory=sqlite3.Row
            curr=conn.cursor()
            curr.execute('insert into '+name+' values(?,?,?,?,?,?,?)',(sno,que,a,b,c,d,ans))
            curr.execute(query)
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from {}'.format(name))
            rows = cur.fetchall()
         return render_template("set_paper.html",rows=rows,name=name)
   else:
      return redirect(url_for('login'))
@app.route('/edit_paper',methods=['GET','POST'])
def edit_paper():
   if 'eno' in session:
      if request.method == 'POST' or request.method=='GET':
         name=request.form['name']
         sno=request.form["sr_no"]
         que=request.form['question']
         a=request.form['a']
         b = request.form['b']
         c = request.form['c']
         d = request.form['d']
         ans=request.form['ans']
         button=request.form['edit']
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            if button == 'Edit':
               cur.execute('update '+name+' set question=?,a=?,b=?,c=?,d=?,ans=? where sr_no=?',(que,a,b,c,d,ans,sno))
            else:
               pass
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from {}'.format(name))
            rows = cur.fetchall()
         return render_template("set_paper.html",rows=rows,name=name)
   else:
      return redirect(url_for('login'))

@app.route('/view_examinaton_or_result',methods=['GET','POST'])
def view_examinaton_or_result():
   if 'eno' in session:
      if request.method == 'POST' or request.method=='GET':
         datenow = datetime.datetime.now()
         id=request.form['id']
         subject=request.form['subject']
         with sqlite3.connect('online_examination.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute('select * from examination where id=?',(id))
            row = cur.fetchone()
         with sqlite3.connect('online_examination.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('select * from {}'.format(row['subject_name']))
            rows = cur.fetchall()
         with sqlite3.connect('online_examination.db') as connn:
            connn.row_factory = sqlite3.Row
            cur = connn.cursor()
            cur.execute('select * from {}student where eno=? '.format(row['subject_name']),(session['eno'],))
            ro = cur.fetchone()
         with sqlite3.connect('online_examination.db') as c:
            c.row_factory = sqlite3.Row
            cur = c.cursor()
            cur.execute("select * from {}result where eno=?".format(subject),(session['eno'],))
            r=cur.fetchone()
         if (ro is not None):
            return render_template('result.html',row=r)
         if datenow.strftime("%Y-%m-%d")==row['date_of_exam']:
            x = (int(datenow.strftime("%H-%M")[:2]) * 3600) + (int(datenow.strftime("%H-%M")[3:]) * 60)
            y = (int(row['start_time'][:2]) * 3600) + (int(row['start_time'][3:]) * 60)
            w = (int(row['end_time'][:2]) * 3600) + (int(row['end_time'][3:])) * 60
            if (x >= y) and (x <= w):
               z=(w-x)*1000
               return render_template("exam_paper.html",rows=rows,subject=request.form['subject'],timeout=z)
            else:
               return render_template('result.html',row=r)
         else:
            return datenow.strftime("%Y-%m-%d")#render_template('result.html',row=r)
   else:
      return redirect(url_for('login'))
@app.route('/setans',methods=['GET','POST'])
def setans():
   if 'eno' in session:
      if request.method == 'POST' or request.method=='GET':
         try:
            length=request.form["length"]
            subject=request.form['subject']
            ans=[]
            for i in range(1,int(length)):
               ans.append(request.form["{}".format(i)])
            with sqlite3.connect('online_examination.db') as con:
               con.row_factory = sqlite3.Row
               cur = con.cursor()
               cur.execute("insert into {}student(eno) values(?)".format(subject),(session['eno'],))
               for i in range(0,(int(length)-1)):
                  cur.execute("update "+subject+"student set no"+str(i+1)+"=? where eno=?",(ans[i],session['eno']))
               cur.execute('select * from '+subject+'student where eno=?',(session['eno'],))
               row=cur.fetchone()
            with sqlite3.connect('online_examination.db') as conn:
               conn.row_factory=sqlite3.Row
               curr =conn.cursor()
               curr.execute('select * from '+subject)
               rows=curr.fetchall()
               count=0
               i=1
               for ro in rows:
                  if(ro['Ans']==row['no'+str(i)]):
                     count=count+1
                  i = i + 1
               curr.execute('insert into '+subject+'result values(?,?,?)',(session['eno'],count,i-1))
            with sqlite3.connect('online_examination.db') as con:
               con.row_factory = sqlite3.Row
               cur = con.cursor()
               cur.execute("select * from {}result where eno=?".format(subject),(session['eno'],))
               row=cur.fetchone()
            return render_template('result.html',row=row)
         except:
            return redirect(url_for('login'))
      else:
         return redirect(url_for('login'))
if __name__ == '__main__':
   app.run(debug=True)