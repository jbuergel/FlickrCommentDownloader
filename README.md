FlickrCommentDownloader
=======================

A quick Python script to download photos (in original size) from Flickr, along with their associated comments.  I whacked this together to pull down some of my data and not lose my descriptive comments, because I couldn't find anything else that would do it.

To use, replace flickr.API_KEY and flickr.API_SECRET in getfullset.py with your appropriate API key and secret from Flickr.  If you don't have any, you can get them from http://www.flickr.com/services/apps/create/apply/

Once set up, you can run 'python getfullset.py' and get help.  You can print a list of sets and then download individual sets with comments.

This was written using Python 3.3.  It's built on top of flickr.py (https://code.google.com/p/flickrpy/), updated to be Python 3 compatible.

Known issues:  two of my sets weren't recognized by this app, but they were ones I didn't care about, so I didn't worry about it.