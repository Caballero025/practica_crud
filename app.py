import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

#Cargar las variables de entorno
load_dotenv()

#Crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    categoria = db.Column(db.String)
    precio = db.Column(db.String)
    cantidad_stock = db.Column(db.Integer)

    def to_dict(self):
        return{
            'id ':self.id ,
            'nombre':self.nombre,
            'descripcion':self.descripcion,
            'categoria':self.categoria,
            'precio':self.precio,
            'cantidad_stock':self.cantidad_stock,
        }
 

#Ruta raiz
@app.route('/')
def index():
    #Trae todos los alumnos
    productos = Productos.query.all()
    return render_template('index.html', productos = productos)

#Ruta productos crear un nuevo producto 
@app.route('/productos/new', methods=['GET','POST'])
def create_producto():
     if request.method == 'POST':
         #Agregar Alumno 
         id = request.form['id']
         nombre = request.form['nombre']
         descripcion = request.form['descripcion']
         categoria = request.form['categoria']
         precio = request.form['precio']
         cantidad_stock = request.form['cantidad_stock']

         nvo_producto = Productos(id = id, nombre = nombre,descripcion = descripcion, categoria = categoria, precio = precio, cantidad_stock = cantidad_stock)

         db.session.add(nvo_producto)
         db.session.commit()
         return redirect(url_for('index'))
     #Aqui sigue si es GET
     return render_template('create_producto.html')

#Eliminar producto
@app.route('/productos/delete/<int:id>')
def delete_producto(id):
    producto = Productos.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))

#AActualizar alumno
@app.route('/productos/update/<int:id>', methods=['GET','POST'])
def update_producto(id):
    producto = Productos.query.get(id)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.categoria = request.form['categoria']
        producto.precio = request.form['precio']
        producto.cantidad_stock = request.form['cantidad_stock']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_producto.html',producto = producto)
 

if __name__ == '__main__':
    app.run(debug=True)