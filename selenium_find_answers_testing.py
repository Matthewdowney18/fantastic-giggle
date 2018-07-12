from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

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
    bad_count = 0
    list = []
    post_elems = browser.find_elements_by_class_name("question_link")
    for po in post_elems:
        url = po.get_attribute('href')
        if "unanswered" not in url:
            bad_count = filter_url_or_answer(url)
            if bad_count == 0:
                list.append(url)
    return list


def filter_url_or_answer(string):
    """
    a huge list of dirty/inappropriate/bad words are included in this function so that any string passed into this
    function will be compared to the list. If the string is found to be containing any of the words the counter for
    bad words will go up and be returned. Essentially a function that is just used for filtering
    :param string: any string to be compared against the list, in the current case, urls and answers
    :return: the number of bad words found in the string
    """
    bad_count = 0
    arrBad = [
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
        'xx', 'xxx', 'yaoi', 'yellow showers', 'yiffy', 'zoophilia', 'kiss', 'kissing', 'kisses', 'gay', 'jerk',
        'poop', 'rave', 'overdose', 'weed', 'ecstasy', 'crossdress', 'rob', 'drugs', 'instagram', 'Instagram',
        'cheating', 'navel', 'exhibitionist']
    for word in arrBad:
        if word in string:
            bad_count += 1
    return bad_count

def find_answers(browser, urls):
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
            #creating the misspelled word set might go here? not sure might need to test
            with open(str(answer_counter) + '_Experiences_in_life_' + str(question_counter) + '.txt', "w+") as f:
                text = answer.find_element_by_css_selector('span[class="ui_qtext_rendered_qtext"]').text
                bad_count = filter_url_or_answer(text)
                if bad_count == 0:
                    f.write(text)
                    answer_counter += 1
                    #spellchecker stuff should be put right here im pretty sure
                    #
                    #
                    #
            #dictionary stuff might be here im pretty sure
            #
            #
            #
        browser.close()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)
        count += 1
        if count == 2: #this is just used to limit the amount of urls opened, testing purposes
            break
        #wont need to return anything with this version since this function takes in all the urls instead of just one

def main(topic):
    driverLocation = '/home/kevin/Desktop/chromedriver_linux64/chromedriver'
    browser = webdriver.Chrome(driverLocation)

    browser.get("https://www.quora.com/topic/" + topic + "/top_questions")
    time.sleep(1)

    scroll_page(3, browser.find_element_by_tag_name("body"))

    urls = get_urls_list(browser)
    print(urls)
    find_answers(browser, urls)


main(str('Experiences-in-Life'))