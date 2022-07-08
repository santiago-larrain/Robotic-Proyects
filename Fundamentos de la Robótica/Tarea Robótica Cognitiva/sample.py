lines2 = []
with open("sample.txt", "r") as file:
    line = file.readline().strip()
    while line:
        if "inflating" in line:
            line = line[11:]
            line2 = f"'/content/{line}.mp4',"
            lines2.append(line2)
        line = file.readline().strip()

with open("sample2.txt", "w") as file2:
    print("[", end= "", file= file2)
    for line in lines2:
        print(line, file= file2)
    print("]", file= file2)