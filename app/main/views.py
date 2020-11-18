import os
from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import AddPostForm
from datetime import datetime
from .. import db,photos
from app.models import Case,User,Role,Status
from flask_login import login_required

# views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    cases = Case.query.order_by(Case.category)
    return render_template('index.html',cases=cases)

@main.route("/Add/case/",methods = ["GET","POST"])
@login_required
def case():
    form = AddPostForm()
    title = "Add Post"
    if form.validate_on_submit():
        category = form.category.data
        title = form.title.data
        description = form.description.data
        geolocation = form.geolocation.data
        status_id = 1

        if "photo" in request.files:
            pic = photos.save(request.files["photo"])
            file_path = f"photos/{pic}"
            image = file_path
        post = Case(category = category, title = title, description=description, geolocation=geolocation, image = image, status_id=status_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".dashboard"))
        
        
    return render_template("add_incidences.html",form = form,title = title)

@main.route('/map/<string:place>',methods=['GET','POST'])
def map(place):

    return render_template('add_incidence.html',place=place)

@main.route('/dashboard')
def dashboard():

    '''
    View root page function that returns the dashboard page and its data
    '''
    cases = Case.query

    return render_template('dashboard.html', cases=cases)

@main.route("/post/<int:id>",methods = ["GET","POST"])
def post_page(id):
    post = Case.query.filter_by(id = id).first()
    
    return render_template("display.html", post = post)
 
@main.route("/delete/case/<id>")
def delete_case(id):
    case = Case.query.filter_by(id = id).first()
    case_id = case.id
    db.session.delete(case)
    db.session.commit()
    return redirect(url_for(".dashboard"))

@main.route('/status', methods=["GET", "POST"] )
def status():

    '''
    View root page function that returns the index page and its data
    '''
    state= request.form.get("state")
    new_status=Status(status=state)
    db.session.add(new_status)
    db.session.commit()

    return render_template("edit_incidences.html")