# SmallCrawl

This repo contains a couple of things that you should use to crawl a site with a Mozilla binary as well as a GeckoDriver Process running.

The idea with all of this code is to be able to pretend that you're a browser.

## Gettin' Started

Requirements to run:

|Tool | Link |
| --- | ---- |
| Python Port of Webdriver | [webdriver geckodriver python wrapper](https://github.com/w3c/webdriver) |
| GeckoDriverBinary | [Releases Page](https://github.com/mozilla/geckodriver/releases/latest) |
| Mozilla Profile | [Needs Link]() | 

BrowserSession.py needs to be imported.  Take a look at [BrowserSession.py](https://gitlab.com/ch7ck/infomat/blob/master/BrowserSession.py#L101).

You will need geckodriver running locally:

    geckodriver -vv --marionette-port 2928


### To run this you will need the W3c [webdriver geckodriver python wrapper](https://github.com/w3c/webdriver). 


### Lookup Word

Lookup word's primary purpose is to ensure that you can lookup a word on google.  This commit should include some simple flags to allow a plugin to interact with lookupword and save a screenshot of the whole webpage.


