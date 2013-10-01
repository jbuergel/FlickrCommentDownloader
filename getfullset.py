#!/usr/bin/python
"""
    getfullset.py
    Copyright 2013 Joshua Buergel <jbuergel@gmail.com>

THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND, AND MAY BE
COPIED, MODIFIED OR DISTRIBUTED IN ANY WAY, AS LONG AS THIS NOTICE
AND ACKNOWLEDGEMENT OF AUTHORSHIP REMAIN.

"""

import os
import flickr
import argparse
from urllib.request import urlretrieve
import webbrowser
import string

valid_file_name_chars = frozenset("-_.()/ {0}{1}".format(string.ascii_letters, string.digits))

def clean_file_name(filename):
    return ''.join(c for c in filename if c in valid_file_name_chars)

def get_all_sets():
    """Gets the names for all sets on the account"""
    set_names = []
    user = flickr.test_login()
    sets = user.getPhotosets()
    for set in sets:
        set_names.append(set.title)
    return set_names

def get_single_set(set_name):
    """Gets a single set sets on the account"""
    user = flickr.test_login()
    sets = user.getPhotosets()
    target_set = None
    for set in sets:
        if (set.title == set_name):
            target_set = set
    return target_set

def print_comments(set_name, photo):
    os.makedirs(clean_file_name(set_name), exist_ok=True)
    f = open(clean_file_name('{0}/{1}.txt'.format(set_name, photo.title)), 'w')
    comments = photo.getComments()
    try:
        for comment in comments.comment:
            f.write('{0}: {1}\n'.format(comment.realname, comment.text))
    except TypeError:
        f.write('{0}: {1}\n'.format(comments.comment.realname, comments.comment.text))
    except AttributeError:
        pass
    f.close()
    urlretrieve(photo.getURL(size='Original', urlType='source'), clean_file_name('{0}/{1}.jpg'.format(set_name, photo.title)))

def create_token():
    a = flickr.Auth()
    frob = a.getFrob()
    login_link = a.loginLink('read', frob)
    webbrowser.open(login_link)
    input('Please accept the read permission in the browser window, and then hit enter.')
    token = a.getToken(frob)
    f = open('token.txt', 'w')
    f.write(token)
    f.close()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', dest='email', required=True)
    parser.add_argument('-p', '--password', dest='password', required=True)
    parser.add_argument('-a', '--all', dest='all_sets', action="store_true")
    parser.add_argument('-s', '--set', type=int, dest='set_number')
    args = parser.parse_args()

    flickr.API_KEY = 'INSERT_YOUR_API_KEY_HERE'
    flickr.API_SECRET = 'INSERT_YOUR_SECRET_HERE'
    flickr.email = args.email
    flickr.password = args.password
    
    if not os.path.exists('token.txt'):
        create_token()
    
    set_names = get_all_sets()
    
    if (args.all_sets):
        print(set_names)
    else:
        set_name = set_names[args.set_number]
        target_set = get_single_set(set_name)
        photos = target_set.getPhotos()
        for photo in photos:
            print_comments(set_name, photo)
    
if __name__ == '__main__':
    main()
