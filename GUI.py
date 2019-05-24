import pygame, sys, os
from datetime import *
from pygame.locals import *
from Colours import *

GAME_STATES = ['ReaderAsking', 'PlayerAnswering', 'NoPointsShowAnswer']
QUESTION_TYPES = ['OpenTopic', 'Assign', 'WhoWhat', 'Tiebreak', 'Shootout', 'Team', 'Scramble']

class GraphicalUserInterface:
    ''' Creates a window for the reader to interact with '''

    def __init__(self, width, height, background_clr = WHITE):

        ## Initializes the pygame module
        pygame.init()
        ## Records the width and height provided
        self.width = width
        self.height = height
        ## Creates a pygame window
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('Reach for the Top')
        pygame.display.set_icon(pygame.image.load(os.path.join('Resources/Images', 'ReachForTheTopLogo.png')).convert_alpha())
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        ## Ignores events we don't need to check
        pygame.event.set_blocked([pygame.ACTIVEEVENT,
                                  pygame.KEYUP,
                                  pygame.KEYDOWN,
                                  pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEMOTION,
                                  pygame.JOYAXISMOTION,
                                  pygame.JOYBALLMOTION,
                                  pygame.JOYHATMOTION,
                                  pygame.JOYBUTTONUP,
                                  pygame.JOYBUTTONDOWN,
                                  pygame.VIDEOEXPOSE,
                                  pygame.USEREVENT])
        ## ↓↓ List of all pyagme event types (for future reference) ↓↓
        #QUIT,ACTIVEEVENT,KEYDOWN,KEYUP,MOUSEMOTION,MOUSEBUTTONUP,MOUSEBUTTONDOWN,JOYAXISMOTION,JOYBALLMOTION,JOYHATMOTION,JOYBUTTONUP,JOYBUTTONDOWN,VIDEORESIZE,VIDEOEXPOSE,USEREVENT

        self.state = None
        self.question_type = None
        self.text_fields = dict()
        self.background_fill = background_clr
        self.user_mouse_input = None

    def start_new_question(self, question_type, state_str):
        
        if state_str in GAME_STATES and question_type in QUESTION_TYPES:

            # Update the GUI's state
            #self.state = state_str
            self.question_type = question_type

            # Clear/delete all the existing fields/buttons
            self.text_fields.clear()

            #################################################            gui,     x,      y, width, height,                           text, background_clr, text_clr, outline_clr, font_name, font_size, input_text, is_visible, show_background, show_outline, horz_algnmt, vert_algnmt
            if self.question_type == 'OpenTopic' or True:
                self.text_fields['title']                   = TextField(self, 0.025, 0     , 0.95 , 0.112 , 'Reach for the Top'                           , None        , BLACK, None , 'opensans', 108, None          , True , False, False, 'center', 'center')
                self.text_fields['question_type_and_topic'] = TextField(self, 0.025, 0.12  , 0.6  , 0.06  , 'Open Question: '                             , None        , BLACK, None , 'opensans', 24 , None          , True , False, False, 'left'  , 'center')
                self.text_fields['points']                  = TextField(self, 0.65 , 0.12  , 0.325, 0.06  , 'Points: __'                                  , None        , BLACK, None , 'opensans', 24 , None          , True , False, False, 'right' , 'center')
                self.text_fields['question_container']      = TextField(self, 0.025, 0.2   , 0.6  , 0.1875, 'Question:'                                   , None        , BLACK, BLACK, 'opensans', 24 , None          , True , False, True , 'left'  , 'top')
                self.text_fields['question_text']           = TextField(self, 0.025, 0.25  , 0.6  , 0.1375, '...'                                         , None        , BLACK, None , 'opensans', 14 , None          , True , False, False, 'left'  , 'top')
                self.text_fields['answer_container']        = TextField(self, 0.025, 0.425 , 0.6  , 0.1875, 'Answer:'                                     , None        , BLACK, BLACK, 'opensans', 24 , None          , True , False, True , 'left'  , 'top')
                self.text_fields['answer_text']             = TextField(self, 0.025, 0.4625, 0.6  , 0.1375, '...'                                         , None        , BLACK, None , 'opensans', 14 , None          , True , False, False, 'left'  , 'top')
                self.text_fields['show_answer_button']      = TextField(self, 0.65 , 0.2   , 0.325, 0.7   , 'No Response...'                              , LIGHT_GREEN , BLACK, BLACK, 'opensans', 42 , 'ShowAnswer'  , False, True , True , 'center', 'center')
                self.text_fields['correct_button']          = TextField(self, 0.65 , 0.2   , 0.325, 0.3375, 'Correct'                                     , LIGHT_GREEN , BLACK, BLACK, 'opensans', 42 , 'Correct'     , True , True , True , 'center', 'center')
                self.text_fields['incorrect_button']        = TextField(self, 0.65 , 0.5625, 0.325, 0.3375, 'Incorrect'                                   , LIGHT_RED   , BLACK, BLACK, 'opensans', 42 , 'Incorrect'   , True , True , True , 'center', 'center')
                self.text_fields['next_question_button']    = TextField(self, 0.65 , 0.2   , 0.325, 0.7   , 'Next Question'                               , LIGHT_YELLOW, BLACK, BLACK, 'opensans', 42 , 'NextQuestion', False, True , True , 'center', 'center')
                self.text_fields['date_and_time']           = TextField(self, 0.65 , 0.9   , 0.325, 0.075 , datetime.now().strftime('%A, %B %d; %I:%M %p'), None        , BLACK, None , 'opensans', 24 , None          , True , False, False, 'right' , 'bottom')
                self.text_fields['basic_scores']            = TextField(self, 0.025, 0.6   , 0.6  , 0.325 , '...'                                         , None        , BLACK, None , 'opensans', 42 , None          , True , False, False, 'center', 'center')

            elif self.question_type == 'Assign':
                pass
            elif self.question_type == 'WhoWhat':
                pass
            elif self.question_type == 'Tiebreak':
                pass
            elif self.question_type == 'Shootout':
                pass
            elif self.question_type == 'Team':
                pass
            elif self.question_type == 'Scramble':
                pass

    def render(self):
        ''' Renders all the text fields, etc. '''
        # Renders the background for the next frame
        self.window.fill(self.background_fill)
        # Updates the date and time (in bottom right corner)
        if 'date_and_time' in self.text_fields:
            self.text_fields.get('date_and_time').update_text(datetime.now().strftime('%A, %B %d; %I:%M %p'))
        # Adds every text field to the display
        for field in self.text_fields:
            self.text_fields.get(field).render()
        # Update the display with newly-rendered text fields
        pygame.display.update()
        # Limits the frames rendered per second (avoids unneccecary CPU load)
        self.clock.tick(24)

    def check_events(self):
        ''' Procedure that iterates through events (e.g. mouse clicks) and handles them appropriately '''
        for event in pygame.event.get():

            # Closes the window if promopted by user
            if event.type == pygame.QUIT:
                self.close()

            # Allows the user to resize the window
            elif event.type == pygame.VIDEORESIZE:
                # Changes the window size
                self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                # Resize each of the text fields, buttons, etc.
                for field in self.text_fields:
                    self.text_fields.get(field).resize(event)

            # Check for mouse clicks on buttons
            elif event.type == pygame.MOUSEBUTTONUP:
                for field in self.text_fields:
                    if self.text_fields.get(field).is_visible and self.text_fields.get(field).user_input:
                        if self.text_fields.get(field).rect.collidepoint(event.pos):
                            self.user_mouse_input = self.text_fields.get(field).user_input
                    

    def close(self):
        pygame.display.quit()
        pygame.quit()
        quit()


class Scoreboard:

    def __init__(self, names = [['Player ' + t + str(p+1) for p in range(4)] for t in 'AB'], points = [[0]*4]*2):
        pass

class TextField:
    ''' Backend class used by GUI class for creating and rendering text, buttons, etc. '''

    def __init__(self, gui, x, y, width, height, text, background_clr, text_clr, outline_clr, font_name, font_size, input_text_on_click, is_visible, show_background, show_outline, horz_algnmt, vert_algnmt):
        # Size, location, etc.
        self.x_percent = x
        self.x = x * gui.width
        self.y_percent = y
        self.y = y * gui.height
        self.width_percent = width
        self.width = width * gui.width
        self.height_percent = height
        
        self.height = height * gui.height
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.gui = gui
        # Background colour, outline, etc.
        self.is_visible = is_visible
        self.has_background_filled = show_background
        if not background_clr: background_clr = (0, 0, 0)
        self.background_colour = background_clr
        self.background_colour += tuple([255]) if self.has_background_filled else tuple([0])
        self.has_outline = show_outline
        self.outline_colour = outline_clr
        self.outline_width = 2 if self.has_outline else 0
        # Text and font
        self.text = text
        self.font_name = font_name
        self.preferred_font_size = font_size
        self.font_size = self.preferred_font_size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_colour = text_clr
        self.horz_alignment = horz_algnmt
        self.vert_alignment = vert_algnmt
        self.render_text()
        # Message passed to main program if button is clicked
        self.user_input = input_text_on_click

    def update_text(self, new_text):
        ''' Method for updating the text; don't try updating only self.text (need to render also) '''
        self.text = str(new_text)
        self.render_text()

    def resize(self, resize_event):
        ''' Resizes the field when the window is resized '''
        # Scales the rectangle to match the new window (while maintaing its proprtions within the window)
        self.x = self.x_percent * resize_event.w
        self.y = self.y_percent * resize_event.h
        self.width = self.width_percent * resize_event.w
        self.height = self.height_percent * resize_event.h
        self.rect = Rect(self.x, self.y, self.width, self.height)
        # Text may need to be resized
        self.render_text()

    def render_text(self):
        ''' Renders the text; adjusts size, newlines, etc. '''

        #### TODO ####
        ## handle text that requires multiple lines
        
        ## if font is too small, make it bigger
        self.font_size = self.preferred_font_size
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        
        while True:
            
            # renders the text with the given font, size
            if self.has_background_filled:
                self.rtext = self.font.render(self.text, True, self.text_colour, self.background_colour)
            else:
                self.rtext = self.font.render(self.text, True, self.text_colour, None)
            
            # if the text is not too big, break from loop
            if self.rtext.get_width() < self.width - 2*self.outline_width and self.rtext.get_height() < self.height - 2*self.outline_width:
                break
            else: # try making the font smaller
                self.font_size -= 1
                self.font = pygame.font.SysFont(self.font_name, self.font_size)

        #### Sets the horizontal position of the text, based on its alignment
        if self.horz_alignment == 'left':
            self.text_x = self.x + self.outline_width
        elif self.horz_alignment in ['center', 'centre']:
            self.text_x = self.x + (self.width - self.rtext.get_width())/2
        elif self.horz_alignment == 'right':
            self.text_x = self.x + self.width - self.rtext.get_width() - self.outline_width
        else:
            ## raise alignmentNotFoundError
            pass

        if self.vert_alignment == 'top':
            self.text_y = self.y + self.outline_width
        elif self.vert_alignment in ['center', 'centre', 'middle']:
            self.text_y = self.y + (self.height - self.rtext.get_height())/2
        elif self.vert_alignment == 'bottom':
            self.text_y = self.y + self.height - self.rtext.get_height() - self.outline_width
        else:
            ## raise alignmentNotFoundError
            pass

    def render(self):
        ''' Draws the text field to the provided GUI (including background, border, text as necesary)'''
        # split text or use smaller font if too big
        # draw/write the text (centred)

        if self.is_visible:

            if self.has_background_filled:
                pygame.draw.rect(self.gui.window, self.background_colour, self.rect)

            if self.has_outline:
                pygame.draw.rect(self.gui.window, self.outline_colour, self.rect, self.outline_width)
            
            if self.text:
                ## draws the text based on pos set in previous conditional
                self.gui.window.blit(self.rtext, (self.text_x, self.text_y))

    def click(self, gui):
        ''' Updates the GUI based on mouse input from the reader '''

        if self.user_input:
            gui.user_mouse_input = self.user_input