import os
def get_ids():       # 1.Get file names from directory
    file_list=os.listdir(r"/home/mlz387/mental-health-research/comments")
    new_file_list = []
    for file in file_list:
        split_file = file.split('-')
        new_file_list.append(split_file[1])
    
    print(new_file_list)

get_ids()

