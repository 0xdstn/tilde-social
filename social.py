#!/usr/bin/env python3

import sys
import os
import getpass
import time
import re
from datetime import datetime
from pathlib import Path

username = getpass.getuser()

rootDir = str(Path.home()) + '/.social/'
postsPath = rootDir + 'posts'
configPath = rootDir + 'config'
followingPath = rootDir + 'following'

print('')

###
# Colored messages
###

err = '\x1b[1;31m'
suc = '\x1b[1;32m'
wrn = '\x1b[1;33m'
inf = '\x1b[1;34m'
end = '\x1b[0m'

def success(msg):
    print(suc + msg + end)

def error(msg):
    print(err + msg + end)

def info(msg):
    print(inf + msg + end)

def userExists():
    return os.path.exists(rootDir)

def noProfile():
    error('You do not have a profile set up in ' + rootDir + '. Try running the init command.')

###
# Classes
###
class UserConfig:
    def __init__(self):
        self.name = ''
        self.bio = ''
        self.url = ''

    def setItem(self, key, val):
        if key == 'name': self.name = val
        elif key == 'bio': self.bio = val
        elif key == 'url': self.url = val

###
# Helpers
###

def parseConfig(user):
    # Open the config file
    with open(configPath.replace(username,user)) as f:
        content = f.readlines()

    # Convert lines to array
    content = [x.strip() for x in content]

    # Create a new UserConfig
    conf = UserConfig()

    # Loop through lines and set the items
    for line in content:
        line = line.split('=')
        conf.setItem(line[0],line[1])

    # return the UserConfig
    return conf

def getDisplayDate(ts):
    return datetime.utcfromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S UTC')

def printPost(line,username):
    pieces = line.split(' PST ')
    now = round(time.time() * 1000)
    # Make sure it isn't malformed or in the future
    if len(pieces) == 2 and int(pieces[0]) <= now:
        print(end)
        info('~' + username + ' ' + getDisplayDate(pieces[0]))
        lines = pieces[1].split('\\n')
        for l in lines:
            if len(l) > 0:
                print(l.rstrip() + end)
        return True
    return False

def showProfile(user):

    user = user.replace('~','')
    userPath = rootDir.replace(username,user)

    if os.path.exists(userPath):

        # Display user info
        data = parseConfig(user)
        print('User: ~' + user)
        print('Name: ' + data.name)
        print('Bio:  ' + data.bio)
        print('URL:  ' + data.url)

        # Get the user post
        postFile = open(postsPath.replace(username,user),'r')

        # Convert lines to array
        content = [x.strip() for x in postFile]

        # Loop through lines and display 20 most recent posts
        displayed = 0
        posts = []
        for line in reversed(content):
            if ' PST ' in line:
                displayed = displayed + 1
                posts.append(line)
            if displayed == 20:
                break
        for pst in reversed(posts):
            printPost(pst,user)
    else:
        error('User ~' + user + ' does not have an account')

def showFollowing(user):
    userPath = rootDir.replace(username,user)
    userFollowingPath = followingPath.replace(username,user)

    if os.path.exists(userPath):

        # Get the user following
        followingFile = open(userFollowingPath,'r')
        content = [x.strip() for x in followingFile]
        for line in content:
            info(line)
        followingFile.close()
    else:
        error('User ~' + user + ' does not have an account')

def showFollowers(user):
    userPath = rootDir.replace(username,user)

    if os.path.exists(userPath):
        users = os.listdir('/home')
        for u in users:
            if os.path.exists(rootDir.replace(username,u)):
                followingFile = open(followingPath.replace(username,u),'r')
                content = [x.strip() for x in followingFile]
                for line in content:
                    if line == user:
                        info(u)
                followingFile.close()
                 
    else:
        error('User ~' + user + ' does not have an account')

###
# Commands
###

def about():
    info('Version:      1.0.11')
    info('Author:       ~dustin')
    info('Source:       https://github.com/0xdstn/tilde-social')
    info('More info:    https://tilde.town/~dustin/projects/tilde-social')

def usage():
    print('Usage: timeline [command]')
    print('')
    print('Commands:')
    print('  init                              Initialize your profile')
    print('  users                             View a list of users who have a profile')
    print('  feed                              View a feed of users you follow')
    print('  local                             View a feed of all users')
    print('  me                                View your profile')
    print('  following                         View a list of users you follow')
    print('  followers                         View a list of users who follow you')
    print('  mentions                          View a list posts you are mentioned in')
    print('  post "Message"                    Post a new message')
    #print('  delete 123456789                   Delete a post')
    #print('  boost user/123456789              Boost a post')
    #print('  reply user/123456789 "Message"    Reply to a post')
    #print('  view user/123456789               View a specific post')
    print('  follow username                   Follow a user')
    print('  unfollow username                 Unfollow a user')
    print('  profile username                  view the profile of a user')
    print('  following username                view a list of users another user is following')
    print('  followers username                view a list of users who follow a user')
    print('')
    print('You can mention another user via their ~town name like this: Mentioning ~dustin in a post')

def init():
    # Make sure they don't already have a .social dir
    if not os.path.exists(rootDir):
        info('Initializing profile setup')

        # Ask some questions
        name = input(wrn + '[?]' + end + ' Name (John Smith): ')
        bio = input(wrn + '[?]' + end + ' Bio (Developer, computer user): ')
        url = input(wrn + '[?]' + end + ' URL (http://yoursite.com): ')

        # Create new .social dir in the home dir
        os.makedirs(rootDir)
        success('Created ' + rootDir)

        # Create the config file
        configFile = open(configPath,'w')
        configFile.write('name=' + name + '\n')
        configFile.write('bio=' + bio + '\n')
        configFile.write('url=' + url)
        configFile.close()
        success('Created ' + configPath)

        # Create other files
        open(postsPath,'w').close()
        success('Created ' + postsPath)

        open(followingPath,'w').close()
        success('Created ' + followingPath)
    else:
        error(rootDir + ' already exists')

def userList():
    # Get the user's following list
    following = ''
    if os.path.exists(rootDir):
        followingFile = open(followingPath,'r')
        following = followingFile.read()
        followingFile.close()

    # Loop through home directories and find social users to display
    users = os.listdir('/home')
    for u in users:
        if os.path.exists(rootDir.replace(username,u)):
            followingFile = open(followingPath.replace(username,u),'r')
            userFollowing = followingFile.read()
            followingFile.close()
            isFollowing = ('', inf + ' [following]' + end)[u in following]
            followsYou = ('', suc + ' [follows you]' + end)[username in userFollowing]
            isMe = ('', wrn + ' [this is you!]' + end)[u == username]
            print('~' + u + isFollowing + followsYou + isMe)

def me():
    if userExists():
        showProfile(username)
    else:
        noProfile()

def feed():
    if os.path.exists(rootDir):
        userPosts = []
        followingFile = open(followingPath,'r')

        # Loop through following users
        for u in followingFile:
            u = u.strip()

            # Make sure the user exists
            if os.path.exists(rootDir.replace(username,u)):

                postsFile = open(postsPath.replace(username,u), 'r')

                # Loop through user's posts
                for pst in postsFile:
                    pst = pst.strip()
                    userPosts.append(pst + 'SPLT' + u)

                postsFile.close()

        followingFile.close()

        # Include the user posts
        postsFile = open(postsPath, 'r')

        # Loop through user's posts
        for pst in postsFile:
            pst = pst.strip()
            userPosts.append(pst + 'SPLT' + username)

        postsFile.close()

        displayed = 0
        toDisplay = []
        for post in reversed(sorted(userPosts)):
            displayed = displayed + 1
            toDisplay.append(post)
            if displayed == 20:
                break
        displayed = 0
        for post in reversed(toDisplay):
            parts = post.split('SPLT')
            if printPost(parts[0],parts[1]):
                displayed = displayed + 1
                if displayed == 20:
                    break
    else:
        noProfile()

def local():
    users = os.listdir('/home')
    userPosts = []

    # Loop through following users
    for u in users:

        # Make sure the user exists
        if os.path.exists(rootDir.replace(username,u)):

            postsFile = open(postsPath.replace(username,u), 'r')

            # Loop through user's posts
            for pst in postsFile:
                pst = pst.strip()
                userPosts.append(pst + 'SPLT' + u)

            postsFile.close()

    # Loop through posts sorted by time, display 20 most recent
    displayed = 0
    toDisplay = []
    for post in reversed(sorted(userPosts)):
        displayed = displayed + 1
        toDisplay.append(post)
        if displayed == 20:
            break
    displayed = 0
    for post in reversed(toDisplay):
        parts = post.split('SPLT')
        if printPost(parts[0],parts[1]):
            displayed = displayed + 1
            if displayed == 20:
                break

def post():
    if userExists():
        if len(sys.argv) > 2:
            # Generate a unix timestamp for the ID
            id = str(round(time.time() * 1000))

            # Write to the post log
            postFile = open(postsPath,'a')

            # Make sure we get the full message even if there were no quotes
            pieces = sys.argv
            pieces.pop(0)
            pieces.pop(0)
            text = ' '.join(pieces)

            postFile.write(id + ' PST ' + text.replace('\n','\\n') + '\n')

            postFile.close()

            success('Posted: ' + text)
        else:
            error('No post text provided')
    else:
        noProfile()

def follow():
    if len(sys.argv) > 2:
        toFollow = sys.argv[2]

        # Make sure the user exists
        if toFollow == username:
            error('You cannot follow yourself')
        elif os.path.exists(rootDir.replace(username,toFollow)):

            followingFile = open(followingPath, 'r+')

            # Make sure the user isn't already following them
            if toFollow not in followingFile.read():
                followingFile.write(toFollow + '\n')
                success('You are now following ~' + toFollow)
            else:
                error('You are already following ~' + toFollow)

            followingFile.close()
        else:
            error('Provided user does not exist')

    else:
        error('No user provided')

def unfollow():
    if len(sys.argv) > 2:
        toUnfollow = sys.argv[2]
        followingFile = open(followingPath, 'r')
        contents = followingFile.read()

        # Make sure the user is following them
        if toUnfollow in contents:
            updateFile = open(followingPath, 'w')
            updateFile.write(contents.replace(toUnfollow + '\n',''))
            success('You are no longer following ~' + toUnfollow)
        else:
            error('You are not following ~' + toUnfollow)

        followingFile.close()

    else:
        error('No user provided')

def profile():
    if len(sys.argv) > 2:
        showProfile(sys.argv[2])
    else:
        error('No user provided')

def following():
    if len(sys.argv) > 2:
        showFollowing(sys.argv[2])
    else:
        showFollowing(username)

def followers():
    if len(sys.argv) > 2:
        showFollowers(sys.argv[2])
    else:
        showFollowers(username)

def mentions():
    if os.path.exists(rootDir):
        users = os.listdir('/home')
        posts = []

        # Loop through all users
        for u in users:

            # Make sure they have a profile and it's not the current uesr
            if os.path.exists(rootDir.replace(username,u)) and u != username:
                postsFile = open(postsPath.replace(username,u),'r')
                for line in postsFile:
                    if '~' + username in line and ' PST ' in line:
                        posts.append(line + 'SPLT' + u)
                postsFile.close()

        for post in sorted(posts):
            parts = post.split('SPLT')

            printPost(parts[0],parts[1])
    else:
        noProfile()

###
# Run command
###

if len(sys.argv) == 1:
    usage()
else:
    cmd = sys.argv[1]
    # Creating a new profile
    if cmd == 'init': init()
    elif cmd == 'help': usage()
    elif cmd == 'about': about()
    elif cmd == 'users': userList()
    elif cmd == 'me': me()
    elif cmd == 'feed': feed()
    elif cmd == 'timeline': feed()
    elif cmd == 'local': local()
    elif cmd == 'mentions': mentions()
    elif cmd == 'post': post()
    elif cmd == 'follow': follow()
    elif cmd == 'unfollow': unfollow()
    elif cmd == 'profile': profile()
    elif cmd == 'following': following()
    elif cmd == 'followers': followers()
    else: error('Unrecognized command')
