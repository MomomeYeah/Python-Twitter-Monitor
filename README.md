# Python-Twitter-Monitor

This is a program which will monitor posts from a given Twitter account.

## Restrictions

The following restrictions apply to this implementation:

* the program must output text from new tweets to stdout
* the program must output the 5 most recent tweets right after execution
* then, it must check for (and display) new tweets every 10 mins
* the Twitter handle will be provided as a commandline argument by the user starting the program
* make sure to use scraping, or APIs that do not require user authentication or a twitter developer account
* using open source libraries like Twint or Tweepy to do the heavy lifting is not allowed

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

## Known Limitations

* Currently, Tweets are fetched using the legacy version of twitter.com, because
  on this version Tweets are fetched synchronously, which easily lends itself to
  scraping. According to Twitter, this version will be shut down on December
  15th 2020, at which point this tool presumably will no longer function. To
  get around this, it may be possible to reverse engineer the Twitter async
  protocol, and make calls to this instead. This is the method employed by tools
  such as `twitter_scraper`, but no tools that I've tried so far actually work.
  If that doesn't work, it might be possible to do this via Selenium, or possibly
  Scrapy with a JavaScript-loading addition
* By the default the legacy Twitter site loads 30 Tweets at a time. If the specified
  use has Tweeted more than 30 times in the last 10 minutes, not all Tweets will
  be fetched. The page does have a `Load older Tweets` button, so it shouldn't be
  too hard to keep searching until we're all caught up

## TODO Items

* pep8 compliance
* Dockerise
* improve stdout formatting
