from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.timezone import now
# Create your models here.

class BaseModel(models.Model):
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

role_choices=(
('artist','artist'),
('customer','customer')
)


class CustomUser(AbstractUser):
    role=models.CharField(max_length=20,choices=role_choices)
    

    def __str__(self):
        return self.username

class UserProfile(BaseModel):
    profile_picture=models.ImageField(upload_to="profiles",null=True,blank=True,default="profiles/default.jpg")
    phone=models.CharField(max_length=200,null=True)
    owner=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    # user_role=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.owner.username}-{self.owner.role}"

class Category(BaseModel):
    category_type=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.category_type

class ArtWork(BaseModel):
    title=models.CharField(max_length=200)
    description=models.TextField()
    picture=models.ImageField(upload_to="artimages",null=True,blank=True)
    price=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    # fetch the first active discount that is valid
    def get_active_discounts(self):
        active_discount=self.discounts.filter(is_active=True,
            start_date__lte=now().date(),
            end_date__gte=now().date())
        return active_discount.first()
    
    def get_discounted_price(self):
        discount=self.get_active_discounts()
        if discount:
            return max(self.price-discount.discount_price,0)
        return self.price

class Discount(BaseModel):
    art=models.ForeignKey(ArtWork,on_delete=models.CASCADE,related_name='discounts')
    discount_price=models.DecimalField(max_digits=5,decimal_places=2)
    start_date=models.DateField()
    end_date=models.DateField()
    
    def __str__(self) -> str:
        return f"{self.discount_price}"

class CartItems(BaseModel):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ForeignKey(ArtWork,on_delete=models.CASCADE)
    is_checkout=models.BooleanField(default=False)

class WishList(BaseModel):
    art_object=models.ManyToManyField(ArtWork)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Order(BaseModel):
    cart_items=models.ManyToManyField(CartItems)
    order_id=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)

class Review(BaseModel):
    art_object=models.ForeignKey(ArtWork,on_delete=models.CASCADE)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ratings=models.CharField(max_length=10,null=True)
    review_message=models.TextField()
    date_posted=models.DateTimeField(auto_now=True)

class Notification(BaseModel):
    new_releases=models.ForeignKey(ArtWork,on_delete=models.CASCADE)
    discount_message=models.ForeignKey(Discount,on_delete=models.CASCADE)


def create_user_profile(sender,instance,created,**kwargs):

    if created:
        UserProfile.objects.create(owner=instance)
post_save.connect(create_user_profile,settings.AUTH_USER_MODEL)

def create_customer_wishlist(sender,instance,created,**kwargs):
    if created and instance.role=='customer':
        WishList.objects.create(user=instance)
post_save.connect(create_customer_wishlist,settings.AUTH_USER_MODEL)