import os
import yaml

''' Read config.yaml and provide it as a module import for the other files. Since python caches loading of modules,
this lets all files use the same instance of config.yaml    
'''
def read_yaml_file(filepath):
    with open(filepath  ) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

config=read_yaml_file(os.path.join(os.getcwd(),'config.yaml'))
