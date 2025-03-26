from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.users import UserRegister, UserLogin

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # 🔒 Clave secreta para firmar tokens
api = Api(app)
jwt = JWTManager(app)

# Rutas
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    app.run(debug=True)
