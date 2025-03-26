from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import User

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('password', type=str, required=True, help="Este campo no puede estar vacío")

    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.find_by_username(data['username'])

        if user and user.verify_password(data['password']):
            access_token = create_access_token(identity=str(user.id))  # Convertimos user.id a string
            return {"access_token": access_token}, 200
        
        return {"message": "Credenciales inválidas"}, 401


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('password', type=str, required=True, help="Este campo no puede estar vacío")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "Usuario ya existe"}, 400

        User.create_user(data['username'], data['password'])
        return {"message": "Usuario creado exitosamente"}, 201
