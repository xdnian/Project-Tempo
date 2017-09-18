import os

files = os.listdir("./DEST")
with open("data.txt", "w") as data:
    for filename in files:
        with open("./DEST/" + filename, "r") as f:
            for line in f:
                data.write(''.join(line.split()))
                data.write(' ')
            data.write('\n')
