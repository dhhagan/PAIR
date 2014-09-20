"""
    Classes and functions needed to grab PAIR data from Google
"""

import pandas as pd
from pandas import DataFrame, Series
import requests
import zipfile
import StringIO
import sys

__all__ = []

class patent_app:
    def __init__(self, app_number = None):
        self.number = app_number
        self.link = 'http://storage.googleapis.com/uspto-pair/applications/' + self.number + '.zip'
        self.last_updated = None
        self.status = None

    def get_zip(self):
        try:
            r = requests.get(self.link)
            if r.ok:
                z = zipfile.ZipFile(StringIO.StringIO(r.content))
            else:
                sys.exit("The zip file may be corrupt.")
        except:
            raise NameError('Could not download the zip file from Google.')

        return z

    def parse_agents(self, z = None):
        if z is None:
            z = self.get_zip()

        f = z.open(self.number + '/' + self.number + '-address_and_attorney_agent.tsv')
        df = pd.read_table(f, sep='\t', skiprows=4)
        df['Last'] = df['Name'].apply(lambda x: str.split(x, ',')[0])
        df['First'] = df['Name'].apply(lambda x: str.split(x, ',')[1])
        del df['Name']

        f.close()

        return df

    def parse_app_data(self, z = None):
        if z is None:
            z = self.get_zip()

        f = z.open(self.number + '/' + self.number + '-application_data.tsv')
        df = pd.read_table(f, sep='\t', header=None)

        f.close()

        return df

    def parse_transaction_history(self, z = None):
        if z is None:
            z = self.get_zip()

        f = z.open(self.number + '/' + self.number +'-transaction_history.tsv')
        df = pd.read_table(f, sep='\t')

        f.close()

        return df