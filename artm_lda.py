# -*- coding: utf-8 -*-

import pandas
import sys
import numpy



# making russian text visible
reload(sys)
sys.setdefaultencoding('utf8')

import artm


batch_vectorizer = artm.BatchVectorizer(data_path="vw.txt", data_format="vowpal_wabbit", target_folder="batches", batch_size=1000)

T = 10   # количество тем
model_artm = artm.ARTM(num_topics=T, topic_names=["sbj"+str(i) for i in range(T)], class_ids={"text":1})

model_artm.scores.add(artm.PerplexityScore(name='PerplexityScore', use_unigram_document_model=False, dictionary_name='dictionary'))
model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore', class_id="text"))
model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=15, class_id="text"))


