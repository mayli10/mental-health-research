import requests
import json
import csv
import time
import datetime
import pickle

post_ids = []

def getPushshiftData(after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission?subreddit='+str(sub)+'&after='+str(after)+'&before='+str(before)+'&size=1000'
    # url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    post_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    num_comments = subm['num_comments']
    permalink = subm['permalink']
    text = subm['selftext']
    stickied = subm['stickied']
    over_18 = subm["over_18"]
    is_video = subm["is_video"]

    post_ids.append(post_id)

    subData.append((post_id,title,url,author,score,created,num_comments,permalink,flair, text, stickied, over_18, is_video))
    subStats[post_id] = subData

#Subreddit to query
sub='EDAnonymous'
#before and after dates
before = "1582764592" #2/26/2020
after = "1542067200" #11/13/2018
# after = "1542153600"  #11/14/2018
subCount = 0
subStats = {}

data = getPushshiftData(after, before, sub)
# Will run until all posts have been gathered
# from the 'after' date up until before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(after, before, sub)

print(len(data))

print(str(len(subStats)) + " submissions have added to list")
print("1st entry is:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))

def updateSubs_file():
    upload_count = 0
    location = "./reddit-data-final2"
    print("input filename of submission file, please add .csv")
    filename = input()
    file = location + filename
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair", "Text", "Stickied", "Over 18", "Is Video"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1

        print(str(upload_count) + " submissions have been uploaded")
updateSubs_file()

with open('./post-ids.p', 'wb') as fp:
    pickle.dump(post_ids, fp)


########################### Get Comments #######################
