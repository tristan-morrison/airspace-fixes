
import os

cwd = os.getcwd()

# for each directory in the cwd
for name in os.listdir(cwd):
    if os.path.isdir(name) and name != '.git':
        # for each file in this directory
        for filename in os.listdir(name):
            # open the file
            with open(cwd + '/' + name + '/' + filename, 'r+') as file:
                lines = file.readlines()
                file.seek(0, 0)

                index = len(lines) - 1

                file.write("[\n")

                for x in range(0, len(lines)):
                    line = lines[x]
                    if line.startswith('\t\t"updated'):
                        line = line.replace('",', '"');
                    if x == index:
                        line = "\t}\n"
                    file.write(line)

                file.write("]\n")

                file.truncate()
                file.close()
