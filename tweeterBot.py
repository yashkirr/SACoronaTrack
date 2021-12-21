"""
Author: Yashkir Ramsamy
Contact: me@yashkir.co.za
Date: 2020/07/13

Purpose: Bot which tweets corona virus stat updates
"""
import os
import time
import tweepy
import CoronaTrackerAPI
import firestore
import operator
import traceback
import json
from fileOperations import *
from config import *
from datetime import datetime
from pytz import timezone


# emojis
chart_increasing = "\U0001F4C8"  # for cases
wilting_rose = "\U0001F940"  # for deaths
sneezing_face = "\U0001F927"  # for active cases
sick_emoji = "\U0001F912"  # for active cases
raising_hands = "\U0001F64C"  # for recoveries
new_emoji = "\U0001F195"  # for new cases
hospital_emoji = "\U0001F3E5"  # for critical cases

DATA_FILE = "data.txt"

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_account = tweepy.API(auth)



# params: cases, deaths, recoveries, active_cases, critical_cases, fatality_rate, recovery_rate
def setOldCases(c):
    old_cases = c
    data_dict = {"old_cases": old_cases}
    writeToFile("old_cases.txt", data_dict)


def tweet(c, d, r, a_c, n_c, fr, pr):
    cases = "{:,}".format(c)
    deaths = "{:,}".format(d)
    recoveries = "{:,}".format(r)
    active_cases = "{:,}".format(a_c)
    new_cases = "{:,}".format(n_c)
    fatality_rate = "{:.1f}".format(float(fr))
    recovery_rate = "{:.1f}".format(float(pr))

    south_africa = timezone('Africa/Johannesburg')
    sa_time = datetime.now(south_africa)
    date = sa_time.strftime('%d/%m')

    status_text = \
        "South Africa's COVID-19 STATS - {date}" \
        "\n\n{chart_increasing} Cases: {cases}" \
        "\n{wilting_rose} Deaths: {deaths}" \
        "\n{raising_hands} Recoveries: {recoveries}" \
        "\n{sneezing_face} Active Cases: {active_cases}" \
        "\n{new_emoji} New Cases: {new_cases}" \
        "\n\nFatality Rate: {fatality_rate}%      Recovery Rate: {recovery_rate}%" \
        "\n\n#SACoronaTracker #CoronaVirusSA #COVID19 {pop_tag}" \
            .format(cases=cases, deaths=deaths, recoveries=recoveries, active_cases=active_cases,
                    chart_increasing=chart_increasing, wilting_rose=wilting_rose, sneezing_face=sneezing_face,
                    raising_hands=raising_hands, date=date, pop_tag=getTrendingTag(),
                    recovery_rate=recovery_rate, fatality_rate=fatality_rate, new_emoji=new_emoji, new_cases=new_cases)
    print("SUCCESS: Tweeting")
    print(status_text)
    twitter_account.update_status(status_text)
    print("SUCCESS: Tweeted!")


def getTrendingTag():
    trends_dict = twitter_account.get_place_trends(23424942)  # woeid for South Africa
    trends = trends_dict[0]
    trends_dict_sum = {}
    for dict in trends['trends']:
        if dict['tweet_volume'] is None:
            dict['tweet_volume'] = 0
        trends_dict_sum[dict['name']] = dict['tweet_volume']
    print("NOTICE: Finding most popular tag from: " + json.dumps(trends_dict_sum))
    return max(trends_dict_sum.items(), key=operator.itemgetter(1))[0]



# Run Bot
def main():
    twitter_account.send_direct_message(yashkirr_id, "I'm running :)")
    print("RUNNING: Checking cases")
    stats = CoronaTrackerAPI.getNationalStats()
    cases = stats[0]
    old_cases = firestore.getOldCases()
    print(old_cases, cases)

    if cases == old_cases:
        south_africa = timezone('Africa/Johannesburg')
        sa_time = datetime.now(south_africa)
        date = sa_time.strftime('%H:%M')
        print("NOTICE: Checked for data update at", date,
                        "and there is no change.\nGoing back to sleep for 30 minutes")
    else:
        twitter_account.send_direct_message(yashkirr_id, "I'm tweeting :)")
        print("NOTICE: New data found, sending a tweet.")
        stats = CoronaTrackerAPI.getNationalStats()
        cases = stats[0]
        new_cases = cases - (int)(old_cases)
        deaths = stats[1]
        recoveries = stats[2]
        active_cases = stats[0] - stats[2]
        fatality_rate = stats[4]
        recovery_rate = stats[5]
        try:
            tweet(cases, deaths, recoveries, active_cases, new_cases, fatality_rate, recovery_rate)
            print("SUCCESS: Tweet sent.")
            firestore.setOldCases(cases)
        except tweepy.errors.TweepyException:
            print("NOTICE: Tweet already sent, hash has changed.")
            print("NOTICE: Updating cases on firestore.")
            firestore.setOldCases(cases)
            print("NOTICE: Saved Data. Going back to sleep")

if __name__ == "__main__":
    try:
        main()
    except:
        twitter_account.send_direct_message(yashkirr_id, "I broke. Check me please")
        traceback.print_exc()
