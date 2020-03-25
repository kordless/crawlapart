# RUN ALL WEBSITES CRAWL

We are going to use this repo as a base for tooling surrounding crawling sites that require javascript to be running...Geckodriver is a cli based tool that we can use to get data from various sources.



For the majority of the scripting we are going to assume that geckodriver binary is in your path:

If you need to download it head over here:
https://github.com/mozilla/geckodriver/releases


WE DO NEED A BASE MARIONETTE ENABLED MOZILLA PROFILE....

We need to enable marrionette when we launch mozilla

Because I wanted to use a different port marionette is enabled on port
2928

## RUNNING FIREFOX AND CONNECTING TO MARIONETTE
```bash
user@host:~/rawcrawl$ firefox-esr --new-instance --marionette --profile <PATHTOPROFILE>

```

## GETTING GECKODRIVER

A better strategy is to start the geckodriver process and then request a new firefox instance using our capabilities profile YMMV

`$ geckodriver -vvv --marionette-port 2928 &`


## INTERACTING WITH GECKODRIVER

Use HTTP METHODS to send commands to the firefox instance that you have spawned up.  The commands for the webdriver spec are:

[At W3 org site](https://www.w3.org/TR/webdriver1/#dfn-commands)


To open a firefox session with gecko use the [Capabilities](https://developer.mozilla.org/en-US/docs/Web/WebDriver/Capabilities/firefoxOptions) options within firefox:

```bash
curl -d @capabilities.json --url 'http://localhost:4444/session

```
SAVE THE SESSION ID ABOVE!!!!!!!!!!


To go to a specific URL Do the following:

```bash

To navigate to a url:

curl -XPOST -d'{"url": "https://biddie.de/info"}' --url "http://localhost:4444/session/${sessionId}/url"
```

## NAVIGATING TO WINDOWS

```bash
curl "http://localhost:4444/session/${THECURLSESSION}/window/handles/"
{"value":["2147483649","4294967297"]}
```

Switch to window from the above:

```bash
# SWITCH TO FIRST WINDOW
curl -XPOST -d'{"handle": "2147483649"}' --url "http://localhost:4444/session/${THECURLSESSION}/window"
```

## GET HTML AND OTHER ATTRIBUTES

[ELEMENT RETRIEVAL](https://www.w3.org/TR/webdriver1/#element-retrieval)


You must POST a JSON object i.e:

```javascript
{
  "using": "tag name",
  "value": "html"
}

```

If you don't put in a valid parameter you'll get the following error:


```javascript
{
  "value": {
    "error": "invalid argument",
    "message": "unknown variant `id`, expected one of `css selector`, `link text`, `partial link text`, `tag name`, `xpath` at line 1 column 14",
    "stacktrace": ""
  }
}

```



```bash
curl -d'{"using": "tag name", "value": "html"}' --url "http://localhost:4444/session/${THECURLSESSION}/element/"

```
```json
{"value":{"element-6066-11e4-a52e-4f735466cecf":"97ac75c4-144a-4607-ab80-ddc422a8319b"}}
```
```bash
ELEMENTID="97ac75c4-144a-4607-ab80-ddc422a8319b"

curl --url "http://localhost:4444/session/${THECURLSESSION}/element/${ELEMENTID}/property/innerText"


# TO GET THE INNER HTML
$ curl --url "http://localhost:4444/session/${THECURLSESSION}/element/{ELEMENTID}/property/innerHTML"
```




## NAVIGATING
Typing Text
```bash
curl -d'{"input": "key", "text": "hey there"}' --url "http://localhost:4444/session/${THECURLSESSION}/element/${ELEMENTID}/value"
```

Clear Text from box:
```
curl -d'{"input": null}' --url "http://localhost:4444/session/${THECURLSESSION}/element/65730faf-674e-4c1d-b386-a2e6fe03f077/clear"
```

## RUNNING JAVASCRIPT

This examples opens up a new tab within the browser:
```bash
curl -d'{"script": "window.open()", "args": ["about:blank"]}' --url "http://localhost:4444/session/${THECURLSESSION}/execute/async"
```

When running javascript you have two parameters "script" which is the js command you want to run an then `args` which is just a list of the arguments you want to pass. 



# THE COMMANDS HAVE BEEN IMPLEMENTED IN SELENIUM
[COMMANDS](https://github.com/SeleniumHQ/selenium/blob/8adf509682f459e2fa2c6c7d9f10450ac1c5352b/py/selenium/webdriver/remote/remote_connection.py#L104)
[BETTERCOMMANDS](https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol)
[PROXY CAPABILITIES](https://w3c.github.io/webdriver/#proxy)
