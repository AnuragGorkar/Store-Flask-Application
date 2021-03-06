from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.itemModel import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type= float,
            required = True,
            help = "Thie price field cannot be left blank"
        )
    parser.add_argument('store_id',
            type= int,
            required = True,
            help = "Thie store_id field cannot be left blank"
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message' : "Item not found"}, 404

        
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message' : f"An item with name {name} already exists."}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name,**data)
        
        try:
            item.save_to_db()
        except:
            return {'message' : "An error occured while inserting an item."}, 500
    
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'message' : f"Item {name} deleted."}
        else:
            return {'message' : f"Item {name} cannot be found in database."}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        
        return item.json()

    
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}