from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products')
    discount = models.SmallIntegerField()
    size = models.ManyToManyField(Size, null=True, blank=True, related_name='products')  # many product many size
    color = models.ManyToManyField(Color, related_name='products')  # many product many color

    def __str__(self):
        return self.title


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='informations')  # one product one informatin
    text = models.TextField()

    def __str__(self):
        return self.text[:30]