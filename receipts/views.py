import uuid
import math
from datetime import datetime, time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from typing import Any, Dict


class Receipt():
    def __init__(self, receipt: Dict[str, Any]={}, points: int=0):
        self.receipt = receipt
        self.points = points

# In memory store for receipts and their ids
class ReceiptStore():
    def __init__(self):
        self.receipt_store = {} # id to Receipt
    
    def create_and_save_id(self, receipt: Dict[str, Any]) -> str:
        receipt_id = str(uuid.uuid4())
        self.receipt_store[receipt_id] = Receipt(receipt, 0)
        return receipt_id

    def get_receipt(self, id: str) -> Any:
        if id not in self.receipt_store:
            return None
        
        return self.receipt_store[id].receipt

    def is_id_in_receipt_store(self, id) -> bool:
        if id not in self.receipt_store:
            return False
        return True
    
    def get_points(self, id) -> int:
        if id not in self.receipt_store:
            return -1
        
        return self.receipt_store[id].points
    
    def calculate_and_save_points(self, id, receipt) -> float:
        points = 0
        retailer = receipt.get("retailer", "")
        total = float(receipt.get("total", 0))
        items = receipt.get("items", [])
        purchase_date = datetime.strptime(receipt.get("purchaseDate", ""), "%Y-%m-%d")
        purchase_time = datetime.strptime(receipt.get("purchaseTime", ""), "%H:%M").time()

        # one point for every alphanumeric character in retailer name
        for c in retailer:
            if c.isalnum():
                points += 1
        
        # 50 points if the total is a round dollar amount with no cents
        if total == int(total):
            points += 50

        # 25 points if the total is a multiple of 0.25
        if (total * 100) % 25 == 0:
            points += 25

        # 5 points for every two items on the receipt
        if items:
            points += (len(items) // 2) * 5

        """
        If the trimmed length of the item description is a multiple of 3,
          multiply the price by 0.2 and round up to the nearest integer. 
          The result is the number of points earned.
        """
        for item in items:
            description = item.get("shortDescription", "").strip()
            price = float(item.get("price", 0))
            if len(description) % 3 == 0:
                points += math.ceil(price * 0.2)
  
        
        # 6 points if the day in the purchase date is odd.
        if purchase_date.day % 2 == 1:
            points += 6

        #10 points if the time of purchase is after 2:00pm and before 4:00pm.
        if time(14, 0) <= purchase_time < time(16, 0):
            points += 10
        
        self.receipt_store[id].points = points

        return points



receipt_store = ReceiptStore()

class ProcessReceiptView(APIView):
    def post(self, request):
        receipt = request.data
        receipt_id = receipt_store.create_and_save_id(receipt=receipt)
        points = receipt_store.calculate_and_save_points(receipt_id, receipt)
        return Response({"id": receipt_id})

class GetPointsView(APIView):
    def get(self, request, id):
        if not receipt_store.is_id_in_receipt_store(id):
            raise Http404("Receipt not found")
        return Response({"points": receipt_store.get_points(id)})
