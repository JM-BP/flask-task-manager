from flask_restful import Resource, reqparse
from models.user import User

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
