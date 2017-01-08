# Imports
import pickle as pic
import numpy as np
import nltk
import string
import pandas as pd
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from sklearn.cross_validation import train_test_split
import time
import matplotlib.pyplot as plt


# Define Functions
stemmer = nltk.stem.porter.PorterStemmer()

stop = set(stopwords.words('english'))


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens if item not in stop]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(None, string.punctuation)))


def lda_evaluation(corpus, texts, dictionary, num_folds=3,
                   topics=10, random_state=None):
    # Create train-test split
    train_corp, test_corp, train_texts, test_texts = train_test_split(corpus, texts, random_state=random_state)

    # Train LDA Model
    start = time.time()
    lda = models.LdaMulticore(train_corp, id2word=dictionary,
                              num_topics=topics, iterations=50)
    train_time = time.time()
    print "Model trained in %s seconds." % (train_time - start)

    # Find perplexity on held out documents
    perplexity = lda.bound(test_corp)
    number_of_words = sum(len(doc) for doc in test_texts)
    per_word_perplex = np.exp2(-perplexity / number_of_words)
    perplexity_time = time.time()
    print "Perplexity found in %s seconds." % (perplexity_time - train_time)

    # Calculate coherence measures
    cm_cv = CoherenceModel(model=lda, texts=train_texts,
                           dictionary=dictionary, coherence='c_v')
    cm_umass = CoherenceModel(model=lda, corpus=train_corp,
                              dictionary=dictionary, coherence='u_mass')
    cv_coherence = cm_cv.get_coherence()
    umass_coherence = cm_umass.get_coherence()
    coherence_time = time.time()
    print "Coherence scores found in %s seconds." % (coherence_time - perplexity_time)

    # Return results
    result = [perplexity, per_word_perplex, cv_coherence, umass_coherence]
    return result


def test_topic_num(topic_num_list, corpus, texts,
                   dictionary, random_state=None):
    # Create Reults DataFrame
    results = pd.DataFrame()

    # Evaluate topic model for each number of topics in list
    for num in topic_num_list:
        print "Number of topics being evaluated: %s" % num
        evaluation = lda_evaluation(corpus, texts, dictionary,
                                    topics=num, random_state=random_state)
        print evaluation
        scores = pd.DataFrame(np.array([num] + evaluation, ndmin=2))
        results = results.append(scores)

    results.rename(columns={0: 'num_topics', 1: 'perplex',
                   2: 'per_word_perplex', 3: 'cv', 4: 'umass'}, inplace=True)
    return results


def create_chart(df, x, y, x_lab, y_lab, file_name):
    df.plot(x=x, y=y)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.legend([y_lab])
    plt.savefig("../Images/%s" % file_name)



# Load Data
all_data = pic.load(open("../Data/all_data.p"))

# Get Text and Index
ann_text = all_data['ann_text'].values
ref_text = all_data['fragment'].values

Normalize our annotations and Referent Text
print "Normalizing..."
ann_text_bow = np.array(map(normalize, ann_text))
ref_text_bow = np.array(map(normalize, ref_text))

ann_dictionary = corpora.Dictionary(ann_text_bow)
ref_dictionary = corpora.Dictionary(ref_text_bow)


# Create our corpuses
print "Creating corpuses..."
ann_corpus_bow = np.array([ann_dictionary.doc2bow(text) for text in ann_text_bow])
ref_corpus_bow = np.array([ref_dictionary.doc2bow(text) for text in ref_text_bow])


# Annotation LDA Evaluation
print "Starting Annotation Evaluation..."
topic_num_list = range(5, 51, 5)
ann_results = test_topic_num(topic_num_list, ann_corpus_bow,
                             ann_text_bow, ann_dictionary, random_state=40)

# Pickle Data
pic.dump(ann_results, open("../Data/ann_lda_results.p", "wb"))

# Graph Results
create_chart(ann_results, "num_topics", "per_word_perplex", "Number of Topics",
             "Per Word Perplexity", "ann_lda_per_word_perplex.png")

create_chart(ann_results, "num_topics", "cv", "Number of Topics",
             "C_V coherence", "ann_lda_cv.png")

create_chart(ann_results, "num_topics", "umass", "Number of Topics",
             "UMass coherence", "ann_lda_umass.png")

# Referent LDA Evaluation
print "Starting Referent Evaluation..."
topic_num_list = range(5, 51, 5)
ref_results = test_topic_num(topic_num_list, ref_corpus_bow,
                             ref_text_bow, ref_dictionary, random_state=40)

# Pickle Data
pic.dump(ref_results, open("../Data/ref_lda_results.p", "wb"))

# Graph Results
create_chart(ref_results, "num_topics", "per_word_perplex", "Number of Topics",
             "Per Word Perplexity", "ref_lda_per_word_perplex.png")

create_chart(ref_results, "num_topics", "cv", "Number of Topics",
             "C_V coherence", "ref_lda_cv.png")

create_chart(ref_results, "num_topics", "umass", "Number of Topics",
             "UMass coherence", "ref_lda_umass.png")
