import csv

import tweepy


class UserTweetsDownloader:
    MAX_COUNT = 200

    def __init__(self, api, user_name):
        self.api = api
        self.user_name = user_name
        self.all_tweets = []

    def _get_last_tweet_id(self):
        return self.all_tweets[-1].id - 1

    def _save_tweets(self, path_destination):
        out_tweets = [[
            tweet.id_str,
            tweet.created_at,
            tweet.text,
            tweet._json.get('retweet_count'),
            tweet._json.get('favorite_count')
        ] for tweet in self.all_tweets]

        with open(path_destination, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text",  "retweet", "favorite"])
            writer.writerows(out_tweets)

    def _add_new_tweets(self, new_tweets):
        self.all_tweets.extend(new_tweets)

    def download_tweets(self, **kwargs):
        return self.api.user_timeline(**kwargs)

    def download_all_tweets(self, path_destination):
        new_tweets = self.download_tweets(screen_name=self.user_name, count=self.MAX_COUNT)
        self._add_new_tweets(new_tweets)
        oldest = self._get_last_tweet_id()

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print(f"Getting tweets before {oldest}")

            new_tweets = self.download_tweets(screen_name=self.user_name, count=self.MAX_COUNT, max_id=oldest)
            self._add_new_tweets(new_tweets)
            oldest = self._get_last_tweet_id()

            print(f"...{len(self.all_tweets)} tweets downloaded so far")

        self._save_tweets(path_destination)
