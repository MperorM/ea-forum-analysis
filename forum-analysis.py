import requests
import numpy as np
import json
import pandas as pd
import tags

query = """{
    posts(input: {
        terms: {
            limit: 200
            meta: null
        }
        }) {
        results {
            _id
            title slug pageUrl
            postedAt
            baseScore
            voteCount
            commentCount
            meta
            question
            url
            user {
            username
            slug
            }
            tags {
            name
            }
        }
    }
}"""

# make graphQL query and turn into dataframe
url = 'https://forum.effectivealtruism.org/graphql'
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)
df_data = json_data['data']['posts']['results']
df = pd.DataFrame(df_data)

# clean up tags
def tag_cleaner(tag_list):
    tag_list = [tag['name'] for tag in tag_list]
    return tag_list
df.tags = df.tags.apply(lambda x: tag_cleaner(x))

# save to disk
df.to_pickle('data/forum-analysis.pkl')

# categorise post by tag category

# Check if tags have at-least one element common
def tag_checker(x):
    tag_categories = []
    for tag_type in tags.tag_types:
        print(type(tag_type))
        if (not set(tags.tag_types.get(tag_type)).isdisjoint(x)):
            tag_categories.append(tag_type)
    return tag_categories


df.tag_categories = df.tags.apply(lambda x: tag_checker(x))