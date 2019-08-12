import h5py as h5
import numpy as np


class FileService:

    def read_file(self, path, mode='r'):
        with open(path, mode) as file:
            return file.read()

    def read_h5_file(self, path):
        with h5.File(path, 'r') as file:
            return np.array(file['X_test'])

    def write_file(self):
        pass