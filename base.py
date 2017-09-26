import json
import requests
import os.path


def main():
    config = Properties()
    print config


def get_session():
    props = Properties()
    con = requests.Session()
    con.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
    con.auth = (props.username, props.password)
    return con


class Properties(object):
    def __init__(self, config_file=None):
        if config_file is None:
            self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuration.json')
        else:
            self.config_file = config_file

        with open(self.config_file) as fp:
            self.json = json.load(fp)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        ret = ""
        for key in self.json:
            ret += "{} : {}\n".format(key, self.json.get(key))
        return ret

    def __getitem__(self, item):
        return self.json.get(item)

    def __getattr__(self, item):
        return self.__getitem__(item)


if (__name__ == '__main__'):
    main()
