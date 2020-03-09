import statistics
import json
import glob

files = glob.glob("./reddit-files/comments/*.json")

comments = []
deleted_authors = []
bot_authors = []
texts_words_lens = []
author_dict = {}
upvotes = []

for file in files:
    with open(file) as json_file:
        data = json.load(json_file, strict=False)

        def get_comments(data):
            if type(data) is list:
                for item in data:
                    get_comments(item)
            else:
                if data.has_key("Comment ID"):
                    if data["Author"] == '[deleted]':
                        deleted_authors.append(data)
                    elif data["Author"] == 'Bot_Metric':
                        bot_authors.append(data)
                    else:
                        comments.append(data)
                        words = data["Text"].split()
                        texts_words_lens.append(len(words))
                        upvotes.append(data["Upvotes"])
                        if author_dict.get(data["Author"]) == None:
                            author_dict[data["Author"]] = 1
                        else:
                            author_dict[data["Author"]] += 1
                else:
                    comment_ids = data.keys()
                    for c_id in comment_ids:
                        get_comments(data[c_id])
        get_comments(data)

print "Number of deleted authors: " + str(len(deleted_authors))
print "Number of bot authors: " + str(len(bot_authors))
print "Total number of comments: " + str(len(comments))
print "Mean comment length (words): " + str(statistics.mean(texts_words_lens))
print "Median comment length (words): " + str(statistics.median(texts_words_lens))
print "Population Standard Deviation of comment length (words): " + str(statistics.pstdev(texts_words_lens))
print "Sample Standard Deviation of comment length (words): " + str(statistics.stdev(texts_words_lens))
print "Number of unique authors: " + str(len(author_dict.keys()))
print "Mean comments per user: " + str(statistics.mean(author_dict.values()))
print "Median comments per user: " + str(statistics.median(author_dict.values()))
print "Mean upvotes of comments: " + str(statistics.mean(upvotes))
print "Median upvotes of comments: " + str(statistics.median(upvotes))
