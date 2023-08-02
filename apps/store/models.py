from django.db import models
from apps.customers.models import Customer
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg')
    tags = TaggableManager()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(default='', null=True, blank=True)
    stock = models.PositiveIntegerField()

    # Overwriting the name of the product, adding "Out of stock" at the end
    # if the stock is equal to 0.

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.name = self.name + ' (Out of stock)'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def place_order(self):
        self.save()

    # Calculates the total ammount to be paid of all the products in the order.
    @property
    def get_order_price(self):
        products = self.productorder_set.all()
        order_price = sum([product.get_total_price for product in products])
        return order_price

    # Calculates the total ammount of products that will be bought.
    @property
    def get_total_products(self):
        products = self.productorder_set.all()
        total_products = sum([product.quantity for product in products])
        return total_products

    # Function that return the customer orders ordered by the creation date.
    @staticmethod
    def get_order_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-created_at')

    def __str__(self):
        return f'{self.id} | Completed: {self.completed}'


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)

    # Calculates the total price of the products in an order

    @property
    def get_total_price(self):
        total = self.product.price * self.quantity
        return total

    # Preventing the customer to place a product into a order if there is no stock,
    # if the quantity of products ordered is equal to 0 or if the quantity of
    # products ordered exceed the stock available.

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock or self.product.stock == 0:
            return
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Product: {self.product.name} | Quantity: {str(self.quantity)}'


class Checkout(models.Model):
    PAYMENT_CHOICES = [
        ('PP', 'PayPal'),
        ('ZL', 'Zelle'),
        ('BT', 'Bank Transfer')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    payment_method = models.CharField(
        max_length=2, choices=PAYMENT_CHOICES, default='PP')
    date_added = models.DateTimeField(auto_now_add=True)
    transfer_reference = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.address


#################
#### SIGNALS ####
#################
@receiver(post_save, sender=Checkout)
def update_product_stock(sender, instance, created, *args, **kwargs):
    order_products = instance.order.productorder_set.all()
    for product in order_products:
        old_stock = product.product.stock
        new_stock = old_stock - product.quantity
        Product.objects.filter(id=product.product.id).update(stock=new_stock)
        Order.objects.filter(id=instance.order.id).update(completed=True)
