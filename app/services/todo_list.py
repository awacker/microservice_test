import datetime

from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from lib.mongo import Feed

error_msg = dict(
    duplicate='Duplicate name value',
    invalid_id='Invalid identifier',
    not_found='Object not found'
)


def _encode(item):
    _id = item.pop('_id', None)
    if _id:
        item['id'] = str(_id)
    return item


class TodoListFeed(Feed):

    def fetch_todo_lists(self, limit=100) -> list:

        collection = self.collection()
        _list = collection.find({}, {'items': False}).limit(limit)

        return [_encode(i) for i in _list]

    def create_todo_list(self, obj: dict) -> dict:

        collection = self.collection()
        try:
            collection.insert_one(obj)
        except DuplicateKeyError:
            return {'error': error_msg['duplicate']}

        return _encode(obj)

    def fetch_todo_list(self, obj) -> dict:

        collection = self.collection()
        _id = obj.pop('id')
        if not all([_id, ObjectId.is_valid(_id)]):
            return {'error': error_msg['invalid_id']}

        result = collection.find_one({'_id': ObjectId(_id)})

        if not result:
            return {'error': error_msg['not_found']}

        return _encode(result)

    def put_todo_list(self, obj) -> dict:
        collection = self.collection()

        _id = obj.pop('id')
        if not all([_id, ObjectId.is_valid(_id)]):
            return {'error': error_msg['not_found']}

        obj['_id'] = ObjectId(_id)
        try:
            result = collection.replace_one(
                {'_id': ObjectId(_id)},
                obj,
                upsert=True
            )
        except DuplicateKeyError:
            return {'error': error_msg['duplicate']}

        obj['updated'] = result.matched_count == 1
        return _encode(obj)

    def delete_todo_list(self, obj) -> bool:

        collection = self.collection()
        _id = obj.pop('id')
        if not all([_id, ObjectId.is_valid(_id)]):
            return False

        result = collection.delete_one({'_id': ObjectId(_id)})

        return result.deleted_count == 1

    def create_todo_list_item(self, todo_list_id, obj) -> dict:

        collection = self.collection()
        if not ObjectId.is_valid(todo_list_id):
            return {'error': error_msg['invalid_id']}

        gen_time = datetime.datetime.now()
        obj['item_id'] = str(ObjectId.from_datetime(gen_time))

        collection.update_one(
            {'_id': ObjectId(todo_list_id)},
            {'$push': {'items': obj}}
        )
        return obj

    def put_todo_list_item(self, todo_list_id, todo_list_item_id,
                           obj) -> dict:

        collection = self.collection()
        if not all([ObjectId.is_valid(todo_list_id),
                    ObjectId.is_valid(todo_list_item_id)]):
            return {'error': error_msg['not_found']}

        obj['item_id'] = todo_list_item_id
        result = collection.update_one(
            {'_id': ObjectId(todo_list_id),
             'items.item_id': todo_list_item_id},
            {'$set': {'items.$': obj}}
        )
        if result.matched_count == 0:
            collection.update_one(
                {'_id': ObjectId(todo_list_id)},
                {'$push': {'items': obj}}
            )

        obj['updated'] = result.matched_count == 1
        return _encode(obj)

    def delete_todo_list_item(self, todo_list_id,
                              todo_list_item_id) -> bool:

        collection = self.collection()
        if not all([ObjectId.is_valid(todo_list_id),
                    ObjectId.is_valid(todo_list_item_id)]):
            return False

        result = collection.update_one(
            {'_id': ObjectId(todo_list_id),
             'items.item_id': todo_list_item_id},
            {'$pull': {'items': {'item_id': todo_list_item_id}}}
        )
        return result.matched_count == 1
