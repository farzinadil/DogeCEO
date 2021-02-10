import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
import time
from datetime import datetime
from twilio.rest import Client

def sid():
    return os.environ.get("TWILIO_ACCOUNT_SID")

def twilioAuth():
    return os.environ.get("TWILIO_AUTH_TOKEN")

def auth():
    return os.getenv("BEARER_TOKEN")

def create_url():
    user_id = 44196397
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,attachments"}

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    numbers_to_message = ['+0000000000'] #enter numbers here
    account_sid = sid()
    auth_token = twilioAuth()
    client = Client(account_sid, auth_token)
    lastDate = datetime.strptime('2021-01-01 20:05:25.000', '%Y-%m-%d %H:%M:%S.%f')
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()
    while True:
        json_response = connect_to_endpoint(url, headers, params)
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        tweets = json_response['data']
        print(tweets)
        print("Search: ")
        for tweet in tweets:
            tweetDate = datetime.strptime(tweet['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
            if tweetDate > lastDate:
                tweetContent = tweet['text'].lower()
                with open ('cryptos.json') as cryptoJsonFile:
                    cryptoData = json.load(cryptoJsonFile)
                    for crypto in cryptoData['cryptos']:
                        if tweetContent.find(crypto['symbol'].lower()) != -1 or tweetContent.find(crypto['name'].lower()) != - 1 :
                            cryptoMessage = "crypto found: " + crypto['name'] + " in Elon's tweet: " + tweet['text']
                            print(cryptoMessage)
                            for number in numbers_to_message:
                                client.messages.create(
                                    body=cryptoMessage,
                                    from_='+000000000',
                                    to=number
                                )

                            print("\n")
                with open('stocks.json') as stocksJsonFile:
                    stockData = json.load(stocksJsonFile)
                    for stock in stockData['popular_stocks']:
                        if tweetContent.find(" " + stock['name'].lower() + " ") != -1 : #or tweetContent.find(stock['name'].lower() + " ") != -1
                            stockMessage = "stock found: " + stock['name'] + " in Elon's tweet: " + tweet['text']
                            print(stockMessage)
                            for number in numbers_to_message:
                                client.messages.create(
                                    body=stockMessage,
                                    from_='+000000000',
                                    to=number
                                )

                            print("\n")
        lastDate = datetime.strptime(tweets[0]['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
        print("Waiting 2 minutes")
        time.sleep(60)
        print("Waiting 60 seconds")
        time.sleep(60)





if __name__ == "__main__":
    main()
