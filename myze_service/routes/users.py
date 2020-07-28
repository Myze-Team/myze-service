from flask import request, Blueprint, jsonify
from .. import db


userBlueprint = Blueprint("userBlueprint", __name__)


"""
Get data associated with a user id.
"""
@userBlueprint.route("/<id>", methods=["GET"])
def get_user(id):
    client = db.get_client()

    res = client.get_item(
        TableName = "Profiles",
        Key = {
            "PK": {"S": "USER_" + str(id)},
            "SK": {"S": "USER_" + str(id)},
        }
    )

    return res

"""
Create new user
Expects body to contain
userId: user id from cognition
gender: gender of user
"""
@userBlueprint.route("/new", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return (jsonify("Bad Arguments"), 400)

    userId = data.get("userId")
    gender = data.get("gender")

    if not userId:
        return (jsonify("Bad Arguments"), 400)

    if not gender:
        return (jsonify("Bad Arguments"), 400)

    client = db.get_client()

    res = client.put_item(
        TableName = "Profiles",
        ConditionExpression = "attribute_not_exists(PK)",
        Item = {
            "PK": {"S": "USER_" + str(userId)},
            "SK": {"S": "USER_" + str(userId)},
            "gender": {"S": gender}
        }
    )

    return res
