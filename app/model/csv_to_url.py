# -*- coding: utf-8 -*-

import re
import csv
import pandas as pd

from app import app

class CsvToUrl():

    def get_url(self, filename):
        try:
            df = pd.read_csv(filename)
            df_new = df[['url']]

            val = []
            for i, row in df_new.iterrows():
                val.append(df.iat[i, 0])

        except Exception as e:
            app.logger.error(e.args)
            raise

        return val

