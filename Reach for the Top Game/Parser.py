#
# Parser for Reach for the Top question packs
#



def parse(filename):
    """ Parse the Reach for the Top question pack from the file called `filename`. """
    import re

    def isnumeric(char):
        """
        Quick-and-dirty implementation of str.isnumeric() method.

        Used for backwards-compatibility with Python 2.
        """
        return char in '0123456789'

    def read_multiline(Text, i, filter_):
        """ Read lines sequentially until `filter_` matches. """

        def is_question_or_answer_or_clue(text):
            """ Returns true if `text` matches the question, answer, or clue regexes. """
            reg = re.compile(new_question_regex + '|' + question_regex + '|' + answer_regex + '|' + clue_regex)
            if reg.match(text) == None:
                return False
            else:
                return True

        def is_footer(text):
            """ Returns True if 'text' is a PDF page footer. """
            footer = re.compile('.*REACH.*FOR.*THE.*TOP|.*SCHOOLREACH.*PACK.*|Page.*of.*')
            if footer.match(text) == None:
                return False
            else:
                return True

        def ignore(text):
            """ Used by `read_multiline`; returns true if `text` is just noise. """
            ignore_ = re.compile('.*PART.*|.*FOR.*EACH.*CORRECT.*ANSWER|.*MINUTE.*BREAK.*TO.*ROUND|END.*OF.*GAME|\n')
            if ignore_.match(text) == None:
                return False
            else:
                return True

        out = ''
        end_multiline = re.compile(filter_)
        while (i < len(Text)
            and end_multiline.match(Text[i]) == None
            and not is_question_or_answer_or_clue(Text[i])):

            if not is_footer(Text[i]) and not ignore(Text[i]):
                out += ' ' + Text[i][:-1]
            i += 1

        return out, i



    # Open the file to parse
    File = open(filename, 'r')

    # Read the file
    tmp_text = File.readlines()
    Text = []

    # Replace cp1252 characters with similar ASCII characters
    for line in tmp_text:
        line = line.replace('\x91', "`")
        line = line.replace('\x92', "'")
        line = line.replace('\x93', "``")
        line = line.replace('\x94', "''")
        line = line.replace('\x95', "")
        line = line.replace('\r'  , "")
        Text.append(line)

    # Create the regexes
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


    # Parser state variables
    Temp = []
    Mainlist = []
    question_count = 0
    Count = -1

    # Parsing loop
    for i in range(len(Text)):

        # Start of a new question
        if new_question_line.match(Text[i]):
            # SNAPSTART, SNAPOUT, SPECIAL, CHAIN SNAPPERS are treated the same as OPEN questions
            # TODO: Are there other question types that need this?
            if len(Temp) > 0 and re.compile('.*OPEN|.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(Temp[0]) is not None:
                # OPEN questions need a question count
                Temp.insert(3, question_count)
                Temp[0] = 'OPEN QUESTION'

            # Remove leading/trailing spaces
            new_temp = []
            for thing in Temp:
                new_temp.append(thing.strip().rstrip() if isinstance(thing, str) else thing)

            # Add the previously parsed question to the question list
            Mainlist.append(new_temp)

            # Reset/update the parser variables
            Temp=[]
            question_count = 0
            Count += 1

            # type_ ==> [ OPEN | TEAM | <whatever> ] QUESTION (- <topic>)?
            char_index = Text[i].index('-')
            type_ = Text[i][char_index+1+6:]

            # This handles question types that have topics, such as OPEN questions.
            try:
                # tmp ==> [ <question type>, <topic> ]
                tmp = type_.split('-')

                question_type = tmp[0]
                topic = tmp[1]

                # Lines are formatted as  `XX-POINT <question type> QUESTION - <topic>',
                # so slicing up to the index of the first '-' will give us XX, aka the
                # number of points this question is worth
                points = int(Text[i][:Text[i].find('-')])                      

                # Start building the parsed list
                Temp.append(question_type)

                # ASSIGNED questions don't need a points argument
                if re.compile('.*ASSIGNED QUESTION').match(question_type) == None:
                    Temp.append(points)
                else:
                    Temp.append(10)

                Temp.append(topic)
           
                
            # This handles question types that do not have topics, such as WHO/WHAT AM I.
            #
            # Since these question types don't have topics, `tmp` will only have a length
            # of 1, meaning `tmp[1]` is out of range, raising an IndexError that we catch
            # here
            except IndexError:
                try:
                    # Get the question type
                    question_type = type_
                    Temp.append(question_type)

                    # WHO/WHAT AM I questions don't need a points field
                    if re.compile('.*(WHO|WHAT) AM').match(type_[:-1]) == None:
                        # Lines are formatted as  `XX-POINT <question type> QUESTION - <topic>',
                        # so slicing up to the index of the first '-' will give us XX, aka the
                        # number of points this question is worth
                        Temp.append(int(Text[i][:Text[i].find('-')]))

                    # SNAPSTART, SNAPOUT, SPECIAL, CHAIN SNAPPERS questions don't need a <???> field
                    # TODO: What is this for?
                    if re.compile('.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(question_type) is not None:
                        Temp.append('')

                    # WHO/WHAT AM I questions need a field that tells
                    # whether it's a WHO AM I or a WHAT AM I question
                    if Temp[0] == 'WHO/WHAT AM I':
                        if type_[:3] == 'WHO':
                            Temp.append('WHO')
                        else:
                            Temp.append('WHAT')

                # This is for TIE-BREAKERS. (I don't think this works?)
                except ValueError:
                    Temp = [ Text[i][:-1] ]
                    Temp.append(10)


        # A sub-question. (eg. `12. What's the deal with airline peanuts?')
        elif question_line.match(Text[i]):
            # WHO/WHAT AM I questions' sub-question is just an
            # explanation of how WHO/WHAT AM I questions work,
            # so we skip them
            if Temp[0] != 'WHO/WHAT AM I':
                # Otherwise, we just grab the actual
                # question text from the line
                dot_idx = Text[i].find('.')
                Temp.append(Text[i][dot_idx+2:-1])

                # Multiline questions
                # We stop reading once we see an answer line
                r = read_multiline(Text, i+1, answer_regex)
                Temp[-1] += r[0]
                i = r[1]

                # SCRAMBLE questions have some extra stuff
                if scramble_question.match(Temp[-1]) is not None:
                    Temp[-1] = ''.join(Temp[-1].split(' ')).replace(',','').replace('.','')

        # A clue line. (eg. `CLUE B: I am very cool. WHO AM I?')
        # These are only used for WHO/WHAT AM I questions
        elif clue_line.match(Text[i]):
            # Grab the clue text
            Temp.append(Text[i][8:-1])

            # Multiline clues
            # We stop reading once we see another clue or an answer
            r = read_multiline(Text, i+1, clue_regex + '|' + answer_regex)
            Temp[-1] += r[0]
            i = r[1]

        # An answer line. (eg. `A. FAT ALBERT')
        elif answer_line.match(Text[i]):
            # Grab the answer text
            Temp.append(Text[i][3:-1])
            # Increment the question count for this question
            question_count += 1

            # Multiline answers.
            # We stop reading once we see another sub-question or a new question
            r = read_multiline(Text, i+1, question_regex + '|' + new_question_regex )
            Temp[-1] += r[0]
            i = r[1]

            # SCRAMBLE questions have some extra stuff
            if scramble_answer.match(Temp[-1]) is not None:
                Temp[-1] = Temp[-1].split(' or ')[1:]

    # END PARSING LOOP        

    # Add the final question to the mainlist

    # SNAPSTART, SNAPOUT, SPECIAL, CHAIN SNAPPERS are treated the same as OPEN questions
    # TODO: Are there other question types that need this?
    if len(Temp) > 0 and re.compile('.*OPEN|.*SNAPSTART|.*SNAPOUT|.*SPECIAL|.*CHAIN SNAPPERS').match(Temp[0]) is not None:
        # OPEN questions need a question count
        Temp.insert(3, question_count)
        Temp[0] = 'OPEN QUESTION'

    # Remove leading/trailing spaces
    new_temp = []
    for thing in Temp:
        new_temp.append(thing.strip().rstrip() if isinstance(thing, str) else thing)

    # Add the previously parsed question to the question list
    Mainlist.append(new_temp)


    # Remove empty lists from Mainlist
    try:
        while True:
            Mainlist.remove([])
    except ValueError:
        pass

    # Close the parsed file
    File.close()

    return Mainlist
# END `parse` FUNCTION



if __name__ == '__main__':
    out = parse('_tset.txt')
##    for m in out:
##        for i in m:
##            print(i)
##        print()
