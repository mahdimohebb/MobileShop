from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.



class CustomUserManager(UserManager):
    
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("phone_number needed!")

        phone_number = phone_number
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)
    
    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone_number, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    name = models.CharField(max_length=255)
    eamil = models.EmailField(blank=True, null=True, max_length=254)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    post_code = models.CharField(max_length=20, blank=True, default=None, null=True)
    address = models.TextField(blank=True, null=True)

    last_session_key = models.CharField(max_length=40, null=True, blank=True, default=None)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']



class Category_blog(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name
    

class Category_Product(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=75)
    farsi_name = models.CharField(max_length=75, default="")    
    hex_color = models.CharField(max_length=9)
    
    
    def __str__(self):
        return self.name



class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    details = models.TextField(null=True)
    category = models.ForeignKey(Category_Product, on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True, null=True)
    main_image = models.ImageField(upload_to='')
    second_image = models.ImageField(upload_to='', null=True) 
    rate = models.IntegerField(null=True)
    price = models.IntegerField()
    colors = models.ManyToManyField(Color)
    sell_count = models.IntegerField()
    
    def __str__(self):
        return self.title

    

class Blog(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='')
    content = models.TextField()
    category = models.ForeignKey(Category_blog, on_delete=models.CASCADE)
    date_publish = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    views = models.IntegerField(default=1)


    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=100, default="Not payed")
    amount = models.IntegerField(blank=True, null=True)
    tracking_code = models.CharField(max_length=255, blank=True, null=True)
    date_payed = models.DateTimeField(blank=True, null=True)
    gateway_payed = models.CharField(max_length=150, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    offer_present = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    
    def __str__(self):
        return f'user: {self.user}  |  status: {self.status}'


class Cart_item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    
    

class Wishlists(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)


class Wishlists_items(models.Model):
    wishlist = models.ForeignKey(Wishlists,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Special_offer(models.Model):
    date_started = models.DateTimeField(auto_now=True)
    date_end = models.DateTimeField()
    is_active = models.BooleanField(blank=True)
    
class Product_images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, default="بدون عنوان")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    date_publish = models.DateTimeField(auto_now_add=True)
    
class Comments_likes(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None, null=True)
