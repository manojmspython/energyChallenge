from django.test import TestCase
from backend.models import NemData
from backend.serializer import NemSerializer


class NemDataTestCase(TestCase):
    def setUp(self):
        NemData.objects.create(nmi="9520021491",
                               serialNumber="HKYDFUE2PONY",
                               reading="24227.0",
                               dateTime="2004-01-07 15:12:06",
                               flowName="input.csv")

    def test_nem_data_insertion(self):
        """Check whether data gets loaded"""
        row = NemData.objects.get(nmi="9520021491")
        self.assertEqual(row.serialNumber, 'HKYDFUE2PONY')

    def test_nem_data_serializer_validates_structure(self):
        """Check whether serializer validates structure"""
        row = NemSerializer(data={})
        self.assertEqual(row.is_valid(), False)

    def test_nem_data_serializer_insert_data(self):
        """Check whether serializer validates structure and saves data if its valid"""
        row = NemSerializer(data={'nmi': "2291137510",
                                  "serialNumber": "R4ZFLS6ZY1UV",
                                  "reading": "56311.0",
                                  "dateTime": "2004-01-07 10:03:33",
                                  "flowName": "input.csv"})
        self.assertEqual(row.is_valid(), True)
        row.save()
        row_data = NemData.objects.get(nmi="2291137510")
        self.assertEqual(row_data.serialNumber, 'R4ZFLS6ZY1UV')
