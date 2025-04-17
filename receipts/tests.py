from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .views import ReceiptStore
import uuid

receipt1 = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
receipt1_total_points = 28

receipt2 = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                }
            ],
            "total": "9.00"
        }
receipt2_total_points = 109 

class ReceiptStoreTest(TestCase):
    def setUp(self):
        self.receipt_store = ReceiptStore()
    
    def test_create_and_save_id(self):
        receipt_id = self.receipt_store.create_and_save_id(receipt1)
        receipt = self.receipt_store.receipt_store[receipt_id].receipt
        self.assertEqual(receipt, receipt1)

    def test_get_receipt(self):
        bad_id = "747824242"
        self.assertEqual(self.receipt_store.get_receipt(bad_id), None)
        receipt_id = self.receipt_store.create_and_save_id(receipt1)
        self.assertEqual(self.receipt_store.get_receipt(receipt_id), receipt1)


    def test_is_id_in_receipt_store(self):
        bad_id = "747824242"
        self.assertEqual(self.receipt_store.is_id_in_receipt_store(bad_id), False)
        receipt_id = self.receipt_store.create_and_save_id(receipt1)
        self.assertEqual(self.receipt_store.is_id_in_receipt_store(receipt_id), True)

    def test_get_points(self):
        bad_id = "747824242"
        self.assertEqual(self.receipt_store.get_points(bad_id), -1)
        receipt_id = self.receipt_store.create_and_save_id(receipt1)
        self.assertEqual(self.receipt_store.get_points(receipt_id), 0)


    def test_calculate_points(self):
        receipt_id = self.receipt_store.create_and_save_id(receipt1)
        points1 = self.receipt_store.calculate_and_save_points(receipt_id, receipt1)
        self.assertEqual(points1, receipt1_total_points)
        self.assertEqual(self.receipt_store.receipt_store[receipt_id].points, points1)
        receipt_id = self.receipt_store.create_and_save_id(receipt2)
        points2 = self.receipt_store.calculate_and_save_points(receipt_id,receipt2)
        self.assertEqual(points2, receipt2_total_points)
        self.assertEqual(self.receipt_store.receipt_store[receipt_id].points, points2)
        

class ReceiptPointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        receipt_store_test = ReceiptStoreTest()
    
    def _is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
        
    def test_process_receipt_returns_id(self):
        response = self.client.post('/receipts/process', receipt1, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.json())
        self.assertTrue(self._is_valid_uuid(response.json()["id"]))

    def test_get_points_returns_points(self):
        # First post to create a receipt
        post_response = self.client.post('/receipts/process', receipt1, format='json')
        receipt_id = post_response.json().get("id")

        # Then get points
        get_response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertIn("points", get_response.json())
        self.assertIsInstance(get_response.json()["points"], int)
        self.assertEqual(get_response.json()["points"], receipt1_total_points)

    def test_get_points_invalid_id(self):
        bad_id = str(uuid.uuid4())
        response = self.client.get(f'/receipts/{bad_id}/points')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

