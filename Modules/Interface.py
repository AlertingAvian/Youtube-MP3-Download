import PySimpleGUI as sg

sg.change_look_and_feel('DefaultNoMoreNagging')

frame1_layout = [
                
                ]

tab1_frame_layout = [ # Tabs must first be in a frame and then a tab layout before they can be included in the window
                [sg.Input(),sg.Submit()],
                [sg.Frame('Results',frame1_layout,'red',visible=False)]
                ]

tab1_layout = [ 
            [sg.Frame('Search for a Video',tab1_frame_layout,title_color='red')]
            ]

layout = [
            [sg.TabGroup([[sg.Tab('Search',tab1_layout,title_color='red')]])],
            [sg.Exit()]
            ]

window = sg.Window('Window',layout)

while True:
    event, values = window.read()

    # print(event, values) # debug

    if event in (None, 'Exit', 'Cancel'):
        break

    elif event[:4:] == 'Exit':
        break
    
window.close()