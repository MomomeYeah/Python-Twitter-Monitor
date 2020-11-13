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

## Running the Program

### Vagrant

If you have Vagrant installed, the easiest way to run this program would be:

* `vagrant up` - provision an Ubuntu 20.04 VM
* `vagrant ssh` - SSH into the newly-created VM
* `cd /vagrant` - go to the Vagrant working directory
* `python3 monitor.py --handle <handle>`
