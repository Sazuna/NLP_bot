import bao
def preprocess_message(m):
	m = m.replace("%27", "'")
	m = bao.del_urls(m)
	m = bao.lowercase(m)
	m = bao.del_stopwords(m)
	m = bao.lemmatize(m)
	m = bao.del_punct(m)
	m = bao.del_digits(m)
	return m
