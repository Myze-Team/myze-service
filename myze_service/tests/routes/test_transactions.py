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


class GetTransactionsByUserTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()


    @ignore_warnings
    def test_nonexisting_user(self):
        response = self.app.get("transactions/user/123")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User has no transactions", data)


    @ignore_warnings
    def test_nonexisting_transactions(self):
        response = self.app.get("transactions/user/2")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("User has no transactions", data)


    @ignore_warnings
    def test_existing_user_and_transaction(self):
        response = self.app.get("transactions/user/1")
        data = json.loads(response.data)


        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))
        self.assertEqual({"S": "USER_1"}, data[0]["PK"])
        self.assertEqual({"S": "TRANSACTION_1"}, data[0]["SK"])
        self.assertEqual({"N": "0"}, data[0]["rating"])
        self.assertEqual({"BOOL": True}, data[0]["returned"])
        self.assertEqual({"S": "CLOTHES_1"}, data[0]["User-Item-GSI"])
        self.assertEqual({"S": "team knit short"}, data[0]["ClothesName"])
        self.assertEqual({"S": "doesn't fit"}, data[0]["review"])

        self.assertEqual({"S": "USER_1"}, data[1]["PK"])
        self.assertEqual({"S": "TRANSACTION_2"}, data[1]["SK"])
        self.assertEqual({"N": "0"}, data[1]["rating"])
        self.assertEqual({"BOOL": False}, data[1]["returned"])
        self.assertEqual({"S": "CLOTHES_3"}, data[1]["User-Item-GSI"])
        self.assertEqual({"S": "dry academy pro pullover hoodie"}, data[1]["ClothesName"])
        self.assertEqual({"S": "fits nice"}, data[1]["review"])


class GetTransactionsByClothesTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    @ignore_warnings
    def test_nonexisting_clothes(self):
        response = self.app.get("transactions/clothes/123")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Item has no transactions", data)


    @ignore_warnings
    def test_nonexisting_transactions(self):
        response = self.app.get("transactions/clothes/2")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Item has no transactions", data)

    @ignore_warnings
    def test_existing_clothes_and_transaction(self):
        response = self.app.get("transactions/clothes/1")
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(data))
        self.assertEqual({"S": "USER_1"}, data[0]["PK"])
        self.assertEqual({"S": "TRANSACTION_1"}, data[0]["SK"])
        self.assertEqual({"N": "0"}, data[0]["rating"])
        self.assertEqual({"BOOL": True}, data[0]["returned"])
        self.assertEqual({"S": "CLOTHES_1"}, data[0]["User-Item-GSI"])
        self.assertEqual({"S": "team knit short"}, data[0]["ClothesName"])
        self.assertEqual({"S": "doesn't fit"}, data[0]["review"])


class CreateClothingsTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    
    @ignore_warnings
    def test_missing_args(self):
        response = self.app.post("/transactions/new")
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Bad Arguments", data)

        """
        test missing userId
        """
        payload = {
            "clothesId": "2",
            "name": "team knit short",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'userId'", data)

        """
        test missing clothesId
        """
        payload = {
            "userId": "3",
            "name": "team knit short",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'clothesId'", data)

        """
        test missing name
        """
        payload = {
            "userId": "3",
            "clothesId": "2",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'name'", data)

        """
        test missing rating
        """
        payload = {
            "userId": "3",
            "clothesId": "2",
            "name": "team knit short",
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'rating'", data)

        """
        test missing returned value
        """
        payload = {
            "userId": "3",
            "clothesId": "2",
            "name": "team knit short",
            "rating": 4,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'returned'", data)


        """
        test missing review
        """
        payload = {
            "userId": "3",
            "clothesId": "2",
            "name": "team knit short",
            "rating": 4,
            "returned": False
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'review'", data)


    @ignore_warnings
    def test_fail_nonexisting_user(self):
        payload = {
            "userId": "123",
            "clothesId": "2",
            "name": "team knit short",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(500, response.status_code)
        self.assertEqual("Could not add transaction", data)

    @ignore_warnings
    def test_fail_nonexisting_clothes(self):
        payload = {
            "userId": "1",
            "clothesId": "35",
            "name": "team knit short",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(500, response.status_code)
        self.assertEqual("Could not add transaction", data)


    @ignore_warnings
    def test_create_existing_user_existing_clothes(self):
        payload = {
            "userId": "2",
            "clothesId": "1",
            "name": "team knit short",
            "rating": 4,
            "returned": False,
            "review": "good fit"
        }

        response = self.app.post("/transactions/new", json=payload)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Successfully added transaction", data)
