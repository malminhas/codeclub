# My Magic8Ball
# -------------
# - After School Code Club April 2014 -
# This is an implementation in Python of the Magic 8Ball game.
# You ask a question and 8Ball provides you with a random answer!
# There are some important new Python features in here:
# 1. list - we are using a Python list to hold the answers
# 2. len(str) - used to find the length of a string
# 3. raw_input - used to pick up user input up to when they press ENTER
# 4. random - random.randint() returns a random number in provided range
# 5. randint needs to be in range 0..7 because list is 0,1,2,3...
# Good luck with 8Ball's fortune!
# Bonus extra: Can you think how you would make this code loop around
# so you don't have to re-run the program every time?
# Hint: It might take you a "while" :-)
#

import time         # Inbuilt module for time functions
import random       # Inbuilt module for random functions

# 1. Setup answers list
answers = []
answers.append("Go for it!")
answers.append("No way, Jose!")
answers.append("I'm not sure.  Ask me again")
answers.append("Fear of the unknown is what imprisons us")
answers.append("It would be madness to do that!")
answers.append("Only you can save humanity!")
answers.append("Whatever.  It makes no difference to me if you do or don't")
answers.append("Yes, I think on balance that is the right choice")

# 2. Find out the user's name
name = raw_input("What's your name?\n")
welcomeString = "* Welcome to MyMagic8Ball, %s! *" % name
print("*" * len(welcomeString))
print(welcomeString)
print("*" * len(welcomeString))

# 3. Get the users question then shake 4 times
question = raw_input("Ask me for advice then press ENTER to shake me.\n")
for i in range(4):
    print("shaking....")
    time.sleep(0.5)

# 4. Use the randint() function to select question
choice = random.randint(0, 7)
answer = answers[choice]
print("*" * len(answer))
print(answer)
print("*" * len(answer))

# 5. Exit
print("\nThank you and goodbye from Magic8Ball!")
