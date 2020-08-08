import unittest
import warnings
import json
from ...__init__ import create_app
from ...db import init_table

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test


class GetUsersTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    @ignore_warnings
    def test_nonexisting_item(self):
        response = self.app.get("/users/123")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User not found", data)


    @ignore_warnings
    def test_existing_user(self):
        response = self.app.get("/users/1")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual({"S": "USER_1"}, data["PK"])
        self.assertEqual({"S": "USER_1"}, data["SK"])
        self.assertEqual({"S": "male"}, data["gender"])


class CreateUsersTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    
    @ignore_warnings
    def test_missing_args(self):
        response = self.app.post("/users/new")
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Bad Arguments", data)

    
        """
        test missing userid
        """
        payload = {
            "gender": "male"
        }
        response = self.app.post("/users/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'userId'", data)


        """
        test missing gender
        """
        payload = {
            "userId": "123"
        }
        response = self.app.post("/users/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'gender'", data)

    
    @ignore_warnings
    def test_fail_when_existing_userId(self):
        payload = {
            "userId": "1",
            "gender": "male"
        }
        response = self.app.post("/users/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(500, response.status_code)
        self.assertEqual("Could not add user", data)

    
    @ignore_warnings
    def test_create_nonexisting_userId(self):
        payload = {
            "userId": "123",
            "gender": "male"
        }
        response = self.app.post("/users/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertEqual("Successfully created user", data)
