import statistics
import json

with open('../reddit-comments-final.json') as json_file:
    data = json.load(json_file, strict=False)

    texts_words_lens = []
    author_dict = {}
    comments_per_post_dict = {}
    deleted_authors = 0
    bot_authors = 0
    removed_comments = 0
    total_comments = 0
    scores = []

    for comment in data:
        if comment["Author"] == '[deleted]':
            deleted_authors += 1
        if comment["Author"] == 'Bot_Metric':
            bot_authors += 1
        elif comment["Text"] == '[removed]':
            removed_comments += 1
        else:
            total_comments += 1
            words = comment["Text"].split()
            texts_words_lens.append(len(words))
            scores.append(int(comment["Score"]))
            if author_dict.get(comment["Author"]) == None:
                author_dict[comment["Author"]] = 1
            else:
                author_dict[comment["Author"]] += 1
            if comments_per_post_dict.get(comment["Parent ID"]) == None:
                comments_per_post_dict[comment["Parent ID"]] = 1
            else:
                comments_per_post_dict[comment["Parent ID"]] += 1


    print("Number of deleted authors: " + str(deleted_authors))
    print("Number of bot authors: " + str(bot_authors))
    print("Number of removed comments: " + str(removed_comments))
    print("Total number of non-deleted comments: " + str(total_comments))
    print("Mean comment length (words): " + str(statistics.mean(texts_words_lens)))
    print("Median comment length (words): " + str(statistics.median(texts_words_lens)))
    print("Population Standard Deviation of comment length (words): " + str(statistics.pstdev(texts_words_lens)))
    print("Number of unique authors: " + str(len(author_dict.keys())))
    print("Mean comments per author: " + str(statistics.mean(author_dict.values())))
    print("Median comments per author: " + str(statistics.median(author_dict.values())))
    print("Mean comments per post: " + str(statistics.mean(comments_per_post_dict.values())))
    print("Median comments per post: " + str(statistics.median(comments_per_post.values())))
    print("Mean scores of comments: " + str(statistics.mean(scores)))
    print("Median scores of comments: " + str(statistics.median(scores)))
