from datetime import datetime
from os import system, environ, path
from pathlib import Path

import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from backend.serializer import NemSerializer

DJANGO_SU_NAME = environ.get('DJANGO_SU_NAME', 'admin')
DJANGO_SU_EMAIL = environ.get('DJANGO_SU_EMAIL', '')
DJANGO_SU_PASSWORD = environ.get('DJANGO_SU_PASSWORD', 'Password@12345')


def parse_datetime(record: str):
    """
    Parse a datetime string into a python datetime object.

    :param record: datetime string
    :return: datetime object
    """
    format_strings = "%Y%m%d%H%M%S"
    if record == "" or record is None:
        return None

    try:
        timestamp = datetime.strptime(
            record.strip()[:14], format_strings
        )
    except (ValueError, KeyError) as e:
        print(e)
        return "Invalid date"

    return timestamp


class ReadNem(object):
    """
    Class fro parsing the nem file and loading it into the DB.
    """

    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.validate_file()
        self.validate_date = []
        self.flow_name = ""

    def validate_record_indicator100(self):
        """
        Validates and parses row with indicator 100.
        :return: None
        """
        data = self.data[self.data[0] == 100]
        for record in data.iterrows():
            # considered columns are [RecordIndicator, VersionHeader, DateTime, FromParticipant, ToParticipant]
            list(record[1])[:5]

    def validate_record_indicator250(self):
        """
        Validates and parses row with indicator 250.
        :return: None
        """
        data = self.data[self.data[0] == 250]
        # [NMI, MeterSerialNumber, CurrentRegisterRead, CurrentRegisterReadDateTime]
        key_column_mapping = {'nmi': 1, 'serialNumber': 6, 'reading': 13, 'dateTime': 14}

        for record in data.iterrows():
            # considered columns are [RecordIndicator, NMI, NMIConfiguration , RegisterID,
            # NMISuffix, MDMDataStreamIdentifier, MeterSerialNumber, DirectionIndicator, PreviousRegisterRead,
            # PreviousRegisterReadDateTime, PreviousQualityMethod, PreviousReasonCode, PreviousReasonDescription,
            # CurrentRegisterRead, CurrentRegisterReadDateTime, CurrentQualityMethod, CurrentReasonCode,
            # CurrentReasonDescription, Quantity, UOM, NextScheduledReadDate, UpdateDateTime, MSATSLoadDateTime]
            column_values = list(record[1])[:23]
            record_data = {'flowName': self.flow_name}
            for key, value in key_column_mapping.items():
                record_data[key] = str(parse_datetime(str(column_values[value]))) if value == 14 else str(
                    column_values[value])

            serialzer_object = NemSerializer(data=record_data)
            if serialzer_object.is_valid():
                serialzer_object.save()

    def validate_record_indicator550(self):
        """
        Validates and parses row with indicator 550.
        :return: None
        """
        data = self.data[self.data[0] == 550]
        for record in data.iterrows():
            # considered columns are [RecordIndicator, PreviousTransCode, PreviousRetServiceOrder,
            # CurrentTransCode, CurrentRetServiceOrder]
            list(record[1])[:5]

    def validate_record_indicator900(self):
        """
        Validates and parses row with indicator 900.
        :return: None
        """
        data = self.data[self.data[0] == 900]
        for record in data.iterrows():
            # considered columns are [RecordIndicator]
            list(record[1])[:1]

    def validate_file(self):
        if not path.isfile(self.filename):
            raise Exception(f"Not a file: {self.filename}")
        df = pd.read_csv(self.filename, header=None)
        record_indicators = set(df[0])
        assert {100, 250, 900} == record_indicators or {100, 250, 550, 900} == record_indicators, \
            "Not valid nem13 file check the record indicators"
        self.data = df
        self.flow_name = Path(self.filename).name
        # as per the challenge only the following columns are needed hence only the 250 indicator is needed
        # column names are [NMI, MeterSerialNumber, CurrentRegisterRead, CurrentRegisterReadDateTime]

        system('python manage.py flush --no-input')
        self.validate_record_indicator250()
        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)
        superuser.save()


class Command(BaseCommand):
    help = 'Import data from json file'

    def add_arguments(self, parser):
        """
        Adds the argument filepath to command line.
        :param parser: parser
        :return: None
        """
        parser.add_argument('filepath', type=str, help='Indicates the path of nem13 file')

    def handle(self, *args, **options):
        """
        Execute the Django command.
        :param args: args
        :param options: Command line arguments
        :return: None
        """
        filename = options['filepath']
        try:
            ReadNem(filename)
            self.stdout.write(self.style.SUCCESS('Successfully loaded the data'))
        except Exception as e:
            system('python manage.py flush --no-input')
            self.stdout.write(self.style.ERROR(f'There was some issue with message: {e}'))
