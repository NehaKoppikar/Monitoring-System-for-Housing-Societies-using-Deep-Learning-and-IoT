import os

first_name = input("What is First Name?")
last_name = input("What is Last Name?")

# Make directory
parent_directory = "images"
directory = f"{first_name}_{last_name}"
# mode 
mode = 0o666
path = os.path.join(parent_directory, directory)
os.mkdir(path, mode)
print("Directory Created!")
