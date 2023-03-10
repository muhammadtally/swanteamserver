import copy
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tqdm import tqdm
from NLP.nlp import *

def doc2vec(docs, query_str="", _vector_size=20, n_top_docs=10, is_matrix_mode=True,):
    """
    :param docs: dictionary of documents - {doc_location: doc_words}.
    :param query_str:
    :param _vector_size: doc2Vec vector_size.
    :param n_top_docs: the number of most similar documents to be returned.
    :param is_matrix_mode: if True the function will return matrix, otherwise the function will return the cosine
    distance matrix of all documents to the 'query'.
    :return:
    """
    docs = copy.deepcopy(docs)
    tagged_data = [TaggedDocument(doc_words, [doc_name]) for doc_name, doc_words in docs.items()]
    model = Doc2Vec(tqdm(tagged_data), vector_size=_vector_size, window=2, min_count=1, workers=4, epochs=100)
    if is_matrix_mode:
        return model.docvecs.vectors.tolist(), list(model.docvecs.key_to_index.keys())
    else:
        test_doc = tokenize_hebrew(query_str)
        return model.docvecs.most_similar(positive=[model.infer_vector(test_doc)], topn=n_top_docs)