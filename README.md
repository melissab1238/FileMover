# Backing Up (my files) From Google Drive to Harddrive

## Problem

I have a lot of files on Google Drive and I'm paying $15/month for 2TB of storage, but I really only need about 200GB of space. Unfortunately, the jump for paid Google Drive is above 15 GB which is barely anything, especially when dealing with GoPro video files I have yet to look through from previous trips.

## Solution

I have used Google's Cloud Drive API to access files and folders in Google Drive before. My solution is to create an interactive Python script that copies files from any Google Drive Folder and then downloads them into your computer's (or in my case, my harddrive's) local file system.

## Setup

1. In the Google Cloud Console, navigate to "APIs & Services" > "Credentials", click on "Create Credentials" and select "OAuth client ID". Follow the prompts to create your OAuth client ID.
2. Save this OAuth client ID in a file called `credentials.json`.
