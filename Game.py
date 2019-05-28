from GUI import *

#################### INIT ####################
gui = GraphicalUserInterface(600, 450, WHITE)

gui.start_new_question('OpenTopic')
## Update all the relevant text fields

#### MAIN ####

while True:

    # Handles events (e.g. mouse clicks) from user
    gui.check_events()
    
    if gui.user_mouse_input:

        ##print(gui.user_mouse_input)
        
        if gui.user_mouse_input == 'ShowAnswer':
            gui.update_state('NoPointsShowAnswer')

        elif gui.user_mouse_input == 'Correct':
            # Record points
            pass
            # Start the next question
            gui.start_new_question('OpenTopic')

        elif gui.user_mouse_input == 'Incorrect':
            if True: # someone else is eligble to answer the question
                gui.update_state('ReaderAsking')
            else: # No one is eligble, show the answer
                gui.update_state('NoPointsShowAnswer')

        elif gui.user_mouse_input == 'NextQuestion':
            # Start the next qestion...
            gui.start_new_question('OpenTopic')

        # Reset the GUI's mouse input attribute
        gui.user_mouse_input = None
    
    gui.render()
