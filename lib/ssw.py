import requests
import json

class GeoLocation:
    def __init__(self, api_token:str) -> None:
        request_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={api_token}'
        response = requests.get(request_url)
        
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
