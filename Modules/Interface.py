import PySimpleGUI as sg

sg.change_look_and_feel('DefaultNoMoreNagging')

frame1_layout = [
                [sg.Image(filename='image.png')]
                ]

layout = [
            [sg.Input(),sg.Submit()],
            [sg.Frame('Results',frame1_layout,'red')],
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