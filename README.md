# Python-Twitter-Monitor

This is a program which will monitor posts from a given Twitter account.

The main loop is, loosely:

1. query the Twitter web page for the given handle, grabbing the 5 most recent
   Tweets (or as many as possible, if the handle has Tweeted fewer than 5 times)
1. sleep for 10 minutes
1. query the Twitter web page again, possible multiple times if the handle has
   Tweeted more than 20 times in the past 10 minutes
1. GOTO 2.

## Restrictions

The following restrictions apply to this implementation:

* the program must output text from new tweets to stdout
* the program must output the 5 most recent tweets right after execution
* then, it must check for (and display) new tweets every 10 mins
* the Twitter handle will be provided as a commandline argument by the user starting the program
* make sure to use scraping, or APIs that do not require user authentication or a twitter developer account
* using open source libraries like Twint or Tweepy to do the heavy lifting is not allowed

## Assumptions

* Tweets should be displayed in order of most to least recent, and this order
  should be maintained when polling for new Tweets

## Running the Program Directly

Assuming you have Python 3 installed, along with Pip 3:

* `pip3 install -r requirements.txt` - install all requirements
* `python3 monitor.py --handle <handle>` - use `--help` for additional options

## Running the Program with Vagrant

If you have Vagrant installed, the easiest way to run this program would be:

* `vagrant up` - provision an Ubuntu 20.04 VM
* `vagrant ssh` - SSH into the newly-created VM
* `cd /vagrant` - go to the Vagrant working directory
* `python3 monitor.py --handle <handle>` - use `--help` for additional options
* On the host machine, access `localhost:8080/api/tweets`

Note that Vagrant / VirtualBox doesn't seem to play nicely if Docker is installed,
the issue seems to be with Hyper-V. https://github.com/hashicorp/vagrant/issues/10070

## Running the Program with Docker

If you have Docker installed, the easiest way to run this program would be:

* `docker build -t python-twitter-monitor .`
* `docker run -itp 8000:8000 python-twitter-monitor`
* On the host machine, access `localhost:8000/api/tweets`

In order to change the listening interval, and set the Twitter handle, edit the
`Dockerfile` and modify the final `CMD` accordingly.

## Known Limitations

* Currently, Tweets are fetched using the legacy version of twitter.com, because
  on this version Tweets are fetched synchronously, which easily lends itself to
  scraping. According to Twitter, this version will be shut down on December
  15th 2020, at which point this tool presumably will no longer function. To get
  around this, it may be possible to reverse engineer the Twitter async protocol
  and make calls to this instead. This is the method employed by tools such as
  `twitter_scraper`, but no tools that I've tried so far actually work. If that
  doesn't work, it might be possible to do this via Selenium, or possibly Scrapy
  with a JavaScript-loading addition
* The API server is shutdown cleanly by the main program, by accessing the
  `/shutdown` endpoint. This can be accessed by any user of the program though,
  which will obviously cause the API server to stop functioning
