import numpy as np
import rasterio
from os import path, listdir
import re


def read_files_from_landsat_meta(data):
    bands = []
    content = None
    for file in listdir(data):
        if file.endswith('_MTL.txt'):
            with open(path.join(data, file)) as file:
                content = file.readlines()
            break
    if content:
        pattern = r'"([A-Za-z0-9_\./\\-]*)"'  # search for quoted string
        for line in content:
            if 'FILE_NAME_BAND' in line:
                regex = re.search(pattern, line)
                if regex:
                    bands.append(path.join(data, regex.group().replace('"', '')))
    return None if len(bands) <= 0 else bands


def stack_DatasetReader(rasterfiles_list):
    stack = dict()
    for raster in rasterfiles_list:
        with rasterio.open(raster) as dataset:
                stack[raster] = dataset.read()
    return stack



class Satellite:
    def __init__(self, data, bands=[]):
        self.data = dict()
        if isinstance(data, str):
            if path.isdir(data):
                landsat_meta = read_files_from_landsat_meta(data)
                if landsat_meta != None:
                    self.data = stack_DatasetReader(landsat_meta)
                else:
                    # TODO function for reading bands in correct order from folder
                    pass
            elif path.isfile(data):
                with rasterio.open(data) as dataset:
                    self.data['band01'] = dataset.read()
            else:
                pass
        elif isinstance(data, rasterio.io.DatasetReader):
            self.data['band01'] = data.read()
        elif isinstance(data, np.ndarray):
            self.data = data
        else:
            raise TypeError("Expected str, ndarray or rasterio.io.DatasetReader, got: " + str(type(data)))


#dataset = Satellite('testdata/LC81200352013335LGN00')
Satellite('testdata/LC81200352013335LGN00')
