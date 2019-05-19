from kiwipiepy import Kiwi

class ReaderExam:
    def __init__(self, filePath):
        self.file = open(filePath)

    def read(self, id):
        if id == 0: self.file.seek(0)
        return self.file.readline()
kiwi = Kiwi()
numThread = 4
kiwi = Kiwi(numThread)
reader = ReaderExam('../../data/test.txt')
minCount = 3
maxWordLength = 6
minScore = 0.25
kiwi.extractWords(reader.read, minCount, maxWordLength, minScore)
kiwi.prepare()
texts = ["아무도 없는 곳 하얀 하늘을 보며 그대를 생각해 그 대여 함께 해요.","뜨거운 태양 아래에 서 있는 너의 모습에 한순간 나의 마음을 뺏기고 말았어"]
topN = 1
for text in texts:
    for uu in kiwi.analyze(text, topN):
        for u in uu[0]:
            print(u[0], u[1])
    print("___________________")