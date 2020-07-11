import os
import json
from flask import Flask
from flask import request
from werkzeug.security import generate_password_hash
#from werkzeug.security import check_password_hash
from cerberus import Validator

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    dynamodb = db.get_db()
    table = dynamodb.Table('Profiles')

    @app.route('/users', methods=['GET', 'POST'])
    def get_items():
        if request.method == 'GET':
            return json_response(table.scan()['Items'])
        else:
            # add custom email validation
            v = Validator({
                'email': {'type': 'string', 'required': True},
                'password':{'type': 'string', 'required': True, 'minlength': 8}
            })

            body = {
                'email': request.args.get('email'),
                'password': request.args.get('password')
            }

            if v.validate(body):
                # add unique email check
                table.put_item(
                    Item={
                        'id': str(table.item_count),
                        'email': body['email'],
                        'password': generate_password_hash(body['password'])
                    }
                )
                return {"message": "student entry created"}
            else:
                return {"message": v.errors}
  
    return app


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}