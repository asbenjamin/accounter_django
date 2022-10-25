from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ReceiptViewSet, generate_pdf, send_reminder

router = DefaultRouter()
router.register("receipts", ReceiptViewSet, basename="receipts")

urlpatterns = [
    path('', include(router.urls)),
    path('receipts/<int:receipt_id>/generate_pdf/', generate_pdf, name='generate_pdf'),
    path('receipts/<int:receipt_id>/send_reminder/', send_reminder, name='send_reminder'),
]
