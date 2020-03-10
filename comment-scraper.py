import requests
import json
import csv
import time
import datetime
import pickle

old_post_ids = []
commentCount = 0
commentStats = {}

with open ('./post-ids.p', 'rb') as fp:
    old_post_ids = pickle.load(fp)

post_ids = old_post_ids[old_post_ids.index("acvl9n") + 1:]
print(len(post_ids))

def getPushshiftComments(id):
    url = 'https://api.pushshift.io/reddit/comment/search/?link_id='+str(id)+'&limit=20000'
    # url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def collectCommentData(comment):
    commentData = list() #list to store data points
    author = comment['author']
    comment_id = comment['id']
    score = comment['score']
    created = datetime.datetime.fromtimestamp(comment['created_utc']) #1520561700.0
    permalink = comment['permalink']
    text = comment['body']
    stickied = comment['stickied']
    parent_id = comment['parent_id']
    link_id = comment['link_id']
    is_submitter = comment["is_submitter"]

    commentData.append((comment_id,link_id,parent_id,author,score,created,permalink,text, stickied,is_submitter))
    commentStats[comment_id] = commentData

def create_comments_file(id):
    file = "./comments-csv/comments-csv/comment-" + str(id) + ".csv"
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Comment ID","Link ID","Parent ID","Author","Score","Publish Date","Permalink","Text", "Stickied", "Is Submitter"]
        a.writerow(headers)
        for comment in commentStats:
            a.writerow(commentStats[comment][0])

for id in post_ids:
    data = getPushshiftComments(id)
    for comment in data:
        collectCommentData(comment)
        create_comments_file(id)

# print(str(len(commentStats)) + " comments have added to list")
# print("1st entry is:")
# print(list(commentStats.values())[0][0][1] + " created: " + str(list(commentStats.values())[0][0][5]))
# print("Last entry is:")
# print(list(commentStats.values())[-1][0][1] + " created: " + str(list(commentStats.values())[-1][0][5]))
