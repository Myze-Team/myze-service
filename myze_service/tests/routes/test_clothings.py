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

class GetClothingsTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    @ignore_warnings
    def test_nonexisting_item(self):
        response = self.app.get("/clothings/123")
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Item not found", data)

    @ignore_warnings
    def test_existing_item(self):
        response = self.app.get("/clothings/1")
        data = json.loads(response.data)
        
        self.assertEqual(200, response.status_code)
        self.assertEqual({"S": "CLOTHES_1"}, data["PK"])
        self.assertEqual({"S": "CLOTHES_1"}, data["SK"])
        self.assertEqual({"S": "SIZE_S"}, data["Item-Size-GSI"])
        self.assertEqual({"S": "$30"}, data["price"])
        self.assertEqual({"S": "team knit short"}, data["name"])
        self.assertEqual({"S": "Nike"}, data["brand"])
        self.assertEqual({"S": "short"}, data["category"])
        self.assertEqual({"N": "1"}, data["count"])


class CreateClothingsTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()

    @ignore_warnings
    def test_missing_args(self):
        response = self.app.post("/clothings/new")
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Bad Arguments", data)

        """
        test missing name
        """
        payload = {
            "brand": "Nike",
            "category": "short",
            "price": "$30",
            "size": "L"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'name'", data)

        """
        test missing brand
        """
        payload = {
            "name": "team knit short",
            "category": "short",
            "price": "$30",
            "size": "L"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'brand'", data)

        """
        test missing category
        """
        payload = {
            "name": "team knit short",
            "brand": "Nike",
            "price": "$30",
            "size": "L"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'category'", data)

        """
        test missing price
        """
        payload = {
            "name": "team knit short",
            "brand": "Nike",
            "category": "short",
            "size": "L"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'price'", data)

        """
        test missing size
        """
        payload = {
            "name": "team knit short",
            "brand": "Nike",
            "category": "short",
            "price": "$30"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'size'", data)

    @ignore_warnings
    def test_fail_when_same_name_same_size(self):
        payload = {
            "name": "team knit short",
            "brand": "Nike",
            "price": "$30",
            "category": "$30",
            "size": "S"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)

        self.assertEqual(500, response.status_code)
        self.assertEqual("Could not add clothing", data)


    @ignore_warnings
    def test_create_when_same_name_diff_size(self):
        payload = {
            "name": "team knit short",
            "brand": "Nike",
            "price": "$30",
            "category": "$30",
            "size": "L"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Successfully added clothing", data)

    @ignore_warnings
    def test_create_when_different_name_same_size(self):
        payload = {
            "name": "Dri-FIT Giannis 'Freak' Naija",
            "brand": "Nike",
            "price": "$35",
            "category": "t-shirt",
            "size": "S"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Successfully added clothing", data)

    @ignore_warnings
    def test_create_when_different_name_diff_size(self):
        payload = {
            "name": "Thermal Victory",
            "brand": "Nike",
            "price": "$75",
            "category": "zip golf top",
            "size": "XL"
        }

        response = self.app.post("/clothings/new", json=payload)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Successfully added clothing", data)


class GetBrandNamesTest(unittest.TestCase):
    @classmethod
    @ignore_warnings
    def setUpClass(self):
        self.app = create_app().test_client()
        init_table()


    @ignore_warnings
    def test_missing_args(self):
        response = self.app.get("/clothings/names")
        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing argument 'brand'", data)

    @ignore_warnings
    def test_nonexisting_brand(self):
        response = self.app.get("/clothings/names?brand=Adidas")
        data = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertEqual("Brand not found", data)

    
    @ignore_warnings
    def test_existing_brand(self):
        response = self.app.get("/clothings/names?brand=Nike")
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))
        self.assertEqual({"S": "BRAND_Nike"}, data[0]["PK"])
        self.assertEqual({"S": "dry academy pro pullover hoodie"}, data[0]["SK"])
        self.assertEqual({"S": "BRAND_Nike"}, data[1]["PK"])
        self.assertEqual({"S": "team knit short"}, data[1]["SK"])