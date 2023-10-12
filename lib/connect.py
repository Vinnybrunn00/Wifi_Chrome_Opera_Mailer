from requests import exceptions
import requests

def checkNetwork(url:str='https://www.google.com/', timeout:int=5):
    try:
        requests.get(url, timeout=timeout)
        return True
    except exceptions.ConnectionError:
        return False