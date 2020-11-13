import argparse
import requests
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Account Monitor")
    parser.add_argument("--handle", required=True, help="The Twitter handle to monitor")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    print ("Fetching most recent Tweets for user {}".format(args.handle))

    # use legacy (no-JS) URL
    # TODO: can we reverse engineer the Twitter async protocol?
    # Perhaps check out twitter_scraper for ideas
    url = "https://mobile.twitter.com/{}".format(args.handle)

    response = requests.get(url)
    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        tweet_objs = soup.find_all("div", attrs = {
            "class": "tweet-text"
        })
        tweets = {tweet.get("data-id"):tweet.get_text().strip() for tweet in tweet_objs[:5]}

        for id, tweet in tweets.items():
            print ("{}: {}\n\n".format(id, tweet))
    else:
        print ("Failed to get Tweets for user {}".format(args.handle))
        exit(1)
