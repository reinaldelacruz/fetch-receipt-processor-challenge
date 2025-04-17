from django.urls import path
from .views import ProcessReceiptView, GetPointsView

urlpatterns = [
    path('receipts/process', ProcessReceiptView.as_view(), name='process-receipt'),
    path('receipts/<str:id>/points', GetPointsView.as_view(), name='get-receipt-points'),
]
