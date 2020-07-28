from flask import request, Blueprint, jsonify
import json
import uuid
from .. import db

transactionBlueprint = Blueprint("transactionBlueprint", __name__)

"""
Get all transaction information made by a user. (All items bought by user)
"""
@transactionBlueprint.route("/user/<id>", methods=["GET"])
def get_transaction_by_user(id):
    client = db.get_client()

    res = client.query(
        TableName = "Profiles",
        KeyConditionExpression = "#pkey = :pkey And begins_with(#skey, :skey)",
        ExpressionAttributeNames = {"#pkey":"PK","#skey":"SK"},
        ExpressionAttributeValues = {":pkey": {"S":"USER_" + str(id)},":skey": {"S":"TRANSACTION_"}}
    )

    return res

"""
Get all transaction information by clothing id. (All users who bought clothing)
"""
@transactionBlueprint.route("/clothes/<id>", methods=["GET"])
def get_transaction_by_item(id):
    client = db.get_client()

    res = client.query(
        TableName = "Profiles",
        IndexName = "User-Item-GSI",
        KeyConditionExpression ="#pkey = :pkey",
        ExpressionAttributeNames = {"#pkey": "User-Item-GSI"},
        ExpressionAttributeValues = {":pkey": {"S":"CLOTHES_" + str(id)}}
    )

    return res

"""
Add a new transaction.
Expects query parameters to contain
userId: id of user in transaction
clothesId: id of clothing in transaction

Expects body to contain
name: name of clothing
review: review of item
returned: whether or not the item was returned
rating: the rating user gave product
"""
@transactionBlueprint.route("/new", methods=["POST"])
def create_transaction():
    userId = request.args.get("userId")
    clothesId = request.args.get("clothesId")

    if not userId:
        return (jsonify("Bad Arguments"), 400)

    if not clothesId:
        return (jsonify("Bad Arguments"), 400)

    data = request.get_json()
    if not data:
        return (jsonify("Bad Arguments"), 400)

    name = data.get("name")
    rating = data.get("rating")
    returned = data.get("returned")
    review = data.get("review")
    
    if not name:
        return (jsonify("Bad Arguments"), 400)
    
    if not rating:
        return (jsonify("Bad Arguments"), 400)

    if returned is None:
        return (jsonify("Bad Arguments"), 400)

    if not review:
        return (jsonify("Bad Arguments"), 400)

    transactionId = uuid.uuid4()

    client = db.get_client()

    """
    Is rating, returned, review required for user to put in?
    """
    res = client.put_item(
        TableName = "Profiles",
        Item = {
            "PK": {"S": "USER_" + userId},
            "SK": {"S": "TRANSACTION_" + str(transactionId)},
            "User-Item-GSI": {"S": "CLOTHES_" + clothesId},
            "ClothesName": {"S": name},
            "returned": {"BOOL": returned},
            "rating": {"N": str(rating)},
            "review": {"S": review}
        }
    )

    """
    Adds transaction and increments count
    """
    res = client.transact_write_items(
        TransactItems = [
            {
                "Put": {
                    "TableName": "Profiles",
                    "Item": {
                        "PK": {"S": "USER_" + userId},
                        "SK": {"S": "TRANSACTION_" + str(transactionId)},
                        "User-Item-GSI": {"S": "CLOTHES_" + clothesId},
                        "ClothesName": {"S": name},
                        "returned": {"BOOL": returned},
                        "rating": {"N": str(rating)},
                        "review": {"S": review}
                    }
                }
            },
            {
                "Update": {
                    "TableName": "Profiles",
                    "Key": {
                        "PK": {"S": "CLOTHES_" + clothesId},
                        "SK": {"S": "CLOTHES_" + clothesId},
                    },
                    "UpdateExpression": "ADD #count :increment",
                    "ExpressionAttributeNames": {
                        "#count": "count"
                    },
                    "ExpressionAttributeValues": {
                        ":increment": {"N": "1"}
                    }
                    
                }
            }
        ]
    )

    return res