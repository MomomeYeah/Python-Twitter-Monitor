import argparse
import requests
import threading
import time
from bs4 import BeautifulSoup
from api import APIServer


def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Account Monitor")
    parser.add_argument("--handle", required=True, help="The Twitter handle to monitor")
    parser.add_argument("--interval", required=False, default=10, type=int, help="The length of time in minutes between monitoring intervals")
    parser.add_argument("--initial", required=False, default=5, type=int, help="The number of Tweets to initially fetch")

    return parser.parse_args()

# Test inactive: BillNye
# Test active: Telkomsel / kirin_brewery
class TweetMonitor:
    def __init__(self, handle):
        self.handle = handle
        self.tweet_ids = []
        self.tweets = []

    def get_tweets_for_handle(self, limit=None):
        # use legacy (no-JS) URL - this is only valid until December 15th, 2020
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
        # creation. To ensure we keep the same object ID for self.tweets, we
        # make sure not to assign a new variable here. This is so that the
        # reference to this object used by the API remains valid
        new_tweet_content = [tweet["text"] for tweet in new_tweets][:limit]
        self.tweets[:0] = new_tweet_content

        # return new Tweets
        return new_tweet_content

if __name__ == "__main__":
    args = parse_args()
    print ("*"*80 + "\n")
    print ("Welcome to Twitter monitor!\n")
    print ("\n    Args:")
    print ("\n      Handle: {}".format(args.handle))
    print ("\n      Interval: {}".format(args.interval))
    print ("\n      Initial Count: {}".format(args.initial))
    print ("\n" + "*"*80)

    try:
        # new monitor instance
        monitor = TweetMonitor(handle=args.handle)

        # new instance of API server
        server = APIServer(resource=monitor.tweets, endpoint_name="tweets")
        server_thread = threading.Thread(target=server.run)
        server_thread.start()

        # main loop
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
    except KeyboardInterrupt as e:
        # stop API server
        shutdown_url = "http://localhost:{}{}".format(server.port, server.shutdown_url)
        requests.get(shutdown_url)
        server_thread.join()
