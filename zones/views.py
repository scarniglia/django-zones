# from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.gis.geos import GEOSGeometry
from rest_framework_gis.pagination import GeoJsonPagination

from zones.models import Provider, ServiceArea
from zones.serializers import (
    ProviderSerializer,
    ServiceAreaSerializer,
)


class ProviderViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Person
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    pagination_class = GeoJsonPagination


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Person
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    pagination_class = GeoJsonPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        if latitude is not None and longitude is not None:
            try:
                point = GEOSGeometry('POINT({} {})'.format(str(latitude), str(longitude)))
                if latitude is not None and longitude is not None:
                    queryset = queryset.filter(poly__contains=point)
                return queryset
            except ValueError:
                return queryset.none()

        return queryset

