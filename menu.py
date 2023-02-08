import os

file_uploaded = False
while (file_uploaded == False):

    directory = input("Enter input file(s) path:")

    if os.path.isdir(directory):
        print(f"{directory} exists.")
        file_uploaded = True
    else:
        print(f"{directory} does not exist, please try again")
        file_uploaded

