from GUI import *

gui = GraphicalUserInterface(600, 450, WHITE)

gui.start_new_question('OpenTopic', 'ReaderAsking')
## Update all the relevant text fields

#### MAIN ####

while True:

    # Handles events (e.g. mouse clicks) from user
    gui.check_events()
    
    if gui.user_mouse_input:
        print(gui.user_mouse_input)
        ## Probably handle the event first
        gui.user_mouse_input = None
    
    gui.render()
