# https://dev.twitter.com/overview/api/response-codes
import sys
import tweepy
import pandas as pd

def get_access_creds():
    '''
        Twitter API authentication credentials are stored in a file as:
            consumer_key \t consumer_secret \t access_token \t access_secret 
    '''
    oauths = []
    app_auths = []

    print('Building list of developer access credentials...')
    credentials = pd.read_csv('twitter_dev_accounts', sep='\t', header=None, names=['consumer_key', 'consumer_secret', 'access_token', 'access_secret'])

    for index, row in credentials.iterrows():
        auth = tweepy.auth.OAuthHandler(str(row['consumer_key']), str(row['consumer_secret']))
        auth.set_access_token(str(row['access_token']), str(row['access_secret']))
        app_api = tweepy.API(auth)
        oauth_api = tweepy.API(auth)
        #app_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        #oauth_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if(verify_working_credentials(oauth_api)):
            oauths.append(oauth_api)
            app_auths.append(app_api)

    return oauths, app_auths

def verify_working_credentials(api):
    verified = True

    try:
        api.verify_credentials()

    except tweepy.TweepError as e:
        verified = False

    except Exception as e:
        print(str(e))

    finally:
        return verified

def manage_auth_handlers(auths):
    index = 0
    while True:
        api = auths[index]

        try:
            limit = api.rate_limit_status()
            status_limit = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
            if status_limit > 180:
                return api

        except tweepy.TweepError as e:
            pass

        except Exception as e:
            print(str(e))

        finally:
            if index == (len(auths) - 1):
                index = 0
            else:
                index += 1

