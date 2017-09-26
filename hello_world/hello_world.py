import requests
from pprint import pprint


def main():
    """Issue a simple request to list the monitored systems"""
    result = requests.get('http://mpstack.wic.openenglab.netapp.com:8081/devmgr/v2/storage-systems',
                          headers={'Accept': 'application/json'},
                          auth=('rw', 'rw'))
    pprint(result.json())


if __name__ == '__main__':
    main()









