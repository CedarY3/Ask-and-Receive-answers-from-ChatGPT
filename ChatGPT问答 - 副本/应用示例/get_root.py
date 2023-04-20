from config import proxies, API_URL, API_KEY, TIMEOUT_SECONDS, MAX_RETRY, LLM_MODEL
import time, re, pickle
from predict import predict_no_ui as ask
fast_debug = False
def cigengeshi(root):
    return f'Please tell me all (and I mean all!) the words with "{root}" as the root. Output your answer in the following format: ["word1", "word2", ..., "wordx"]. Give me as many words as possible, ideally all that you know. To emphasize again, please give me as many words as possible !!!'
def zhaocigen():
    return 'Please tell me all (yes, all!) the English word roots that you know, and output your answer in the following format: ["root1", "root2", ..., "rootx"]. Give me as many English word roots as possible, ideally all that you know. Again, I emphasize, please give me as many English word roots as possible!!!'
def zhaocizhui():
    return 'Please tell me all (yes, all!) the English word roots that you know, and output your answer in the following format: ["root1", "root2", ..., "rootx"]. Give me as many English word roots as possible, ideally all that you know. Again, I emphasize, please give me as many English word roots as possible!!!'


kaoyanci = []
with open("../data/word_kaoyan5542.txt", 'r', encoding='utf-8') as f:
    for line in f:
        kaoyanci.append(line.strip())

words_info = {}
chenggongci = []
shibaici = []
for i in range(0, len(kaoyanci)):
    wd = kaoyanci[i]
    # 获取当前时间
    start_time = time.localtime()

    # print(ask(f'Please tell me what is the prefix, suffix, and root of the word {wd}. Please output your answer in the following format: ["Prefix", "Suffix", "Root"]. If {wd} does not have a prefix, suffix, or root, replace it with "xxxx".The answer should contain only lowercase letters, not "-".'))
    try:
        info = ask(f'Please tell me what is the prefix, suffix, and root of the word {wd}. Please output your answer in the following format: ["Prefix", "Suffix", "Root"]. If {wd} does not have a prefix, suffix, or root, replace it with "xxxx".The answer should contain only lowercase letters, not "-".')
        words_info[wd] = eval(info)
        chenggongci.append(wd)
    except:
        shibaici.append(wd)

    # 获取结束的时间
    end_time = time.localtime()
    # 计算时间间隔
    start_seconds = time.mktime(start_time)
    end_seconds = time.mktime(end_time)
    interval = end_seconds - start_seconds
    if interval < 20:
        interval = 20 - interval
        time.sleep(interval)
    # 打开文件，以二进制写入模式写入数据
    with open('../data/words_info.pickle', 'wb') as f:
        # 使用pickle.dump()函数将列表写入文件
        pickle.dump(words_info, f)
    with open('../data/cgc.pickle', 'wb') as f:
        # 使用pickle.dump()函数将列表写入文件
        pickle.dump(chenggongci, f)
    with open('../data/sbc.pickle', 'wb') as f:
        # 使用pickle.dump()函数将列表写入文件
        pickle.dump(shibaici, f)
    print('===========================================')
    print(f'{i}:  {interval} :  {len(chenggongci)}    {len(shibaici)}')
    print('===========================================')




# print(ask('如何将字符串["con", "ate", "centr"]转化为对应格式的list'))






