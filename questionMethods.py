#See the group project page for agreed upon transmission order/format

questionTypes = ["open", "team", "whowhat", "assigned", "shootout",  "tiebreaker"]

global score;
score = [0, 0, 0, 0, 0, 0, 0, 0];

questions = readinput

def updateScore(button, points)
    score[button -1] += points

def openQuestion(question):

    points = question[1]
    topic = question[2]
    
    sendPoints(points)
    sendTopic(topic)
    nQuestions = question[3]
    
    for q in range(0, nQuestions*2 -2, 2):
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        sendQ(question[4 + q])
        sendA(question[5 + q])
        answerCount = 0
        endQuestion = False
        while receiveFirstButton() == 0 and endQuestion == False:
            endQuestion = nextButtonPressed()
        while answerCount < 2 and endQuestion == False:
            if receiveAnswerCheck():
                updateScore(receiveFirstButton(), points)
                sendScore()
                answerCount = 2;
            else:
                if receiveFirstButton() >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                if receiveFirstButton() <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                answerCount +=1;

def teamQuestion(question):

    topic = question[1]
    sendPoints(10)
    sendQ(question[2])
    sendA(question[3])
    sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
    sendTopic("Scramble")
    endQuestion = False
    scrambleWinner = -1
    while receiveFirstButton() == 0 and endQuestion == False:
        endQuestion = nextButtonPressed()

    while answerCount < 2 and endQuestion == False:
        if receiveAnswerCheck():
            if receiveFirstButton() <= 4:
                scrambleWinner = 0
            if receiveFirstButton() > 4:
                scrambleWinner = 1
            updateScore(receiveFirstButton(), points)
            sendScore()
            answerCount = 2;
        else:
            if receiveFirstButton() >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                if receiveFirstButton() <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                answerCount +=1;
        
    if scrambleWinner == -1: 
        for q in range(0, 4, 2):
            sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
            sendQ(question[4 + q])
            sendA(question[5 + q])
            answerCount = 0
            endQuestion = False
            while receiveFirstButton() == 0 and endQuestion == False:
                endQuestion = nextButtonPressed()
            while answerCount < 2 and endQuestion = False:
                if receiveAnswerCheck():
                    updateScore(receiveFirstButton(), points)
                    sendScore()
                    answerCount = 2;
                else:
                    if receiveFirstButton() >= 5:
                        sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                    if receiveFirstButton() <= 4:
                        sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                    answerCount +=1;
    else:
        eligibleBuzzers = [[0,0,0,0,0,0,0,0]]
        for i in range(4*scrambleWinner, 4 + 4*scrambleWinner, 1):
            eligibleBuzzers[i] = 1
        for q in range(0, 4, 2):
            sendEligibleBuzzers([eligibleBuzzers])
            sendQ(question[4 + q])
            sendA(question[5 + q])
            answerCount = 0
            endQuestion = False
            while receiveFirstButton() == 0 and endQuestion == False:
                endQuestion = nextButtonPressed()
            while answerCount < 2 and endQuestion = False:
                if receiveAnswerCheck():
                    updateScore(receiveFirstButton(), points)
                    sendScore()
                    answerCount = 2;
                else:
                    answerCount +=1;
    
def whoAmIQuestion(question):

    whowhat = question[1]
    sendWhowhat()
    answer = question[2]
    sendA(answer)
    sendPoints(10)
    sendTopic("")
    answered = False
    endQuestion = False
    
    for c in range(0, 6, 2):
        if answered == True:
            break
        sendEligibleBuzzers([[1,1,1,1,1,1,1,1]])
        sendQ(question[3 + q])
        answerCount = 0;
        while receiveFirstButton() == 0 and endQuestion == False:
            endQuestion = nextButtonPressed()
        while answerCount < 2 and endQuestion = False:
            if receiveAnswerCheck():
                updateScore(receiveFirstButton(), 40 - 10*(q/2))
                sendScore()
                answered = True
            else:
                if receiveFirstButton() >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                if receiveFirstButton() <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
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
            updateScore(q/2, 10)
            sendScore()
        else:
            eligibleBuzzers[q/2] = 0
            if q < 4:
                eligibleBuzzers[q + 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                if receiveAnswerCheck():
                    updateScore(q/2 + 4, 10)
                    sendScore()
                else:
                    ()
            else:
                eligibleBuzzers[q/2 - 4] = 1
                sendEligibleBuzzers([eligibleBuzzers])
                if receiveAnswerCheck():
                    updateScore(q/2 - 4, 10)
                    sendScore()
                else:
                    ()

def shootoutQuestion(question):

    totalEligibleBuzzers = [1,1,1,1,1,1,1,1]
    answeredBuzzers = [0,0,0,0,0,0,0,0]
    nQuestions = question[1]
    sendPoints(10)
    sendTopic("")
    checkWin = False:
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
        endQuestion = False
        if checkWin == True:
            break
        while receiveFirstButton() == 0 and endQuestion == False:
            endQuestion = nextButtonPressed()
        while answerCount < 2 and endQuestion == False:
            if receiveAnswerCheck():
                answeredBuzzers[receiveFirstButton()] = 1
                answerCount = 2
            else:
                if receiveFirstButton() >= 5:
                    eligibleBuzzers = [[1,1,1,1,0,0,0,0][i] - answeredBuzzers[i] for i in range(8)]
                    for i in eligibleBuzzers:
                        if i == -1:
                            i = 0
                    
                if receiveFirstButton() <= 4:
                    eligibleBuzzers = [[0,0,0,0,1,1,1,1][i] - answeredBuzzers[i] for i in range(8)]
                    for i in eligibleBuzzers:
                        if i == -1:
                            i = 0
                
                sendEligibleBuzzers([eligibleBuzzers])
                answerCount +=1


def endQuestion(question):

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
        endQuestion = False
        winCondition = False
        while receiveFirstButton() == 0 and endQuestion == False:
            endQuestion = nextButtonPressed()
        while answerCount < 2 and endQuestion == False:
            if receiveAnswerCheck():
                winCondition = True
            else:
                if receiveFirstButton() >= 5:
                    sendEligibleBuzzers([[1,1,1,1,0,0,0,0]])
                if receiveFirstButton() <= 4:
                    sendEligibleBuzzers([[0,0,0,0,1,1,1,1]])
                answerCount +=1;
        if winCondition == True:
            break
    
questionMethods = [openQuestion, teamQuestion, whowhatQuestion, assignedQuestion, shootoutQuestion, endQuestion]

while endGame = False:
    
    for question in questions:
        questionMethods[question[0](question)]
    
