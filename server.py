from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource

app = Flask(__name__)
api = Api(app)
docs = FlaskApiSpec(app)


todos = {"1":"abc"}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in todos.keys():
        abort(404, message="Todo {} doesn't exist".format(todo_id))

class TodoSimple(MethodResource, Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {todo_id: todos[todo_id]}, 200

    def put(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        #todos[todo_id] = request.form['data']
        todos[todo_id]  = request.json["data"]
        return {todo_id: todos[todo_id]}, 201

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        todos.pop(todo_id)
        return {}, 204

class TodoList(MethodResource, Resource):
    def get(self):
        return todos, 200

    def post(self):
        todo_id = str(int(max(todos.keys())) + 1)
        todos[todo_id] = request.json['data']
        return todos[todo_id], 201

api.add_resource(TodoList, '/todos')
api.add_resource(TodoSimple, '/todos/<todo_id>')

docs.register(TodoList)
docs.register(TodoSimple)

if __name__ == '__main__':
    app.run(debug=True)