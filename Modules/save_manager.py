from PIL import Image
import pathlib

class save_manager(object):
    def __init__(self):
        print('[INFO] Initializing Save Manager...')
        self.cwd = pathlib.Path.cwd()
        self.sp = self.cwd.joinpath(pathlib.Path('YTMD_SaveData'))
        self.isp = self.sp.joinpath(pathlib.Path('YTMD_ImageSaveData'))
        print('[SUCCESS] Save Manager Initialized.')
    
    def prepare_save(self):
        print('[INFO] Checking Save Directories')
        try:
            if not self.sp.is_dir():
                print(f'[NOTICE] \'{self.sp}\' missing. Creating...')
                self.sp.mkdir()
                print(f'[SUCCESS] \'{self.sp}\' Created.')
            if not self.isp.is_dir():
                print(f'[NOTICE] \'{self.isp}\' missing. Creating...')
                self.isp.mkdir()
                print(f'[SUCCESS] \'{self.sp}\' Created.')
        except Exception as e:
            print('[ERROR] Save Directory Error')
            return e
        else:
            print('[SUCCESS] Save Directory Complete.')
            return True
    


def save():
    pass

def rm_save():
    pass