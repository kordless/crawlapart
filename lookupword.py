#!/usr/bin/env python3

import webdriver
import json
import random
import time
import base64
import sys
import threading 
import requests
import traceback

configpath=""

config = json.loads(open('config.json', 'r').read())

def lookup_url(url, save_text=False):
    with webdriver.Session(config['webdriverip'], config['webdriverport'],capabilities=config['capabilities']) as session:

        if url is not None:
            session.url = url
        else:
            session.url = "https://google.com"
        session.window.fullscreen()
        sessionid = session.session_id 
        print("sessionID -------> {}".format(sessionid))
        #find_page_element = session.find
        #element_selector = {'using': 'css selector', 'value': '#article-summary'}
        #query_results = find_page_element.css(element_selector=element_selector['value'])
        #for element in query_results:
        #    print(dir(element))
        #print(query_results)
        #input()
        #if save_text:
        #    save_viewable_text(human_text=query_results.text,sessionid=sessionid,query=query)
        time.sleep(3)
        save_screenshot(sessionid,fullscreen=True)


def go_to_url(url, verbose=False):
    # TODO
    # should write a function to check that url is valid!
    session = webdriver.Session(config['webdriverip'], 
                           config['webdriverport'],
                           capabilities=config['capabilities'])

    session.url = url
    session.window.fullscreen()
    sessionid = session.session_id
    some_string = input("would you like to keep this session open for further debugging?")
    
    save_string = input("Would you like to take a screenshot?")

    if 'y' in save_string:
        save_screenshot(sessionid,fullscreen=True)
    if 'y' in some_string:
        pass
    else:
        session.close()
    return
    
def lookup_word(text,define=False,save_text=False,video=False, url=None,screenshot=True):
    

    oldsession = webdriver.Session(config['webdriverip'], config['webdriverport'],capabilities=config['capabilities'])
    #oldsession.session_id = "89cfc006-bba3-4ee5-9feb-ef13f5e8692e"
    
    if video:
        f_stop = threading.Event()
        

    with webdriver.Session(config['webdriverip'], config['webdriverport'],capabilities=config['capabilities']) as session:

        if url is not None:
            session.url = url
        else:
            session.url = "https://google.com"
        session.window.fullscreen()
        sessionid = session.session_id 
        print("sessionID -------> {}".format(sessionid))
    
        if video:
            f(f_stop,sessionid)

        time.sleep(random.randint(1, 99) * .01 + random.randint(0,1))
        texttotype = "{0}{search_text}"
        
        if define:
            query = texttotype.format('define: ',search_text=text)
            element_selector = {'using': 'css selector', 'value': '#dictionary-modules'}
        else:
            query = texttotype.format("",search_text=text)
            element_selector = {'using': 'css selector', 'value': '#searchform'}
        
        print("typing {query} in {url}".format(query=query,url=session.url))
        typingaction = session.actions
        for letter in query:
            time.sleep(random.randint(1, 99) * .01)
            typingaction.sequence('key', 'id').key_down(letter).key_up(letter).perform()

        time.sleep(random.randint(1, 99) * .01 + 1)
        
        print("pressing Enter!!!!!!!!!!")
        typingaction.sequence('key', 'id').key_down('\uE007').key_up('\uE007').perform()
        
        time.sleep(2)
        # Wait until page loads

        find_page_element = session.find
        query_results = find_page_element.css(element_selector=element_selector['value'])
        if len(query_results) == 0:
            print("Nothing matched CSS element/selector")
        for element in query_results:
            print("element -> {} \n =======\n TEXT: {} \n =======".format(element, element.text))

        if save_text:
            save_viewable_text(human_text=element.text,sessionid=sessionid,query=query) 
        if screenshot:
            save_screenshot(sessionid,fullscreen=True)

        
        

        #wait_to_close_session()
    try:
        f_stop.set()
    except:
        pass
    return


def save_viewable_text(human_text,sessionid,query):
    try:
        newhtmlfile = open(str('textgrab/' + query.replace(" ", "_") + "-" + str(int(time.time())) + '.txt'), 'w')
        newhtmlfile.write(human_text)
        newhtmlfile.close()   
    except IOError as err:
        print("I/O error: {0}".format(err))
    return


def wait_to_close_session():

    print("Type 'DONE' then press enter to close window\n")
    someinput = True
    while someinput:
        newinput = input('Prompt--->')
        if newinput.lower() == 'done':
            someinput = False
    return

def save_property(element,attributename):
    """YOU SHOULD WRITE THIS FUNCTION SOON to replace "saveHTML"
    """
    html_selector = {'property': 'innerHTML'}
    return
        

def save_screenshot(sessionid,filename=None,video=False,fullscreen=False,verbose=False):


    if filename is None:
        filename = sessionid
        
    if video:
        filename = "Screenshots/video/frames/" + filename + "-"  + str(int(time.time())) + ".png"
    else:
        filename = "Screenshots/named_screenshots/" + filename + str(int(time.time())) + ".png"
    try:
        if fullscreen:
            r = requests.get(url="http://localhost:4444/session/" + sessionid + "/moz/screenshot/full")
            print(r.status_code)
        else:
            r = requests.get(url="http://localhost:4444/session/" + sessionid + "/screenshot")
        if r.status_code == 200:
            try:
                
                with open(filename, 'wb') as screenshot:
                    screenshot.write(base64.b64decode(r.json()['value']))
            except IOError as err:
                print("I/O error: {0}".format(err))
            return 
        elif r.status_code == 404:
            print("Something is wrong with the session? maybe it's closed????")
            print(r.json())
            return
    except Exception:
        traceback.print_exc()

    return


    

def f(f_stop,sessionid):
    save_screenshot(sessionid,video=True)
    print("Taking another screenshot?")
    if not f_stop.is_set():
        threading.Timer(1.8,f, [f_stop,sessionid]).start()
    
    


def main():
    print(sys.argv)
    time.sleep(4)
    define = False
    save_text = False
    video=False
    url=None
    if 'url' in sys.argv:
        url = sys.argv[-1]
        print(url)
    if 'define' in sys.argv:
        define = True
    else:
        print("attempting regular search")

    if 'savetext' in sys.argv:
        save_text = True

    if 'createvideo' in sys.argv:
        video=True
    
    go_to_url(url=url)
    #lookup_url(url, save_text=save_text)
    #lookup_word(text=sys.argv[2],define=define,save_text=save_text,video=video,url=url)

if __name__ == "__main__":
    main()
