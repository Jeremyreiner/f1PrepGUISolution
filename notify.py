#import the necessary module!
from plyer import notification

def ThrowNotification():


    notification.notify(title= "F1SCRIPT COMPLETED LOADING",
                    message= "Thank you for the patience",
                    app_name="Dialogue Title",
                    app_icon = None,
                    timeout= 5,
                    ticker="Maldita perra",
                    toast=False)
