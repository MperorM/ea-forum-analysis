import requests
import numpy as np
import json
import pandas as pd
import tags
import matplotlib.pyplot as plt

## uncomment until line 61 recreate dataset

# query = """{
#     posts(input: {
#         terms: {
#             limit: 1000
#             offset: %s
#             meta: null
#         }
#         }) {
#         results {
#             _id
#             title slug pageUrl
#             postedAt
#             baseScore
#             voteCount
#             commentCount
#             meta
#             question
#             url
#             user {
#             username
#             slug
#             }
#             tags {
#             name
#             }
#         }
#     }
# }"""

# # make series of graphQL query and turn into dataframe
# posts = pd.DataFrame()
# url = 'https://forum.effectivealtruism.org/graphql'
# offset = 0

# for i in range(0, 10):
#     offset_query = query % (offset)
#     r = requests.post(url, json={'query': offset_query})
#     json_data = json.loads(r.text)
#     df_data = json_data['data']['posts']['results']
#     posts = posts.append(pd.DataFrame(df_data))
#     offset += 1000

# posts = posts.reset_index(drop=True)

# # clean up tags
# def tag_cleaner(tag_list):
#     tag_list = [tag['name'] for tag in tag_list]
#     return tag_list
# posts.tags = posts.tags.apply(lambda x: tag_cleaner(x))

# # save to disk
# posts.to_pickle('data/forum-analysis.pkl')

# Load from disk

posts = pd.read_pickle('data/forum-analysis.pkl')

# categorise post by tag category
## tag category could for example be "global poverty"
## Macro tag could for exmaple be "cause areas"

# Check if tags have at-least one element common
def tag_checker(x):
    tag_categories = []

    for tag_macro_category in tags.tag_types:
        for tag_type in tags.tag_types[tag_macro_category]:
            if (not set(tags.tag_types[tag_macro_category][tag_type]).isdisjoint(x)):
                tag_categories.append(tag_type)
    return tag_categories


posts['tag_categories'] = posts.tags.apply(lambda x: tag_checker(x))


# Get macro tags for each posts tag categories
def macro_tag_checker(x):
    macro_tag_categories = []
    for tag_macro_category in tags.tag_types:
        if (not set(tags.tag_types[tag_macro_category]).isdisjoint(x)):
            macro_tag_categories.append(tag_macro_category)
    return macro_tag_categories

posts['macro_tag_categories'] = posts.tag_categories.apply(lambda x: macro_tag_checker(x))


# format postedat to real dates

posts.postedAt = pd.to_datetime(posts.postedAt)

# save to disk

posts.to_pickle('data/forum-analysis.pkl')