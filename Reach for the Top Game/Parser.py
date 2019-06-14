
def parse(filename):
    import re

    #Returns True if 'text' is a PDF page footer
    def is_footer(text):
        footer = re.compile('.*REACH.*FOR.*THE.*TOP|.*SCHOOLREACH.*PACK.*|Page.*[0-9]+.*of.*[0-9]+')
        if footer.match(text) == None:
            return False
        else:
            return True

    def ignore(text):
        ignore_ = re.compile('.*PART.*|.*FOR.*EACH.*CORRECT.*ANSWER|.*MINUTE.*BREAK.*TO.*ROUND|END.*OF.*GAME|\n')
        if ignore_.match(text) == None:
            return False
        else:
            return True

    # first_int: returns the next number in the text
    def first_int(Text):
        for char in Text:
            if char.isnumeric():
                return char
        return 0

    # next_character returns the next non-numeric, non-space character in 'ine'                 
    def next_character(line):
        for char in line:
            if not char.isspace() and not char.isnumeric():
                return char

    def is_question_or_answer_or_clue(text):
        reg = re.compile(new_question_regex + '|' + question_regex + '|' + answer_regex + '|' + clue_regex)
        if reg.match(text) == None:
            return False
        else:
            return True

    #
    def read_multiline(Text, i, filter_):
        out = ''

        end_multiline = re.compile(filter_)
        while i < len(Text) and end_multiline.match(Text[i]) == None and not is_question_or_answer_or_clue(Text[i]):
            if not is_footer(Text[i]) and not ignore(Text[i]):
                out += ' ' + Text[i][:-1]
            i += 1

        return out, i



    #Opens file 
    File = open(filename, 'r')

    new_question_regex = '.*[0-9]+\-POINT|.*TIE-BREAKERS IF NECESSARY'
    question_regex = '.*[0-9]+\. '
    answer_regex = '.*A\. '
    clue_regex = '.*CLUE [A-Z]: '

    new_question_line = re.compile(new_question_regex)
    question_line = re.compile(question_regex)
    answer_line   = re.compile(answer_regex)
    clue_line     = re.compile(clue_regex)

    scramble_question = re.compile('(.[\.\,] .)+')
    scramble_answer = re.compile('\(any one of\) (.* or .*)*')

    Count = -1
    questions = []
    Text = File.readlines()
    Temp=[]
    Mainlist=[]
    Mainlist2=[]
    question_count = 0

    for i in range(len(Text)):
        char = next_character(Text[i])

    #A '-' follows the point number in the PDF, so the characters following a '-' describe the type of the question (eg. OPEN QUESTION, etc.)                            
        if new_question_line.match(Text[i]):
            if len(Temp) > 0 and ('OPEN' in Temp[0] or 'SPECIAL' in Temp[0]):
                Temp.insert(3, question_count)

            new_temp = []
            for thing in Temp:
                new_temp.append(thing.strip().rstrip() if isinstance(thing, str) else thing)
            if len(Temp) != 0 and re.compile('.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(new_temp[0]) != None:
                new_temp[0] = 'OPEN QUESTION'
            Mainlist.append(new_temp)
            Temp=[]
            question_count = 0
            Count += 1
            char_index = Text[i].index(char)
            type_ = Text[i][char_index+1+6:]
          
        

            #This handles question types that have topics, such as Open Questions.
            try:
                tmp = type_.split('-')
                tmp[1] = tmp[1][:-1]

                question_type = tmp[0]
                topic = tmp[1]
                points = int(Text[i][:Text[i].find(char)])                      
                Temp.append(question_type)

                if re.compile('.*ASSIGNED QUESTION').match(question_type) == None:
                    Temp.append(points)
                else:
                    Temp.append(10)
                Temp.append(topic)
           
                
            #This handles question types that do not have topics, such as Who Am I.
            except IndexError:
                try:
                    # QUESTION TYPE
                    question_type = type_[:-1]
                    if re.compile('.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(question_type) != None:
                        Temp.append('OPEN QUESTION')
                    else:
                        Temp.append(question_type)

                    # NOT WHO/WHAT AM I
                    if re.compile('.*(WHO|WHAT) AM').match(type_[:-1]) == None:
                        Temp.append(int(Text[i][:Text[i].find(char)]))  # POINTS

                    if re.compile('.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(question_type) != None:
                        Temp.append('')

                    # WHO/WHAT AM I
                    else:
                        Temp[-1] = 'WHO/WHAT AM I'
                        if type_[:3] == 'WHO':
                            Temp.append('WHO')
                        else:
                            Temp.append('WHAT')

                # This handles the tiebreakers. Since the tiebreaker line has a '-' in it, we just treat this as a special case.
                except ValueError:
                    Temp = [ Text[i][:-1] ]
                    Temp.append(10)
            

        # question line
        elif question_line.match(Text[i]):
            if Temp[0] != 'WHO/WHAT AM I':
                dot_idx = Text[i].find('.')
                Temp.append(Text[i][dot_idx+2:-1])

                # multiline questions
                # we stop reading once we see an answer
                r = read_multiline(Text, i+1, answer_regex)
                Temp[-1] += r[0]
                i = r[1]

                if scramble_question.match(Temp[-1]) != None:
                    Temp[-1] = ''.join(Temp[-1].split(' ')).replace(',','').replace('.','')

        # clue line
        elif clue_line.match(Text[i]):
            Temp.append(Text[i][8:-1])

            # multiline clues
            # we stop reading once we see another clue or an answer
            r = read_multiline(Text, i+1, clue_regex + '|' + answer_regex)
            Temp[-1] += r[0]
            i = r[1]

        # answer line
        elif answer_line.match(Text[i]):
            Temp.append(Text[i][3:-1])
            question_count += 1

            r = read_multiline(Text, i+1, question_regex + '|' + new_question_regex )
            Temp[-1] += r[0]
            i = r[1]

            if scramble_answer.match(Temp[-1]) != None:
                Temp[-1] = Temp[-1].split(' or ')[1:]
            
        
        
    if len(Temp) > 0 and Temp[0] == 'OPEN QUESTION':
        Temp.insert(3, question_count)
    Mainlist.append(Temp)
        

    # remove empty lists from Mainlist
    try:
        while True:
            Mainlist.remove([])
    except ValueError:
        pass

    File.close()

    return Mainlist


#    for m in Mainlist:
#        for i in m:
#            print(i)
#        print()


if __name__ == '__main__':
    parse('test.txt')
