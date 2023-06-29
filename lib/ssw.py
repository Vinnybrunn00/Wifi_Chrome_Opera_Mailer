import requests
import json, sys
from tkinter import messagebox
from lib.connect import checkNetwork

messagebox.showinfo('HTTPSConnectionPool Error', message='Connect Network Error') | sys.exit() if checkNetwork('https://google.com', timeout=5) == False else None

API_KEY = '409adf0f8bcf4b96bb3d5df44d235f61'
request_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={API_KEY}'
response = requests.get(request_url)

class GeoLocation:
    def __init__(self) -> None:
        self.result = json.loads(response.content)

    def ip_addr(self):
        return self.result['ip_address']
    
    def city(self):
        return self.result['city']

    def region(self):
        return self.result['region']
        
    def postal_code(self):
        return self.result['postal_code']
        
    def country(self):
        return self.result['country']

    def longitude(self):
        return self.result['longitude']

    def latitude(self):
        return self.result['latitude']

    def organization_name(self):
        return self.result['connection']['organization_name']
