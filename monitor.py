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
# TODO: pep8
# TODO: simple REST API
# TODO: Dockerise
class TweetMonitor:
    def __init__(self, handle):
        self.handle = handle
        self.tweet_ids = []
        self.tweets = []

    # TODO: what's the limit on how many we can query here? what if the account posts too much?
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
        new_tweets = [
            {
                "id": tweet.get("data-id"),
                "text": tweet.get_text().strip()
            } for tweet in tweet_containers
            if tweet.get("data-id") not in self.tweet_ids
        ]

        # save all Tweet IDs
        self.tweet_ids += [tweet["id"] for tweet in new_tweets]

        # save all Tweet content, sliced if `limit` is set. Save new ones to
        # the start of the list, to maintain the list in descending order of
        # creation
        new_tweet_content = [tweet["text"] for tweet in new_tweets][:limit]
        self.tweets = new_tweet_content + self.tweets

        # return new Tweets
        return new_tweet_content

if __name__ == "__main__":
    args = parse_args()
    print ("Args: {}".format(args))

    monitor = TweetMonitor(handle=args.handle)
    limit = args.initial
    spacer = "-"*30
    while (True):
        print ("Fetching latest Tweets for user {}...".format(args.handle))
        tweets = monitor.get_tweets_for_handle(limit=limit)
        limit = None

        if not tweets:
            print ("None found!")
        else:
            for tweet in tweets:
                print ("{}\n\n{}\n".format(spacer, tweet))

        print ("{}\n\nSleeping for {} minutes...\n\n\n\n".format(spacer, args.interval))
        time.sleep(args.interval * 60)
