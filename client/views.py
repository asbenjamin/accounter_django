from django.shortcuts import render

from rest_framework import viewsets 
from rest_framework.request import Request

from .serializers import ClientSerializer
from .models import Client

from django.core.exceptions import PermissionDenied

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def update(self, request: Request, *args, **kwargs):
        # serializer = ClientSerializer
        serializer.is_valid(raise_exception=True)

        # obj = self.get_object()

        # if self.request.user != obj.created_by:
        #     raise PermissionDenied('Wrong object owner')
    
        serializer.save()
