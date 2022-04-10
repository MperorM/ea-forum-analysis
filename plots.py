import requests
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

posts = pd.read_pickle('data/forum-analysis.pkl')

# Graph amount of posts with each tag

# taken from https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
def to_1D(series):
 return pd.Series([x for _list in series for x in _list])

tags = to_1D(posts["tag_categories"]).value_counts().index
posts_per_tag = to_1D(posts["tag_categories"]).value_counts().values

fig, ax = plt.subplots(figsize = (14,4))
ax.bar(tags,
        posts_per_tag)
ax.set_ylabel("forum posts", size = 12)
ax.set_xlabel("tag")
ax.set_title("Posts per forum tags", size = 14)
fig.autofmt_xdate()

plt.savefig('data/posts_per_tag.png')

# Graph amount of posts with each macro tag

fig, ax = plt.subplots(figsize = (14,4))
ax.bar(to_1D(posts["macro_tag_categories"]).value_counts().index,
        to_1D(posts["macro_tag_categories"]).value_counts().values)
ax.set_ylabel("forum posts", size = 12)
ax.set_xlabel("tag")
ax.set_title("forum post macro tags", size = 14)
fig.autofmt_xdate()

plt.savefig('data/posts_per_macro_tag.png')

###
# Posts by tag by year
###

# remove posts from before 2011 (post-humous posts)
posts = posts[~(posts['postedAt'].dt.year < 2011)]

# plot posts by year, each bar with tags stacked on top of each other with a different color

years = posts.postedAt.dt.year.value_counts().index
posts_per_year = pd.DataFrame(columns=tags)
for year in years:
    posts_this_year = posts[posts.postedAt.dt.year == year]
    tags_this_year = to_1D(posts_this_year["tag_categories"]).value_counts()
    tags_this_year = tags_this_year.rename(year)
    posts_per_year = posts_per_year.append(tags_this_year)

posts_per_year = posts_per_year.fillna(0)
posts_per_year.sort_index().plot(kind='bar', stacked=True, ylabel='Number of posts', xlabel='Year', legend='reverse', title='Posts by tag by year')

plt.savefig('data/posts_per_tag_per_year.png')

# plot posts by year, normalized

normalized_posts_per_year = posts_per_year.div(posts_per_year.sum(axis=1), axis=0)

normalized_posts_per_year.sort_index().plot(kind='bar', stacked=True, ylabel='Number of posts', xlabel='Year', figsize=(14,4), legend='reverse', title='Normalized posts by tag by year')

plt.savefig('data/posts_per_tag_per_year_normalized.png')

###
# Average upvote per post
###

# taken from https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
def boolean_df(item_lists, unique_items):# Create empty dict
    bool_dict = {}
    
    # Loop through all the tags
    for i, item in enumerate(unique_items):
        
        # Apply boolean mask
        bool_dict[item] = item_lists.apply(lambda x: item in x)
            
    # Return the results as a dataframe
    return pd.DataFrame(bool_dict)

unique_tags = tags
tags_bool = boolean_df(posts["tag_categories"], unique_tags)

upvotes_per_tag = pd.Series(index=unique_tags, data=0)

# TODO: rewrite to list comprehension
for i in posts.iterrows():
    for tag in posts.loc[i[0]]['tag_categories']:
        upvotes_per_tag[tag] += posts.loc[i[0]]['baseScore']

fig, ax = plt.subplots(figsize = (14,4))
upvotes_per_post = upvotes_per_tag / posts_per_tag
ax.bar(upvotes_per_post.sort_values().index, upvotes_per_post.sort_values())
ax.set_ylabel("upvotes", size = 12)
ax.set_xlabel("tag")
ax.set_title("Average upvote for tagged posts", size = 14)
fig.autofmt_xdate()

plt.savefig('data/upvotes_per_tag_per_post.png')

###
# Average comments per post
###

posts.commentCount = posts.commentCount.fillna(0)
comments_per_tag = pd.Series(index=unique_tags, data=0)

# TODO: rewrite to list comprehension
for i in posts.iterrows():
    for tag in posts.loc[i[0]]['tag_categories']:
        comments_per_tag[tag] += posts.loc[i[0]]['commentCount']

fig, ax = plt.subplots(figsize = (14,4))
comments_per_post = comments_per_tag / posts_per_tag
ax.bar(comments_per_post.sort_values().index, comments_per_post.sort_values())
ax.set_ylabel("comments", size = 12)
ax.set_xlabel("tag")
ax.set_title("Average amount of comments", size = 14)
fig.autofmt_xdate()

plt.savefig('data/comments_per_tag_per_post.png')

plt.show()