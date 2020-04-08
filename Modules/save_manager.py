import urllib.request
import pathlib
from PIL import Image
from uuid import uuid4
from time import time

class save_manager(object):
    def __init__(self):
        print('[INFO] Initializing Save Manager...')
        self.cwd = pathlib.Path.cwd()
        self.sp = self.cwd.joinpath(pathlib.Path('YTMD_SaveData'))
        self.isp = self.sp.joinpath(pathlib.Path('YTMD_ImageSaveData'))
        self.lsp = self.sp.joinpath(pathlib.Path('YTMD_Logs'))
        self.msp = self.sp.joinpath(pathlib.Path('YTMD_MP3'))
        self.paths = [self.sp, self.isp, self.lsp, self.msp]
        self.file_type_save_loc = {'img':self.isp,}
        print('[SUCCESS] Save Manager Initialized.')
    
    def prepare_save(self):
        print('[INFO] Checking Save Directories')
        for path in self.paths:
            if not path.is_dir():
                print(f'[INFO] \'{path}\' missing. Creating...''')
                try:
                    path.mkdir()
                except Exception as e:
                    print('[ERROR] Unabe to create \'{path}\'')
                    return e
                else:
                    print(f'[SUCCESS] \'{path}\' Created.')
        return True

    def save_img(self, img_url):
        im = Image.open(urllib.request.urlopen(img_url))
        isn = self.isp.joinpath(pathlib.Path(f'thumbnail_{uuid4()}.png'))
        try:
            im.save(isn)
        except Exception as e:
            return e
        else:
            return (True, isn)

    def save_log(self, e):
        log = open(f'error_{int(time())}.log','w+')
        log.write(e)
        log.close()

    def save_other(self, file, path):
        # This is probably not going to be used. Currently just a place holder.
        pass

    def rm_save(self, path: 'WindowsPath'):
        if not isinstance(path, pathlib.WindowsPath):
            raise TypeError(f'Argument was of type {type(path)}, but must be of type pathlib.WindowsPath')
        if not path.exists():
            raise FileNotFoundError(f'The system cannot find the path specified: {path}')
        check = input('ARE YOU SURE (y/n): ') # this will be removed once the UI is made
        if check != 'y':
            print('[WARN] STOPPING')
            raise SystemExit
        for file in path.iterdir(): 
            file.unlink()
            print(f'[INFO] Removed {file}')
        path.rmdir()
        print(f'[INFO] Removed {path}')