#!/usr/bin/env python3

from BrowserSession import BrowserSession
import sys
import argparse
import logging

def screenshot_page(url, verbose=False):
    if verbose:
        print("Fetching -----> {}".format(url))
    browser = BrowserSession()
    browser.headless = True
    browser.setup_session()
    browser.go_to_url(url)
    browser.save_screenshot()
    

def tesseract(url, verbose=False):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="specify url")
    parser.add_argument("-ss", "--screenshot", action="store_false")
    parser.add_argument("--debug", help="add debug informational output", action="store_true")
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    if args.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.debug("Increased level of output for debug mode")
    
    if args.screenshot:
        screenshot_page(args.url, verbose=args.debug)
        
          

if __name__ == '__main__':
    main()
