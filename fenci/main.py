from gensim.models import word2vec
import jieba.posseg as posseg
import pymysql
from tool import *


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


def calc():
    # 模型加载
    model = word2vec.load('model/keyword.model')
    db = pymysql.connect(host="101.132.43.76", port=3306,
                         user="jingyu", password="jingyu", database="jingyu")
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    # 调出用户历史感兴趣，对关键词加权
    # t = "SELECT * from history LIMIT 3"
    # cursor1.execute(t)
    # likes = cursor1.fetchall()
    likes = ['Acid_Wash_Ankle_Jeans', 'Baroque_Print_Blouse', 'Basic_Bodycon_Jeans']
    styles = []
    for like in likes:
        styles = styles + like.split('_')
    # 调出根据用户输入所过滤的关键词
    match_thick = str(getTemperature())
    match_scene = str(getScene())
    sql = "SELECT * from score \
                WHERE Thickness = %s" % match_thick + " AND Scene = %s" % match_scene
    filtered_list = []
    score_list = []
    try:
        # 执行SQL语句
        cursor2.execute(sql)
        # 获取所有记录列表
        results = cursor2.fetchall()
        for row in results:
            result = str(row[0])
            filtered_list.append(result)
    except Exception as e:
        print(str(e))
    # 为过滤后的每件服饰进行算法评估得到分数列表
    for clothe in filtered_list:
        words = clothe.split('_')
        try:
            score_list.append(model.wv.n_similarity(words, styles))
        except Exception as e:
            score_list.append(-1)
            continue
    # 取出最高得分的服饰
    max_idx = score_list.index(max(score_list))
    return score_list[max_idx], filtered_list[max_idx]
