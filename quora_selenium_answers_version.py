"""
This module is a web scraper for quora which gathers all answers from 'Experiences in Life'
and compares them against the parameters we need like between so and so words or none mispelled
or no dirty words. Then it creates a dataframe and saves it to a dataframe so it is easily
visible what each answer has wrong with it
"""
from __future__ import print_function
import time
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.tokenize import RegexpTokenizer
import hunspell



HOBJ = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
TOKENIZER = RegexpTokenizer(r'\w+')


def make_dictionary(answer_counter, question_counter, url, columns, mispelled, q_text, length):
    """
    creates a dictionary that can be used in making a table

    :param answer_counter: answer number
    :param question_counter: question number
    :param url: url
    :param columns: column header
    :param mispelled: list of mispelled words
    :param q_text:
    :param length:
    :return:
    """
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
    """
    creates a list of misspelled words in text
    :param text: the text
    :return: list of errors
    """
    incorrect = []
    length = 0
    words = TOKENIZER.tokenize(text)
    for element in words:
        length += 1
        if not HOBJ.spell(element):
            incorrect.append(element)
    return incorrect, length


def get_size(string):
    """
    takes a string and find the size of it
    :param string: any string that could be passed in
    :return: an int value that represents the size of the string
    """
    return [int(s) for s in string.split() if s.isdigit()]


def filter_url_or_answer(string):
    """
    a huge list of dirty/inappropriate/bad words are included in this function so that any string
    passed into this function will be compared to the list. If the string is found to be containing
    any of the words the counter for bad words will go up and be returned. Essentially a function
    that is just used for filtering
    :param string: any string to be compared against the list, in the current case, urls and answers
    :return: the number of bad words found in the string
    """
    string_words = set(TOKENIZER.tokenize(string))

    bad_count = 0
    arrbad = set([
        '2g1c', '2 girls 1 cup', 'acrotomophilia', 'anal', 'anilingus', 'anus', 'arsehole', 'ass',
        'asshole', 'assmunch', 'auto erotic', 'autoerotic', 'babeland', 'baby batter', 'ball gag',
        'ball gravy', 'ball kicking', 'ball licking', 'ball sack', 'ball sucking', 'bangbros',
        'bareback', 'barely legal', 'barenaked', 'bastardo', 'bastinado', 'bbw', 'bdsm',
        'beaver cleaver', 'beaver lips', 'bestiality', 'bi curious', 'big black', 'big breasts',
        'big knockers', 'big tits', 'bimbos', 'birdlock', 'bitch', 'black cock', 'blonde action',
        'blonde on blonde action', 'blow j', 'blow your l', 'blue waffle', 'blumpkin', 'bollocks',
        'bondage', 'boner', 'boob', 'boobs', 'booty call', 'brown showers', 'brunette action',
        'bukkake', 'bulldyke', 'bullet vibe', 'bung hole', 'bunghole', 'busty', 'butt',
        'buttcheeks', 'butthole', 'camel toe', 'camgirl', 'camslut', 'camwhore', 'carpet muncher',
        'carpetmuncher', 'chocolate rosebuds', 'circlejerk', 'cleveland steamer', 'clit',
        'clitoris', 'clover clamps', 'clusterfuck', 'cock', 'cocks', 'coprolagnia', 'coprophilia',
        'cornhole', 'cum', 'cumming', 'cunnilingus', 'cunt', 'darkie', 'date rape', 'daterape',
        'deep throat', 'deepthroat', 'dick', 'dildo', 'dirty pillows', 'dirty sanchez', 'dog style',
        'doggie style', 'doggiestyle', 'doggy style', 'doggystyle', 'dolcett', 'domination',
        'dominatrix', 'dommes', 'donkey punch', 'double dong', 'double penetration', 'dp action',
        'eat my ass', 'ecchi', 'ecs', 'ejaculation', 'erotic', 'erotism', 'escort', 'ethical slut',
        'eunuch', 'faggot', 'fecal', 'felch', 'fellatio', 'feltch', 'female squirting', 'femdom',
        'figging', 'fingering', 'fisting', 'foot fetish', 'footjob', 'frotting', 'fuck', 'fucking',
        'fuck buttons', 'fudge packer', 'fudgepacker', 'futanari', 'g-spot', 'gang bang', 'gay sex',
        'genitals', 'giant cock', 'girl on', 'girl on top', 'girls gone wild', 'goatcx', 'goatse',
        'gokkun', 'golden shower', 'goo girl', 'goodpoop', 'goregasm', 'grope', 'group sex', 'guro',
        'hand job', 'handjob', 'hard core', 'hardcore', 'hentai', 'homoerotic', 'honkey', 'hooker',
        'hot chick', 'how to kill', 'how to murder', 'huge fat', 'humping', 'incest', 'intercourse',
        'jack off', 'jail bait', 'jailbait', 'jerk', 'lesbian', 'jigaboo', 'jiggaboo', 'jiggerboo',
        'jizz', 'juggs', 'kike', 'kinbaku', 'kinkster', 'kinky', 'knobbing', 'leather restraint',
        'leather straight jacket', 'lemon party', 'lolita', 'lovemaking', 'make me come',
        'male squirting', 'masturbate', 'menage a trois', 'milf', 'missionary position',
        'motherfucker', 'mound of venus', 'mr hands', 'muff diver', 'muffdiving', 'nambla',
        'nawashi', 'negro', 'neonazi', 'nig nog', 'nigga', 'nigger', 'nimphomania', 'nipple',
        'nipples', 'nsfw images', 'nude', 'nudity', 'nympho', 'nymphomania', 'octopussy',
        'omorashi', 'one cup two girls', 'one guy one jar', 'orgasm', 'orgy', 'paedophile',
        'panties', 'panty', 'pedobear', 'pedophile', 'pegging', 'penis', 'phone sex',
        'piece of shit', 'piss pig', 'pissing', 'pisspig', 'playboy', 'pleasure chest',
        'pole smoker', 'ponyplay', 'poof', 'poop chute', 'poopchute', 'porn', 'porno',
        'pornography', 'prince albert piercing', 'pthc', 'pubes', 'pussy', 'queaf', 'raghead',
        'raging boner', 'rape', 'raping', 'rapist', 'rectum', 'reverse cowgirl', 'rimjob',
        'rimming', 'rosy palm', 'rosy palm and her 5 sisters', 'rusty trombone', 's&m', 'sadism',
        'scat', 'schlong', 'scissoring', 'semen', 'sex', 'sexo', 'sexy', 'shaved beaver',
        'shaved pussy', 'shemale', 'shibari', 'shit', 'shota', 'shrimping', 'slanteye', 'slut',
        'smut', 'snatch', 'snowballing', 'sodomize', 'sodomy', 'spic', 'spooge', 'spread legs',
        'strap on', 'strapon', 'strappado', 'strip club', 'style doggy', 'suck', 'sucks',
        'suicide girls', 'sultry women', 'swastika', 'swinger', 'tainted love', 'taste my',
        'tea bagging', 'threesome', 'throating', 'tied up', 'tight white', 'tit', 'tits',
        'titties', 'titty', 'tongue in a', 'topless', 'tosser', 'towelhead', 'tranny', 'tribadism',
        'tub girl', 'tubgirl', 'tushy', 'twat', 'twink', 'twinkie', 'two girls one cup',
        'undressing', 'upskirt', 'urethra play', 'urophilia', 'vagina', 'venus mound', 'vibrator',
        'violet blue', 'violet wand', 'vorarephilia', 'voyeur', 'vulva', 'wank', 'wet dream',
        'wetback', 'white power', 'women rapping', 'wrapping men', 'wrinkled starfish', 'xx',
        'xxx', 'yaoi', 'yellow showers', 'yiffy', 'zoophilia', 'kiss', 'kissing', 'kisses', 'gay',
        'jerk', 'poop', 'rave', 'overdose', 'weed', 'ecstasy', 'crossdress', 'rob', 'drugs',
        'instagram', 'Instagram', 'cheating', 'navel', 'exhibitionist', 'dirty'])
    for word in arrbad:
        if word in string:
            bad_count += 1
    return bool(arrbad & string_words)


def scroll_page(no_of_pagedowns, pause_time, elem):
    """
    scrolls down the browser page to get more linkg
    :param no_of_pagedowns: the number of pages you want to scroll
    :param elem: the element that contains the scroll idk
    :return:
    """
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(pause_time)
        print('pagedowns left:' + str(no_of_pagedowns))
        no_of_pagedowns -= 1


def get_urls_list(browser):
    """
    finds the wanted links in the browser
    :param browser: the browser object
    :return: the list of urls of the questions
    """
    list_urls = []
    post_elems = browser.find_elements_by_class_name("question_link")
    for post in post_elems:
        list_urls.append(post.get_attribute('href'))
    return list_urls


def find_answers(urls, columns):
    """
    opens each url, and then collects various information from it and then
    creates a dictionary from it. It puts the dictionary, and creates a table.
    It's pretty bad lol
    :param urls: the list of urls
    :param columns: used for creating the dctionary and creating the table
    """
    driverlocation = '/home/downey/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverlocation)

    i = 0
    answer_counter = 0
    question_counter = 0
    dictionaries = []

    table = pd.DataFrame.from_records(dictionaries, columns=columns)
    table.to_csv(path_or_buf='experiences_table.csv')

    for url in urls:
        print(url)
        print('urls left: ' + str(len(urls) - i))
        i += 1

        searchobj = re.search('Unanswered', url, re.M | re.I)
        if filter_url_or_answer(url) or searchobj:
            print('unusable')
            continue

        browser.execute_script("window.open('');")
        time.sleep(.5)
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        time.sleep(1)
        scroll_page(0, .5, browser.find_element_by_tag_name("body"))

        question = browser.find_elements_by_css_selector('h1')
        if not question == []:
            question_text = question[0].find_elements_by_css_selector(
                'span[class="ui_qtext_rendered_qtext"]')
            answers = browser.find_elements_by_css_selector(
                'div[class="Answer AnswerBase"]')
            for answer in answers:
                answer_url = answer.find_element_by_css_selector(
                    'a[class="answer_permalink"]').get_attribute('href')
                length = 0
                with open(str(answer_counter) +
                          '_Experiences_in_life_' +
                          str(question_counter) + '.txt', "w+") as text_file:
                    text = answer.find_element_by_css_selector(
                        'span[class="ui_qtext_rendered_qtext"]').text
                    text_file.write(text)
                    misspelled, line_length = check_spelling(text)
                    length += line_length
                dictionary = make_dictionary(answer_counter, question_counter,
                                             answer_url, columns, misspelled,
                                             question_text[0].text, length)
                dictionaries.append(dictionary)
                answer_counter += 1
        browser.close()
        time.sleep(.5)
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(.5)

        question_counter += 1

        os.remove('experiences_table.csv')
        table = pd.DataFrame.from_records(dictionaries, columns=columns)
        table.to_csv(path_or_buf='experiences_table.csv')


def main(topic, number_of_scroll_downs, file_name):
    """
    main function gathers the list of urls and then sends them to the make dictionaries function.
    this makes a file with all the text files of the answers, a text file with the urls, and a csv
    with information about the answers
    :param topic: the topic on quorsa
    :param number_of_scroll_downs: how many scroll downs to get urls
    :param file_name: the name of the file it makes
    """

    driverlocation = '/home/downey/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverlocation)

    browser.get("https://www.quora.com/topic/"+topic+ "/all_questions")
    time.sleep(1)

    scroll_page(number_of_scroll_downs, 10, browser.find_element_by_tag_name("body"))

    urls = get_urls_list(browser)
    print(urls)
    with open('urls'+ '.txt', "w+") as text_file:
        for url in urls:
            text_file.write(url)
            text_file.write('\n')

    os.makedirs("/home/downey/PycharmProjects/quora/"+file_name)
    os.chdir("/home/downey/PycharmProjects/quora/" + file_name)

    columns = ['URL', 'Q_id', 'Q_text', 'answer_id', 'list_of_mispelled',
               'length_of_mispelled', 'length_of_text']

    find_answers(urls, columns)


main(str('Experiences-in-Life'), 250, 'texts_4')
