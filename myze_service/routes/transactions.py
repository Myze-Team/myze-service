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


    if res["Count"]:
        return json.dumps(res["Items"])
    else:
        return (jsonify("User has no transactions"), 404)

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

    if res["Count"]:
        return json.dumps(res["Items"])
    else:
        return (jsonify("Item has no transactions"), 404)


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
    data = request.get_json()
    if not data:
        return (jsonify("Bad Arguments"), 400)

    userId = data.get("userId")
    clothesId = data.get("clothesId")
    name = data.get("name")
    rating = data.get("rating")
    returned = data.get("returned")
    review = data.get("review")

    if not userId:
        return (jsonify("Missing argument 'userId'"), 400)

    if not clothesId:
        return (jsonify("Missing argument 'clothesId'"), 400)
    
    if not name:
        return (jsonify("Missing argument 'name'"), 400)
    
    if not rating:
        return (jsonify("Missing argument 'rating'"), 400)

    if returned is None:
        return (jsonify("Missing argument 'returned'"), 400)

    if not review:
        return (jsonify("Missing argument 'review'"), 400)

    transactionId = uuid.uuid4()

    client = db.get_client()

    """
    Check if user and clothing exists
    """
    user = client.get_item(
        TableName = "Profiles",
        Key = {
            "PK": {"S": "USER_" + userId},
            "SK": {"S": "USER_" + userId}
        }
    )

    if not user.get("Item"):
        return (jsonify("Could not add transaction"), 500)

    clothes = client.get_item(
        TableName = "Profiles",
        Key = {
            "PK": {"S": "CLOTHES_" + clothesId},
            "SK": {"S": "CLOTHES_" + clothesId}
        }
    )

    if not clothes.get("Item"):
        return (jsonify("Could not add transaction"), 500)


    """
    Is rating, returned, review required for user to put in?
    """


    """
    Adds transaction and increments count
    """
    try:
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
        return (jsonify("Successfully added transaction"), 200)
    except Exception as e:
        print (e)
        return (jsonify("Could not add transaction"), 500)
