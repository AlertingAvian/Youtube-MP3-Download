"""
Copyright (C) 2020 Patrick Maloney

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import urllib
import pathlib
import simplejson
import webbrowser
import validators
import youtube_search
import PySimpleGUI as sg
import youtube_dl as ytdl
from PIL import Image

''' Frames and Layouts for UI '''

save_settings_tab_frame = [[sg.Input(default_text='MP3 Save Location',key='save_loc_input',disabled=True,size=(74,None),tooltip='Leaving unchanged will save in the same location as the program.'),sg.FolderBrowse(tooltip='Select where you want to save the MP3s')],] # Frame for save settings tab

save_settings_tab = [[sg.Frame('Save Settings',save_settings_tab_frame,title_color='white')],] # Save Settings Tab, Should have all save setting nested inside.

search_tab_frame = [[sg.Input(size=(74,None)),sg.Button('Search',bind_return_key=True,key='Search0')],
                    [sg.Image(size=(150,100),background_color='grey',key='v_thumb'),sg.VerticalSeparator(),sg.Text('Search For A Video',size=(50,None),key='v_title',auto_size_text=True)], #result
                    [sg.Button('Download'),sg.ProgressBar(100, orientation='h',size=(39,20),key='dl_progress')]]# download button and progress bar # Frame for search tab

search_tab = [[sg.Frame('Search',search_tab_frame,title_color='white')],] # Search Tab, Should have all search related things nested inside.

debug_tab_frame = [[sg.Output(size=(80,20))],] # Frame for debug tab

debug_tab = [[sg.Frame('Debug',debug_tab_frame,title_color='red')],] # Debug Tab, Should have debug nested inside.

about_tab_frame = [[sg.Text('Copyright (C) 2020 Patrick Maloney'),],
                   [sg.Text('This program is free software: you can redistribute it and/or modify it\nunder the terms of the GNU General Public License as published by the Free\nSoftware Foundation, either version 3 of the License, or (at your option)\nany later version. This program is distributed in the hope that it will be\nuseful, but WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General\nPublic License for more details. You should have received a copy of the GNU\nGeneral Public License along with this program. If not, see\nhttps://www.gnu.org/licenses/.')],
                   [sg.Text('https://github.com/AlertingAvian',enable_events=True,tooltip='Go to GitHub',text_color='#0645AD',font=('Helvetica', 10, 'underline'))],]

about_tab = [[sg.Frame('About',about_tab_frame,title_color='white')]]


main_layout = [[sg.TabGroup([[sg.Tab('Save Settings',save_settings_tab),sg.Tab('Search',search_tab),sg.Tab('Debug',debug_tab),sg.Tab('About',about_tab)]]),],
               [sg.Button('Reset Settings'),sg.VerticalSeparator(),sg.Exit(),],] # The main layout for the UI. Everything should be nested inside of this.

window = sg.Window('Youtube MP3 Downloader', main_layout)

''' Logic and Stuff '''


''' ytdl logger class '''
class Logger(object):
    def debug(self,msg):
        pass
    
    def warning(self,msg):
        print(f'[WARN] {msg}')
    
    def error(self,msg):
        print(f'[ERROR] {msg}')


def hook(d):
    """
    YTDL hook
    """
    if d['status'] == 'finished':
        print('[COMPLETE] Download Complete')
        sg.popup('Download Complete')
        window['dl_progress'].update_bar(0)
    if d['status'] == 'downloading':
        p = d['_percent_str']
        p = p.replace('%','')
        window['dl_progress'].update_bar(p)

while True:
    event, values = window.read()
    
    # print(f'Event: {event}; Values: {values}') # Debug
    
    if event in (None, "Exit", "Cancel"):
        break
    elif event == 'https://github.com/AlertingAvian': # Open github if text is clicked in about tab
        webbrowser.open('https://github.com/AlertingAvian',autoraise=True)
        print('[INFO] Opening GitHub')
    elif event == 'Reset Settings':
        window['save_loc_input'].update('MP3 Save Location')
    elif event == 'Search0':
        print('[INFO] Starting Search')
        query = values[0]
        if len(query) > 0 or query.isspace():
            nexep = True # No Exeptions, used if there is an error during the search process.
            if validators.url(query):
                print('[INFO] URL lookup initiated')
                url_data = urllib.parse.urlparse(query)
                if url_data[1] == 'www.youtube.com': # www.youtube.com/watch?v=<id> links
                    url = query
                    v_id = url_data[4][2:13:]
                    lookup_url = f'https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={v_id}&format=json'
                    json = simplejson.load(urllib.request.urlopen(lookup_url))
                    title = json['title']
                    thumb = json['thumbnail_url']
                elif url_data[1] == 'youtu.be': # youtu.be/<id> links
                    url = query
                    v_id = url_data[2][1:12:]
                    lookup_url = f'https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={v_id}&format=json'
                    json = simplejson.load(urllib.request.urlopen(lookup_url))
                    title = json['title']
                    thumb = json['thumbnail_url']
            else:
                print('[INFO] Search term lookup initiated')
                try:
                    thumb, url, title = youtube_search.search_youtube(query)
                    # print(f'[DEBUG] TITLE: {title}')
                except Exception as e:
                    sg.popup_error('Error','An error occured during the search process, please try again later. \nFor more information see the debug panel.')
                    print(f'[ERROR] {str(e)}')
                    nexep = False
            if nexep:
                urllib.request.urlretrieve(thumb, 'thumb.png')
                pil_img = Image.open('thumb.png')
                pil_img.thumbnail((150,100))
                pil_img.save('thumb.png')
                window['v_thumb'].update(filename='thumb.png')
                window['v_title'].update(title)
                print('[COMPLETE] Lookup Complete')
        else:
            sg.popup('Enter Search Query')
            print('[WARN] Search Query Required')
    elif event == 'Download':
        if values['save_loc_input'] == 'MP3 Save Location':
            save_path = pathlib.Path.cwd().joinpath('YT_MP3')
            if not save_path.exists():
                save_path.mkdir()
            print('[INFO] Save location unchanged')
            print(f'[INFO] Using default save location: {str(save_path)}')
        else:
            print('[INFO] Setting save location set to: {0}'.format(values['save_loc_input']))
            save_path = pathlib.Path(values['save_loc_input'])
            try:
                os.chdir(save_path)
            except Exception as e:
                sg.popup_error('Unable to set save location. Using Default.\nSee the debug panel for more information.')
                print(f'[ERROR] {str(e)}')
                save_path = pathlib.Path.cwd().joinpath('YT_MP3')
                if not save_path.exists():
                    save_path.mkdir()
                print(f'[INFO] Using default save location: {str(save_path)}')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{save_path}/{title}.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': Logger(),
            'progress_hooks': [hook]
        }
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            print('[INFO] Starting Download')
            ydl.download([url])
        os.remove('thumb.png')

window.close()
