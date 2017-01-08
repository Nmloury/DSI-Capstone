import pickle as pic
import numpy as np
import seaborn as sb
import nltk, string
import pandas as pd
from gensim import corpora, models, similarities
from collections import defaultdict
from nltk.corpus import stopwords
import gensim
from itertools import compress


# Load data
all_data = pic.load(open("../Data/all_data.p"))

# Create users df with the count of referents
ref_count = all_data.groupby('annotator_id').size().reset_index()
users = ref_count
users.rename(columns={0: "num_of_refs"}, inplace=True)

# Add Voter Statistics
vote_group = all_data.groupby('annotator_id')['votes_total']
vote_info = vote_group.agg([sum, min, max, np.mean, np.median, np.std])
vote_info = vote_info.reset_index(drop=True)
vote_columns = {
    "sum": "vote_total",
    "min": "vote_min",
    "max": "vote_max",
    "median": "vote_median",
    "mean": "vote_avg",
    "std": "vote_std"
}
vote_info.rename(columns=vote_columns, inplace=True)
users = pd.concat([users, vote_info], axis=1)

# Add Comment Statistics
comment_group = all_data.groupby('annotator_id')['comment_count']
comment_info = comment_group.agg([sum, min, max, np.mean, np.median, np.std])
comment_info = comment_info.reset_index(drop=True)
comment_columns = {
    "sum": "comment_total",
    "min": "comment_min",
    "max": "comment_max",
    "median": "comment_median",
    "mean": "comment_avg",
    "std": "comment_std"
}
comment_info.rename(columns=comment_columns, inplace=True)
users = pd.concat([users, comment_info], axis=1)

# Add Comment Statistics
ann_char_group = all_data.groupby('annotator_id')['annotation_length_char']
ann_char_info = ann_char_group.agg([sum, min, max, np.mean, np.median, np.std])
ann_char_info = ann_char_info.reset_index(drop=True)
ann_char_columns = {
    "sum": "ann_char_total",
    "min": "ann_char_min",
    "max": "ann_char_max",
    "median": "ann_char_median",
    "mean": "ann_char_avg",
    "std": "ann_char_std"
}
ann_char_info.rename(columns=ann_char_columns, inplace=True)
users = pd.concat([users, ann_char_info], axis=1)
users.shape

# Add Comment Statistics
all_data['ann_length_char'] = all_data['ann_text'].apply(lambda x: len(x))

ann_char_group = all_data.groupby('annotator_id')['ann_length_char']
ann_char_info = ann_char_group.agg([sum, min, max, np.mean, np.median, np.std])
ann_char_info = ann_char_info.reset_index(drop=True)
ann_char_columns = {
    "sum": "ann_char_total",
    "min": "ann_char_min",
    "max": "ann_char_max",
    "median": "ann_char_median",
    "mean": "ann_char_avg",
    "std": "ann_char_std"
}
ann_char_info.rename(columns=ann_char_columns, inplace=True)
users = pd.concat([users, ann_char_info], axis=1)
users.shape

# Add Annotation Word Statistics
all_data['ann_length_word'] = all_data['ann_text'].apply(lambda x: len(x.split()))
ann_word_group = all_data.groupby('annotator_id')['ann_length_word']
ann_word_info = ann_word_group.agg([sum, min, max, np.mean, np.median, np.std])
ann_word_info = ann_word_info.reset_index(drop=True)
ann_word_columns = {
    "sum": "ann_word_total",
    "min": "ann_word_min",
    "max": "ann_word_max",
    "median": "ann_word_median",
    "mean": "ann_word_avg",
    "std": "ann_word_std"
}
ann_word_info.rename(columns=ann_word_columns, inplace=True)
users = pd.concat([users, ann_word_info], axis=1)
users.shape

# Add Annotation Character Statistics
all_data['ann_length_char'] = all_data['ann_text'].apply(lambda x: len(x))

ann_char_group = all_data.groupby('annotator_id')['ann_length_char']
ann_char_info = ann_char_group.agg([sum, min, max, np.mean, np.median, np.std])
ann_char_info = ann_char_info.reset_index(drop=True)
ann_char_columns = {
    "sum": "ann_char_total",
    "min": "ann_char_min",
    "max": "ann_char_max",
    "median": "ann_char_median",
    "mean": "ann_char_avg",
    "std": "ann_char_std"
}
ann_char_info.rename(columns=ann_char_columns, inplace=True)
users = pd.concat([users, ann_char_info], axis=1)
users.shape

#
