from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
   
    def __str__(self):
        return self.name
    



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits = 10)
    image = models.ImageField(upload_to='image/')
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    

    @property 
    def is_active(self):
        return self.quantity > 0
    
    def __str__(self):
        return self.name
    

    
class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     is_active = models.BooleanField(default=True)

     @property
     def quantity(self):
        quantity = 0
        products = CartItem.objects.filter(card_id = self.id)
        for i in products:
            quantity +=i.quantity
        return quantity
     

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',null=True,on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, related_name='cart_items',on_delete=models.CASCADE,    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    
    

    @property
    def get_cost(self):
        return self.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s order"