#See the group project page for agreed upon transmission order/format
QUESTION_TYPES = ["OpenTopic", "Assign", "WhoWhat", "Tiebreak", "Shootout", "Team", "Scramble"] #question types Zane


from GUI import *

##from pyonLIB import *
from pyonLib import pyonLIB

from Parser import *

global GUI, ENDQUESTION, FIRSTBUTTON, SCORE

filename = "test.txt"

SERCOM=pyonLIB.SERCOM(1)

GUI = GraphicalUserInterface(600, 450, WHITE)

ENDQUESTION = False
FIRSTBUTTON = None

questionTypes = ["OPEN QUESTION", "TEAM QUESTION", "WHO/WHAT AM I", "ASSIGNED QUESTION", "SHOOTOUT",  "TIE-BREAKERS IF NECESSARY", "WORD SCRAMBLE"] #Question types Sunny

SCORE = [0, 0, 0, 0, 0, 0, 0, 0];


##questions = readinput

#######

def receiveFirstButton():

    GUI.update_state("ReaderAsking")

    FIRSTBUTTON = SERCOM.read() #update the global variable storing the first button that was pressed
    if FIRSTBUTTON != None: #If there has been a button pressed (this function is run in a loop so
        GUI.update_state("PlayerAnswering") #Update the GUI state
        FIRSTBUTTON += 1 #that is not always the case), add 1 to the value passed for easier use later
        return FIRSTBUTTON #return which button was pressed first
    
    

def sendEligibleBuzzers(buzzers): #Send to the arduino which buzzers are eligible

    SERCOM.write(buzzers) #'buzzers' in [1,0,1,0,1,0,1,0] format, 1 = yes, 0 = no
    SERCOM.clear() #clear the serial communication to prevent buffering/buildup

def updateScore(button, points):
    print(button)
    print(SCORE[button -1])
    print(points)
    SCORE[button -1] += points
def sendQ(question):
    GUI.text_fields.get('question_text').update_text(question)
def sendA(answer):
    GUI.text_fields.get('answer_text').update_text(answer)
def sendScore():
    GUI.text_fields.get('basic_scores').update_text(repr(SCORE))
def sendTopic(topic, questionType):
    GUI.text_fields.get('question_type_and_topic').update_text(questionType + ": " + topic)
def sendPoints(points):
    GUI.text_fields.get('points').update_text("Points: " + str(points))

    # this is borked, GUI.text_fields.get('points') is returning None
    #GUI.text_fields.get('points').update_text("Points: " + str(points))
    pass


def unansweredLoop(): #unanswered screen loop
    GUI.update_state('ReaderAsking') #Update state
    FIRSTBUTTON = receiveFirstButton()
    print(FIRSTBUTTON)
    #Check to receive first button pressed from arduino
    ENDQUESTION = False #Var to keep track of loop end
    while FIRSTBUTTON == None and ENDQUESTION == False:
        #While no button has been pressed
        GUI.check_events() #Check for click
        if GUI.user_mouse_input: #If click,
            if GUI.user_mouse_input == "ShowAnswer":
                #On button
                ENDQUESTION = True #End loop
                GUI.update_state("NoPointsShowAnswer")
                #Update state
                GUI.user_mouse_input = None
                #Reset mouse input
        FIRSTBUTTON = receiveFirstButton()
        print(FIRSTBUTTON)
        #Check to receive first button for next loop

def receiveAnswerCheck(): #check answer screen loop
    ENDQUESTION = False #Var to keep track of loop end
    while ENDQUESTION == False: #While no click
        GUI.check_events() #Check for click
        if GUI.user_mouse_input: #If click
            if GUI.user_mouse_input == 'Correct':
                #On correct button
                return True #return they got answer
                ENDQUESTION = True #end loop
                GUI.update_state('ReaderAsking')
                #Update state
                GUI.user_mouse_input = None
                #Reset mouse input
            elif GUI.user_mouse_input == 'Incorrect':
                #On incorrect button
                return False #return they got wrong
                ENDQUESTION = True #end loop
                
def finishQuestion(): #2 wrong answers loop
    GUI.update_state("NoPointsShowAnswer")
    #Update state to screen that shows answer
    ENDQUESTION = False #Var to keep track of loop end
    while ENDQUESTION == False:
        #While stay on the show answer screen
        GUI.check_events() #Check for click
        if GUI.user_mouse_input: #If click
            if gui.user_mouse_input == 'NextQuestion':
                #On next question button
                ENDQUESTION = True #end loop
                GUI.update_state('ReaderAsking')
                #Update state
                GUI.user_mouse_input = None
                #Reset mouse input

def openQuestion(question):

    points = question[1]
    topic = question[2]
    nQuestions = question[3]
    #Assign variables to store the information provided
    #by the question's list according to format
    
    for q in range(0, nQuestions*2 -2, 2):
    #Open questions often come in large bunches, so we combined
    #open questions in sequence into one bigger 'question' with
    #many subquestions to be more efficient
        
        GUI.start_new_question("OpenTopic") #Tell the GUI the question type
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]]) #Send eligible buzzers to arduino
        
        sendQ(question[4 + q])
        sendA(question[5 + q])
        sendPoints(points)
        sendTopic(topic, "Open Question")
        #Send information regarding the question to the GUI
        answerCount = 0
        #Counter variable for how many times people have tried to answer
        ENDQUESTION = False
        #Set the global variable keeping track of whether the current question is over yet to False
        
        unansweredLoop() #Run the loop for when the question hasn't been answered yet
        #This exits itself when a button is pressed and keeps track of which button was pressed first
        #If question is over, ie nobody guesses answer, changes ENDQUESTION variable to true
        while answerCount < 2 and ENDQUESTION == False:
            #While there are still attempts to answer remaining and the question isn't over
            answer = receiveAnswerCheck()
            #Runs the loop to update GUI state to give reader option to say whether the answer is
            #correct or incorrect, stores True/False in answer variable
            if answer: #If the answer was right
                updateScore(FIRSTBUTTON, points)
                sendScore()
                #Update and send the score
                answerCount = 2; #No remaining answer attempts, question will end itself next loop
            else: #Answer was wrong
                if FIRSTBUTTON >= 5: #If the answer came from team 2,
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]]) #They are now ineligible to answer
                    unansweredLoop()
                    #Update GUI state, start unanswered loop for other team to get a chance to answer
                if FIRSTBUTTON <= 4: #Same as previous if block, except for if answer came from team 2
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                    unansweredLoop()
                answerCount +=1; #Add one answer attempt to the count
            if answerCount >= 2 and answer == False:
                #If answer attempt count is max at 2 (1 each team)
                finishQuestion() #Update GUI state to show the answer, then proceed to next question

def teamQuestion(question):

    topic = question[1]
    GUI.start_new_question("Team")

    topic = ""
    sendPoints(10)
    sendQ(question[2])
    sendA(question[3])
    sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
    sendTopic("", "Scramble")
    ENDQUESTION = False
    scrambleWinner = -1
    unansweredLoop()

    answerCount = 0

    while answerCount < 2 and ENDQUESTION == False:
        answer = receiveAnswerCheck()
        if answer:
            if FIRSTBUTTON <= 4:
                scrambleWinner = 0
            if FIRSTBUTTON > 4:
                scrambleWinner = 1
            updateScore(FIRSTBUTTON, points)
            sendScore()
            answerCount = 2;
        else:
            if FIRSTBUTTON >= 5:
                sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                unansweredLoop()
            if FIRSTBUTTON <= 4:
                sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                unansweredLoop()
            answerCount +=1;
        if answerCount >= 2 and answer == False:
                finishQuestion()
        
    if scrambleWinner == -1: 
        for q in range(0, 4, 2):
            sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
            GUI.start_new_question("Team")
            sendQ(question[4 + q])
            sendA(question[5 + q])
            sendPoints(10)
            sendTopic(topic)
            sendTopic(topic, "Team Question")
            answerCount = 0
            ENDQUESTION = False
            unansweredLoop()
            while answerCount < 2 and ENDQUESTION == False:
                answer = receiveAnswerCheck()
                if answer:
                    updateScore(FIRSTBUTTON, points)
                    sendScore()
                    answerCount = 2;
                else:
                    if FIRSTBUTTON >= 5:
                        sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                        unansweredLoop()
                    if FIRSTBUTTON <= 4:
                        sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                        unansweredLoop()
                    answerCount +=1;
                if answerCount >= 2 and answer == False:
                    finishQuestion()
    else:
        eligibleBuzzers = [0,0,0,0,0,0,0,0]
        for i in range(4*scrambleWinner, 4 + 4*scrambleWinner, 1):
            eligibleBuzzers[i] = 1
        for q in range(0, 4, 2):
            sendEligibleBuzzers([eligibleBuzzers])
            GUI.start_new_question("Team")
            sendQ(question[4 + q])
            sendA(question[5 + q])
            sendPoints(10)
            sendTopic(topic)
            sendTopic(topic, "Team Question")
            ENDQUESTION = False
            unansweredLoop()
            answer = receiveAnswerCheck()
            if answer:
                updateScore(FIRSTBUTTON, points)
                sendScore()
            else:
                finishQuestion()
    
def whoAmIQuestion(question):
    whowhat = question[1]
    answer = question[6]
    answered = False
    ENDQUESTION = False
    
    for q in range(0, 6, 2):
        if answered == True:
            break
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        GUI.start_new_question("WhoWhat")
        sendQ(question[2 + q])
        sendA(answer)
        sendTopic("", whowhat + " Am I?")
        sendPoints(40 - 10*(q/2))
        answerCount = 0;
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            answer = receiveAnswerCheck()
            if answer:
                updateScore(FIRSTBUTTON, 40 - 10*(q/2))
                sendScore()
                answered = True
            else:
                if FIRSTBUTTON >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                    unansweredLoop()
                if FIRSTBUTTON <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                    unansweredLoop()
                answerCount +=1;
            if answerCount >= 2 and answer == False:
                finishQuestion()

def assignedQuestion(question):

    topic = question[1]

    for q in range(0, 14, 2):
        eligibleBuzzers  = [0,0,0,0,0,0,0,0]
        eligibleBuzzers[q/2] = 1
        sendEligibleBuzzers([eligibleBuzzers])
        GUI.start_new_question("Assign")
        sendQ(question[2 + q/2])
        sendA(question[3 + q/2])
        sendPoints(10)
        sendTopic(topic, "Assigned Question")
        answer = receiveAnswerCheck()
        if answer:
            updateScore((q+2)/2, 10)
            sendScore()
        else:
            eligibleBuzzers[q/2] = 0
            if q/2 < 4:
                eligibleBuzzers[q/2 + 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                answer = receiveAnswerCheck()
                if answer:
                    updateScore((q+2)/2 + 4, 10)
                    sendScore()
                else:
                    finishQuestion()
            else:
                eligibleBuzzers[q/2 - 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                answer = receiveAnswerCheck()
                if answer:
                    updateScore((q+2)/2 - 4, 10)
                    sendScore()
                else:
                    finishQuestion()

                    
def shootoutQuestion(question):
    totalEligibleBuzzers = [1,1,1,1,1,1,1,1]
    answeredBuzzers = [0,0,0,0,0,0,0,0]
    nQuestions = question[1]
    checkWin = False
    for q in range(0, nQuestions*2 -2, 2):
        winCondition = 4
        for a in range(4):
            if answeredBuzzers[a] == 1:
                count +=1
        if count == winCondition:
            for i in range(4):
                updateScore(i + 1, 10)
                checkWin = True
        else:
            count = 0
        for a in range(4, 8):
            if answeredBuzzers[a] == 1:
                count +=1
        if count == winCondition:
            for i in range(4, 8):
                updateScore(i + 1, 10)
                checkWin = True
        else:
            count = 0
        sendScore()
        
        eligibleBuzzers = [totalEligibleBuzzers[i] - answeredBuzzers[i] for i in range(8)]
        sendEligibleBuzzers([eligibleBuzzers])
        GUI.start_new_question("Shootout")
        sendQ(question[2 + q])
        sendA(question[3 + q])
        sendPoints(10)
        sendTopic("", "Shootout Question")
        answerCount = 0
        ENDQUESTION = False
        if checkWin == True:
            break
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            answer = receiveAnswerCheck()
            if answer:
                answeredBuzzers[FIRSTBUTTON] = 1
                answerCount = 2
            else:
                if FIRSTBUTTON >= 5:
                    eligibleBuzzers = [[1,1,1,1,0,0,0,0][i] - answeredBuzzers[i] for i in range(8)]
                    for i in eligibleBuzzers:
                        if i == -1:
                            i = 0
                    sendEligibleBuzzers([eligibleBuzzers])
                    unansweredLoop()
                    
                if FIRSTBUTTON <= 4:
                    eligibleBuzzers = [[0,0,0,0,1,1,1,1][i] - answeredBuzzers[i] for i in range(8)]
                    for i in eligibleBuzzers:
                        if i == -1:
                            i = 0
                    sendEligibleBuzzers([eligibleBuzzers])
                    unansweredLoop()
                
                answerCount +=1
            if answerCount >= 2 and answer == False:
                finishQuestion()

                
def tiebreaker(question):
    points = question[1]
    topic = question[2]

    nQuestions = question[3]

    for q in range(0, nQuestions*2 -2, 2):
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        GUI.start_new_question("")
        sendQ(question[4 + q])
        sendA(question[5 + q])
        sendPoints(1)
        sendTopic(topic, "Tiebreaker")
        answerCount = 0
        ENDQUESTION = False
        winCondition = False
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            answer = receiveAnswerCheck()
            if answer:
                winCondition = True
                send
            else:
                if FIRSTBUTTON >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                    unansweredLoop()
                if FIRSTBUTTON <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                    unansweredLoop()
                answerCount +=1;
            if answerCount >= 2 and answer == False:
                finishQuestion()
        if winCondition == True:
            break


def wordscramble(question):
    pass


questionMethods = [openQuestion, teamQuestion, whoAmIQuestion, assignedQuestion, shootoutQuestion, tiebreaker, wordscramble]

def main():

##    questions = parse(filename)
##        
##    for question in questions:
##        for q in questionTypes:
##            if question[0] == q:
##            questionMethods[q](question)
    
    questions = parse(filename)

    ##SERCOM.write([[1,1,1,1,1,1,1,1]])

    while True and False:
        print(SERCOM.read())

    for question in questions:
        q = questionTypes.index(question[0])
        questionMethods[q](question)

    SERCOM.close()

main()
