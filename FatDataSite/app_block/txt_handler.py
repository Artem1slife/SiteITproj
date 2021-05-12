from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.tokenize import sent_tokenize

import base64

from pymorphy2 import MorphAnalyzer as MorphAnalyzer_rus

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from scipy.spatial import distance

from wordcloud import WordCloud

from nltk.tokenize import word_tokenize

import numpy as np
import string

import nltk

patterns = "[0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+“”"

nltk.download('stopwords')

stopWords_eng = set(stopwords.words('english'))
stopWords_rus = set(stopwords.words('russian'))

class TextHandler:

    def make_bagofwords(txt):
            # токенизируем
            txt_tokenized = tokenize(txt)

            # фильтрация
            txt_tokenized_filtered = []
            txt_tokenized_filtered = TextHandler.__filtration_txt(txt_tokenized)

            # лемматизация русская
            txt_lemmatizated = []
            txt_lemmatizated = TextHandler.__lemmatization_rus(txt_tokenized_filtered)

            # лемматизация английская
            txt_lemmatizated = TextHandler.__english_lemmatizer(txt_lemmatizated)

            return txt_lemmatizated

        # определение типа слов на английском слов (сказуемые, существительные и тд)
    def __get_wordnet_pos_for_english(word):
            tag = pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)

        # лемматизация английских слов
    def __english_lemmatizer(word_list):
            lemmatizer = WordNetLemmatizer()
            txt_lemmatizated_all = []
            for w in word_list:
                txt_lemmatizated_all.append(lemmatizer.lemmatize(w, TextHandler.__get_wordnet_pos_for_english(w)))

            return txt_lemmatizated_all

        # лемматизация русских слов
    def __lemmatization_rus(txt_tokenized_filtered):
            morph_rus = MorphAnalyzer_rus()

            txt_lemmatizated = []

            for elem in txt_tokenized_filtered:
                elem = elem.strip()
                txt_lemmatizated.append(morph_rus.normal_forms(elem)[0])

            return txt_lemmatizated

    def __filtration_txt(txt_tokenized):
            txt_tokenized_filtered = []

            for w in txt_tokenized:
                w = w.lower()
                if (w not in stopWords_rus) and (w not in stopWords_eng) and (w not in patterns):
                    txt_tokenized_filtered.append(w)

            return txt_tokenized_filtered

class TextHandlerFrequency(TextHandler):
    #количественный анализ - простой и нескольких файлов
    def frequency_analysis(self, textes):
        results = {}
        number = 0
        for text in textes:
            file = open(text, "r", encoding='utf-8')
            text_from_file = file.read()
            file.close()
            bag_txt = TextHandler.make_bagofwords(text_from_file)
            fdist = FreqDist(bag_txt)
            results["Text" + str(number)] = fdist
            number = number+1
        return results

    # количественный анализ в сравнении содержит файл, который сочетает в себе пересечение слов во всех файлах
    def comparison_frequency_analysis(self, textes):
        results = []
        results_dict = {}
        union_bag = []
        number = 0
        for text in textes:
            file = open(text, "r", encoding='utf-8')
            text_from_file = file.read()
            file.close()
            bag_txt = TextHandler.make_bagofwords(text_from_file)
            fdist = FreqDist(bag_txt)
            results_dict["Text" + str(number)] = fdist
            union_bag = union_bag + bag_txt
            number = number+1
        fdist = FreqDist(union_bag)
        results_dict["All_text"] = fdist
        return results_dict

    def comparison_frequency_analysis_str(self, textes):
        results = []
        results_dict = {}
        union_bag = []
        number = 0
        for text in textes:
            bag_txt = TextHandler.make_bagofwords(text)
            fdist = FreqDist(bag_txt)
            results_dict["Text" + str(number)] = fdist
            union_bag = union_bag + bag_txt
            number = number+1
        fdist = FreqDist(union_bag)
        results_dict["All_text"] = fdist
        return results_dict

class TextHandlerSemantic(TextHandler):
    #вес слов - работа с несколькими файлами
    def semantic_analysis(self, textes):
        vectorizer = TfidfVectorizer()

        text_after_work = []
        all_json = {}
        all_df = []
        for text in textes:
            file = open(text, "r", encoding='utf-8')
            text_from_file = file.read()
            file.close()
            text_from_file = sent_tokenize(text_from_file)
            text_from_file = TextHandlerSemantic.__make_doc_ready_for_tfd(text_from_file)
            text_after_work.append(text_from_file)

        number = 0

        for text in text_after_work:
            vectors = vectorizer.fit_transform(text)
            feature_names = vectorizer.get_feature_names()
            dense = vectors.todense()
            denselist = dense.tolist()
            df = pd.DataFrame(denselist, columns=feature_names)
            all_df.append(df)
            js_result = df.to_json(force_ascii=False)
            all_json["Text" + str(number)] = js_result
            number = number+1
        #new_df = pd.concat(all_df, ignore_index=True)

        return all_json

    # вес слов - сравнение файлов - нужна матрица
    def comparison_semantic_analysis(self, textes):
        text_after_work = []
        all_mas = []
        text_after_work_word_doc = []

        for text in textes:
            file = open(text, "r", encoding='utf-8')
            text_from_file = file.read()
            file.close()
            text_from_file = sent_tokenize(text_from_file)
            text_from_file = TextHandlerSemantic.__make_doc_ready_for_tfd(text_from_file)

            text_file = " ".join(text_from_file)
            text_after_work_word_doc.append(text_file)

            text_after_work.append(text_from_file)
        all_mas = TextHandlerSemantic.__add_sugg(text_after_work[0], text_after_work[1])

        tfidfvectorizer = TfidfVectorizer(analyzer='word')
        tfidf_wm = tfidfvectorizer.fit(all_mas)

        df_tfidfvect = []

        text1_idf = tfidf_wm.transform(text_after_work[0])
        df_tfidfvect1 = pd.DataFrame(data=text1_idf.toarray())
        df_tfidfvect1['combine'] = df_tfidfvect1.values.tolist()
        df_tfidfvect1['key'] = 0

        i = 0
        for text_work in text_after_work:
            if i != 0:
                text2_idf = tfidf_wm.transform(text_work)
                df_tfidfvect2 = pd.DataFrame(data=text2_idf.toarray())
                df_tfidfvect2['combine'] = df_tfidfvect2.values.tolist()
                df_tfidfvect2['key'] = 0
                df_tfidfvect.append(df_tfidfvect2)
            else:
                i = i + 1

        for tfidfvector in df_tfidfvect:
            df_all = pd.merge(df_tfidfvect1, tfidfvector, on='key')

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(all_mas)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        df = pd.DataFrame(denselist, columns=feature_names)

        df = pd.DataFrame()
        df['x'] = df_all['combine_x']
        df['y'] = df_all['combine_y']
        df['dist'] = df.apply(lambda x: TextHandlerSemantic.dist(x['x'], x['y']), axis=1)

        return df

    def __make_doc_ready_for_tfd(documents):  #
        for s in range(len(documents)):
            t = documents[s]

            txt_lemmatizated = TextHandler.make_bagofwords(t)

            sentence = ''
            for w in txt_lemmatizated:
                sentence = sentence + w
                sentence = sentence + ' '

            documents[s] = sentence
        return documents

    def __add_sugg(doc1, doc2):
        all_mas = []
        for i in doc1:
            if i in all_mas:
                continue
            else:
                all_mas.append(i)
        for j in doc2:
            if j in all_mas:
                continue
            else:
                all_mas.append(j)
        return all_mas

    # вычисление дистанции между векторами для сравнения
    def dist(x, y):
        return distance.cosine(x, y)

    def get_tf_idf_query_similarity(self, docs):
        vocab = TextHandlerSemantic.__createVocab(docs)

        termDict = {}

        docsTFMat = np.zeros((len(docs), len(vocab)))
        docsIdfMat = np.zeros((len(vocab), len(docs)))

        docTermDf = pd.DataFrame(docsTFMat, columns=sorted(vocab.keys()))
        docCount = 0

        for doc in docs:
            doc = doc.translate(str.maketrans('', '', string.punctuation))
            words = word_tokenize(doc.lower())
            for word in words:
                if (word in vocab.keys()):
                    docTermDf[word][docCount] = docTermDf[word][docCount] + 1

            docCount = docCount + 1

        # Computed idf for each word in vocab
        idfDict = {}

        for column in docTermDf.columns:
            idfDict[column] = np.log((len(docs) + 1) / (1 + (docTermDf[column] != 0).sum())) + 1

        # compute tf.idf matrix
        docsTfIdfMat = np.zeros((len(docs), len(vocab)))
        docTfIdfDf = pd.DataFrame(docsTfIdfMat, columns=sorted(vocab.keys()))

        docCount = 0
        for doc in docs:
            for key in idfDict.keys():
                docTfIdfDf[key][docCount] = docTermDf[key][docCount] * idfDict[key]
            docCount = docCount + 1

        vectorizer = TfidfVectorizer(analyzer='word', norm=None, use_idf=True, smooth_idf=True)
        tfIdfMat = vectorizer.fit_transform(docs)

        feature_names = sorted(vectorizer.get_feature_names())

        docList = []
        number = 0
        for doc in docs:
            docList.append("Doc"+str(number))
            number = number+1

        skDocsTfIdfdf = pd.DataFrame(tfIdfMat.todense(), index=sorted(docList), columns=feature_names)

        csim = cosine_similarity(tfIdfMat, tfIdfMat)

        csimDf = pd.DataFrame(csim, index=sorted(docList), columns=sorted(docList))

        return csimDf

    def __createVocab(docList):
        vocab = {}
        for doc in docList:
            print(doc)
            doc = doc.translate(str.maketrans('', '', string.punctuation))

            words = word_tokenize(doc.lower())
            for word in words:
                if (word in vocab.keys()):
                    vocab[word] = vocab[word] + 1
                else:
                    vocab[word] = 1
        return vocab


class TextHandlerCloud(TextHandler):
    def WordCloud(self, text_raw):
        bag_txt = TextHandler.make_bagofwords(text_raw)
        StrA = " ".join(bag_txt)
        wordcloud = WordCloud().generate(StrA)
        return wordcloud

class TextHandlerLSA(TextHandler):
    def LSA_analysis(self):
        pass

