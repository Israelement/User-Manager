from flask import Flask, request
import json
from types import SimpleNamespace

#Creamos la aplicación
app = Flask(__name__)

#Menú principal
@app.route("/")
def menu():
  return """
        <h1>Menú de administración de usuarios:</h1>
        <ul>
            <li><h2><a href='/agregar_usuario'>Agregar Usuario</a></h2></li> 
            <li><h2><a href='/lista_usuarios'>Ver Usuarios</a></h2></li>
        </ul>
    """

#Página para añadir usuarios
@app.route("/agregar_usuario", methods=["GET", "POST"])
def agregar_usuario():
  if request.method == "POST": #Método que crea un diccionario con los datos del nuevo usuario
        nuevo_usuario = {
            "email": request.form["email"],
            "nombre": request.form["nombre"],
            "apellidos": request.form["apellidos"],
            "contraseña": request.form["contraseña"],
            "telefono": request.form["telefono"],
            "edad": request.form["edad"]
        }
    # Guardar en archivo JSON
        try:
            with open("usuarios.json", "r") as file: #Esto carga el archivo jJSON donde se guardan los usuarios
                usuarios = json.load(file)
        except FileNotFoundError:
            usuarios = []

        usuarios.append(nuevo_usuario) #Añadimos el suuario

        with open("usuarios.json", "w") as file: #Guardamos el usuario en el JSON
            json.dump(usuarios, file, indent=4)

        return "<h1>Usuario agregado con éxito</h1><a href='/'>Volver al menú</a>"
  
  #Formulario HTML para la parte visual de recoger los datos de usuario
  return """
        <h1>Agregar Usuario</h1>
        <form action="" method="post">
            <label>Email:</label> <input type="text" name="email" required><br>
            <label>Nombre:</label> <input type="text" name="nombre" required><br>
            <label>Apellidos:</label> <input type="text" name="apellidos" required><br>
            <label>Contraseña:</label> <input type="password" name="contraseña" required><br>
            <label>Teléfono:</label> <input type="text" name="telefono" required><br>
            <label>Edad:</label> <input type="number" name="edad" required><br>
            <input type="submit" value="Registrar">
        </form>
        <br><a href='/'>Volver al menú</a>
    """

#Página para ver listado de usuarios
@app.route("/lista_usuarios")
def lista_usuarios():
  try:
        with open("usuarios.json", "r") as file:
            usuarios = json.load(file)  # Cargamos el archivo con los usuarios del JSON
  except FileNotFoundError:
      usuarios = []  

  tabla = "<h1>Lista de Usuarios</h1><table border='1'><tr><th>Nombre</th><th>Apellidos</th><th>Email</th><th>Teléfono</th><th>Edad</th><th>Acciones</th></tr>"
  
  #ESto nos muestra los ususarios en la tabla que acabamos de crear
  for i, usuario in enumerate(usuarios):
        tabla += f"<tr><td>&nbsp{usuario['nombre']}</td><td>&nbsp{usuario['apellidos']}</td><td>&nbsp{usuario['email']}</td><td>&nbsp{usuario['telefono']}&nbsp</td><th>{usuario['edad']}</th>"
        tabla += f"<td>&nbsp<a href='/editar_usuario/{i}'>Editar</a> &nbsp <a href='/eliminar_usuario/{i}'>Eliminar</a>&nbsp</td></tr>"

  tabla += "</table><br><a href='/'>Volver al menú</a>"
    
  return tabla

#Página en la que podremos editar el usuario
@app.route("/editar_usuario/<int:index>", methods=["GET", "POST"])
def editar_usuario(index):
    try:
        with open("usuarios.json", "r") as file:
            usuarios = json.load(file)       # Cargamos el archivo con los usuarios del JSON
    except FileNotFoundError:
        return "<h1>Error: No hay usuarios registrados</h1><a href='/'>Volver al menú</a>"

    # Verificamos que el índice existe en la lista
    if index < 0 or index >= len(usuarios):
        return "<h1>Error: Usuario no encontrado</h1><a href='/lista_usuarios'>Volver a la lista</a>"

    usuario = usuarios[index]  

    if request.method == "POST":
        # Actualizamos los datos del usuario
        usuario_actualizado = {
            "email": request.form["email"],
            "nombre": request.form["nombre"],
            "apellidos": request.form["apellidos"],
            "contraseña": request.form["contraseña"],
            "telefono": request.form["telefono"],
            "edad": request.form["edad"]
        }

        usuarios[index] = usuario_actualizado  # Actualizamos el usuario en la lista

        with open("usuarios.json", "w") as file:
            json.dump(usuarios, file, indent=4)  # Guardamos los cambios en  el JSON

        return "<h1>Usuario actualizado con éxito</h1><a href='/lista_usuarios'>Volver a la lista</a>"

    #Formulario HTML para la parte visual para editar los datos del usuario
    return f"""
        <h1>Editar Usuario</h1>
        <form action="" method="post">
            <label>Email:</label> <input type="text" name="email" value="{usuario['email']}" required><br>
            <label>Nombre:</label> <input type="text" name="nombre" value="{usuario['nombre']}" required><br>
            <label>Apellidos:</label> <input type="text" name="apellidos" value="{usuario['apellidos']}" required><br>
            <label>Contraseña:</label> <input type="password" name="contraseña" value="{usuario['contraseña']}" required><br>
            <label>Teléfono:</label> <input type="text" name="telefono" value="{usuario['telefono']}" required><br>
            <label>Edad:</label> <input type="number" name="edad" value="{usuario['edad']}" required><br>
            <input type="submit" value="Guardar Cambios">
        </form>
        <br><a href='/lista_usuarios'>Volver a la lista</a>
    """

#Página en la que se ejecuta el borrar usuario
@app.route("/eliminar_usuario<int:index>")
def eliminar_usuario(index):
  try:
      with open("usuarios.json", "r") as file:
            usuarios = json.load(file)     # Cargamos el archivo con los usuarios del JSON
  except FileNotFoundError:
        usuarios = []

  if 0 <= index < len(usuarios):
      usuarios.pop(index)  # Borra el usuario en la posición index
        
      with open("usuarios.json", "w") as file:
          json.dump(usuarios, file, indent=4)

  return "<h1>Usuario eliminado con éxito</h1><a href='/lista_usuarios'>Volver a la lista</a>"

app.run()
