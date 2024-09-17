from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Industry(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='industries_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    logo = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores_owned')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stores_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='categories')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customers_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')
    created_on = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    additional_info = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='variants_created')
    created_on = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"

class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='order_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.id} - {self.product_variant.name}"

class PaymentOption(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payment_options_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PaymentOptionTypes(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    paymentoption = models.ForeignKey(PaymentOption, on_delete=models.CASCADE, related_name='types')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payment_options_tyeps_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=150, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"Payment {self.id} - {self.transaction_id}"

class ShippingAddress(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='shipping_addresses')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='shipping_addresses')

    def __str__(self):
        return f"Address {self.id} - {self.customer.user.username if self.customer else 'No Customer'}"

class StoreLocation(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=191)
    state = models.CharField(max_length=191)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=191)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='locations')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='locations_created')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location {self.id} - {self.store.name}"
