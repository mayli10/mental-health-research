import statistics
import json

with open('../reddit-data-final.json') as json_file:
    data = json.load(json_file, strict=False)

    texts_words_lens = []
    author_dict = {}
    deleted_authors = 0
    authors_under_18 = 0
    authors_over_18 = 0
    total_posts = 0
    scores = []

    for post in data:
        if post["Author"] == '[deleted]':
            deleted_authors += 1
        else:
            total_posts += 1
            words = post["Text"].split()
            texts_words_lens.append(len(words))
            scores.append(int(post["Score"]))
            if author_dict.get(post["Author"]) == None:
                author_dict[post["Author"]] = 1
                if post["Over 18"] == "False":
                    authors_under_18 += 1
                else:
                    authors_over_18 += 1
            else:
                author_dict[post["Author"]] += 1


    print("Number of deleted authors: " + str(deleted_authors))
    print("Total number of posts: " + str(total_posts))
    print("Mean post length (words): " + str(statistics.mean(texts_words_lens)))
    print("Median post length (words): " + str(statistics.median(texts_words_lens)))
    print("Population Standard Deviation of post length (words): " + str(statistics.pstdev(texts_words_lens)))
    print("Number of unique authors: " + str(len(author_dict.keys())))
    print("Number of authors who are under 18: " + str(authors_under_18))
    print("Number of authors who are over 18: " + str(authors_over_18))
    print("Mean posts per author: " + str(statistics.mean(author_dict.values())))
    print("Median posts per author: " + str(statistics.median(author_dict.values())))
    print("Mean scores of posts: " + str(statistics.mean(scores)))
    print("Median scores of posts: " + str(statistics.median(scores)))
