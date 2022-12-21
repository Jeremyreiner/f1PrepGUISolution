from SwitchBoard import *
# Main function iterates through gui check list waiting for one of three requests
# 1: Turn all switches on
#   a: Turns all switches on while shutting off "all off" switch
#   b: Updates switches current boolean value inside of toggleMap dictionary to correct boolean value
# 2: Turn all switches off
#   a: Turns all switches off while shutting off "all on" switch
#   b: Updates switches current boolean value inside of toggleMap dictionary to correct boolean value
# 3: Dynamic request looking for csv list item
#   a: Dynamic list item is read from csv, and given unique identifying key
#   b: each csv list item has locally saved dictionary [toggleMap] indicating if item is true or false (on / off)
#   c: csv data does not save if item is on / off, only that the item exhists

def main():

    window = Make_Win1()

    while True:           
        event, values = window.read()
        
        #print(event, values)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == '-TOGGLE-GRAPHIC-All-ON-':
            if not toggleMap['AllOn']:
                toggleMap['AllOn'], toggleMap['AllOff'] = True, True
            else:
                toggleMap['AllOn'], toggleMap['AllOff'] = False, True

                for x in requests:
                    toggleMap[x + "-graphic_off-"] = toggleMap['AllOn']

                    window[f'-TOGGLE-GRAPHIC-{x}-'].update(image_data=toggle_btn_off if toggleMap[x + "-graphic_off-"]  else toggle_btn_on)

        elif event == '-TOGGLE-GRAPHIC-All-OFF-':
            if not toggleMap['AllOff']:
                toggleMap['AllOn'], toggleMap['AllOff'] = True, True
            else:
                toggleMap['AllOn'],toggleMap['AllOff'] = True, False

                for x in requests:
                    toggleMap[x + "-graphic_off-"] = toggleMap['AllOn']

                    window[f'-TOGGLE-GRAPHIC-{x}-'].update(image_data=toggle_btn_off if toggleMap[x + "-graphic_off-"]  else toggle_btn_on)

        else:
            for x in requests:
                if event == f'-TOGGLE-GRAPHIC-{x}-':
                    toggleMap['AllOn'],toggleMap['AllOff'] = True, True
                    
                    toggleMap[x + "-graphic_off-"] = not toggleMap[x + "-graphic_off-"] 

                    window[f'-TOGGLE-GRAPHIC-{x}-'].update(image_data=toggle_btn_off if toggleMap[x + "-graphic_off-"]  else toggle_btn_on)
       
        window['-TOGGLE-GRAPHIC-All-ON-'].update(image_data=toggle_btn_off if toggleMap["AllOn"]  else toggle_btn_on)
            
        window['-TOGGLE-GRAPHIC-All-OFF-'].update(image_data=toggle_btn_off if toggleMap["AllOff"]  else toggle_btn_on)
               
    window.close()


if __name__ == '__main__':
    main()