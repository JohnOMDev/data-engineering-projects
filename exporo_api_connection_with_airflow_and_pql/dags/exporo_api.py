#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 29 01:38:55 2021

@author: john
"""

import os
import logging
import requests
from pandas.io.json import json_normalize
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("Exporo api")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

class ExporoAPI():
    """
        This class is to download marketing metrics from Exporo

    """

    def __init__(self):
        self.base_api_endpoint = "https://read.financing.exporo.io/v1/projects/meta/active/"



    def get_api_details(self):
        payload = {
            }
                
        headers = {
          'Content-Type': 'application/json'
        }
        try:
            resource_url = self.base_api_endpoint
            response = requests.request("GET", resource_url, headers=headers, data=payload)
            data = response.json()
            df = json_normalize(data)
        except requests.exceptions.HTTPError as error:
            LOG.info(error)
        return df
