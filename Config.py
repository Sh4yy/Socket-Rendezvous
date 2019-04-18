import yaml
import os


def get_path():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_dir, 'config.yaml')

with open(get_path(), 'r') as data:
    config = yaml.load(data)
