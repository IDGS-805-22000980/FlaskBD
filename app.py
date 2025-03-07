from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from models import db
from models import Alumnos
import forms


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm2(request.form) 
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)


@app.route("/detalles")
def detalles():
    create_form =forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nom=alum.nombre
        ape=alum.apaterno
        email=alum.email
        return render_template("detalles.html", form=create_form, nom=nom, ape=ape, email=email)
    
#Insertar Nuevo Alumno
@app.route("/Alumnos1", methods=['GET', 'POST'])
def Alumnos1():
    create_form = forms.UserForm2(request.form)
    if request.method == 'POST':
        alum=Alumnos(nombre=create_form.nombre.data,
                    apaterno=create_form.apaterno.data,
                    email=create_form.email.data)
        #Insertar alumnos() values()
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos1.html", form=create_form)

#Modificar Alumno
@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()  
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = str.rstrip(alum.nombre)
        create_form.apaterno.data = alum.apaterno
        create_form.email.data = alum.email
    if request.method == 'POST':
        id=create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum.nombre = str.rstrip(create_form.nombre.data)
        alum.apaterno = create_form.apaterno.data
        alum.email = create_form.email.data
        db.session.add(alum)
        db.session.commit()  
        flash("Alumno actualizado correctamente")
        return redirect(url_for('index'))
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        # select * from alumnos where id==id
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum.nombre
        create_form.apaterno.data=alum.apaterno
        create_form.email.data=alum.email
    if request.method == 'POST':
        id=create_form.id.data
        alum = Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html", form=create_form)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()