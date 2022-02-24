from gensim.models import word2vec
import jieba.posseg as posseg


def match(text):
    # 词性
    seg2 = posseg.lcut(text)
    filted = [x.word for x in seg2 if x.flag == 'n' or x.flag == 'vn' or x.flag == 'v' and len(x.word) >= 2]

    label = ['休闲', '聚会', '运动', '职场']
    model = word2vec.Word2Vec.load('model/wiki.zh.text.model')
    predict = ''
    predict_value = 0
    for j in range(0, len(filted)):
        for i in range(0, 4):
            temp = model.wv.similarity(filted[j], label[i])
            if temp > predict_value:
                predict_value = temp
                predict = label[i]
    return predict

