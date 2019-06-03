#See the group project page for agreed upon transmission order/format

QUESTION_TYPES = ["OpenTopic", "Assign", "WhoWhat", "Tiebreak", "Shootout", "Team", "Scramble"]

##*REWRITE METHOD CALLING

from GUI import *
#import pyonLIB.py as Serial
from pyonLIB import *

from Parser import *

global GUI
global ENDQUESTION
global FIRSTBUTTON
global SCORE;

filename = "test.txt"

SERCOM=SERCOM(1)

GUI = GraphicalUserInterface(600, 450, WHITE)

ENDQUESTION = False
FIRSTBUTTON = None



questionTypes = ["OPEN QUESTION", "TEAM QUESTION", "whowhat", "ASSIGNED QUESTION", "SHOOTOUT",  "TIE-BREAKERS IF NECESSARY", "WORD SCRAMBLE"]

SCORE = [0, 0, 0, 0, 0, 0, 0, 0];


questions = readinput

#######

def receiveFirstButton():

    FIRSTBUTTON = SERCOM.read()
    if FIRSTBUTTON != None:
        FIRSTBUTTON += 1
    SERCOM.clear()
    return FIRSTBUTTON

def sendEligibleBuzzers(buzzers):

    SERCOM.write(buzzers)

def updateScore(button, points):
    SCORE[button -1] += points

def sendQ(question):
    GUI.text_fields.get('question_text').update_text(question)

def sendA(answer):
    GUI.text_fields.get('answer_text').update_text(answer)

def sendScore():
    GUI.text_fields.get('basic_SCOREs').update_text(repr(SCORE))

def sendPoints(points):
    GUI.text_fields.get('points').update_text("Points: " + str(points))

def sendTopic(topic, questionType):
    GUI.text_fields.get('question_type_and_topic').update_text(questionType + ": " + topic)

def unansweredLoop():
    FIRSTBUTTON = receiveFirstButton()
    while FIRSTBUTTON == None and ENDQUESTION == False:
        GUI.check_events()
        if GUI.user_mouse_input:
            if GUI.user_mouse_input == "ShowAnswer":
                ENDQUESTION == True
                GUI.update_state("NoPointsShowAnswer")
            GUI.user_mouse_input = None
        FIRSTBUTTON = receiveFirstButton()

def receiveAnswerCheck():
    pass
    
def finishQuestion():
    pass

def openQuestion(question):

    points = question[1]
    topic = question[2]
    
    nQuestions = question[3]
    
    for q in range(0, nQuestions*2 -2, 2):
        GUI.start_new_question("OpenTopic")
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        sendQ(question[4 + q])
        sendA(question[5 + q])
        sendPoints(points)
        sendTopic(topic)
        answerCount = 0
        ENDQUESTION = False
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            if receiveAnswerCheck():
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

def teamQuestion(question):

    topic = question[1]
    sendPoints(10)
    sendQ(question[2])
    sendA(question[3])
    sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
    sendTopic("Scramble")
    ENDQUESTION = False
    scrambleWinner = -1
    unansweredLoop()

    while answerCount < 2 and ENDQUESTION == False:
        if receiveAnswerCheck():
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
        
    if scrambleWinner == -1: 
        for q in range(0, 4, 2):
            sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
            sendQ(question[4 + q])
            sendA(question[5 + q])
            sendPoints(10)
            sendTopic(topic)
            answerCount = 0
            ENDQUESTION = False
            unansweredLoop()
            while answerCount < 2 and ENDQUESTION == False:
                if receiveAnswerCheck():
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
    else:
        eligibleBuzzers = [0,0,0,0,0,0,0,0]
        for i in range(4*scrambleWinner, 4 + 4*scrambleWinner, 1):
            eligibleBuzzers[i] = 1
        for q in range(0, 4, 2):
            sendEligibleBuzzers([eligibleBuzzers])
            sendQ(question[4 + q])
            sendA(question[5 + q])
            sendPoints(10)
            sendTopic(topic)
            ENDQUESTION = False
            unansweredLoop()
            if receiveAnswerCheck():
                updateScore(FIRSTBUTTON, points)
                sendScore()
            else:
                ()
    
def whoAmIQuestion(question):

    whowhat = question[1]
    #sendWhowhat()
    answer = question[6]
    sendA(answer)
    sendTopic("")
    sendPoints(40)
    answered = False
    ENDQUESTION = False
    
    for c in range(0, 6, 2):
        if answered == True:
            break
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        sendQ(question[2 + q])
        sendA(answer)
        sendTopic("")
        answerCount = 0;
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            if receiveAnswerCheck():
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
    
def assignedQuestion(question):

    topic = question[1]
    sendPoints(10)
    sendTopic(topic)
    
    for q in range(0, 14, 2):
        eligibleBuzzers  = [0,0,0,0,0,0,0,0]
        eligibleBuzzers[q/2] = 1
        sendEligibleBuzzers([eligibleBuzzers])
        sendQ(question[2 + q/2])
        sendA(question[3 + q/2])
        
        if receiveAnswerCheck():
            updateScore((q+2)/2, 10)
            sendScore()
        else:
            eligibleBuzzers[q/2] = 0
            if q/2 < 4:
                eligibleBuzzers[q/2 + 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                if receiveAnswerCheck():
                    updateScore((q+2)/2 + 4, 10)
                    sendScore()
                else:
                    ()
            else:
                eligibleBuzzers[q/2 - 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                if receiveAnswerCheck():
                    updateScore((q+2)/2 - 4, 10)
                    sendScore()
                else:
                    ()

def shootoutQuestion(question):

    totalEligibleBuzzers = [1,1,1,1,1,1,1,1]
    answeredBuzzers = [0,0,0,0,0,0,0,0]
    nQuestions = question[1]
    sendPoints(10)
    sendTopic("")
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
        sendQ(question[2 + q])
        sendA(question[3 + q])
        answerCount = 0
        ENDQUESTION = False
        if checkWin == True:
            break
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            if receiveAnswerCheck():
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

def tiebreaker(question):

    points = question[1]
    topic = question[2]
    
    sendPoints(1)
    sendTopic(topic)
    nQuestions = question[3]
    
    for q in range(0, nQuestions*2 -2, 2):
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        sendQ(question[4 + q])
        sendA(question[5 + q])
        answerCount = 0
        ENDQUESTION = False
        winCondition = False
        unansweredLoop()
        while answerCount < 2 and ENDQUESTION == False:
            if receiveAnswerCheck():
                winCondition = True
            else:
                if FIRSTBUTTON >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                    unansweredLoop()
                if FIRSTBUTTON <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                    unansweredLoop()
                answerCount +=1;
        if winCondition == True:
            break

def wordscramble(question):
    pass
    

questionMethods = [openQuestion, teamQuestion, whowhatQuestion, assignedQuestion, shootoutQuestion, tiebreaker, wordscramble]

def main():
    
##    questions = parse(filename)
##        
##    for question in questions:
##        for q in questionTypes:
##            if question[0] == q:
##            questionMethods[q](question)

    sendEligibleBuzzers([[1,0,1,0,1,0,1,0]])
    SERCOM.close()

main()
