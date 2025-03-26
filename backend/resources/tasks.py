from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task import Task

class TaskResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="El título no puede estar vacío")
    parser.add_argument('description', type=str, required=False)

    @jwt_required()
    def get(self, task_id=None):
        user_id = get_jwt_identity()
        if task_id:
            task = Task.get_task_by_id(task_id, user_id)
            if task:
                return {"id": task.id, "title": task.title, "description": task.description}, 200
            return {"message": "Tarea no encontrada"}, 404
        tasks = Task.get_tasks_by_user(user_id)
        return [{"id": task.id, "title": task.title, "description": task.description} for task in tasks], 200

    @jwt_required()
    def post(self):
        data = TaskResource.parser.parse_args()
        user_id = get_jwt_identity()
        task = Task.create_task(data['title'], data['description'], user_id)
        return {"id": task.id, "title": task.title, "description": task.description}, 201

    @jwt_required()
    def put(self, task_id):
        data = TaskResource.parser.parse_args()
        user_id = get_jwt_identity()
        task = Task.get_task_by_id(task_id, user_id)
        if task:
            task.update_task(data['title'], data['description'])
            return {"message": "Tarea actualizada", "task": {"id": task.id, "title": task.title, "description": task.description}}, 200
        return {"message": "Tarea no encontrada"}, 404

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.get_task_by_id(task_id, user_id)
        if task:
            task.delete_task()
            return {"message": "Tarea eliminada"}, 200
        return {"message": "Tarea no encontrada"}, 404