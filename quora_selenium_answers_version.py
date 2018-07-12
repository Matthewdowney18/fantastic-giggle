import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.tokenize import RegexpTokenizer
import hunspell
import pandas as pd
import os
from difflib import SequenceMatcher
import re

hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
tokenizer = RegexpTokenizer(r'\w+')


def make_dictionary(answer_counter, question_counter, url, columns, mispelled, q_text, length):
    '''creates a dictionary that can be used in making a table

    :param answer_counter: answer number
    :param question_counter: question number
    :param url: url
    :param columns: column header
    :param mispelled: list of mispelled words
    :param q_text:
    :param length:
    :return:
    '''
    text_info = {}
    text_info[columns[0]] = url
    text_info[columns[1]] = question_counter
    text_info[columns[2]] = q_text
    text_info[columns[3]] = answer_counter
    text_info[columns[4]] = mispelled
    text_info[columns[5]] = len(mispelled)
    text_info[columns[6]] = length
    return text_info


def check_spelling(text):
    '''creates a list of misspelled words in text
    :param text: the text
    :return: list of errors
    '''
    incorrect = []
    length = 0
    words = tokenizer.tokenize(text)
    for element in words:
        length += 1
        if not hobj.spell(element):
            incorrect.append(element)
    return incorrect, length


def find_answers(urls):
    """
    Goes through the soup object to find all divs that contain the answer class (Answer AnswerBase) then searches within
    those tags for the <p> tags which contain the actual text for the answer and then creates a new txt file which
    contains that text
    :param soup: the soup object from BeautifulSoup and allows for the parsing of the website
    :return: returns the count of how many text files have been made so more files can continue to be made
    """
    driverLocation = '/home/downey/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverLocation)
    count = 0
    question_counter = 0
    bad_count = 0
    for url in urls:
        answer_counter = 1
        question_counter += 1
        browser.execute_script("window.open('');")
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        time.sleep(2)
        scroll_page(3, browser.find_element_by_tag_name("body"))
        answers = browser.find_elements_by_css_selector('div[class="Answer AnswerBase"]')
        for answer in answers:
            # creating the misspelled word set might go here? not sure might need to test
            with open(str(answer_counter) + '_Experiences_in_life_' + str(question_counter) + '.txt', "w+") as f:
                text = answer.find_element_by_css_selector('span[class="ui_qtext_rendered_qtext"]').text
                bad_count = filter_url_or_answer(text)
                if bad_count == 0:
                    f.write(text)
                    answer_counter += 1
                    # spellchecker stuff should be put right here im pretty sure
                    #
                    #
                    #
            # dictionary stuff might be here im pretty sure
            #
            #
            #
        browser.close()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)
        count += 1
        if count == 2:  # this is just used to limit the amount of urls opened, testing purposes
            break
        # wont need to return anything with this version since this function takes in all the urls instead of just one
        #except maybe the dictionary but im not sure how thats working so im not gunna mess with that

def soup_given_url(given_url):
    """
    Takes in a url then using the BeautifulSoup library, creates a soup object which then can be parsed
    :param given_url: the url which you wish to go to and create the soup object from
    :return: returns the soup object back to main so it can be worked with and parsed
    """
    url = given_url
    content = urllib.request.urlopen(url)
    soup = BeautifulSoup(content, "html.parser")
    return soup


def filter_url_or_answer(string):
    """
    a huge list of dirty/inappropriate/bad words are included in this function so that any string passed into this
    function will be compared to the list. If the string is found to be containing any of the words the counter for
    bad words will go up and be returned. Essentially a function that is just used for filtering
    :param string: any string to be compared against the list, in the current case, urls and answers
    :return: the number of bad words found in the string
    """
    string_words = set(tokenizer.tokenize(string))

    bad_count = 0
    arrBad = set([
        '2g1c', '2 girls 1 cup', 'acrotomophilia', 'anal', 'anilingus', 'anus', 'arsehole', 'ass', 'asshole', 'assmunch'
        , 'auto erotic', 'autoerotic', 'babeland', 'baby batter', 'ball gag', 'ball gravy', 'ball kicking',
        'ball licking', 'ball sack', 'ball sucking', 'bangbros', 'bareback', 'barely legal', 'barenaked', 'bastardo',
        'bastinado', 'bbw', 'bdsm', 'beaver cleaver', 'beaver lips', 'bestiality', 'bi curious', 'big black',
        'big breasts', 'big knockers', 'big tits', 'bimbos', 'birdlock', 'bitch', 'black cock', 'blonde action',
        'blonde on blonde action', 'blow j', 'blow your l', 'blue waffle', 'blumpkin', 'bollocks', 'bondage', 'boner',
        'boob', 'boobs', 'booty call', 'brown showers', 'brunette action', 'bukkake', 'bulldyke', 'bullet vibe',
        'bung hole', 'bunghole', 'busty', 'butt', 'buttcheeks', 'butthole', 'camel toe', 'camgirl', 'camslut',
        'camwhore', 'carpet muncher', 'carpetmuncher', 'chocolate rosebuds', 'circlejerk', 'cleveland steamer',
        'clit', 'clitoris', 'clover clamps', 'clusterfuck', 'cock', 'cocks', 'coprolagnia', 'coprophilia', 'cornhole',
        'cum', 'cumming', 'cunnilingus', 'cunt', 'darkie', 'date rape', 'daterape', 'deep throat', 'deepthroat',
        'dick', 'dildo', 'dirty pillows', 'dirty sanchez', 'dog style', 'doggie style', 'doggiestyle', 'doggy style',
        'doggystyle', 'dolcett', 'domination', 'dominatrix', 'dommes', 'donkey punch', 'double dong',
        'double penetration', 'dp action', 'eat my ass', 'ecchi', 'ejaculation', 'erotic', 'erotism', 'escort',
        'ethical slut', 'eunuch', 'faggot', 'fecal', 'felch', 'fellatio', 'feltch', 'female squirting', 'femdom',
        'figging', 'fingering', 'fisting', 'foot fetish', 'footjob', 'frotting', 'fuck', 'fucking', 'fuck buttons',
        'fudge packer', 'fudgepacker', 'futanari', 'g-spot', 'gang bang', 'gay sex', 'genitals', 'giant cock',
        'girl on', 'girl on top', 'girls gone wild', 'goatcx', 'goatse', 'gokkun', 'golden shower', 'goo girl',
        'goodpoop', 'goregasm', 'grope', 'group sex', 'guro', 'hand job', 'handjob', 'hard core', 'hardcore', 'hentai',
        'homoerotic', 'honkey', 'hooker', 'hot chick', 'how to kill', 'how to murder', 'huge fat', 'humping', 'incest',
        'intercourse', 'jack off', 'jail bait', 'jailbait', 'jerk off', 'jigaboo', 'jiggaboo', 'jiggerboo', 'jizz',
        'juggs', 'kike', 'kinbaku', 'kinkster', 'kinky', 'knobbing', 'leather restraint', 'leather straight jacket',
        'lemon party', 'lolita', 'lovemaking', 'make me come', 'male squirting', 'masturbate', 'menage a trois',
        'milf', 'missionary position', 'motherfucker', 'mound of venus', 'mr hands', 'muff diver', 'muffdiving',
        'nambla', 'nawashi', 'negro', 'neonazi', 'nig nog', 'nigga', 'nigger', 'nimphomania', 'nipple', 'nipples',
        'nsfw images', 'nude', 'nudity', 'nympho', 'nymphomania', 'octopussy', 'omorashi', 'one cup two girls',
        'one guy one jar', 'orgasm', 'orgy', 'paedophile', 'panties', 'panty', 'pedobear', 'pedophile', 'pegging',
        'penis', 'phone sex', 'piece of shit', 'piss pig', 'pissing', 'pisspig', 'playboy', 'pleasure chest',
        'pole smoker', 'ponyplay', 'poof', 'poop chute', 'poopchute', 'porn', 'porno', 'pornography',
        'prince albert piercing', 'pthc', 'pubes', 'pussy', 'queaf', 'raghead', 'raging boner', 'rape', 'raping',
        'rapist', 'rectum', 'reverse cowgirl', 'rimjob', 'rimming', 'rosy palm', 'rosy palm and her 5 sisters',
        'rusty trombone', 's&m', 'sadism', 'scat', 'schlong', 'scissoring', 'semen', 'sex', 'sexo', 'sexy',
        'shaved beaver', 'shaved pussy', 'shemale', 'shibari', 'shit', 'shota', 'shrimping', 'slanteye', 'slut', 'smut',
        'snatch', 'snowballing', 'sodomize', 'sodomy', 'spic', 'spooge', 'spread legs', 'strap on', 'strapon',
        'strappado', 'strip club', 'style doggy', 'suck', 'sucks', 'suicide girls', 'sultry women', 'swastika',
        'swinger', 'tainted love', 'taste my', 'tea bagging', 'threesome', 'throating', 'tied up', 'tight white', 'tit',
        'tits', 'titties', 'titty', 'tongue in a', 'topless', 'tosser', 'towelhead', 'tranny', 'tribadism', 'tub girl',
        'tubgirl', 'tushy', 'twat', 'twink', 'twinkie', 'two girls one cup', 'undressing', 'upskirt', 'urethra play',
        'urophilia', 'vagina', 'venus mound', 'vibrator', 'violet blue', 'violet wand', 'vorarephilia', 'voyeur',
        'vulva', 'wank', 'wet dream', 'wetback', 'white power', 'women rapping', 'wrapping men', 'wrinkled starfish',
        'xx', 'xxx', 'yaoi', 'yellow showers', 'yiffy', 'zoophilia'])
    for word in arrBad:
        if word in string:
            bad_count += 1
    return bool(arrBad & string_words)


def get_dictionaries(url_list, columns, browser):
    '''
    with the provided urls, it determines which ones are good, and then creates a dictionary for them. then it
    combines the dictionaries into a list that can be used to make a table in pandas
    :param url_list: the list of urls
    :param columns: the colums for the tables, and the dictionaries
    :return: the list of dictionaries
    '''
    list_of_dictionaries = []
    answer_count = 0
    question_counter = 0
    i = 0
    for url in url_list:
        print(url)
        print('urls left: '+str(len(url_list)-i))
        i += 1
        searchObj = re.search('Unanswered', url, re.M | re.I)
        if not filter_url_or_answer(url) and not searchObj:
            soup = soup_given_url(url)
            answer_count, question_counter, dictionary = find_answers(browser, url) #may need to change this or modify my
                                                                                    #function so that it works with one url
            list_of_dictionaries += dictionary
            print('its good')
    return list_of_dictionaries


def scroll_page(no_of_pagedowns, elem):
    '''
    scrolls down the browser page to get more linkg
    :param no_of_pagedowns: the number of pages you want to scroll
    :param elem: the element that contains the scroll idk
    :return:
    '''
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        no_of_pagedowns -= 1


def get_urls_list(browser):
    '''
    finds the wanted links in the browser
    :param browser: the browser object
    :return: the list of urls of the questions
    '''
    list = []
    post_elems = browser.find_elements_by_class_name("question_link")
    for post in post_elems:
        list.append(post.get_attribute('href'))
    return list


def main(topic, number_of_scroll_downs, file_name):
    '''
    main function calls all the other functions and prints the output
    :param topic: the topic in quora
    '''
    driverLocation = '/home/downey/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverLocation)

    browser.get("https://www.quora.com/topic/"+topic+ "/all_questions")
    time.sleep(1)

    scroll_page(number_of_scroll_downs, browser.find_element_by_tag_name("body"))

    urls = get_urls_list(browser)
    print(urls)

    os.makedirs("/home/downey/PycharmProjects/quora/"+file_name)
    # then we change the directory that python looks at to the new place.
    os.chdir("/home/downey/PycharmProjects/quora/texts")

    columns = ['URL', 'Q_id', 'Q_text', 'answer_id', 'list_of_mispelled', 'length_of_mispelled', 'length_of_text']

    dictionaries = get_dictionaries(urls, columns, browser)

    table = pd.DataFrame.from_records(dictionaries, columns=columns)
    table.to_csv(path_or_buf='experiences_table.csv')

# can be run from the command line
main(str('Experiences-in-Life'), 50, 'texts')