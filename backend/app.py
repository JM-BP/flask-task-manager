from flask import Flask
from flask_restful import Api
from resources.users import UserRegister

app = Flask(__name__)
api = Api(app)

# Ruta para registrar usuarios
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(debug=True)
