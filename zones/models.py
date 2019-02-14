from django.contrib.gis.db import models


class Provider(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    language = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    poly = models.PolygonField()
    point = models.PointField(null=True)
    provider = models.ForeignKey(Provider,
                                 on_delete=models.CASCADE,
                                 related_name='areas')

    def __str__(self):
        return self.name

    def polygon(self):
        return self.poly.geojson

    def provider_name(self):
        return self.provider.name
