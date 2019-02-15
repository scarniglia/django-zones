from django.contrib.gis.geos import Polygon, Point
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import Provider, ServiceArea


class ProviderModelTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('zones.urls')),
    ]

    def setUp(self):
        p1 = Provider.objects.create(name='Test Provider 1',
                                     email='info@provider1.com',
                                     phone_number='1111',
                                     language='US',
                                     currency='USD',
                                     )

        p2 = Provider.objects.create(name='Test Provider 2',
                                     email='info@provider2.com',
                                     phone_number='2222',
                                     language='AR',
                                     currency='ARS',
                                     )

        zone1 = ((-123.046875, 47.109375),
                 (-101.689453125, 47.109375),
                 (-101.77734375, 34.716796875),
                 (-123.22265625, 34.892578125),
                 (-123.046875, 47.109375),
                 )

        zone2 = ((-111.62109375, 39.375),
                 (-86.396484375, 39.375),
                 (-86.396484375, 50.9765625),
                 (-111.533203125, 51.591796875),
                 (-111.62109375, 39.375),
                 )

        zone3 = ((-111.4453125, 40.78125),
                 (-103.095703125, 40.60546875),
                 (-103.359375, 49.921875),
                 (-111.4453125, 49.658203125),
                 (-111.4453125, 40.78125),
                 )

        ServiceArea.objects.create(name='Test Service Area 1',
                                   poly=Polygon(zone1),
                                   provider=p1,
                                   price=1
                                   )

        ServiceArea.objects.create(name='Test Service Area 2',
                                   poly=Polygon(zone2),
                                   provider=p1,
                                   price=2,
                                   )

        ServiceArea.objects.create(name='Test Service Area 3',
                                   poly=Polygon(zone3),
                                   provider=p2,
                                   price=2,
                                   )

        """
        lp = [-119.03652191162, 43.590660095215]
        cp = [-107.2265625, 44.736328125]
        rp = [-89.560546875, 46.845703125]
        """

    def test_can_create_providers(self):
        """Providers could be created"""
        p1 = Provider.objects.get(name="Test Provider 1")
        p2 = Provider.objects.get(name="Test Provider 2")
        self.assertEqual(p1.email, 'info@provider1.com')
        self.assertEqual(p2.email, 'info@provider2.com')

    def test_service_area_filter_by_coordinate(self):
        """
        Ensure web can filter Service Area by a coordinate
        """

        # Test a point that belongs to 'Test Service Area 1'
        p = Point((-119.03652191162, 43.590660095215))
        qs1 = ServiceArea.objects.filter(poly__contains=p)
        qs2 = ServiceArea.objects.filter(name='Test Service Area 1')
        self.assertListEqual(list(qs1), list(qs2))

        # Test a point that belongs all Service Areas
        p = Point((-107.2265625, 44.736328125))
        qs1 = ServiceArea.objects.filter(poly__contains=p).order_by('name')
        qs2 = ServiceArea.objects.all().order_by('name')
        self.assertListEqual(list(qs1), list(qs2))

    def test_create_provider(self):
        """
        Ensure we can create a new provider object.
        """
        url = reverse('provider-list')
        data = {'name': 'API Test Provider',
                'email': 'info@apiprovider.com',
                'phone_number': '1111',
                'language': 'AR',
                'currency': 'USD',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 3)
        qs = Provider.objects.filter(name='API Test Provider')
        self.assertEqual(qs.count(), 1)

    def test_list_providers(self):
        """
        Ensure we can list provider objects.
        """
        url = reverse('provider-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_provider(self):
        """
        Ensure we can update a provider object.
        """
        provider = Provider.objects.get(name='Test Provider 2')
        self.assertEqual(provider.language, 'AR')
        url = reverse('provider-detail', kwargs={'pk': provider.id})
        data = {'name': 'Test Provider 2',
                'email': 'info@provider2.com',
                'phone_number': '2222',
                'language': 'US',
                'currency': 'ARS',
                }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_provider = Provider.objects.get(name='Test Provider 2')
        self.assertEqual(updated_provider.language, 'US')

    def test_delete_provider(self):
        """
        Ensure we can delete a provider object.
        """
        provider = Provider.objects.get(name='Test Provider 2')
        url = reverse('provider-detail', kwargs={'pk': provider.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        qs = Provider.objects.filter(name='Test Provider 2')
        self.assertEqual(qs.count(), 0)

    def test_create_service_area(self):
        """
        Ensure we can create a new service area object.
        """
        provider = Provider.objects.get(name='Test Provider 1')
        zone = ((-123.046875, 47.109375),
                (-101.689453125, 47.109375),
                (-101.77734375, 34.716796875),
                (-123.22265625, 34.892578125),
                (-123.046875, 47.109375),
                )
        data = {'name': 'API Service Area',
                'provider': reverse('provider-detail',
                                    kwargs={'pk': provider.id}),
                'price': '1',
                'poly': Polygon(zone).geojson,
                }
        url = reverse('servicearea-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.count(), 4)
        qs = ServiceArea.objects.filter(name='API Service Area')
        self.assertEqual(qs.count(), 1)

    def test_list_service_areas(self):
        """
        Ensure we can list service area objects.
        """
        url = reverse('servicearea-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 3)

    def test_filtered_by_coordinate_service_areas(self):
        """
        Ensure we can list service area objects.
        """
        url = reverse('servicearea-list')

        # Test a point that belongs to 'Test Service Area 1'
        data = {'latitude': '-119.03652191162',
                'longitude': '43.590660095215'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

        # Test a point that belongs all Service Areas
        data = {'latitude': '-107.2265625',
                'longitude': '44.736328125'}
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 3)

    def test_update_service_area(self):
        """
        Ensure we can update a service area object.
        """
        service_area = ServiceArea.objects.get(name='Test Service Area 1')
        self.assertEqual(service_area.price, 1)
        url = reverse('servicearea-detail', kwargs={'pk': service_area.id})
        provider = Provider.objects.get(name='Test Provider 1')
        zone = ((-123.046875, 47.109375),
                (-101.689453125, 47.109375),
                (-101.77734375, 34.716796875),
                (-123.22265625, 34.892578125),
                (-123.046875, 47.109375),
                )
        data = {'name': 'Test Service Area 1',
                'provider': reverse('provider-detail',
                                    kwargs={'pk': provider.id}),
                'price': '2',
                'poly': Polygon(zone).geojson,
                }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_service_area = ServiceArea.objects.get(
            name='Test Service Area 1')
        self.assertEqual(updated_service_area.price, 2)

    def test_delete_service_area(self):
        """
        Ensure we can delete a service area object.
        """
        service_area = ServiceArea.objects.get(name='Test Service Area 1')
        url = reverse('servicearea-detail', kwargs={'pk': service_area.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        qs = Provider.objects.filter(name='Test Service Area 1')
        self.assertEqual(qs.count(), 0)
