#!/usr/bin/env python

"""
###### WARNING ###########
MODIFIED TO READ THE FORMAT OF tags: [tag1, tag2]
BUT TOO MUCH LAZYNESS TO UPDATE THE DOCUMENTATION (:

update_tags.py
Script to automatically create tags posts for a Jekyll blog hosted
in Github pages. First, it fishes all tags. Then, it creates the
tags posts. Lastly, it adds the generated files, commits them, and pushes 
them to the corresponding repository. Preferably run this script
when having a clean working space (nothing to commit/push).
Based on Long Qian's post
https://longqian.me/2017/02/09/github-jekyll-tag/


@author: Arturo Moncada-Torres
arturomoncadatorres@gmail.com
"""

#%% Preliminaries.
import glob
import os
import re

#import git


#%% Define paths.
post_dir = '_posts/'
tag_dir = 'tag/'


#%%
def get_tags(post_dir=post_dir, verbose=True):
    '''
    Adapted from tag_generator.py
    Copyright 2017 Long Qian
    Contact: lqian8@jhu.edu
    This script created tags for a Jekyll blog hosted by Github page.
    No plugins required.
    See https://longqian.me/2017/02/09/github-jekyll-tag/
    
    Updated 2019-12-05
    Arturo Moncada-Torres
    arturomoncadatorres@gmail.com
    Adapted script to process .md files with tags in format
    tags:
        - tag1
        - tag2
        ...
    Notice that for this to work properly, tags must be the last element of the
    Markdown header.
    
    Parameters
    ----------
    post_dir: string
        Path to directory _posts/
        
    verbose: boolean
        Indicate if status messages are printed (True) or not (False)


    Returns
    -------
    total_tags: set
        Set with all the tags used in the different posts.
    '''    
    
    # Get Markdown posts files.
    filenames = glob.glob(post_dir + '*md')
    
    # Loop through all files.
    total_tags = set()
    for filename in filenames:
        f = open(filename, 'r', encoding='utf8')
        #content = f.read()
        # Find all occurrences of [tag1, tag2, tag3]
        for line in f:
            if 'tags:' in line:
                # Find all occurrences of [tag1, tag2, tag3]
                matches = re.findall(r'\[([^]]+)\]', line)
        
        # Iterate over the matches and extract individual tags
        for match in matches:
            total_tags.update([tag.strip() for tag in match.split(',')])
    
    if verbose:
        print("Found " + str(total_tags.__len__()) + " tags")
    
    return total_tags


#%%
def create_tags_posts(tag_dir=tag_dir, total_tags=set(), verbose=True):
    '''
    Adapted from tag_generator.py
    Copyright 2017 Long Qian
    Contact: lqian8@jhu.edu
    This script created tag posts for a Jekyll blog hosted by Github page.
    No plugins required.
    See https://longqian.me/2017/02/09/github-jekyll-tag/
    
    Updated 2019-12-11
    Arturo Moncada-Torres
    arturomoncadatorres@gmail.com
    Modularized for ease of use in update_tags.py.
    
    Parameters
    ----------
    post_dir: string
        Path to directory directory where tag posts will be created.
        
    total_tags: set
        
        
    verbose: boolean
        Indicate if status messages are printed (True) or not (False)


    Returns
    -------
    None
    '''
    
    if total_tags.__len__() == 0:
        print("No tags. Thus, no tag posts were created")
        return None
    
    else:
    
        old_tags = glob.glob(tag_dir + '*.md')
        for tag in old_tags:
            os.remove(tag)
            
        if not os.path.exists(tag_dir):
            os.makedirs(tag_dir)
        
        for tag in total_tags:
            tag_filename = tag_dir + tag + '.md'
            f = open(tag_filename, 'a')
            write_str = '---\nlayout: tag_page\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
            f.write(write_str)
            f.close()
            
        if verbose:
            print("Created " + str(total_tags.__len__()) + " tag posts")
            
        return None


#%%
if __name__ == '__main__':
    tags = get_tags(post_dir)
    create_tags_posts(tag_dir, tags)

    # For Git.
    #repo = git.Repo(os.getcwd())

    # Add files for commit.
    #try:
    #    repo.git.add(tag_dir)
    #except:
    #    print("Error ocurred while adding files to Git.")

    # Commit changes.    
    #try:
    #    repo.git.commit('-m', 'Updated tags and created corresponding posts', author='brerodriguez@github.com')    
    #except:
    #    print("Error occurred while commiting.")
    
    # Push commit.
    #try:
    #    origin = repo.remote(name='origin')
    #    origin.push()
    #except:
    #    print("Error occurred while pushing.")