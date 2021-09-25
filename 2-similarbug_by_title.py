import re
import jieba.analyse
from document_similarity_score.document_similarity_score import Context
from document_similarity_score.document_similarity_score import (ConcreteStrategyJaccardIndex)
import jieba
import xlrd
from nltk import WordNetLemmatizer, SnowballStemmer


def readTitle(path, sheet):
    xlsx = xlrd.open_workbook(path)
    sheet_names = xlsx.sheet_names()
    report = xlsx.sheets()[sheet_names.index(sheet)]

    numbers = report.col_values(0)  # bug number
    titles = report.col_values(1)  # bug report title
    ref_titles = report.col_values(2)  # ref bug report title
    sha = report.col_values(5)  # bug report title
    file_name = report.col_values(6)  # bug report title

    index = 0
    data = set()
    for title in titles:
        title = str(title).lower()
        data.add((numbers[index], title.strip(), ref_titles[index], sha[index], file_name[index]))
        index += 1

    # index = 0
    # data = set()
    # for title in titles:
    #     # print(title)
    #     title = str(title).lower()
    #     title = clean_data(title)
    #     # print(numbers[index],title.strip())
    #     data.add((numbers[index],title.strip()))
    #     # print('-----------------------')
    #     index+=1

    return data


def clean_data(issues):
    issues = re.sub(
        r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#!]*[\w\-\@?^=%&amp;/~\+#!])',
        ' ', issues)  # URL
    issues = re.sub(
        r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1, 13}\.[com,cn,net]{1,3}$',
        ' ', issues)  # email
    issues = re.sub(
        r'[\u4e00-\u9fa5]',
        ' ', issues)  # ZH
    # issues = emoji.demojize(issues)  # emoji
    issues = re.sub(
        r'[*](pr)[*]',
        ' ', issues)  # pr
    issues = re.sub(
        r'[*](cc)[*]',
        ' ', issues)  # cc

    issues = re.sub(
        r'\d+',
        ' ', issues)  #

    issues = re.sub(
        r'\d+ ',
        " ", issues)  # \d+

    issues = re.sub(
        r'@(\w+-\w+-\w+)',
        ' ', issues)  # name
    issues = re.sub(
        r'@(\w+-\w+)',
        ' ', issues)  # name
    issues = re.sub(
        r'@\w+',
        ' ', issues)  # name
    issues = re.sub(
        r'(signed).*',
        ' ', issues)  # name

    # issues = re.sub(
    #     r'```(.*)```',
    #     ' ', issues)  # long code
    # issues = re.sub(
    #     r'`(.*)`',
    #     ' ', issues)  # short code
    #
    # issues = re.sub(
    #     r'\'(.*)\'',
    #     ' ', issues)  # ' '
    # issues = re.sub(
    #     r'\"(.*)\"',
    #     ' ', issues)  # " "
    # issues = re.sub(
    #     r'\[(.*)\]',
    #     ' ', issues)  # [ ]
    # issues = re.sub(
    #     r'\(.*\)',
    #     ' ', issues)  # ( )
    # issues = re.sub(
    #     r'(<).*(>)',
    #     ' ', issues)  # < >

    # stoplist = stopwords.words('english')
    # cleanwordlist = [word for word in issues.lower().split() if word not in stoplist]
    #
    # s = ""
    # for i in cleanwordlist:
    #     s = s + " " + i

    issues = re.sub(
        r'[`~!@#$%^&*()_\-+=<>?:"{}|,.\/;\'\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘’，。、→]',
        ' ', issues)  # char

    issues = seg_depart(issues)  # 读取停词表，去停词

    while 1:
        searchObj = re.search(r'  ', issues, re.M | re.I)
        if searchObj:
            issues = re.sub(
                r'  ',
                ' ', issues)  # blank
        else:
            break

    return issues.lower()


# 创建停用词列表
def stopwordslist():
    stopwords = [line.replace('\n', '') for line in
                 open('/Users/yangyilin/我的坚果云/Python/DataProcess/stopwords/stop_words_eng的副本.txt',
                      encoding='UTF-8').readlines()]
    # pprint(stopwords)
    return stopwords


# 对句子进行分词
def seg_depart(sentence):
    wnl = WordNetLemmatizer()  # 词型还原
    stemmer = SnowballStemmer("english")  # 选择语言
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        # word = wnl.lemmatize(word)
        # word = stemmer.stem(word)  # 词干化单词
        if word not in stopwords:
            # word = stemmer.stem(word)  # 词干化单词
            if word != '\t':
                outstr += word.strip()
                outstr += " "
    return outstr


def rankTitle():
    corpus_reports = readTitle('BugReports.xlsx', 'pandas')
    bugs_reports = readBugInPy()

    # # 1.Jaccard
    context = Context(ConcreteStrategyJaccardIndex())
    # # 2.difflib
    # sequenceMatcher = difflib.SequenceMatcher()

    for b in bugs_reports:
        num = b[0]
        print(num)

        result = []

        tokens_1 = ''
        bug_title = jieba.analyse.extract_tags(b[1].lower())
        bug_title = ' '.join(bug_title)
        bug_ref_title = jieba.analyse.extract_tags(b[2].lower())
        bug_ref_title = ' '.join(bug_ref_title)

        tokens_1 += clean_data(bug_title).strip()
        tokens_1 += ' '
        tokens_1 += clean_data(bug_ref_title).strip()
        tokens_1 += ' '

        # for c in corpus_reports:
        #     corpus_bug_title = jieba.analyse.extract_tags(c[1].lower())
        #     corpus_bug_title = ' '.join(corpus_bug_title)
        #     corpus_bug_ref_title = jieba.analyse.extract_tags(c[2].lower())
        #     corpus_bug_ref_title = ' '.join(corpus_bug_ref_title)
        #
        #     # 1.Jaccard
        #     # similarity_score = context.calculate_document_similarity_score(bug_title, corpus_bug_title)
        #
        #     # 2.difflib
        #     # sequenceMatcher.set_seqs(bug_title+' '+bug_ref_title, corpus_bug_title+' '+corpus_bug_ref_title)
        #     # similarity_score = sequenceMatcher.ratio()
        #
        #     # 3.fuzzywuzzy
        #     similarity_score = fuzz.token_set_ratio(bug_title+' '+bug_ref_title, corpus_bug_title+'
        #     '+corpus_bug_ref_title)
        #
        #     result.append([similarity_score, corpus_bug_title,corpus_bug_ref_title])
        #
        # result = sorted(result, key=lambda x: x[0], reverse=True)
        #
        # candidates = result[0:1]
        # tokens_2 = ''
        # for i in candidates:
        #     tokens_2 += clean_data(i[1]).strip()
        #     tokens_2 += ' '
        #     tokens_2 += clean_data(i[2]).strip()

        tokens_1 = tokens_1.split(' ')
        tokens_1 = sorted(set(tokens_1), key=tokens_1.index)
        tokens_1 = [i for i in tokens_1 if i != '']
        print(tokens_1)

        # tokens_2 = tokens_2.split(' ')
        # tokens_2 = sorted(set(tokens_2),key=tokens_2.index)
        # tokens_2 = [i for i in tokens_2 if i != '']
        # print(tokens_2)

        print('————————————————————————————————————————————————')


def readBugInPy():
    sha = ['e41ee47a90bb1d8a1fa28fcefcd45ed8ef5cb946',
           'e1ee2b0679e5999c993a787606d30e75faaba7a2',
           '27b713ba677869893552cbeff6bc98a5dd231950',
           '765d8db7eef1befef33f4c99d3e206d26e8444c8',
           '8e9b3eee812b70197341c26c40200d8a1a77ed9c',
           'e46026ff4669a30192b91e362ce8cdcbc9693870',
           '53a0dfd41a65a33dd7b0963734b24c749212e625',
           '68b3eb4f5a7fbc223accbbeddbf03ec8ea31af00',
           'b7f061c3d24df943e16918ad3932e767f5639a38',
           '9a222ea0300053ff46da984e3b3f68622ccba9c3',
           '386494d0dc851be9e86b1576f30fa8705df4d47b',
           'c4fa6a52f7737aecda08f6b0f2d6c27476298ae1',
           'f98d2b6587b74c9a640b062d94911b199d962119',
           'e0bd4d5dd07cc481cb52de3cf3c7bf199cb2df07',
           '8aa707298428801199280b2b994632080591700a',
           '30059081e946a2020d08d49bf4fa7b771d10089a',
           '5a0f7e9e03976020ba52a7473f90cb1c8a4354c0',
           'e639af2afd18b90ab9063df9c1927ae1f357a418',
           '710d82c0d393c9031e469ec0371660d8187b7dc3',
           '112e6b8d054f9adc1303138533ed6506975f94db',
           '82c9547ddcaf2fd70e00f1368731f14a03bbac88',
           '91150d976ac41bd93a0e6516b2090c534f91aff2',
           '8efc717e4652e1e4bfbc4455da1d40eb676eed91',
           'bf5848f111c92fc5c6c11a93a3bc2480f138f1b1',
           'c983d52e3a3a8a191359814417f375b1dc8b04c1',
           'f41219179de69fed5c2a4b7df821394af1aa6559',
           '6241b9d3b3b8fd688cf32e45539719f1b9ec25c1',
           '48f1a67469c91c38e78ebb2648061fe73dd79e6b',
           '0ffdbe36f0df732f2700cda4a84be758084ff901',
           '4375daffeed16531bae3fdaf85324b590d1dcb59',
           '411dd249e755d7e281603fe3e0ab9e0e48383df9',
           'df918becf698741861da0e9b7e810d477b0eb194',
           'ffe6cfdbf82d663c3f77567bde11f1666de1df38',
           'f08a1e62e31fc11e7e5bd7bec72b7e6d86473423',
           '773f341c8cc5a481a5a222508718034457ed1ebc',
           '95edcf1cbee630e42daca0404c44d8128ea156fb',
           'fa1364d1299a53093bc704f9c34c595b602a568b',
           'd38627b5889db3f663cad339fe8f995af823b76b',
           '5a227a410c520ceec2d94369a44e2ab774a40dc3',
           'f61deb962ac0853595a43ad024c482b018d1792b',
           '0c0a0cfbadcf01864d499599712edc9022eea12e',
           'e0c63b4cfaa821dfe310f4a8a1f84929ced5f5bd',
           '0bde7cedf46209a9fd4fa8c7f9fbce8b49aa78cd',
           '05cc95971e56b503d4df9911a44cd60a7b74cc79',
           'def01cf7bbb5ef8c9bf2e19737ea918e6a76a143',
           'b1c871ce4b5e76b3cffe1ebd4216d36379872352',
           '62ab439b168d972546e06d329916c6be7ddd1288',
           '74e8607cb163b76ccf272ac72ae6b7848fe930c8',
           'fb62fcf91c874e9c24fa83693c4e6e613f35f864',
           'ca5198a6daa7757e398112a17ccadc9e7d078d96',
           '640d9e1f5fe8ab64d1f6496b8216c28185e53225',
           'f669f94a186ea444cc771985a915e90eecf218a9',
           '61819aba14dd7b3996336aaed84d07cd936d92b5',
           'd44fb07063e9a8bd8a209ddce35b40d8a56c8d02',
           '1fa1ad91b29c5474cbb86cbcbcdcd50537cad0ae',
           '01babb590cb15ef5c6e9ad890ea580a5112e6999',
           'c6a1638bcd99df677a8f76f036c0b30027eb243c',
           '55e8891f6d33be14e0db73ac06513129503f995c',
           '92afd5c2c08216e4e9c80eb6b92b1660f91846e0',
           '56d0934092b8296c90f940c56fce3b731e0de81b',
           '73d614403759831814ef7ab83ef1e4aaa645b33a',
           '70ca24680d3e51fa4b957366e8093b3cc755462d',
           '13dc13f12c0fca943979cde065b7484bb0e40d66',
           'ef9b9387c88cf12b20dd8656dfedfc236e0f3352',
           '4334482c348c3adc69683c8332295e22092c1b57',
           'd3a6a3a58e1a6eb68b8b8399ff252b8f4501950e',
           'd857cd12b3ae11be788ba96015383a5b7464ecc9',
           '8267427bfe567eec9a098aa8c071dddcc1d289f9',
           'c82cb179affed1c1136431ce39e4c66f4f3a65c0',
           '89d8aba76a2bb930e520590d145e3d67b2046e39',
           'cf9ec7854ecb80709804178e769425f02ddf8c64',
           'f10ec595eccaf86a9f52fe9683e1181a51ba675b',
           '51f114b9882a5cf819efddb8be74524814f437e1',
           '845c50c9e2ce611c773422ae9db7097fc3e5fba5',
           'e7ee418fa7a519225203fef23481c5fa35834dc3',
           'a3097b5bd172e76dd3524eb5dbe18b6b4c22df50',
           '2250ddfaff92abaff20a5bcd78315f5d4bd44981',
           '8a5f2917e163e09e08af880819fdf44144b1a5fe',
           '05780a760400e42ce1b00200dd8204ae4f94044a',
           'be7bfe6ab7ae2cba056f61dea6c3b0226bf80082',
           '74f6579941fbe71cf7c033f53977047ac872e469',
           '9e7cb7c102655d0ba92d2561c178da9254d5cef5',
           '37659d47a685ecc5f5117aa56526ece0106c6d0f',
           '821aa25c9039e72da9a7b236cf2f9e7d549cbb7b',
           'ea1d8fadb95fbc7cafe036274006228400817fd4',
           '7017599821e02ba95282848c12f7d3b5f2ce670a',
           'dafec63f2e138d0451dae5b37edea2e83f9adc8a',
           '16684f2affaf901b42a12e50f9c29e7c034ad7ea',
           '8dd9fabd2ad9104e747084437b9ad436d5be087a',
           '8cd8ed3657e52ad9f67e17b7f5c20f7340ab6a2c',
           'fcf7258c19b0a6a712f33fb0bcefdae426be7e7f',
           'f7e2b74f1bcc1d1cbebbc42481e33f0abb2843dc',
           'e1ca66bae38b8026079dfcbe0edad5f278546608',
           'd0c84ce57d23a409169daf7232ec7681e42363fe',
           '1996b17599731b889895b0e1edf758588c068fbb',
           '948f95756c79543bb089a94a85e73011a3730b2d',
           '64336ff8414f8977ff94adb9a5bc000a3a4ef454',
           'a5daff22e6e37af4946c614f85b110905e063be3',
           '0c50950f2a7e32887eff6be5979f09772091e1de',
           '839e7f1416148caff518a5b75327a2480a2bbbb4',
           '9a211aae9f710db23c9113aea0251e2758904755',
           '47922d3b00edfc264f73b1484589734bbd077c11',
           'daef69c1366e31c3c49aea6f2e55f577d0c832fd',
           'bd6b395a1e8fb7d099fa17a0e24f8fe3b628822c',
           'd09f20e29bdfa82f5efc071986e2633001d552f6',
           '339edcdb7ecc6edc6fde1b7d1413dbb746d2bcca',
           'e83a6bddac8c89b144dfe0783594dd332c5b3030',
           '29edd119d31a9ee7d4f89e8c1dc8af96f0c19dce',
           'f792d8c50ee456aa8aa2ae406d8e6b8843f45614',
           '586bcb16023ae870b0ad7769f6d9077903705486',
           'feaa5033b7810f7775fd4806c27b2f9f1e9b5051',
           'cb9a1c7d0319c34a97247973ca96af53ead8033a',
           '613df15047887957f5964d2a6ce59ea20b0c4c91',
           'c99dfea33612f44e97c2365f78c0ca6d5754a1bc',
           '6d67cf9f02dd22cc870fd407f569197512700203',
           '6f690b088190581552e04c53288819472fdb2dbe',
           '09e4b780f09c5aa72bb2a6ae2832612f81dc047f',
           'b8043724c48890e86fda0265ad5b6ac3d31f1940']

    bugs_reports = readTitle('BugReports.xlsx', 'BugsInPy')
    data = set()
    for report in bugs_reports:
        for index in range(0, len(sha)):
            r = map(lambda i: sha[index] in i, list(report))
            try:
                list(r).index(True)
                # print(report)
                data.add(report)
            except:
                pass
    return data


if __name__ == '__main__':
    rankTitle()
