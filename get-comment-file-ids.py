import os
import pickle

with open ('./post-ids.p', 'rb') as fp:
    old_post_ids = pickle.load(fp)

new_file_list = []

def get_ids():       # 1.Get file names from directory
    file_list=os.listdir(r"/home/mlz387/mental-health-research/comments")
    for file in file_list:
        new_file_list.append(file[8:-4])

def get_subset(first, second):
    second = set(second)
    return [item for item in first if item not in second]

get_ids()
post_ids_with_0_comments = get_subset(old_post_ids, new_file_list)
print(len(old_post_ids))
print(len(new_file_list))
print(post_ids_with_0_comments)

for pid in post_ids_with_0_comments:
    with open("./posts-with-0-comments.txt","w") as file:
        file.write(pid + "\n") 
