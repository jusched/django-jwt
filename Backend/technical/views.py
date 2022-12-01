"""Technical views."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from technical.serializers import CarSerializer
from .models import Car



@api_view(["GET"])
def ApiView(request):
    api_urls= {
        'all_items': 'all/',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST', 'GET'])
def add_items(request):
    permission_classes= [AllowAny]
    car = CarSerializer(data=request.data)

# Validating
    if Car.objects.filter(**request.data).exists():
        raise serializers.ValidationError("This car already exists.")

    if car.is_valid():
        car.save()
        return Response(car.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_cars(request):
    
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)

    if cars:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_cars(request, pk):
    
    car= Car.objects.get(pk=pk)
    data= CarSerializer(instance=car, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_cars(request, pk):

    car= get_object_or_404(Car, pk=pk)
    car.delete()
    return Response(status=status.HTTP_202_ACCEPTED)