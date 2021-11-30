import ui
import dose

__all__ = (
    'Application'
)

#-----------
# Dev API
#------------

class Application:
    '''An Application is an instance of the webapp RadPlume.

    '''
    


    def __init__(self):
        self.ui = ui.GUI()
        self.dose = dose.Dose()