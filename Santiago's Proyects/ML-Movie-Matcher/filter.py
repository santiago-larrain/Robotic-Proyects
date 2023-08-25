import time
### Get list of paths for the title, its puntuaction and the main information ###
paths = {"title": [], "points": [], "info": []}
with open("path.txt", "r") as path_file:
    line = path_file.readline()
    while line:
        if line.strip().lower() in paths.keys():
            crrt_path = line.strip().lower()
        else:
            paths[crrt_path].append(line.strip())
        line = path_file.readline()
'''
### Find the title ###
title = False    # bool to indicate if the title has been found
start = time.time()
with open("HTML.txt", "r") as html_file:
    line = html_file.readline()
    while not title:
        if paths["title"][-1] in line:
            line.split(">")
            title = line[1].split("<")
print(time.time() - start)
print(title)
'''
### Find the title ###
title = False    # bool to indicate if the title has been found
next = False
start = time.time()
with open("HTML.txt", "r") as html_file:
    line = html_file.readline()
    while not title:
        sub_lines = line.split("><")
        for sub_line in sub_lines:
            if next:
                title = sub_line.split("</")[0]
                break
            elif paths["title"][-1].split("<")[1].split(">")[0] == sub_line:
                next = True
print(time.time() - start)
print(title)