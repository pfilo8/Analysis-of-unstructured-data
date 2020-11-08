import csv

import tweepy


class HashtagTweetsDownloader:

    MAX_COUNT = 1000

    def __init__(self, api):
        self.api = api
        self.all_tweets = []

    def _save_tweets(self, path_destination):
        out_tweets = [[
            tweet.id_str,
            tweet.created_at,
            tweet.full_text,
            tweet._json.get('user', {}).get('location'),
            tweet._json.get('retweet_count'),
            tweet._json.get('favorite_count')
        ] for tweet in self.all_tweets]

        with open(path_destination, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text", "location", "retweet", "favorite"])
            writer.writerows(out_tweets)

    def download_all_tweets(self, path_destination, **kwargs):
        try:
            for tweet in tweepy.Cursor(self.api.search, tweet_mode='extended', **kwargs).items(self.MAX_COUNT):
                self.all_tweets.append(tweet)
        except Exception as e:
            pass
        finally:
            self._save_tweets(path_destination)
