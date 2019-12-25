from app import injector
from connexion import NoContent
from injector import inject
from services.todo_list import TodoListFeed


class TodoList(object):

    @inject
    def __init__(self, db: TodoListFeed):
        self._db = db

    def get_todo_lists(self, limit):

        result = self._db.fetch_todo_lists(limit)
        return result

    def create_todo_list(self, todo_list: dict):

        result = self._db.create_todo_list(todo_list)
        if result.get('error'):
            return result, 400
        else:
            return result, 201

    def get_todo_list(self, todo_list_id: str):

        result = self._db.fetch_todo_list({'id': todo_list_id})
        if result.get('error'):
            return result, 404
        else:
            return result, 200

    def put_todo_list(self, todo_list_id: str, todo_list: dict):

        todo_list['id'] = todo_list_id
        result = self._db.put_todo_list(todo_list)
        if result.get('error'):
            return result, 404
        elif result.get('updated'):
            return result, 200
        else:
            return result, 201

    def delete_todo_list(self, todo_list_id: str):

        result = self._db.delete_todo_list({'id': todo_list_id})
        if result:
            return NoContent, 204
        else:
            return NoContent, 404

    def create_todo_list_item(self, todo_list_id: str, todo_list_item: dict):

        result = self._db.create_todo_list_item(
            todo_list_id, todo_list_item)
        if result.get('error'):
            return result, 404

        return result, 200

    def put_todo_list_item(self, todo_list_id: str, todo_list_item_id: str,
                           todo_list_item: dict):

        result = self._db.put_todo_list_item(
            todo_list_id, todo_list_item_id, todo_list_item)
        if result.get('error'):
            return result, 404
        elif result.get('updated'):
            return result, 200
        else:
            return result, 201

    def delete_todo_list_item(self, todo_list_id: str, todo_list_item_id: str):

        result = self._db.delete_todo_list_item(
            todo_list_id, todo_list_item_id)
        if result:
            return NoContent, 204
        else:
            return NoContent, 404


class_instance = injector.get(TodoList)
