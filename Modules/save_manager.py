from PIL import Image
import pathlib

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
        pass

    def save_log(self):
        pass
        