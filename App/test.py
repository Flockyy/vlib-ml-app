import configparser
import os
def get_api_key():
    config = configparser.ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'config.ini'))
    
    return config['openweather']['api']


get_api_key()