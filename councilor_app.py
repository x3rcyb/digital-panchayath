from flask import  *
from DBConnection import *

app = Flask(__name__)
db=Db()
app.secret_key="abc"

@app.route('/admin_home')
def admin_home():
    if session['log']=="lin":
        return render_template("admin/admin_index.html")
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/')
def login():
    return render_template("login_index.html")

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login` WHERE `uname`='"+username+"'AND`password`='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['login_id']
        session['log']="lin"
        if res['type']=='admin':
            return redirect('admin_home')
        elif res['type']=='mayor':
            return redirect('president_home')
        elif res['type']=='councilor':
            return redirect('councilor_home')
        elif res['type']=='department':
            return redirect('dept_home')
        elif res['type']=='clerk':
            return redirect('clerk_home')
        else:
            return '''<script>alert("invalid");window.location='/'</script>'''
    else:
        return '''<script>alert("not found");window.location='/'</script>'''

@app.route('/logout')
def logout():
    session['log']=""
    return redirect('/')


@app.route('/add_area')
def add_area():
    if session['log']=="lin":
        return render_template("admin/add_area.html")
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''



@app.route('/add_area_post',methods=['post'])
def add_area_post():
    if session['log'] == "lin":
        db=Db()
        areaname=request.form['textfield']
        qry="INSERT INTO `area`(`area_name`)VALUE('"+areaname+"')"
        res=db.insert(qry)
        return '''<script>alert("success");window.location='/add_area'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_area')
def view_area():
    db=Db()
    qry="SELECT * FROM `area`"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_area.html",data=res)
    else:
        return '''<script>alert('yoy are logout');window.location='/'</script>'''

@app.route('/view_search_area_post',methods=['post'])
def view_search_area_post():
    if session['log']=="lin":

        db=Db()
        search=request.form['search']
        qry="SELECT * FROM `area` WHERE area_name LIKE '%"+search+"%'"
        res=db.select(qry)
        if session['log']=="lin":
            return render_template("admin/view_area.html",data=res)
        else:
            return '''<script>alert('yoy are logout');window.location='/'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/delete_area/<id>')
def delete_area(id):
    if session['log']=="lin":
        db = Db()
        qry = "DELETE FROM `area`WHERE`area_id`='" + id + "'"
        res = db.delete(qry)
        return redirect('/view_area')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''




@app.route('/edit_area/<id>')
def edit_area(id):
    db=Db()
    qry="SELECT * FROM `area` WHERE `area_id`='"+id+"'"
    res=db.selectOne(qry)
    if session['log']=="lin":
        return render_template("admin/edit_area.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_area_post',methods=['post'])
def edit_area_post():
    if session['log'] == "lin":
        area_id=request.form['area_id']
        areaname=request.form['textfield']
        db=Db()
        qry="UPDATE `area` SET `area_name`='"+areaname+"' WHERE `area_id`='"+area_id+"'"
        res=db.update(qry)
        return redirect('/view_area')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''



@app.route('/add_clerk')
def add_clerk():
    if session['log']=="lin":

        db=Db()
        qry="select * from department"
        res=db.select(qry)
        return render_template("admin/add_clerk.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_clerk_post',methods=['post'])
def add_clerk_post():
    if session['log']=="lin":

        db = Db()
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        hname = request.form['textfield3']
        place = request.form['textfield4']
        city = request.form['textfield5']
        district = request.form['textfield6']
        pincode = request.form['textfield7']
        email = request.form['textfield8']
        phone = request.form['textfield9']
        department=request.form['select']
        from datetime import datetime
        photo = request.files['fileField']
        date=datetime.now().strftime('%Y%m%d-%H%M%S')
        photo.save("C:\\final\\prj\\web\\councilor_app\\static\\clerk_pic\\"+date+".jpg")
        path="/static/clerk_pic/"+date+".jpg"
        qry = "INSERT INTO `login`(`uname`,`password`,`type`)VALUES('" + email + "','" + phone + "','clerk')"
        res = db.insert(qry)

        qry1 = "INSERT INTO `clerk`(`c_name`,`gender`,`dob`,`photo`,`house_name`,`place`,`city`,`district`,`pincode`,`email`,`phone`,`lid`,`dept_id`) VALUES('" +name +"','" +gender +"','" +dob +"','" +str(path) +"','" +hname +"','" +place +"','" +city +"','" +district +"','" +pincode +"','" +email +"','"+phone+"','" +str(res) +"','" +str(department)+"')"
        res1 = db.insert(qry1)
        print(qry1)
        return '''<script>alert("success");window.location='/add_clerk'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_clerk')
def view_clerk():
    if session['log'] == "lin":
        db=Db()
        qry="SELECT * FROM `clerk` JOIN`department`ON`clerk`.`dept_id`=`department`.`dept_id`"
        res=db.select(qry)
        return render_template("admin/view_clerk.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_search_clerk_post',methods=['post'])
def view_search_clerk_post():
    if session['log'] == "lin":

        db = Db()
        search=request.form['search']
        qry = "SELECT * FROM `clerk` JOIN`department`ON`clerk`.`dept_id`=`department`.`dept_id` WHERE c_name LIKE '%"+search+"%'"
        res = db.select(qry)
        return render_template("admin/view_clerk.html", data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''



@app.route('/delete_clerk/<id>')
def delete_clerk(id):
    if session['log'] == "lin":
        db=Db()
        qry="DELETE FROM `clerk` WHERE `clerk_id`='"+id+"'"
        res=db.delete(qry)

        return redirect('/view_clerk')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_clerk/<id>')
def edit_clerk(id):
    if session['log']=="lin":

        db=Db()
        qry="SELECT * FROM `clerk` WHERE `clerk_id`='"+id+"'"
        res=db.selectOne(qry)
        qry2="SELECT * FROM `department`"
        res2=db.select(qry2)
        return render_template("admin/edit_clerk.html",data=res,data2=res2)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_clerk_post',methods=['post'])
def edit_clerk_post():
    if session['log']=="lin":

        db=Db()
        clerk_id=request.form['clerk_id']
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        hname = request.form['textfield3']
        place = request.form['textfield4']
        city = request.form['textfield5']
        district = request.form['textfield6']
        pincode = request.form['textfield7']
        email = request.form['textfield8']
        phone = request.form['textfield9']
        department = request.form['select']
        if 'fileField' in request.files:
            photo = request.files['fileField']
            if photo.filename!="":
                from datetime import datetime
                date = datetime.now().strftime('%Y%m%d-%H%M%S')
                photo.save("C:\\final\\prj\\web\\councilor_app\\static\\clerk_pic\\" + date + ".jpg")
                path = "/static/clerk_pic/" + date + ".jpg"
                qry = "UPDATE `clerk`SET`c_name`='"+name+"',`gender`='"+gender+"',`dob`='"+dob+"',`photo`='"+path+"',`house_name`='"+hname+"',`place`='"+place+"',`city`='"+city+"',`district`='"+district+"',`pincode`='"+pincode+"',`email`='"+email+"',`phone`='"+phone+"',dept_id='"+department+"' where clerk_id='"+clerk_id+"'"
                res = db.update(qry)
                return redirect('/view_clerk')
            else:
                qry = "UPDATE `clerk`SET`c_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "' ,dept_id='"+department+"'where clerk_id='" + clerk_id + "'"
                res = db.update(qry)
                return redirect('/view_clerk')
        else:
            qry = "UPDATE `clerk`SET`c_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',dept_id='"+department+"' where clerk_id='" + clerk_id + "'"
            res = db.update(qry)
            return redirect('/view_clerk')

    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_corporation')
def add_corporation():
    if session['log']=="lin":
        return render_template("admin/add_corporation_about.html")
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_corporation_post',methods=['post'])
def add_corporation_post():
    if session['log']=="lin":

        corporation_name=request.form['textfield']
        district=request.form['textfield2']
        state=request.form['textfield3']
        email=request.form['textfield4']
        phone=request.form['textfield5']
        about=request.form['textarea']
        from datetime import datetime
        photo = request.files['fileField']
        date = datetime.now().strftime('%Y%m%d-%H%M%S')
        photo.save("C:\\final\\prj\\web\\councilor_app\\static\\corportn_pic\\" + date + ".jpg")
        path = "/static/corportn_pic/" + date + ".jpg"
        db = Db()
        qry="INSERT INTO `co-orperation_about`(`corporation_name`,`district`,`state`,`email`,`phone`,`photo`,`about`)VALUES('"+corporation_name+"','"+district+"','"+state+"','"+email+"','"+phone+"','"+path+"','"+about+"')"
        res=db.insert(qry)
        return '''<script>alert("success");window.location='/add_corporation'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_corporation')
def view_corporation():
    if session['log']=="lin":

        db=Db()
        qry="SELECT * FROM `co-orperation_about`"
        res=db.select(qry)
        if session['log']=="lin":
            return render_template("admin/view_corporation.html",data=res)
        else:
            return '''<script>alert('yoy are logout);window.location='/'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_corporation_search_post',methods=['post'])
def view_corporation_post():
    if session['log']=="lin":
        db=Db()
        name=request.form['search']
        qry="SELECT * FROM `co-orperation_about` WHERE corporation_name LIKE '%"+name+"%'"
        res=db.select(qry)
        return render_template("admin/view_corporation.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/update_corporation/<id>')
def update_corporation(id):
    db=Db()
    qry="SELECT * FROM `co-orperation_about` WHERE `about_id`='"+id+"'"
    res=db.selectOne(qry)
    if session['log']=="lin":
        return render_template("admin/update_corporation.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/update_corporation_post',methods=['post'])
def update_corporation_post():
    if session['log'] == "lin":
        about_id=request.form['about_id']
        corporation_name = request.form['textfield']
        district = request.form['textfield2']
        state = request.form['textfield3']
        email = request.form['textfield4']
        phone = request.form['textfield5']
        about = request.form['textarea']
        if 'fileField' in request.files:
            photo = request.files['fileField']
            if photo.filename!="":
                from datetime import datetime
                date = datetime.now().strftime('%Y%m%d-%H%M%S')
                photo.save("C:\\final\\prj\\web\\councilor_app\\static\\corportn_pic\\" + date + ".jpg")
                path = "/static/corportn_pic/" + date + ".jpg"
                db = Db()
                qry="UPDATE `co-orperation_about` SET `corporation_name`='"+corporation_name+"',`district`='"+district+"',`state`='"+state+"',`email`='"+email+"',`phone`='"+phone+"',`photo`='"+path+"',`about`='"+about+"' WHERE `about_id`='"+about_id+"'"
                res=db.update(qry)
                return redirect('/view_corporation')
            else:
                db = Db()
                qry = "UPDATE `co-orperation_about` SET `corporation_name`='" + corporation_name + "',`district`='" + district + "',`state`='" + state + "',`email`='" + email + "',`phone`='" + phone + "',`about`='" + about + "' WHERE `about_id`='" + about_id + "'"
                res = db.update(qry)
                return redirect('/view_corporation')
        else:
            db = Db()
            qry = "UPDATE `co-orperation_about` SET `corporation_name`='" + corporation_name + "',`district`='" + district + "',`state`='" + state + "',`email`='" + email + "',`phone`='" + phone + "',`about`='" + about + "' WHERE `about_id`='" + about_id + "'"
            res = db.update(qry)
            return redirect('/view_corporation')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_councilor')
def add_councilor():
    if session['log'] == "lin":
        db=Db()
        qry="select * from area"
        res=db.select(qry)
        return render_template("admin/add_councilor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_councilor_post',methods=['post'])
def add_councilor_post():
    if session['log'] == "lin":

        name=request.form['textfield']
        gender=request.form['RadioGroup1']
        dob=request.form['textfield2']
        photo=request.files['fileField']
        hname=request.form['textfield3']
        place=request.form['textfield4']
        city=request.form['textfield5']
        district=request.form['textfield6']
        pincode=request.form['textfield7']
        email=request.form['textfield8']
        phone=request.form['textfield9']
        yrfrom=request.form['textfield10']
        yrto=request.form['textfield11']
        area=request.form['select']
        db=Db()
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S')
        photo.save("C:\\final\\prj\\web\\councilor_app\\static\\counc_pic\\" + date + ".jpg")
        path = "/static/counc_pic/" + date + ".jpg"
        qry = "INSERT INTO `login`(`uname`,`password`,`type`)VALUES('" + email + "','" + phone + "','councilor')"
        res = db.insert(qry)
        qry2="INSERT INTO `councilor`(`coun_name`,`gender`,`dob`,`photo`,`house_name`,`place`,`city`,`district`,`pincode`,`email`,`phone`,`year_from`,`year_to`,`lid`,`area_id`)VALUES('"+name+"','"+gender+"','"+dob+"','"+str(path)+"','"+hname+"','"+place+"','"+city+"','"+district+"','"+pincode+"','"+email+"','"+phone+"','"+yrfrom+"','"+yrto+"','"+str(res)+"','"+area+"')"
        res2=db.insert(qry2)
        return '''<script>alert("success");window.location='/add_councilor'</script>'''
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_councilor')
def view_councilor():
    if session['log'] == "lin":
        db=Db()
        qry="SELECT * FROM `councilor` JOIN `area`ON `councilor`.`area_id`=`area`.`area_id`"
        res=db.select(qry)
        return render_template("admin/view_councilor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_search_councilor_post',methods=['post'])
def view_councilor_post():
    if session['log']=="lin":
        db=Db()
        name=request.form['search']
        qry="SELECT * FROM `councilor` JOIN `area`ON `councilor`.`area_id`=`area`.`area_id` WHERE coun_name LIKE '%"+name+"%'"
        res=db.select(qry)
        return render_template("admin/view_councilor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/delete_councilor/<id>')
def delete_councilor(id):
    if session['log'] == "lin":
        db=Db()
        qry="delete from councilor WHERE councilor_id='"+id+"'"
        res=db.delete(qry)
        return redirect('/view_councilor')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_councilor/<id>')
def edit_councilor(id):
    if session['log'] == "lin":
        db=Db()
        qry="SELECT * FROM `councilor`WHERE`councilor_id`='"+id+"'"
        res=db.selectOne(qry)
        qry2="select * from area where area_id='"+id+"'"
        res2=db.select(qry2)
        return render_template("admin/edit_councilor.html",data=res,data2=res2)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_councilor_post',methods=['post'])
def edit_councilor_post():
    councilor_id=request.form['councilor_id']
    name = request.form['textfield']
    gender = request.form['RadioGroup1']
    dob = request.form['textfield2']
    hname = request.form['textfield3']
    place = request.form['textfield4']
    city = request.form['textfield5']
    district = request.form['textfield6']
    pincode = request.form['textfield7']
    email = request.form['textfield8']
    phone = request.form['textfield9']
    yrfrom = request.form['textfield10']
    yrto = request.form['textfield11']
    area = request.form['select']
    if 'fileField' in request.files:
        photo = request.files['fileField']
        if photo.filename!="":
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S')
            photo.save("C:\\final\\prj\\web\\councilor_app\\static\\counc_pic\\" + date + ".jpg")
            path = "/static/counc_pic/" + date + ".jpg"
            db=Db()
            qry="UPDATE `councilor`SET `coun_name`='"+name+"',`gender`='"+gender+"',`dob`='"+dob+"',`photo`='"+path+"',`house_name`='"+hname+"',`place`='"+place+"',`city`='"+city+"',`district`='"+district+"',`pincode`='"+pincode+"',`email`='"+email+"',`phone`='"+phone+"',`year_from`='"+yrfrom+"',`year_to`='"+yrto+"' WHERE `councilor_id`='"+councilor_id+"'"
            res=db.update(qry)
            return redirect('/view_councilor')
        else:
            db = Db()
            qry = "UPDATE `councilor`SET `coun_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',`year_from`='" + yrfrom + "',`year_to`='" + yrto + "' WHERE `councilor_id`='" + councilor_id + "'"
            res = db.update(qry)
            return redirect('/view_councilor')
    else:
        db = Db()
        qry = "UPDATE `councilor`SET `coun_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',`year_from`='" + yrfrom + "',`year_to`='" + yrto + "' WHERE `councilor_id`='" + councilor_id + "'"
        res = db.update(qry)
        return redirect('/view_councilor')



@app.route('/add_dept')
def add_dept():
    if session['log']=="lin":
        return render_template("admin/add_department.html")
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_dept_post',methods=['post'])
def add_dept_post():
    db=Db()
    deptname=request.form['textfield']
    headname=request.form['textfield2']
    email=request.form['textfield3']
    phone=request.form['textfield4']
    qry2="INSERT INTO `login`(`uname`,`password`,`type`)VALUE('"+email+"','"+phone+"','department')"
    res=db.insert(qry2)
    qry="INSERT INTO `department`(`dept_name`,`dept_head_name`,`dept_email`,`dept_phone`,deplid)VALUES('"+deptname+"','"+headname+"','"+email+"','"+phone+"','"+str(res)+"')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/add_dept'</script>'''

@app.route('/view_dept')
def view_dept():
    db=Db()
    qry="SELECT * FROM `department`"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_dept.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_dept_search_post',methods=['post'])
def view_dept_post():
    db=Db()
    name=request.form['search']
    qry="SELECT * FROM `department` WHERE dept_name LIKE '%"+name+"%'"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_dept.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/delete_dept/<id>')
def delete_dept(id):
    db=Db()
    qry="DELETE FROM `department` WHERE`dept_id`='"+id+"'"
    res=db.delete(qry)
    if session['log']=="lin":
        return redirect('/view_dept')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_dept/<id>')
def edit_dept(id):
    db=Db()
    qry="SELECT * FROM `department`WHERE`dept_id`='"+id+"'"
    res=db.selectOne(qry)
    if session['log']=="lin":
        return render_template("admin/edit_dept.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_dept_post',methods=['post'])
def edit_dept_post():
    db = Db()
    dept_id=request.form['dept_id']
    deptname = request.form['textfield']
    headname = request.form['textfield2']
    email = request.form['textfield3']
    phone = request.form['textfield4']
    qry="UPDATE `department` SET `dept_name`='"+deptname+"',`dept_head_name`='"+headname+"',`dept_email`='"+email+"',`dept_phone`='"+phone+"' WHERE `dept_id`='"+dept_id+"'"
    res=db.update(qry)
    return redirect('/view_dept')


@app.route('/add_mayor')
def add_mayor():
    if session['log']=="lin":
        return render_template("admin/add_mayor.html")
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/add_mayor_post',methods=['post'])
def add_mayor_post():
    db=Db()
    name = request.form['textfield']
    gender = request.form['RadioGroup1']
    dob = request.form['textfield2']
    hname = request.form['textfield3']
    place = request.form['textfield4']
    city = request.form['textfield5']
    district = request.form['textfield6']
    pincode = request.form['textfield7']
    email = request.form['textfield8']
    phone = request.form['textfield9']
    yrfrom=request.form['textfield10']
    yrto=request.form['textfield11']
    from datetime import datetime
    photo = request.files['fileField']
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    photo.save("C:\\final\\prj\\web\\councilor_app\\static\\mayor_pic\\" + date + ".jpg")
    path = "/static/mayor_pic/" + date + ".jpg"
    qry = "INSERT INTO `login`(`uname`,`password`,`type`)VALUES('" + email + "','" + phone + "','mayor')"
    res = db.insert(qry)
    qry1 = "INSERT INTO `president`(`p_name`,`gender`,`dob`,`photo`,`houseno_name`,`place`,`city`,`district`,`pincode`,`email`,`phone`,`year_from`,`year_to`,`lid`)VALUES('" + name + "','" + gender + "','" + dob + "','" + str(path) + "','" + hname + "','" + place + "','" + city + "','" + district + "','" + pincode + "','" + email + "','" + phone + "','"+yrfrom+"','"+yrto+"','" + str(res) + "')"
    res1 = db.insert(qry1)
    return '''<script>alert("success");window.location='/add_mayor'</script>'''

@app.route('/view_mayor')
def view_mayor():
    db=Db()
    qry="SELECT * FROM `president`"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_mayor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_mayor_search_post',methods=['post'])
def view_mayor_post():
    db=Db()
    name=request.form['search']
    qry="SELECT * FROM `president` WHERE p_name LIKE '%"+name+"%'"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_mayor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/delete_mayor/<id>')
def delete_mayor(id):
    db=Db()
    qry="delete from president WHERE mayor_id='"+id+"'"
    res=db.delete(qry)
    if session['log']=="lin":
        return redirect('/view_mayor')
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_mayor/<id>')
def edit_mayor(id):
    db=Db()
    qry="SELECT * FROM `president`WHERE`mayor_id`='"+id+"'"
    res=db.selectOne(qry)
    if session['log']=="lin":
        return render_template("admin/edit_mayor.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/edit_mayor_post',methods=['post'])
def edit_mayor_post():
    mayor_id=request.form['mayor_id']
    name = request.form['textfield']
    gender = request.form['RadioGroup1']
    dob = request.form['textfield2']
    hname = request.form['textfield3']
    place = request.form['textfield4']
    city = request.form['textfield5']
    district = request.form['textfield6']
    pincode = request.form['textfield7']
    email = request.form['textfield8']
    phone = request.form['textfield9']
    yrfrom=request.form['textfield10']
    yrto=request.form['textfield11']
    if 'fileField' in request.files:
        photo = request.files['fileField']
        if photo.filename!="":
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S')
            photo.save("C:\\final\\prj\\web\\councilor_app\\static\\mayor_pic\\" + date + ".jpg")
            path = "/static/mayor_pic/" + date + ".jpg"
            db=Db()
            qry="UPDATE `president` SET `p_name`='"+name+"',`gender`='"+gender+"',`dob`='"+dob+"',`photo`='"+path+"',`houseno_name`='"+hname+"',`place`='"+place+"',`city`='"+city+"',`district`='"+district+"',`pincode`='"+pincode+"',`email`='"+email+"',`phone`='"+phone+"',`year_from`='"+yrfrom+"',`year_to`='"+yrto+"' WHERE `mayor_id`='"+mayor_id+"'"
            res=db.update(qry)
            return redirect('/view_mayor')
        else:
            db = Db()
            qry = "UPDATE `president` SET `p_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`houseno_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',`year_from`='" + yrfrom + "',`year_to`='" + yrto + "' WHERE `mayor_id`='" + mayor_id + "'"
            res = db.update(qry)
            return redirect('/view_mayor')
    else:
        db = Db()
        qry = "UPDATE `president` SET `p_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`houseno_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',`year_from`='" + yrfrom + "',`year_to`='" + yrto + "' WHERE `mayor_id`='" + mayor_id + "'"
        res = db.update(qry)
        return redirect('/view_mayor')



@app.route('/view_feedback')
def view_feedback():
    db=Db()
    qry="SELECT * FROM `feedback`INNER JOIN `user`ON`feedback`.`user_lid`=`user`.`lid`"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_feedback.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_feedback_search_post',methods=['post'])
def view_feedback_post():
    db=Db()
    ffrom=request.form['textfield2']
    to=request.form['textfield3']
    qry="SELECT * FROM `feedback` INNER JOIN `user` ON `feedback`.`user_lid`=`user`.`lid` WHERE feedback.date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_feedback.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_rating')
def view_rating():
    db=Db()
    qry="SELECT * FROM `rating` JOIN `user` ON `rating`.`user_lid` =`user`.`lid` JOIN `department` ON `rating`.`dept_id`=`department`.`dept_id`"
    res=db.select(qry)
    if session['log']=="lin":
        return render_template("admin/view_rating.html",data=res)
    else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''

@app.route('/view_rating_search_post',methods=['post'])
def view_rating_post():
     db = Db()
     ffrom=request.form['textfield2']
     to=request.form['textfield3']
     qry = "SELECT * FROM `rating` JOIN `user` ON `rating`.`user_lid` =`user`.`lid` JOIN `department` ON `rating`.`dept_id`=`department`.`dept_id` WHERE date BETWEEN '"+ffrom+"'and '"+to+"'"
     res = db.select(qry)
     if session['log'] == "lin":
        return render_template("admin/view_rating.html", data=res)
     else:
        return '''<script>alert('yoy are logout);window.location='/'</script>'''


@app.route('/view_complaint')
def view_complaint():
    db=Db()
    qry="(SELECT `complaint`.*,`councilor`.`coun_name`,`councilor`.`email`,`councilor`.`phone`FROM`complaint`INNER JOIN`councilor`ON`complaint`.`from_id`=`councilor`.`lid`) UNION (SELECT `complaint`.*,`user`.`u_name`,`user`.`email`,`user`.`phone` FROM `complaint` INNER JOIN `user` ON `complaint`.`from_id`=`user`.`lid`)"
    res=db.select(qry)
    return render_template("admin/view_complaint_send_reply.html",data=res)


@app.route('/view_comp_search_post',methods=['post'])
def view_comp_post():
    db=Db()
    ffrom=request.form['textfield2']
    to=request.form['textfield3']
    qry = "SELECT * FROM `complaint` INNER JOIN `department` ON `department`.`dept_id`=`complaint`.`dept_id` INNER JOIN `user` ON `user`.`lid`=`complaint`.`from_id` WHERE complaint.date BETWEEN '"+ffrom+"' AND '"+to+"'"
        # qry="(SELECT `complaint`.*,`councilor`.`coun_name`,`councilor`.`email`,`councilor`.`phone`FROM`complaint`INNER JOIN`councilor`ON`complaint`.`from_id`=`councilor`.`lid`) UNION (SELECT `complaint`.*,`user`.`u_name`,`user`.`email`,`user`.`phone` FROM `complaint` INNER JOIN `user` ON `complaint`.`from_id`=`user`.`lid`) where complaint.date BETWEEN '"+ffrom+"' AND '"+to+"'"
    res=db.select(qry)
    return render_template("admin/view_complaint_send_reply.html",data=res)



@app.route('/sent_reply/<id>')
def sent_reply(id):
    return render_template("admin/send_reply.html",id=id)

@app.route('/sent_reply_post',methods=['post'])
def sent_reply_post():
    id=request.form['comp_id']
    reply=request.form['textarea']
    qry="UPDATE `complaint`SET`reply`='"+reply+"' ,`status`='replied' WHERE `comp_id`='"+id+"'"
    res=db.update(qry)
    return '''<script>alert("Done");window.location='/view_complaint'</script>'''


# <--------------------------------president---------------------------------------------------------------------------------------------->



@app.route('/president_home')
def president_home():
    return render_template("president/president_index.html")

@app.route('/view_mayor_profile')
def view_mayor_profile():
    db=Db()
    qry="SELECT * FROM `president` WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("president/view_profile.html",data=res)

@app.route('/add_notification')
def add_notification():
    print(str(session['lid']))
    return render_template("president/add_notification.html")

@app.route('/add_not_post',methods=['post'])
def add_not_post():
    title=request.form['textfield2']
    notification=request.form['textarea']

    db=Db()

    qry="INSERT INTO `notification`(`title`,`notification`,`date`,`from_lid`,`type`) VALUES('"+str(title)+"','"+str(notification)+"',CURDATE(),'"+str(session['lid'])+"','mayor')"
    res=db.insert(qry)
    print(qry)
    print(title)
    print(notification)
    return '''<script>alert('success');window.location='/add_notification'</script>'''

@app.route('/delete_notif/<id>')
def delete_notif(id):
    db=Db()
    qry="delete from notification WHERE not_id='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_notification')

@app.route('/edit_not/<id>')
def edit_notif(id):
    db=Db()
    qry="select * from notification WHERE not_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template("president/edit_notification.html",data=res)


@app.route('/edit_not_post',methods=['post'])
def edit_not_post():
    not_id=request.form['not_id']
    title = request.form['textfield2']
    notification =request.form ['textarea']
    db = Db()
    qry="UPDATE `notification`SET`title`='"+title+"',`notification`='"+notification+"' WHERE `not_id`='"+not_id+"'"
    res=db.update(qry)
    return redirect('/view_notification')


@app.route('/view_notification')
def view_notification():
    db=Db()
    qry="SELECT * FROM `notification`"
    res=db.select(qry)
    return render_template("president/view_notification.html",data=res)


@app.route('/view_notification_search_post',methods=['post'])
def view_notification_post():
    db=Db()
    ffrom=request.form['textfield2']
    to=request.form['textfield3']
    qry="SELECT * FROM `notification` WHERE date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("president/view_notification.html",data=res)

@app.route('/change_password')
def change_password():
    return render_template("president/change_password.html")

@app.route('/change_password_post',methods=['post'])
def change_password_post():
    currentpw=request.form['textfield']
    newpw=request.form['textfield2']
    confirmpw=request.form['textfield3']
    db=Db()
    qry="select * from login where password='"+currentpw+"'and login_id='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if newpw==confirmpw:
            qry="update login set password='"+confirmpw+"'where login_id='"+str(session['lid'])+"'"
            res=db.update(qry)
            return '''<script>alert('Success');window.location='/'</script>'''
        else:
            return redirect('/change_password')
    else:
        return redirect('/change_password')

@app.route('/create_project')
def create_project():
    return render_template("president/create pjct&policies.html")

@app.route('/create_pjct_post',methods=['post'])
def create_pjct_post():
    title=request.form['textfield2']
    description=request.form['textarea']
    total_funding=request.form['textfield3']
    db=Db()
    qry="INSERT INTO `project_policies`(`title`,`mayor_lid`,`description`,`total_funding`,`created_date`)VALUE('"+title+"','"+str(session['lid'])+"','"+description+"','"+total_funding+"',CURDATE())"
    res=db.insert(qry)
    return '''<script>alert('created');window.location='/create_project'</script>'''


@app.route('/view_pjct_polic')
def view_pjct_polic():
    db=Db()
    qry="SELECT * FROM `project_policies`JOIN`president`ON`project_policies`.`mayor_lid`=`president`.`lid`"
    res=db.select(qry)
    return render_template("president/view_pjct&poli.html",data=res)

@app.route('/view_pjct_polic_search_post',methods=['post'])
def view_pjct_polic_post():
    db=Db()
    ffrom=request.form['textfield2']
    to=request.form['textfield3']
    qry="SELECT * FROM `project_policies`JOIN`president`ON`project_policies`.`mayor_lid`=`president`.`lid` WHERE created_date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("president/view_pjct&poli.html",data=res)




@app.route('/delete_pjct_polic/<id>')
def delete_pjct_polic(id):
    db=Db()
    qry="DELETE FROM `project_policies` WHERE `proplan_id`='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_pjct_polic')

@app.route('/edit_pjct_polic/<id>')
def edit_pjct_polic(id):
    db=Db()
    qry="select * FROM `project_policies` WHERE `proplan_id`='"+id+"'"
    res=db.selectOne(qry)
    return render_template("president/edit_pjct_policy.html",data=res)

@app.route('/edit_pjct_polic_post',methods=['post'])
def edit_pjct_polic_post():
    proplan_id=request.form['proplan_id']
    title = request.form['textfield2']
    description = request.form['textarea']
    total_funding = request.form['textfield3']
    db=Db()
    qry="UPDATE `project_policies` SET `title`='"+title+"',`description`='"+description+"',`total_funding`='"+total_funding+"' WHERE `proplan_id`='"+proplan_id+"'"
    res=db.update(qry)
    return redirect('/view_pjct_polic')





@app.route('/view_pjct_plan')
def view_pjct_plan():
    db=Db()
    qry="SELECT * FROM `counc_project_plan`JOIN `councilor`ON`counc_project_plan`.`coun_lid`=`councilor`.`councilor_id`"
    res=db.select(qry)
    return render_template("president/view_pjct_plan.html",data=res)

@app.route('/view_pjct_plan_search_post',methods=['post'])
def view_pjct_plan_post():
    ffrom = request.form['textfield2']
    to = request.form['textfield3']
    db=Db()
    qry="SELECT * FROM `counc_project_plan`JOIN `councilor`ON`counc_project_plan`.`coun_lid`=`councilor`.`councilor_id` WHERE  date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("president/view_pjct_plan.html",data=res)



@app.route('/approve_pjct_plan/<id>')
def approve_pjct_plan(id):
    db=Db()
    qry="UPDATE `counc_project_plan` SET `status`='approved' WHERE `projct_pln_id`='"+id+"' "
    res=db.update(qry)
    return '''<script>alert('approved');window.loaction='/view_pjct_plan'</script>'''


@app.route('/send_reply/<id>')
def send_reply(id):
    return render_template("president/reply.html",id=id)

@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    id=request.form['comp_id']
    reply=request.form['textarea']
    qry="UPDATE `complaint`SET`reply`='"+reply+"' ,`status`='replied' WHERE`comp_id`='"+id+"'"
    res=db.update(qry)
    return '''<script>alert("Done");window.location='/send_reply'</script>'''


@app.route('/view_complaints')
def view_complaints():
    db=Db()
    qry="SELECT * FROM `complaint`JOIN`department`ON`complaint`.`dept_id`=`department`.`dept_id` JOIN `user`ON`complaint`.`from_id`=`user`.`lid`"
    res=db.select(qry)
    return render_template("president/view_complaint.html",data=res)

@app.route('/view_complaints_search_post',methods=['post'])
def view_complaints_post():
    ffrom = request.form['textfield2']
    to = request.form['textfield3']
    db = Db()
    qry="SELECT * FROM `complaint`JOIN`department`ON`complaint`.`dept_id`=`department`.`dept_id` JOIN `user`ON`complaint`.`from_id`=`user`.`lid` WHERE date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("president/view_complaint.html",data=res)





@app.route('/view_councellor')
def view_councellor():
    db = Db()
    qry = "SELECT * FROM `councilor` JOIN `area`ON `councilor`.`area_id`=`area`.`area_id`"
    res = db.select(qry)
    return render_template("president/view_counceller.html",data=res)

@app.route('/view_councellor_search_post',methods=['post'])
def view_councellor_post():
    db = Db()
    name=request.form['textfield']
    qry = "SELECT * FROM `councilor` JOIN `area`ON `councilor`.`area_id`=`area`.`area_id` WHERE coun_name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template("president/view_counceller.html",data=res)

@app.route('/view_dept_work')
def view_dept_work():
        db = Db()
        qry = "SELECT * FROM `work` JOIN `department`ON`work`.`dept_lid`=`department`.`deplid` JOIN `clerk` ON `work`.`clerk_lid`=`clerk`.`lid`"
        res=db.select(qry)
        return render_template("president/view_dept_work.html",data=res)

@app.route('/view_dept_work_search_post',methods=['post'])
def view_dept_work_post():
        db = Db()
        name=request.form['textfield']
        qry = "SELECT * FROM `work` JOIN `department`ON`work`.`dept_lid`=`department`.`dept_id`JOIN`clerk`ON`work`.`clerk_lid`=`clerk`.`lid` WHERE department.dept_name LIKE '%"+name+"%'"
        res=db.select(qry)
        return render_template("president/view_dept_work.html",data=res)






@app.route('/view_suggestion')
def view_suggestion():
    db=Db()
    qry="SELECT * FROM `suggestion` JOIN `councilor`ON`suggestion`.`coun_lid`=`councilor`.`councilor_id`"
    res=db.select(qry)
    return render_template("president/view_suggestion.html",data=res)


@app.route('/view_suggesion_post', methods=['POST'])
def view_suggesion_post():
    db = Db()
    frm = request.form['textfield2']
    too = request.form['textfield3']
    qry = "select * from suggestion INNER join councilor on suggestion.coun_lid=councilor.councilor_id where suggestion.date between '"+frm+"' and '"+too+"'"
    res = db.select(qry)
    return render_template("president/view_suggestion.html", data=res)


# @app.route('/view_suggestion_search_post',methods=['post'])
# def view_suggestion_post():
#     db=Db()
#     ffrom = request.form['textfield2']
#     to = request.form['textfield3']
#     qry = "SELECT * FROM `suggestion` INNER JOIN `councilor` ON `councilor`.`councilor_id`=`suggestion`.`coun_lid`  WHERE `suggestion`.`date` BETWEEN '"+ffrom+"' AND '"+to+"'"
#     # qry="SELECT * FROM `suggestion` INNER JOIN `councilor` ON `councilor`.`councilor_id`=`suggestion`.`coun_lid` WHERE `suggestion`.`date` BETWEEN '"+ffrom+"' AND '"+to+"'"
#     res=db.select(qry)
#     return render_template("president/view_suggestion.html",data=res)

@app.route('/view_corporation_about')
def view_corporation_about():
    db=Db()
    qry="SELECT * FROM `co-orperation_about`"
    res=db.select(qry)
    return render_template("president/view_corpertn_about.html",data=res)

@app.route('/view_corporation_about_search_post',methods=['post'])
def view_corporation_about_post():
    db=Db()
    name=request.form['textfield']
    qry="SELECT * FROM `co-orperation_about` WHERE corporation_name LIKE '%"+name+"%'"
    res=db.select(qry)
    return render_template("president/view_corpertn_about.html",data=res)

@app.route('/view_pgm_info')
def view_pgm_info():
    db=Db()
    qry="SELECT * FROM `program_info`JOIN`councilor`ON`program_info`.`coun_lid`=`councilor`.`lid`"
    res=db.select(qry)
    return render_template("president/view_pgm_info.html",data=res)

@app.route('/view_pgm_info_search_post',methods=['post'])
def view_pgm_info_post():
    db=Db()
    name=request.form['textfield']
    qry="SELECT * FROM `program_info` JOIN `councilor` ON `program_info`.`coun_lid`=`councilor`.`lid` WHERE program_info.pgm_name LIKE '%"+name+"%'"
    res=db.select(qry)
    return render_template("president/view_pgm_info.html",data=res)

#####################################

@app.route("/chat1")
def chat1():
    # if session['log']=="lin":
        # session["userid"]=id
        return render_template("president/fur_chat.html")
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''

@app.route("/chatview1",methods=['post'])
def chatview1():
    # if session['log']=="lin":
        db=Db()
        qry="select * from councilor"
        # qry="select * from student where user_lid='"+str(session["userid"])+"'"
        res=db.select(qry)
        print(res)
        return jsonify(data=res)
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''

@app.route("/doctor_insert_chat1/<msg>")
def insert_chat1(msg):
    # if session['log']=="lin":
        db=Db()
        qry="insert into chat (date,from_id,to_id,message) values (curdate(),'"+str(session['lid'])+"','"+str(session["userid"])+"','"+msg+"')"
        db.insert(qry)
        return jsonify(status="ok")
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''



@app.route("/drviewmsg1/<id>")        # refresh messages chatlist
def chat_usr_chk1(id):
    # if session['log']=="lin":
        session["userid"]=id
        # qry = "select from_id,message as msg,date,chat_id from chat where (from_id='"+str(session["lid"])+"' and to_id='" + str(id) + "') or ((from_id='" + str(id) + "' and to_id='"+str(session["lid"])+"')) order by chat_id desc"
        qry = "select from_id,message as msg,date,chat_id from chat where (from_id='"+str(session['lid'])+"' and to_id='" + str(session["userid"]) + "') or ((from_id='" + str(session["userid"]) + "' and to_id='"+str(session['lid'])+"')) order by chat_id asc"
        c = Db()
        res = c.select(qry)
        ry = "select * from councilor where lid='" + str(session["userid"]) + "'"
        rest = c.selectOne(ry)
        print(rest)
        return jsonify(data=res,user_name=rest["coun_name"],user_photo=rest["photo"],user_lid=rest["lid"])
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''



#####################


# ------------------------------------councilor--------------------------------------------------------------


@app.route('/councilor_home')
def councilor_home():
    return render_template("councillor/councilor_index.html")

@app.route('/view_coun_profile')
def view_coun_profile():
    db=Db()
    qry="SELECT * FROM `councilor` WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("councillor/view_profile_coun.html",data=res)


@app.route('/view_dept_profile')
def view_dept_profile():
    db=Db()
    qry="SELECT * FROM `department` WHERE `deplid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("department/view_profile_coun.html",data=res)




@app.route('/change_pass')
def change_pass():
    return render_template("councillor/change_password_coun.html")


@app.route('/change_passw_post',methods=['post'])
def change_passw_post():
    currentpw=request.form['textfield']
    newpw=request.form['textfield2']
    confirmpw=request.form['textfield3']
    db=Db()
    qry="select * from login where password='"+currentpw+"'and login_id='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if newpw==confirmpw:
            qry="update login set password='"+confirmpw+"'where login_id='"+str(session['lid'])+"'"
            res=db.update(qry)
            return redirect('/')
        else:
            return redirect('/change_pass')
    else:
        return redirect('/change_pass')


@app.route('/coun_create_pjct_plan')
def coun_create_pjct_plan():
    return render_template("councillor/create_project_plan.html")

@app.route('/coun_create_pjct_plan_post',methods=['post'])
def coun_create_pjct_plan_post():
    title=request.form['textfield2']
    description=request.form['textarea']
    file_name=request.form['textfield3']
    db=Db()
    qry="INSERT INTO `counc_project_plan`(`pjct_title`,`coun_lid`,`description`,`filename`,`date`,`status`)VALUES('"+title+"','"+str(session['lid'])+"','"+description+"','"+file_name+"',curdate(),'pending')"
    res=db.insert(qry)
    return '''<script>alert('success');window.location='/coun_create_pjct_plan'</script>'''

@app.route('/send_complaint')
def send_complaint():
    return render_template("councillor/send_complaints.html")

@app.route('/send_complaint_post',methods=['post'])
def send_complaint_post():
    complaint=request.form['textarea2']
    db=Db()
    qry="INSERT INTO `complaint`(`from_id`,`complaint`,`date`,`reply`,`status`)VALUE('"+str(session['lid'])+"','"+complaint+"',curdate(),'pending','pending')"
    res=db.insert(qry)
    return '''<script>alert('success');window.location='/send_complaint'</script>'''



@app.route('/view_complaint_reply')
def view_reply():
    db=Db()
    qry="SELECT * FROM `complaint` JOIN `councilor`ON `complaint`.`from_id`=`councilor`.`lid` WHERE `lid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("councillor/view_comp_reply.html",data=res)



@app.route('/send_seggestion')
def send_seggestion():
    return render_template("councillor/send_suggestion.html")

@app.route('/send_seggestion_post',methods=['post'])
def send_seggestion_post():
    # coun_details=request.form['textfield2']
    sugg=request.form['textarea']
    qry="INSERT INTO `suggestion`(`suggestion`,`date`,`coun_lid`)VALUE('"+sugg+"',curdate(),'"+str(session['lid'])+"')"
    res=db.insert(qry)
    return '''<script>alert('success');window.location='/send_seggestion'</script>'''

@app.route('/coun_view_reply')
def coun_view_complaint():
    return render_template("councillor/view_comp_reply.html")

@app.route('/view_created_pjct_sta')
def view_created_pjct_sta():
    db=Db()
    qry="SELECT * FROM `counc_project_plan` JOIN `councilor`ON`counc_project_plan`.`coun_lid`=`councilor`.`councilor_id`"
    res=db.select(qry)
    return render_template("councillor/view_created_pjct_status.html",data=res)

@app.route('/view_created_pjct_sta_post',methods=['post'])
def view_created_pjct_sta_post():
    ffrom=request.form['textfield']
    to=request.form['textfield2']
    db=Db()
    qry = "SELECT * FROM `counc_project_plan` JOIN `councilor`ON`counc_project_plan`.`coun_lid`=`councilor`.`councilor_id` WHERE date BETWEEN '"+ffrom+"' AND '"+to+"'"
    res = db.select(qry)
    return render_template("councillor/view_created_pjct_status.html", data=res)


@app.route('/view_mayor_pjct_policy')
def view_mayor_pjct_policy():
    db = Db()
    qry = "SELECT * FROM `project_policies`JOIN`president`ON`project_policies`.`mayor_lid`=`president`.`lid`"
    res = db.select(qry)
    return render_template("councillor/view_mayor_pjct_policy.html",data=res)

@app.route('/view_mayor_pjct_policy_search_post',methods=['post'])
def view_mayor_pjct_policy_post():
    db = Db()
    name=request.form['textfield3']
    qry = "SELECT * FROM `project_policies`JOIN`president`ON`project_policies`.`mayor_lid`=`president`.`lid` WHERE president.p_name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template("councillor/view_mayor_pjct_policy.html",data=res)


@app.route('/view_notif_frm_mayor')
def view_notif_frm_mayor():
    db=Db()
    qry="SELECT * FROM `notification`"
    res=db.select(qry)
    return render_template("councillor/view_notif_frm_mayor.html",data=res)

@app.route('/view_notif_frm_mayor__search_post',methods=['post'])
def view_notif_search_post():
    db=Db()
    ffrom=request.form['textfield2']
    to=request.form['textfield3']
    qry="SELECT * FROM `notification` WHERE date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("councillor/view_notif_frm_mayor.html",data=res)



@app.route('/view_problems')
def view_problems():
    db=Db()
    qry="SELECT * FROM `problem` JOIN `user`ON `problem`.`user_lid`=`user`.`lid`"
    res=db.select(qry)
    return render_template("councillor/view_problem.html",data=res)

@app.route('/view_problems_search_post',methods=['post'])
def view_problems_post():
    db=Db()
    ffrom = request.form['textfield']
    to = request.form['textfield2']
    qry="SELECT * FROM `problem` JOIN `user`ON `problem`.`user_lid`=`user`.`user_id` WHERE `date` BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("councillor/view_problem.html",data=res)


@app.route('/action_taken/<id>')
def action_taken(id):
    db=Db()
    qry="SELECT * FROM `action` WHERE `pblm_id`='"+id+"'"
    id=db.selectOne(qry)
    return render_template("councillor/action_taken.html",id=id)

@app.route('/action_taken_post',methods=['post'])
def action_taken_post():
    db=Db()
    act_id=request.form['id']
    action=request.form['textarea']
    qry="UPDATE `action`SET `actiontaken`='"+action+"',`status`='action taken' WHERE`act_id`='"+act_id+"'"
    res=db.update(qry)
    return '''<script>alert("Done");window.location='/view_problems'</script>'''


@app.route('/send_program_info')
def send_program_info():
    return render_template("councillor/send_program.html")

@app.route('/send_pgm_info_post',methods=['post'])
def send_pgm_info_post():
    db=Db()
    date=request.form['textfield']
    program_name=request.form['textfield2']
    description=request.form['textarea']
    qry="INSERT INTO `program_info`(`pgm_name`,`coun_lid`,`date`,`description`)VALUE('"+program_name+"','"+str(session['lid'])+"','"+date+"','"+description+"')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/send_program_info'</script>'''


@app.route('/view_program_info')
def view_program_info():
    db=Db()
    qry="SELECT * FROM `program_info` JOIN `councilor`ON`program_info`.`coun_lid`=`councilor`.`lid` WHERE `lid`='"+str(session['lid'])+"'  "
    res=db.select(qry)
    return render_template("councillor/view_program_info.html",data=res)


@app.route('/delete_prgm_info/<id>')
def delete_prgm_info(id):
    db=Db()
    qry="delete from program_info where pgm_id='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_program_info')

@app.route('/edit_prgm_info/<id>')
def edit_prgm_info(id):
    db=Db()
    qry="select * from program_info WHERE pgm_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template("councillor/edit_program_info.html",data=res)

@app.route('/edit_prgm_info_post',methods=['post'])
def edit_prgm_info_post():
    db = Db()
    pgm_id=request.form['pgm_id']
    date = request.form['textfield']
    program_name = request.form['textfield2']
    description = request.form['textarea']
    qry="UPDATE`program_info` SET `pgm_name`='"+program_name+"',`date`='"+date+"',`description`='"+description+"' WHERE `pgm_id`='"+pgm_id+"'"
    res=db.update(qry)
    return redirect('/view_program_info')

#################################################chat##########################################3


@app.route("/chat")
def chat():
    # if session['log']=="lin":
        # session["userid"]=id
        return render_template("councillor/fur_chat.html")
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''

@app.route("/chatview",methods=['post'])
def chatview():
    # if session['log']=="lin":
        db=Db()
        qry="select * from president"
        # qry="select * from student where user_lid='"+str(session["userid"])+"'"
        res=db.select(qry)
        print(res)
        return jsonify(data=res)
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''

@app.route("/doctor_insert_chat/<msg>")
def insert_chat(msg):
    # if session['log']=="lin":
        db=Db()
        qry="insert into chat (date,from_id,to_id,message) values (curdate(),'"+str(session['lid'])+"','"+str(session["userid"])+"','"+msg+"')"
        db.insert(qry)
        return jsonify(status="ok")
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''



@app.route("/drviewmsg/<id>")        # refresh messages chatlist
def chat_usr_chk(id):
    # if session['log']=="lin":
        session["userid"]=id
        # qry = "select from_id,message as msg,date,chat_id from chat where (from_id='"+str(session["lid"])+"' and to_id='" + str(id) + "') or ((from_id='" + str(id) + "' and to_id='"+str(session["lid"])+"')) order by chat_id desc"
        qry = "select from_id,message as msg,date,chat_id from chat where (from_id='"+str(session['lid'])+"' and to_id='" + str(session["userid"]) + "') or ((from_id='" + str(session["userid"]) + "' and to_id='"+str(session['lid'])+"')) order by chat_id asc"
        c = Db()
        res = c.select(qry)
        ry = "select * from president where lid='" + str(session["userid"]) + "'"
        rest = c.selectOne(ry)
        print(rest)
        return jsonify(data=res,user_name=rest["p_name"],user_photo=rest["photo"],user_lid=rest["lid"])
    # else:
    #     return '''<script>alert('You Are Loged Out');window.location="/"</script>'''








#########################################################################################################



# <--------------------------------------department------------------------------------------------------------------------->


@app.route('/dept_home')
def dept_home():
    return render_template("department/department_index.html")

@app.route('/add_clerk_dept')
def add_clerk_dept():
    db=Db()
    qry = "select * from department"
    res = db.select(qry)
    return render_template("department/add_clerk.html",data=res)

@app.route('/add_clerk_dept_post',methods=['post'])
def add_clerk_dept_post():
    db=Db()
    name=request.form['textfield']
    gender=request.form['RadioGroup1']
    dob=request.form['textfield2']
    hname=request.form['textfield3']
    place=request.form['textfield4']
    city=request.form['textfield5']
    district=request.form['textfield6']
    pincode=request.form['textfield7']
    email=request.form['textfield8']
    phone=request.form['textfield9']
    # dept_name=request.form['select']
    from datetime import datetime
    photo = request.files['fileField']
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    photo.save("C:\\final\\prj\\web\\councilor_app\\static\\clerk_pic\\" + date + ".jpg")
    path = "/static/clerk_pic/" + date + ".jpg"
    qry = "INSERT INTO `login`(`uname`,`password`,`type`)VALUES('" + email + "','" + phone + "','clerk')"
    res = db.insert(qry)

    qry1 = "INSERT INTO `clerk`(`c_name`,`gender`,`dob`,`photo`,`house_name`,`place`,`city`,`district`,`pincode`,`email`,`phone`,`lid`,`dept_id`) VALUES('" + name + "','" + gender + "','" + dob + "','" + str(
        path) + "','" + hname + "','" + place + "','" + city + "','" + district + "','" + pincode + "','" + email + "','" + phone + "','" + str(
        res) + "','" + str(session['lid']) + "')"
    res1 = db.insert(qry1)
    print(qry1)
    return '''<script>alert("success");window.location='/add_clerk_dept'</script>'''


@app.route('/view_clerk_dept')
def view_clerk_dept():
    db = Db()
    qry = "SELECT * FROM `clerk` INNER JOIN `department` ON `department`.`deplid`=`clerk`.`dept_id` where `department`.`deplid` = '"+str(session['lid'])+"'"
    res = db.select(qry)
    return render_template("department/dept_view_clerk.html", data=res)





@app.route('/view_search_dept_clerk_post', methods=['post'])
def view_search_dept_clerk_post():
    db = Db()
    search = request.form['textfield']
    qry = "SELECT * FROM `clerk` INNER JOIN `department` ON `department`.`deplid`=`clerk`.`dept_id` WHERE clerk.c_name LIKE '%" + search + "%' and department.deplid='"+str(session['lid'])+"'"
    res = db.select(qry)
    return render_template("department/dept_view_clerk.html", data=res)

@app.route('/delete_clerk_dept/<id>')
def delete_clerk_dept(id):
    db = Db()
    qry = "DELETE FROM `clerk` WHERE `clerk_id`='" + id + "'"
    res = db.delete(qry)
    return redirect('/view_clerk_dept')


@app.route('/edit_clerk_dept/<id>')
def edit_clerk_dept(id):
    db = Db()
    qry = "SELECT * FROM `clerk` WHERE `clerk_id`='" + id + "'"
    res = db.selectOne(qry)
    qry2 = "SELECT * FROM `department`"
    res2 = db.select(qry2)
    return render_template("admin/edit_clerk.html", data=res, data2=res2)

@app.route('/edit_clerk_dept_post', methods=['post'])
def edit_clerk_dept_post():
    db = Db()
    clerk_id = request.form['clerk_id']
    name = request.form['textfield']
    gender = request.form['RadioGroup1']
    dob = request.form['textfield2']
    hname = request.form['textfield3']
    place = request.form['textfield4']
    city = request.form['textfield5']
    district = request.form['textfield6']
    pincode = request.form['textfield7']
    email = request.form['textfield8']
    phone = request.form['textfield9']
    department = request.form['select']
    if 'fileField' in request.files:
        photo = request.files['fileField']
        if photo.filename != "":
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S')
            photo.save("C:\\final\\prj\\web\\councilor_app\\static\\clerk_pic\\" + date + ".jpg")
            path = "/static/clerk_pic/" + date + ".jpg"
            qry = "UPDATE `clerk`SET`c_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`photo`='" + path + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',dept_id='" + department + "' where clerk_id='" + clerk_id + "'"
            res = db.update(qry)
            return '''<script>alert("Updated");window.location='/view_clerk_dept'</script>'''
        else:
            qry = "UPDATE `clerk`SET`c_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "' ,dept_id='" + department + "'where clerk_id='" + clerk_id + "'"
            res = db.update(qry)
            return '''<script>alert("Updated");window.location='/view_clerk_dept'</script>'''
    else:
        qry = "UPDATE `clerk`SET`c_name`='" + name + "',`gender`='" + gender + "',`dob`='" + dob + "',`house_name`='" + hname + "',`place`='" + place + "',`city`='" + city + "',`district`='" + district + "',`pincode`='" + pincode + "',`email`='" + email + "',`phone`='" + phone + "',dept_id='" + department + "' where clerk_id='" + clerk_id + "'"
        res = db.update(qry)
        return '''<script>alert("Updated");window.location='/view_clerk_dept'</script>'''


@app.route('/change_password_dept')
def change_password_dept():
      return render_template("department/change_pass_dept.html")

@app.route('/change_password_dept_post', methods=['post'])
def change_password_dept_post():
     currentpw = request.form['textfield']
     newpw = request.form['textfield2']
     confirmpw = request.form['textfield3']
     db = Db()
     qry = "select * from login where password='" + currentpw + "'and login_id='" + str(session['lid']) + "'"
     res = db.selectOne(qry)
     if res is not None:
         if newpw == confirmpw:
             qry = "update login set password='" + confirmpw + "'where login_id='" + str(session['lid']) + "'"
             res = db.update(qry)
             return redirect('/')
         else:
             return '''<script>alert("not match");window.location='/change_password_dept'</script>'''
     else:
        return '''<script>alert("notfound");window.location='/change_password_dept'</script>'''



@app.route('/add_create_work')
def add_create_work():
    db=Db()
    qry="select * from clerk"
    res=db.select(qry)
    return render_template("department/add_create_work.html",data=res)

@app.route('/add_create_work_post',methods=['post'])
def add_create_work_post():
    db=Db()
    upload_date=request.form['textfield']
    work_name=request.form['textfield2']
    clerkname=request.form['select']
    qry="INSERT INTO `work`(`w_name`,`upload_date`,`dept_lid`,`clerk_lid`,`status`)VALUE('"+work_name+"','"+upload_date+"','"+str(session['lid'])+"','"+clerkname+"','pending')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/add_create_work'</script>'''

@app.route('/view_applictn_frm_user')
def view_applictn_frm_user():
    db=Db()
    print("liddd",str(session['lid']))
    qry="SELECT `application`.*, `department`.`dept_name`, `user`.* FROM `application` INNER JOIN `department` ON `department`.`dept_id`=`application`.`dept_lid` INNER JOIN `user` ON `application`.`user_lid`=`user`.`lid` WHERE `department`.`deplid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    print(qry)
    print(res)
    return render_template("department/view_appllicatn_fm_user.html",data=res)

@app.route('/view_complaint_fm_user')
def view_complaint_fm_user():
    db=Db()
    qry="SELECT * FROM `complaint`JOIN `user`ON `complaint`.`from_id`=`user`.`lid`JOIN`department`ON`department`.`dept_id`=`complaint`.`dept_id`"
    res=db.select(qry)
    return render_template("department/view_compl_fm_user.html",data=res)

@app.route('/view_complaint_fm_user_search_post',methods=['post'])
def view_complaint_fm_user_post():
    db=Db()
    ffrom=request.form['textfield']
    to=request.form['textfield2']
    qry="SELECT * FROM `complaint`JOIN `user`ON `complaint`.`from_id`=`user`.`lid`JOIN`department`ON`department`.`dept_id`=`complaint`.`dept_id` where date BETWEEN '"+ffrom+"' and '"+to+"'"
    res=db.select(qry)
    return render_template("department/view_compl_fm_user.html",data=res)

@app.route('/send_reply_dept/<id>')
def send_reply_dept(id):
    return render_template("department/send_reply.html", id=id)

@app.route('/send_reply_dept_post',methods=['post'])
def send_reply__dept_post():
    db=Db()
    id=request.form['comp_id']
    action=request.form['textarea']
    qry="UPDATE `complaint`SET`reply`='"+action+"',`status`='replied' WHERE `comp_id`='"+id+"'"
    res=db.update(qry)
    return '''<script>alert("Done");window.location='/view_complaint_fm_user'</script>'''


@app.route('/send_notif_to_clrk')
def send_notif_to_clrk():
    return render_template("department/sent_notifictn_clk.html")

@app.route('/send_notf_to_clrk_post',methods=['post'])
def send_notf_to_clrk_post():
    db=Db()
    title=request.form['textfield']
    notifictn=request.form['textarea']
    qry="INSERT INTO `notification`(`title`,`notification`,`date`,`from_lid`,`type`)VALUE('"+title+"','"+notifictn+"',curdate(),'"+str(session['lid'])+"','department')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/send_notif_to_clrk'</script>'''

@app.route('/view_notifictn_dept')
def view_notifictn_dept():
    db=Db()
    # qry="SELECT * FROM `notification` JOIN `department`ON `notification`.`from_lid`=`department`.`dept_id` where from_lid='"+str(session['lid'])+"'"
    qry="SELECT * FROM `notification` WHERE `from_lid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("department/view_notification_dept.html",data=res)

@app.route('/view_notifictn_dept_search',methods=['post'])
def view_notifictn_dept_post():
    db=Db()
    ffrom = request.form['textfield']
    to = request.form['textfield2']

    qry="SELECT * FROM `notification` JOIN `department`ON `notification`.`from_lid`=`department`.`dept_id` where date BETWEEN '"+ffrom+"'and'"+to+"'"
    res=db.select(qry)
    return render_template("department/view_notification_dept.html",data=res)

@app.route('/delete_notif_dept/<id>')
def delete_notif_dept(id):
    db=Db()
    qry="DELETE FROM `notification` WHERE `not_id`='"+id+"'"
    res=db.delete(qry)
    return redirect('/view_notifictn_dept')

@app.route('/edit_notif_dept/<id>')
def edit_notif_dept(id):
    db=Db()
    qry="select * from notification where not_id='"+id+"'"
    res=db.selectOne(qry)
    return render_template("department/edit_notification_dept.html",data=res)

@app.route('/edit_not_dept_post',methods=['post'])
def edit_not_dept_post():
    db=Db()
    not_id=request.form['not_id']
    title = request.form['textfield']
    notifictn = request.form['textarea']
    qry="UPDATE `notification` SET `title`='"+title+"',`notification`='"+notifictn+"' WHERE `not_id`='"+not_id+"'"
    res=db.update(qry)
    return redirect('/view_notifictn_dept')


@app.route('/view_notifctn_frm_mayor')
def view_notifctn_frm_mayor():
    db=Db()
    qry="SELECT * FROM `notification` JOIN `president`ON`notification`.`from_lid`=`president`.`lid`"
    res=db.select(qry)
    return render_template("department/view_notifictn_frm_mayor.html",data=res)

@app.route('/view_notifctn_frm_mayor_search_post',methods=['post'])
def view_notifctn_frm_mayor_post():
    db=Db()
    ffrom = request.form['textfield']
    to = request.form['textfield2']

    qry="SELECT * FROM `notification` JOIN `president`ON`notification`.`from_lid`=`president`.`lid`where date BETWEEN '"+ffrom+"'and'"+to+"'"
    res=db.select(qry)
    return render_template("department/view_notifictn_frm_mayor.html",data=res)


@app.route('/view_rating_frm_user')
def view_rating_frm_user():
    db=Db()
    qry="SELECT * FROM `rating`JOIN `user`ON `rating`.`user_lid`=`user`.`lid`"
    res=db.select(qry)
    return render_template("department/view_rating_frm_user.html",data=res)

@app.route('/view_work_report_frm_clrk')
def view_work_report_frm_clrk():
    db=Db()
    qry="SELECT * FROM `work_report`JOIN `work`ON `work_report`.`work_id`=`work`.`work_id`JOIN `clerk`ON`clerk`.`lid`=`work`.`clerk_lid`"
    res=db.select(qry)
    return render_template("department/view_wrk_report_clrk.html",data=res)

@app.route('/view_work')
def view_work():
    db=Db()
    qry="SELECT * FROM `work` JOIN `clerk`ON`clerk`.`lid`=`work`.`clerk_lid` where dept_lid='"+str(session['lid'])+"'"
    res=db.select(qry)
    print(qry,"\n",res)
    return render_template("department/view_wrk.html",data=res)

@app.route('/view_work_report_frm_clrk_search_post',methods=['post'])
def view_work_report_frm_clrk_post():
    db=Db()
    ffrom = request.form['textfield']
    to = request.form['textfield2']
    qry="SELECT * FROM `work_report`JOIN `work`ON `work_report`.`work_id`=`work`.`work_id`JOIN `clerk`ON`clerk`.`lid`=`work`.`clerk_lid`where date BETWEEN '"+ffrom+"'and'"+to+"'"
    res=db.select(qry)
    return render_template("department/view_wrk_report_clrk.html",data=res)


@app.route('/forward_to_clerk/<id>')
def forward_to_clerk(id):
    db=Db()
    c = "select * from application where app_id='"+str(id)+"'"
    p = db.selectOne(c)
    qry="select * from clerk"
    res=db.select(qry)
    # qry2="select * from application"
    # res2=db.select(qry2)
    return render_template("department/forward_to_clk.html",data=res, p=p)

@app.route('/forward_to_clk_post',methods=['post'])
def forward_to_clk_post():
    db=Db()
    clrk_name=request.form['select']
    application=request.form['h1']
    qry1 = "update application set status='Assigned' where app_id='"+application+"'"
    r1 = db.update(qry1)
    qry="INSERT INTO `application_allocation`(`clerk_id`,`app_id`,`date`,`status`)VALUES('"+clrk_name+"','"+application+"',curdate(),'allocated')"
    res=db.insert(qry)
    return '''<script>alert("Allocated");window.location='/view_applictn_frm_user'</script>'''

@app.route('/forward/<id>')
def forward(id):
    db=Db()
    qry="UPDATE `application`SET`status`='allocated' WHERE `app_id`='"+id+"'"
    res=db.update(qry)
    return forward_to_clerk()

# ------------------------------------------clerk-----------------------------------------------------


@app.route('/clerk_home')
def clerk_home():
    return render_template("clerk/clerk_index.html")

@app.route('/view_clk_profile')
def view_clk_profile():
    db=Db()
    qry="SELECT * FROM `clerk` WHERE `lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("clerk/view_profile_clerk.html",data=res)

@app.route('/change_pass_clk')
def change_pass_clk():
    return render_template("clerk/change_password_clerk.html")

@app.route('/change_pass_clk_post',methods=['post'])
def change_pass_clk_post():
    currentpw = request.form['textfield']
    newpw = request.form['textfield2']
    confirmpw = request.form['textfield3']
    db = Db()
    qry = "select * from login where password='" + currentpw + "'and login_id='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if newpw == confirmpw:
            qry = "update login set password='" + confirmpw + "'where login_id='" + str(session['lid']) + "'"
            res = db.update(qry)
            return redirect('/login')
        else:
            return '''<script>alert("not match");window.location='/login'</script>'''
    return '''<script>alert("notfound");window.location='/'</script>'''



@app.route('/upload_cerificate/<id>')
def upload_cerificate(id):
    db = Db()
    qry = "SELECT * FROM `application_allocation` WHERE `app_id`='"+str(id)+"'"
    res = db.selectOne(qry)
    return render_template("clerk/upload_certificate.html",data=res)

@app.route('/upload_certificate_post',methods=['post'])
def upload_certificate_post():
    db=Db()
    id = request.form['h1']
    title=request.form['textfield']
    from datetime import datetime
    photo=request.files['fileField']
    date=datetime.now().strftime('%Y%m%d-%H%M%S')
    photo.save("C:\\final\\prj\\web\\councilor_app\\static\\certificate\\"+date+photo.filename)
    path="/static/certificate/"+date+photo.filename
    qry1 = "update application set status='completed' where app_id='"+str(id)+"'"
    res1 = db.update(qry1)
    qry="INSERT INTO `application_certificate`(`app_id`,`title_name`,`status`,`certificate`)VALUE('"+str(id)+"','"+title+"','Uploaded','"+path+"')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/view_assignedd_applictn'</script>'''

@app.route('/upload_work_report')
def upload_work_report():
    return render_template("clerk/upload_work_report.html")

@app.route('/upload_work_report_post',methods=['post'])
def upload_work_report_post():
    db=Db()
    filename=request.form['textfield']
    description=request.form['textarea']
    qry="INSERT INTO `work_report`(`r_filename`,`work_id`,`date`,`description`)VALUE('"+filename+"','"+str(session['lid'])+"',curdate(),'"+description+"')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/upload_work_report'</script>'''

@app.route('/view_assignedd_applictn')
def view_assignedd_applictn():
    db=Db()
    qry="SELECT * FROM `application_allocation` INNER JOIN `clerk` ON `application_allocation`.`clerk_id`=`clerk`.`lid` INNER JOIN `application` ON `application_allocation`.`app_id`=`application`.`app_id` INNER JOIN `user` ON `application`.`user_lid`=`user`.`lid` WHERE `clerk`.`lid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("clerk/view_assigned_applicatn.html",data=res)

@app.route('/view_completed_work_report')
def view_completed_work_report():
    db=Db()
    qry="SELECT * FROM `work_report` JOIN `work`ON `work_report`.`work_id`=`work`.`work_id`JOIN`department`ON`work`.`dept_lid`=`department`.`deplid`"
    res=db.select(qry)
    return render_template("clerk/view_completed_wk_report.html",data=res)

@app.route('/view_pending_work')
def view_pending_work():
    db=Db()
    # qry="SELECT * FROM `work`  WHERE `work`.`status`='pending' and clerk_lid='"+str(session['lid'])+"'"
    qry="SELECT * FROM `work_report` JOIN `work`ON `work_report`.`work_id`=`work`.`work_id`JOIN`department`ON`work`.`dept_lid`=`department`.`dept_id` WHERE `work`.`status`='pending'"
    res=db.select(qry)
    return render_template("clerk/view_pending_work.html",data=res)

@app.route('/view_pending_works')
def view_pending_works():
    db=Db()
    qry="SELECT * FROM `work`  WHERE `work`.`status`='pending' and clerk_lid='"+str(session['lid'])+"'"
    # qry="SELECT * FROM `work_report` JOIN `work`ON `work_report`.`work_id`=`work`.`work_id`JOIN`department`ON`work`.`dept_lid`=`department`.`dept_id` WHERE `work`.`status`='pending'"
    res=db.select(qry)
    return render_template("clerk/view_wrk.html",data=res)


@app.route('/view_notifctn_frm_dept')
def view_notifctn_frm_dept():
    db=Db()
    qry="SELECT * FROM `notification` JOIN `department`ON `notification`.`from_lid`=`department`.`dept_id`"
    res=db.select(qry)
    return render_template("clerk/view_notificn_frm_dept.html",data=res)

@app.route('/view_not_frm_dept_search_post',methods=['post'])
def view_not_frm_dept_search_post():
    return render_template("clerk/view_notificn_frm_dept.html")








# .............................Android..................................................................

################user########

@app.route('/and_login_post',methods=['post'])
def and_login_post():
    username=request.form['username']
    password=request.form['password']
    db=Db()
    qry="SELECT * FROM `login` WHERE `uname`='"+username+"' AND `password`='"+password+"' "
    res=db.selectOne(qry)
    if res is None:
        return jsonify(status="no")
    else:
        return jsonify(status="ok",lid=res['login_id'],type=res['type'])

@app.route('/and_signup',methods=['post'])
def and_signup():
    name=request.form['name']
    dob=request.form['dob']
    email=request.form['email']
    gender=request.form['gender']
    phone=request.form['phone']
    area_name=request.form['area']
    hname=request.form['hname']
    place=request.form['place']
    city=request.form['city']
    pin=request.form['pin']
    district=request.form['district']
    photo=request.form['photo']

    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    import base64
    a = base64.b64decode(photo)
    fh = open("C:\\final\\prj\\web\\councilor_app\\static\\userimg\\" + date + ".jpg", "wb")
    path = "/static/userimg/" + date + ".jpg"
    fh.write(a)
    fh.close()
    # username=request.form['user']
    password=request.form['pass']

    db = Db()
    qry="INSERT INTO `login`(`uname`,`password`,`type`)VALUE('"+email+"','"+password+"','user')"
    res=db.insert(qry)
    qry1="INSERT INTO `user`(`u_name`,`gender`,`dob`,`email`,`phone`,`area_name`,`hname`,`place`,`city`,`pincode`,`district`,`photo`,`lid`)VALUE('"+name+"','"+gender+"','"+dob+"','"+email+"','"+phone+"','"+area_name+"','"+hname+"','"+place+"','"+city+"','"+pin+"','"+district+"','"+path+"','"+str(res)+"')"
    res1=db.insert(qry1)
    return jsonify(status="ok")




@app.route('/and_user_view_profile',methods=['post'])
def user_view_profile():
    db=Db()
    lid = request.form['lid']
    qry="select * from user WHERE lid='"+lid+"'"
    res=db.selectOne(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_update_profile',methods=['post'])
def and_update_profile():
    db=Db()
    lid=request.form['lid']
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    gender = request.form['gender']
    phone = request.form['phone']
    area_name = request.form['area']
    hname = request.form['hname']
    place = request.form['place']
    city = request.form['city']
    pin = request.form['pin']
    district = request.form['district']
    photo=request.form['photo']
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    import base64
    a = base64.b64decode(photo)
    fh = open("C:\\final\\prj\\web\\councilor_app\\static\\userimg\\" + date + ".jpg", "wb")
    path = "/static/userimg/" + date + ".jpg"
    fh.write(a)
    fh.close()
    qry="UPDATE `user` SET `u_name`='"+name+"',`gender`='"+gender+"',`dob`='"+dob+"',`email`='"+email+"',`phone`='"+phone+"',`area_name`='"+area_name+"',`hname`='"+hname+"',`place`='"+place+"',`city`='"+city+"',`pincode`='"+pin+"',`district`='"+district+"',`photo`='"+path+"',`lid`='"+lid+"' WHERE `user_id`='"+lid+"'"
    res=db.update(qry)
    return jsonify(status="ok")

@app.route('/user_change_pass_post',methods=['post'])
def user_change_pass_post():
    lid=request.form['lid']
    currentpw = request.form['currpass']
    newpw = request.form['newpass']
    confirmpw = request.form['confpass']
    db = Db()
    qry = "select * from login where password='" + currentpw + "'and login_id='" + lid+ "'"
    res = db.selectOne(qry)
    if res is not None:
        if newpw == confirmpw:
            qry = "update login set password='" + confirmpw + "'where login_id='" + lid + "'"
            res = db.update(qry)
            return jsonify(status="ok")
        else:
            return jsonify(status="not found")
    return jsonify(status="not found")


@app.route('/view_notifcatn_frm_mayor',methods=['post'])
def view_notifcatn_frm_mayo():
    db=Db()
    qry="SELECT * FROM `notification`JOIN `president` ON `notification`.`from_lid`=`president`.`lid`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/view_notification_frm_coun',methods=['post'])
def view_notification_frm_coun():
    db=Db()
    qry="SELECT * FROM`notification` INNER JOIN `councilor`ON `notification`.`from_lid`=`councilor`.`lid`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/and_view_dept', methods=['POST'])
def and_view_dept():
    db=Db()
    qry="SELECT * FROM `department`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/sent_applications_post',methods=['post'])
def sent_applications_post():
    db=Db()
    lid=request.form['lid']
    app_title=request.form['app_title']
    filename=request.form['filename']
    dept=request.form['dept']
    narration=request.form['narration']
    qry="INSERT INTO `application`(`app_title`,`filename`,`date`,`user_lid`,`dept_lid`,`status`,`narration`)VALUES('"+app_title+"','"+filename+"',curdate(),'"+lid+"','"+dept+"','pending','"+narration+"')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route('/view_applictn_status',methods=['post'])
def view_applictn_status():
    db=Db()
    lid = request.form['lid']
    qry = "SELECT `application`.*, `user`.*, `department`.`dept_name` FROM `application` INNER JOIN `user` ON `user`.`lid`=`application`.`user_lid` INNER JOIN `department` ON `department`.`dept_id`=`application`.`dept_lid` WHERE `application`.`user_lid`='"+str(lid)+"'"
    # qry="SELECT * FROM application INNER JOIN department ON department.`dept_id` = application.`dept_lid` INNER JOIN USER ON user.`lid` = application.user_lid WHERE application.lid = ''"
    res=db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)


@app.route('/add_dept_rating',methods=['post'])
def add_dept_rating():
    db=Db()
    lid=request.form['lid']
    dept=request.form['dept']
    rating=request.form['rating']
    review=request.form['review']
    qry="INSERT INTO `rating`(`dept_id`,`user_lid`,`rating`,`review`,`date`)VALUES('"+dept+"','"+lid+"','"+rating+"','"+review+"',curdate())"
    res=db.insert(qry)
    print(qry)
    return jsonify(status="ok")

@app.route('/send_pblm_to_counc',methods=['post'])
def send_pblm_to_counc():
    db=Db()
    lid=request.form['lid']
    pblm_title=request.form['pblm']
    description=request.form['desc']
    qry="INSERT INTO `problem`(`pblm_title`,`description`,`user_lid`,`date`,`status`)VALUES('"+pblm_title+"','"+description+"','"+lid+"',curdate(),'pending')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route('/view_send_pblm',methods=['post'])
def view_send_pblm():
    db=Db()
    lid = request.form['lid']
    qry = "SELECT * FROM `problem` WHERE `user_lid`='"+lid+"'"
    res=db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)

@app.route('/sent_feedback_post', methods=['POST'])
def sent_feedback_post():
    db=Db()
    lid=request.form['lid']
    feedback=request.form['feedback']
    qry="INSERT INTO `feedback`(`feedback`,`date`,`user_lid`)VALUES('"+feedback+"',curdate(),'"+lid+"')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route('/view_pjct_policies',methods=['post'])
def view_pjct_policies():
    db=Db()
    qry="SELECT * FROM `project_policies` JOIN `president`ON `project_policies`.`mayor_lid`=`president`.`lid`"
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/and_send_complaint', methods=['POST'])
def and_send_complaint():
    db=Db()
    lid=request.form['lid']
    dept=request.form['dept']
    complaint=request.form['complaint']
    qry="INSERT INTO `complaint`(`from_id`,`complaint`,`date`,`reply`,`dept_id`,`status`)VALUES('"+lid+"','"+complaint+"',curdate(),'pending','"+dept+"','pending')"
    res=db.insert(qry)
    return jsonify(status="ok")

@app.route('/and_view_complaint', methods=['POST'])
def and_view_complaint():
    db=Db()
    lid=request.form['lid']
    qry="SELECT * FROM `complaint` JOIN `user` ON `complaint`.`from_id`=`user`.`lid` JOIN `department`ON `complaint`.`dept_id`=`department`.`dept_id`WHERE `user`.`lid`='"+lid+"'"
    res=db.select(qry)
    return jsonify(status="ok",data=res)



if __name__ == '__main__':
    app.run(debug=True,port=4000,host="0.0.0.0")