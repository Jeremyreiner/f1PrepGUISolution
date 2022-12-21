from threading import Thread
import PySimpleGUI as sg
from trial import *

path = r'C:\Users\Jeremy\OneDrive\WorkPC\f1pygui\f1ObjLogger\demo.json'
data = read_json(path)

table_data = [[f'{x["id"]}', f'{x["name"]}'] for x in data]

layout = [[sg.Table(values=table_data, headings=['ID', 'Name'], max_col_width=25, auto_size_columns=True, alternating_row_color='lightblue', key='table', enable_events=True)],
          [sg.Multiline(size=(40, 5), key='output')]]

window = sg.Window('Table Example').Layout(layout)

th = Thread(target=RunThread(data, len(data), path).Run)
th.start()
while True:
    event, values = window.Read(timeout=1000)
    if event == 'table':
        if values['table'] != []:
            selected_row = values['table'][0]
            window.FindElement('output').Update(data[selected_row])
    
    elif event == '__TIMEOUT__':
        data = read_json(path)

        inter = len(data) - 1

        table_data.append([f'{data[inter]["id"]}', f'{data[inter]["name"]}'])

        window.FindElement('table').Update(values=table_data)
        
    elif event is None:
        th.join()
        break



window.Close()