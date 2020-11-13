import argparse
import requests
import time
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Account Monitor")
    parser.add_argument("--handle", required=True, help="The Twitter handle to monitor")
    parser.add_argument("--interval", required=False, default=10, type=int, help="The length of time in minutes between monitoring intervals")
    parser.add_argument("--initial", required=False, default=5, type=int, help="The number of Tweets to initially fetch")

    return parser.parse_args()

# Test inactive: BillNye
# Test active: Telkomsel
class TweetMonitor:
    def __init__(self, handle):
        self.handle = handle
        self.tweet_ids = []
        self.tweets = []

    # TODO: first time, just get 5
    def get_tweets_for_handle(self, limit=None):
        # use legacy (no-JS) URL
        # TODO: can we reverse engineer the Twitter async protocol?
        # Perhaps check out twitter_scraper for ideas
        # TODO: another option would be using e.g. Selenium
        url = "https://mobile.twitter.com/{}".format(self.handle)

        response = requests.get(url)
        if not response:
            print ("Failed to get Tweets for user {}".format(self.handle))
            exit(1)

        # Each Tweet lives in a div with class `tweet-text`
        soup = BeautifulSoup(response.text, "html.parser")
        tweet_containers = soup.find_all("div", attrs = {
            "class": "tweet-text"
        })

        # Tweets that we've already saved will have their ID saved in
        # self.tweet_ids - throw away any that we've already seen

        # TODO: what's the best way to save all IDs, but only some texts?
        # We're duplicating effort here
        new_tweet_ids = [
            tweet.get("data-id")
            for tweet in tweet_containers
            if tweet.get("data-id") not in self.tweet_ids
        ]
        new_tweet_content = [
            tweet.get_text().strip()
            for tweet in tweet_containers
            if tweet.get("data-id") not in self.tweet_ids
        ][:limit]

        # new_tweets = {
        #     tweet.get("data-id"): tweet.get_text().strip()
        #     for tweet in tweet_containers
        #     if tweet.get("data-id") not in self.tweet_ids
        # }

        # always save every ID
        self.tweet_ids += new_tweet_ids

        # if `limit` arg is set, then only store that many Tweets
        self.tweets += new_tweet_content

        # return new values
        return new_tweet_content

if __name__ == "__main__":
    args = parse_args()
    print ("Args: {}".format(args))

    monitor = TweetMonitor(handle=args.handle)
    limit = args.initial
    spacer = "-"*30
    while (True):
        print ("Fetching latest Tweets for user {}".format(args.handle))
        tweets = monitor.get_tweets_for_handle(limit=limit)
        limit = None

        if not tweets:
            print ("None found!")
        else:
            # for id, tweet in tweets.items():
            #     print ("{}: {}\n\n".format(id, tweet))

            for tweet in tweets:
                print ("{}\n\n{}\n".format(spacer, tweet))

        print ("{}\n\nSleeping for {} minutes\n\n\n\n".format(spacer, args.interval))
        time.sleep(args.interval * 60)
