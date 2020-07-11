from flask import request, Blueprint


helloWorld = Blueprint("helloWorld", __name__)

@helloWorld.route("/api/helloWorld", methods=["GET"])
def helloWorldRoute():
    return ("HelloWorld")