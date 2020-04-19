import requests
import json
import csv
import time
import datetime
import pickle

# to run: python comment-scraper.py

# get post ids
with open ('./post-ids.p', 'rb') as fp:
    old_post_ids = pickle.load(fp)

# # get current post ids that have already been turned into a comment file
# with open ('./post_comment_file_ids.p', 'rb') as fp:
#     post_comment_file_ids = pickle.load(fp)

print(len(old_post_ids))
post_ids = old_post_ids[23330:]
print(len(post_ids))
# print(len(post_comment_file_ids))

def getPushshiftComments(id):
    url = 'https://api.pushshift.io/reddit/comment/search/?link_id='+str(id)+'&limit=20000'
    # url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def collectCommentData(id, comment):
    commentData = list() #list to store data points
    author = comment['author']
    comment_id = comment['id']
    score = comment['score']
    created = datetime.datetime.fromtimestamp(comment['created_utc']) #1520561700.0
    permalink = comment['permalink']
    text = " ".join(comment['body'].split("\n")) #get rid of \n new line
    stickied = comment['stickied']
    parent_id = comment['parent_id']
    link_id = comment['link_id']
    is_submitter = comment["is_submitter"]

    commentData.append((comment_id,link_id,parent_id,author,score,created,permalink,text, stickied,is_submitter))
    commentStats[id][comment_id] = commentData

def create_comments_file(id):
    file = "./comments/comment-" + str(id) + ".csv"
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Comment ID","Link ID","Parent ID","Author","Score","Publish Date","Permalink","Text", "Stickied", "Is Submitter"]
        a.writerow(headers)
        dict_values = commentStats[id].values()
        for comment in dict_values:
            fields = []
            for f in comment:
                fields.extend(f)
            a.writerow(fields)

def posts_with_no_comments(pid):
    file = open("./posts-with-0-comments.txt","w") 
    file.write(pid + "\n") 

# test for one file
# first_id = "cqhbvq"
# commentStats = { first_id : {} }

# data = getPushshiftComments(first_id)

# if len(data) == 0:
#         posts_with_no_comments(first_id)
# else:
#     for comment in data:
#         collectCommentData(first_id, comment)
#     create_comments_file(first_id)
# post_comment_file_ids.append(first_id)

#######################################################
# new correct way of getting all comments for each post
#######################################################
for id in post_ids:
    data = getPushshiftComments(id)
    commentStats = { id : {} }

    if len(data) == 0:
        posts_with_no_comments(id)
    else:
        for comment in data:
            collectCommentData(id, comment)

        create_comments_file(id)

print(len(commentStats.keys()))
#######################################################
# old wrong way of getting all comments for each post:
#######################################################
# for id in post_ids:
#     data = getPushshiftComments(id)
#     for comment in data:
#         collectCommentData(comment)
#         create_comments_file(id)

# pickle the comment ids again
# with open('./post_comment_file_ids.p', 'wb') as fp:
#     pickle.dump(post_comment_file_ids, fp)

# print(str(len(commentStats)) + " comments have added to list")
# print("1st entry is:")
# print(list(commentStats.values())[0][0][1] + " created: " + str(list(commentStats.values())[0][0][5]))
# print("Last entry is:")
# print(list(commentStats.values())[-1][0][1] + " created: " + str(list(commentStats.values())[-1][0][5]))
