import os
import yaml

def read_yaml_file(filepath):
    with open(filepath  ) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


config=read_yaml_file(os.path.join(os.getcwd(),'config.yaml'))
