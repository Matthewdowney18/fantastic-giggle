from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from nltk.tokenize import RegexpTokenizer
import hunspell
import pandas as pd
import os


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


def find_answers(soup, answer_counter, question_counter, url, columns):
    """
    Goes through the soup object to find all divs that contain the answer class (Answer AnswerBase) then searches within
    those tags for the <p> tags which contain the actual text for the answer and then creates a new txt file which
    contains that text
    :param soup: the soup object from BeautifulSoup and allows for the parsing of the website
    :return: returns the count of how many text files have been made so more files can continue to be made
    """
    dictonaries = []
    divs = soup.find_all("div", class_="Answer AnswerBase")  # finds all the div tags with the answer class
    qdiv = soup.find_all("h1")
    for q in qdiv:
        question_text = q.find("span", class_="ui_qtext_rendered_qtext")
        question_counter += 1
    for d in divs:
        answers = d.find_all("p")  # within the span tags finds all the paragraph tags so answers can be kept together
        answer_counter += 1
        all_mispelled = set()
        length = 0
        with open(str(answer_counter) + '_Experiences in life_' + str(question_counter) + ".txt", "w+") as f:
            for a in answers:
                f.write(a.text)  # writes each answer in a separate text file
                f.write("\n")
                mispelled, line_length = check_spelling(a.text)
                length += line_length
                all_mispelled.update(set(mispelled))
        dictonary = make_dictionary(answer_counter, question_counter, url, columns, list(all_mispelled), question_text.text, length)
        dictonaries.append(dictonary)
    return answer_counter, question_counter, dictonaries

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


def scroll_page(no_of_pagedowns, elem):
    '''
    scrolls down the browser page to get more linkg
    :param no_of_pagedowns: the number of pages you want to scroll
    :param elem: the element that contains the scroll idk
    :return:
    '''
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
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


def get_dictionaries(urls, columns):
    list_of_dictionaries = []
    #urls = ['https://www.quora.com/What-is-a-Muslim-religious-service-like']
    answer_count = 0
    question_counter = 0
    for url in urls:
        print('urls left: '+str(len(urls)-question_counter))
        soup = soup_given_url(url)
        answer_count, question_counter, dictionary = find_answers(soup, answer_count, question_counter, url, columns)
        list_of_dictionaries+=dictionary

    return list_of_dictionaries


def main(topic):
    '''
    main function calls all the other functions and creates the text files with answers
    :param topic: the topic in quora
    '''
    os.makedirs("/home/downey/PycharmProjects/quora/texts")
    # then we change the directory that python looks at to the new place.
    os.chdir("/home/downey/PycharmProjects/quora/texts")

    driverLocation = '/home/downey/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverLocation)

    browser.get("https://www.quora.com/topic/"+topic+ "/top_questions")
    time.sleep(1)

    scroll_page(3, browser.find_element_by_tag_name("body"))

    urls = get_urls_list(browser)
    #print(urls)

    columns = ['URL', 'Q_id', 'Q_text', 'answer_id', 'list_of_mispelled', 'length_of_mispelled', 'length_of_text']

    dictionaries = get_dictionaries(urls, columns)

    table = pd.DataFrame.from_records(dictionaries, columns=columns)
    table.to_csv(path_or_buf='experiences_table.csv')

main(str('Experiences-in-Life'))
