from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .utils import clean_phone_number 



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True)  

    def save(self, *args, **kwargs):
        if self.phone_number:
            try:
                self.phone_number = clean_phone_number(self.phone_number)
            except ValueError as e:
                raise ValueError(f"Error saving UserProfile: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        
        return f'{self.user.usernme}\'s Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



class Plant(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField()
    care_instructions = models.TextField()
    image = models.ImageField(upload_to='plants/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    

    def __str__(self):
        return self.name
    # to add care instruction in point form
    @property
    def care_instructions_list(self):
        return [instruction.strip() for instruction in self.care_instructions.split('\n') if instruction.strip()]

class PlantRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    delivery_address = models.TextField() 
    phone_number = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.user.username} - {self.plant.name} ({self.quantity})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=30)
    duration_in_months = models.IntegerField(help_text="Duration in months", default=1)
    category = models.CharField(max_length=50,default='Landscaping', choices=[
        ('planting', 'Planting'),
        ('maintenance', 'Maintenance'),
        ('designing', 'Designing'),
        ('other', 'Other')
    ]      )
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class QuoteRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+254\d{9}$', message="Phone number must be entered in the format: '+254 xxxxxxxxx'.")
    phone = models.CharField(validators=[phone_regex], max_length=13)
    property_image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    location = models.CharField(max_length=100)
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('In Progress', 'In progress'),
        ('Completed', 'Completed')
    ], default='pending')

    def save(self, *args, **kwargs):
        if self.phone:
            try:
                self.phone = clean_phone_number(self.phone)
            except ValueError as e:
                raise ValueError(f"Error saving QuoteRequest: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField() 
    phone = models.CharField(max_length=15)  
    email = models.EmailField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.plant.name} in Order {self.order.id}"



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.plant.name} in {self.user.username}'s cart"

    def total_price(self):
        return self.quantity * self.plant.price
    