from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from datetime import datetime,date


#Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    image = models.ImageField(verbose_name='Venue Image',upload_to='img/',default=None,blank=True)
    startTime = models.TimeField(blank=True,null=True)
    endTime = models.TimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.name}-{self.address}"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

#MENU
# class Menu(models.Model):
#     name = models.CharField("Menu_Name", null=True, max_length=64)
#     venue = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="Venue")
#     startTime = models.TimeField()
#     endTime = models.TimeField()
#
#     def __str__(self):
#         return f"{self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=128,null=True)
    phone = models.CharField(max_length=64,null=True)

    # stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    # one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        if(self.name):
            return self.name
        else:
            return self.user.password

#FoodCategory
class FoodCategory(models.Model):
    name = models.CharField("Catagory_Name",null=True, max_length=64)

    class Meta:
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f"{self.name}"

#FoodItem
class FoodItem(models.Model):
    name = models.CharField(max_length=64)
    # menu = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='Menu_food')
    venue = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    itemCategory = models.ForeignKey(FoodCategory, on_delete=models.DO_NOTHING,related_name="Food_category")
    image = models.ImageField(
        verbose_name="Food Image", upload_to="img/", default=None, blank=True)
    price = models.DecimalField("Price", max_digits=5, decimal_places=2,default=1)
    description = models.TextField()
    # slug = models.SlugField()

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def getCategory(self):
        return self.itemCategory

    def __str__(self):
        return f"{self.name} -{self.itemCategory}"

#Payment
# class Payment(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_payment")
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username}"

#Order

class Order(models.Model):
    STATUS = [
        ("F","False"),
        ("C","Complete"),
        ("P","Pending")
    ]
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_orders")
    restaurant = models.ForeignKey(Restaurant,on_delete=models.DO_NOTHING, related_name="order_restaurants")
    ordered= models.CharField(max_length=1,choices=STATUS,default="F")
    refCode = models.CharField(max_length=20, blank=True, null=True)
    # tableReference = models.CharField("Table Number",max_length=30)
    orderedDate = models.DateTimeField(auto_now_add=True,auto_now=False,blank=True,null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,related_name="order_payment")

    def __str__(self):
        return f"id: {self.id} {self.user}"

    @property
    def getTotalPrice(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.getItemsPrice for item in orderitems])
        return total

    @property
    def getTotalQuantity(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        #OrderDetail


class OrderDetail(models.Model):
    SIZES = [
        ('S','Small'),
        ('L','Large')
    ]
    # user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    foodItem = models.ForeignKey(FoodItem,on_delete=models.CASCADE,related_name="food_details",null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    # size = models.CharField(max_length=1,choices=SIZES,default='S')
    # specification = models.ManyToManyField(Specification,related_name="order_spec",blank=True,null=True)

    def __str__(self):
        return f"id: {self.id} {self.quantity}  "

    # def spec_list(self):
    #     spec_list = [spec.name for spec in self.specification.all() ]
    #     return spec_list

    @property
    def getItemsPrice(self):
            return self.quantity * self.foodItem.price























