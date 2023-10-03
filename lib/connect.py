from requests import exceptions
import requests

def checkNetwork(url, timeout):
    try:
        requests.get(url, timeout=timeout)
        return True
    except exceptions.ConnectionError:
        return False