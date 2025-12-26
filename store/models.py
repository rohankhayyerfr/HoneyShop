from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=150, default='')

    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True, default='')

    short_description = models.TextField(blank=True, null=True)

    description = models.TextField(default='', blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(upload_to='products/main/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    label = models.CharField(max_length=50, default='')

    weight = models.PositiveIntegerField()       # 500

    price = models.DecimalField(max_digits=10, decimal_places=0)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=0,
        null=True, blank=True
    )

    inventory = models.PositiveIntegerField(default=0)

    is_best_seller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((self.old_price - self.price) * 100 / self.old_price)
        return 0

    def __str__(self):
        return f"{self.product.name} - {self.label}"


# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#
#     name = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#
#     rating = models.PositiveSmallIntegerField()  # 1 تا 5
#     comment = models.TextField(blank=True)
#
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specs'
    )
    title = models.CharField(max_length=100, default='')

    value = models.CharField(max_length=255, default='')


    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ProductPolicy(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='policy'
    )
    shipping_text = models.TextField(default='')


    return_text = models.TextField(default='')


    packaging_text = models.TextField(default='')
