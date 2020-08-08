from flask import request, Blueprint, jsonify
import boto3
from botocore.exceptions import ClientError
import uuid
import json
from .. import db


clothingBlueprint = Blueprint("clothingBlueprint", __name__)

"""
Get data associated with a clothing id.
"""
@clothingBlueprint.route("/<id>", methods=["GET"])
def get_cloth(id):
    client = db.get_client()
    
    
    res = client.get_item(
        TableName = "Profiles",
        Key = {
            "PK": {"S": "CLOTHES_" + str(id)},
            "SK": {"S": "CLOTHES_" + str(id)},
        }
    )


    if res.get("Item"):
        return json.dumps(res["Item"])
    else:
        return (jsonify("Item not found"), 404)

"""
Create new clothing item.
Expects body to contain
name: name of clothing
brand: brand of clothing
type: type of clothing
price: price of clothing
size: size of clothing
category: category of clothing

"""
@clothingBlueprint.route("/new", methods=["POST"])
def create_cloth():
    data = request.get_json()
    if not data:
        return (jsonify("Bad Arguments"), 400)

    name = data.get("name")
    brand = data.get("brand")
    category = data.get("category")
    price = data.get("price")
    size = data.get("size")

    if not name:
        return (jsonify("Missing argument 'name'"), 400)
    
    if not brand:
        return (jsonify("Missing argument 'brand'"), 400)
    
    if not category:
        return (jsonify("Missing argument 'category'"), 400)
    
    if not price:
        return (jsonify("Missing argument 'price'"), 400)
    
    if not size:
        return (jsonify("Missing argument 'size'"), 400)

    client = db.get_client()

    clothingId = uuid.uuid4()


    """
    Add the item's metadata and clothing brand. Should fail if item already exists.
    Still adds if item exists but different item size.
    """
    try:
        res = client.transact_write_items(
            TransactItems = [
                {
                    "Put": {
                        "TableName": "Profiles",
                        "ConditionExpression": "attribute_not_exists(PK)",
                        "Item": {
                            "PK": {"S": "CLOTHES_" + str(clothingId)},
                            "SK": {"S": "CLOTHES_" + str(clothingId)},
                            "Item-Size-GSI": {"S": "SIZE_" + size},
                            "name": {"S": name},
                            "brand": {"S": brand},
                            "category": {"S": category},
                            "price": {"S": price},
                            "count": {"N": "0"}
                        }
                    }
                },
                {
                    "Update": {
                        "TableName": "Profiles",
                        "UpdateExpression": "SET size.#measurement = :id",
                        "ExpressionAttributeNames": {
                            "#measurement": size
                        },
                        "ExpressionAttributeValues": {
                            ":id": {"S": "CLOTHES_" + str(clothingId)},
                        },
                        "Key": {
                            "PK": {"S": "BRAND_" + brand},
                            "SK": {"S": name },
                        },
                        "ConditionExpression": "attribute_not_exists(size.#measurement)"
                    }
                }
            ]
        )
        return (jsonify("Successfully added clothing"), 200)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            res = client.transact_write_items(
                TransactItems = [
                    {
                        "Put": {
                            "TableName": "Profiles",
                            "ConditionExpression": "attribute_not_exists(PK)",
                            "Item": {
                                "PK": {"S": "CLOTHES_" + str(clothingId)},
                                "SK": {"S": "CLOTHES_" + str(clothingId)},
                                "Item-Size-GSI": {"S": "SIZE_" + size},
                                "name": {"S": name},
                                "brand": {"S": brand},
                                "category": {"S": category},
                                "price": {"S": price},
                                "count": {"N": "0"}
                            }
                        }
                    },
                    {
                        "Update": {
                            "TableName": "Profiles",
                            "UpdateExpression": "SET #size = :value",
                            "ExpressionAttributeNames": {
                                "#size": "size"
                            },
                            "ExpressionAttributeValues": {
                                ":value": {"M" : {
                                    size: {"S": "CLOTHES_" + str(clothingId)}
                                }},
                            },
                            "Key": {
                                "PK": {"S": "BRAND_" + brand},
                                "SK": {"S": name },
                            }
                        }
                    }
                ]
            )
            return (jsonify("Successfully added clothing"), 200)
        else:
            return (jsonify("Could not add clothing"), 500)
    except Exception as e:
        return (jsonify("Could not add clothing"), 500)

    
    


"""
Get names of all items from a certain brand along with size option available for that item
"""
@clothingBlueprint.route("/names", methods=["GET"])
def get_names():
    brand = request.args.get("brand")

    if not brand:
        return (jsonify("Missing argument 'brand'"), 400)

    client = db.get_client()

    res = client.query(
        TableName = "Profiles",
        KeyConditionExpression = "#pkey = :pkey",
        ExpressionAttributeNames = {"#pkey":"PK"},
        ExpressionAttributeValues = {":pkey": {"S":"BRAND_" + brand}}
    )

    if res["Count"]:
        return json.dumps(res["Items"])
    else:
        return (jsonify("Brand not found"), 404)

"""
Get all items of a specified size
"""
@clothingBlueprint.route("/size/<size>", methods=["GET"])
def get_clothes_by_size(size):
    if not size:
        return (jsonify("Bad Arguments"), 400)
    
    client = db.get_client()

    res = client.query(
        TableName = "Profiles",
        IndexName = "Item-Size-GSI",
        KeyConditionExpression ="#pkey = :pkey",
        ExpressionAttributeNames = {"#pkey": "Item-Size-GSI"},
        ExpressionAttributeValues = {":pkey": {"S":"SIZE_" + size}}
    )

    
    return res