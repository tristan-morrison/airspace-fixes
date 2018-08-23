import os

cwd = os.getcwd()

# for each directory in the cwd
for name in os.listdir(cwd):
    if os.path.isdir(name) and name != '.git':
        # for each file in this directory
        for filename in os.listdir(name):
            # open the file
            with open(cwd + '/' + name + '/' + filename, 'r+') as file:
                # prepend an opening brace
                content = file.read()
                contentToWrite = content.replace("    ", "").replace("'", '"')
                file.seek(0, 0)
                file.write(contentToWrite)
                file.truncate()
                file.close()
