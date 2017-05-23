#works
import os.path
import re
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import urllib
import urllib.request
import urllib.parse
import tkinter
import collections

INTRO = "********************************\n*    Url2Text_parser by Kyso   *\n*    ENTER URL FOR ANALYSIS    *\n********************************\n"

#prepared for the "Do not ignore xml comments checkbox / parameter"
IGNORE_COMMENTS = True

TEST_URL1 = "https://simple.wikipedia.org/wiki/Main_Page"
TEST_URL2 = "http://sranda-vtipy-coviny.blogspot.cz/"
TEST_URL3 = "http://darksouls3.wiki.fextralife.com/Chameleon"
TEST_URL4 = "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.118.181101"
TEST_URL_LOCAL1 = "K:\python\html01.htm"
DOWNLOADED = "downloadedURL.txt"

#basic htm parser
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text

#          **********             stringPlay         *********** 

#what is word, baby dont hurt me
def what_is_word(input_Text):
    #get clean words
    return re.findall(r"[\w']+", input_Text)

#get rid of rest js vars
def strip_js(inputText):
    #get rid of rest js vars
    in_progress = re.sub("(\'*\')", "", inputText, flags=re.MULTILINE)
    in_progress = re.sub("(_+)", "", in_progress, flags=re.MULTILINE)
    #get rid of digits
    in_progress = re.sub("(\d)", "", in_progress, flags=re.MULTILINE)
    return in_progress

def word_count(input_Text):
    #wordlist = input_Text.split()
    wordlist = input_Text
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))

    #print("String\n" + wordstring +"\n")
    #print("List\n" + str(wordlist) + "\n")
    print("Frequencies\n" + str(wordfreq) + "\n")
    #print("Pairs\n" + str(zip(wordlist, wordfreq)))

def find_longest_word(input_Text):
    #word_list = input_Text.split()
    word_list = input_Text
    longest_word = ""
    for word in word_list:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word

def find_most_common_character(input_Text):
    return(collections.Counter(input_Text).most_common(1)[0])

def no_whites(inputText):
    return inputText.replace(" ", "")
    
#mainStuff and testing
#
#

def main():
    print (INTRO)
    print ("URL: ")
    input_URL = input("Some input please: ")
    #input_URL = input
    test = r'''
        <html>
            <body>
                <b>Name:</b> TEST<br>
                <b>Example</b>:<br>
                Some really interesting text, probably TLDR as you do not have time anyways.
            </body>
        </html>
    '''
    #important
    scriptpath = os.path.dirname(__file__)
    req = urllib.request.Request(input_URL)
    response = urllib.request.urlopen(req)
    info = response.info()
    #print(info.get_content_type())      # -> text/html
    #print(info.get_content_maintype())  # -> text
    #print(info.get_content_subtype())   # -> html
    output = response.read()
    # OUTPUT is string now
    stringOutput = str(output,'utf-8')
    parsed1 = dehtml(stringOutput)
    if (IGNORE_COMMENTS):
        parsed2 = re.sub("(<!--.*?-->)", "", parsed1, flags=re.MULTILINE)
    else:
        parsed2 = parsed1
    parsed3 = re.sub("(function\(.*;)", "", parsed2, flags=re.MULTILINE)
    parsed4 = strip_js(parsed3)
    #print (parsed4)
    words = what_is_word(parsed4)
    counter = collections.Counter(words)
    #do for each here for nicer console output
    print ("Word count: \n", counter)
    print ("Word count:")
    #print("{" + "\n".join("{}: {}".format(k, v) for k, v in counter.items()) + "}")
    print ("\n   *   *   *\n")
    counter_max = counter.most_common(1)[-1]
    print (" .. so the most common word is: ", counter_max[0], " with count of ", counter_max[1])
    print ("\n   *   *   *\n")
    print ("The longest word is: ", find_longest_word(words))
    print ("\n   *   *   *\n")
    most_common_letter = collections.Counter(no_whites(parsed4)).most_common(1)[0]
    print ("The most common letter: ", most_common_letter)
    


if __name__ == "__main__":
    main()

#tips

#Since you are using IDLE(GUI) the script may not be launched from the directory where the script resides. I think the best alternative is to go with something like:

#import os.path

#scriptpath = os.path.dirname(__file__)
#filename = os.path.join(scriptpath, 'test.txt')
#testFile=open(filename)
#print(testFile.read())
