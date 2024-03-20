from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import *
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from main import models
from . import serializers

# Create your views here.


# category
@api_view(['GET'])
def category_list(request):
    categories = models.Category.objects.all()
    serializer = serializers.CategorySerializer(categories, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def category_detail(request,pk):
    category = models.Category.objects.get(pk = pk)
    cat_serializer = serializers.CategorySerializer(category)
    context = {
        'category': cat_serializer.data ,
        
    }
    return Response (context)

@api_view(["GET"])
def index(request):
    q = request.GET.get('q')
    if q:
        products = models.Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else: 
        products = models.Product.objects.filter(quantity__gt=0)
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products.filter(category_id=category_id)
    
    product_serializer = serializers.ProductSerializer(products, many = True)
    category_serializer = serializers.CategorySerializer(categorys, many = True)
    context = {
        'products':product_serializer.data,
        'categorys':category_serializer.data,
        
    }
    return Response(context)

@api_view(["GET, POST"])
def login_user(request):
    login_error = False
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username,  password=password)
        if user:
            login(request, user)
            return Response({'detail': 'logged in succesully'})
        else:
            return Response({'detail': 'Incorect username or password'})
    return Response({'detail': 'Not in POST'})



@api_view(["GET, POST"])
def regist(request):
    error = False
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        if not models.User.objects.filter(username = username):
            models.User.objects.create_user(
                username=username,
                password=password
            )
            
            user = authenticate(username = username, password = password)
            login(request, user)
            return Response({'detail': 'Registration successful'})
        else:
            return Response({'detail': 'Username exists'})
    return Response({'detail': 'Not in POST'})

@api_view(["GET, POST"])
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response({'detail': 'Logout successful'})

    return Response({'detail': 'Not in POST'})

# product
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def product_detail(request, HttpRequest, pk):
    try:
        product = models.Product.objects.get(pk=pk)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def product_list(request):
    products = models.Product.objects.all()
    serializer = serializers.ProductSerializer(products, many = True)
    return Response(serializer.data)




@api_view(['GET','POST'])
def product_create(request):
        if request.method == 'POST':
            serializer = serializers.ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        elif request.method == 'GET':
         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['DELETE'])
def product_delete(self, request, pk):
    try:
        product = models.Product.objects.get(pk=pk)
    except product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



# cart
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def cart_detail(request, user_id):
    try:
        cart = models.Cart.objects.get(user_id=user_id)
    except models.Cart.DoesNotExist:
        return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.CartSerializer(cart)
    return Response(serializer.data)


@api_view(["GET"])
def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user).order_by('-id')
    context = {
        'active':serializers.CartSerializer(active, many = True).data,
        'in_active':serializers.CartSerializer(in_active, many = True).data,
        'categorys': serializers.CategorySerializer(models.Category.objects.all(), many = True).data,
    }
    return Response(context)

@csrf_exempt
@api_view(['GET','POST'])
def cart_add(request):
    serializer = serializers.CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def cart_list(request):
    if request.method == 'GET':
        carts = models.Cart.objects.all()
        serializer = serializers.CartSerializer(carts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


api_view(["GET, POST"])
def create_cart(request, pk):      
    product = models.Product.objects.get(pk = pk)
    cart = models.Cart.objects.filter(user = request.user, is_active = True).first()
    if cart:
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    else:
        new_cart = models.Cart.objects.create(
            user = request.user
        )
        serializer = serializers.CartSerializer(new_cart)
        return Response(serializer.data)
    


# order

@csrf_exempt
@api_view([ 'GET', 'POST'])
def create_order(request):
    serializer = serializers.OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def order_delete(request, order_id):
    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
def order_detail(request, pk):
    try:
        order = models.Order.objects.get(pk=pk)
    except models.Order.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def order_list(request):
    if request.method == 'GET':
        orders = models.Order.objects.all()
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

   

@api_view(['GET'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username = username, password = password)
    if user:
        token, _ = Token.objects.get_or_create(user = user)
        data = {
            'token' : token.key
        }
    else:
        data = {
            'detail' : 'incorrect username or password'
        }
    return Response (data)


@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    if not models.User.objects.filter(username = username):

        user = models.User.objects.create_user(
            username = username,
            password= password
        ) 
        token = Token.objects.create(user = user)
        return Response(
            {
                'username':username,
                'token': token.key
            }
        )
    else:
        return Response (
            {
                'detail': 'username is occupied'
            }
        )