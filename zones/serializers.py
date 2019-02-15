from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):

    areas = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='servicearea-detail',
        read_only=True,
    )

    class Meta:
        model = Provider
        fields = ('id',
                  'name',
                  'email',
                  'phone_number',
                  'language',
                  'currency',
                  'areas',
                  )


class ServiceAreaSerializer(GeoFeatureModelSerializer):

    provider = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='provider-detail',
        queryset=Provider.objects.all(),
    )

    class Meta:
        model = ServiceArea
        geo_field = 'poly'
        fields = ('id', 'name', 'price', 'provider_name', 'provider', 'poly')
