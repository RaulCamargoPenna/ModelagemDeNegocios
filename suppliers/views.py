from django.shortcuts import render
from rest_framework import generics
from suppliers.models import Suppliers
from suppliers.serializers import SuppliersSerializer

class ListCreateSuppliersAPIView(generics.ListCreateAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
