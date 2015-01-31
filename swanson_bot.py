#!/usr/bin/python
import praw
import re
import os
import pickle

REPLY = "I want all the bacon and eggs you have."

if not os.path.isfile("inigo_config.txt"):
    print "You must create the file swanson_config.txt with the pickled credentials."
    exit(1)
else:
    print "Loading credentials"
    user_data = pickle.load( open("swanson_config.txt","rb"))
    #print user_data

user_agent = ("Swanson bot 0.1 created by /u/dcooper2.")
r = praw.Reddit(user_agent=user_agent)

r.login(user_data[0], user_data[1])
del user_data

print "Successfully logged in"

# Check for previous replies
if not os.path.isfile("replies.txt"):
    replies = []
else:
    print "Loading previous reply ids"
    with open("replies.txt", "r") as f:
        replies = f.read()
        replies = replies.split("\n")
        replies = filter(None, replies)

# Check for new items to reply to
subreddit = r.get_subreddit('umw_cpsc470Z')
print "Checking for new posts"
for submission in subreddit.get_hot(limit=10):
    print "Checking submission ", submission.id
    if submission.id not in replies:
        if re.search("Ron Swanson", submission.title, re.IGNORECASE) or re.search("Ron Swanson", submission.selftext, re.IGNORECASE):
            submission.add_comment(REPLY)
            print "Bot replying to submission: ", submission.id
            replies.append(submission.id)
    print "Checking comments"
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:
        if comment.id not in replies: 
            if re.search("Ron Swanson", comment.body, re.IGNORECASE):
                print "Bot replying to comment: ", comment.id
                comment.reply(REPLY)
                replies.append(comment.id)

# Save new replies
print "Saving ids to file"
with open("replies.txt", "w") as f:
    for i in replies:
        f.write(i + "\n")
