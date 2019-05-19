from gensim.models.wrappers import FastText

model = FastText.load_fasttext_format('./models/ko.bin')

print(model.most_similar('가족'))

print(model.similarity('사랑', '눈물'))
