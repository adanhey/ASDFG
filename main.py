import requests
from lxml import etree
import jieba
import re
import sys, time
import os


def print_one_by_one(text):
    sys.stdout.write("\r " + " " * 60 + "\r")  # /r 光标回到行首
    sys.stdout.flush()  # 把缓冲区全部输出
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.1)
def chuli():
    stop = [line.strip() for line in open('stopwords.txt', encoding='utf-8').readlines()]
    print("小智：您好，请问您需要问什么呢(对话（快，慢），可控制输出速度)")
    input_word = input("我：")
    # 默认为慢速
    print(input_word)
    if input_word == "快":
        f = open("1.txt", "w")
        f.write("0")
        f.close()
    elif input_word == '慢':
        f = open("1.txt", "w")
        f.write("1")
        f.close()

    sd = jieba.cut(input_word, cut_all=False)
    final = ''
    for seg in sd:
        # 去停用词
        print(seg)
        if seg not in stop:
            final += seg
    process = final

    # 匹配问后面全部内容
    pat = re.compile(r'(.*?)问(.*)')
    # 一个“问”时的处理
    try:
        rel = pat.findall(final)
        process = rel[0][1]
    except:
        pass

    # 两个问时的处理
    try:
        rel = pat.findall(final)
        rel0 = rel[0][1]
        print(rel0)
        rel1 = pat.findall(rel0)
        process = rel1[0][1]
    except:
        pass

    print("问题：" + process)
    if process == '':
        print("小智：OK")
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = requests.get("https://baike.baidu.com/search/word?word=" + process, headers=header)

    # 为了防止中文乱码，编码使用原网页编码
    url.raise_for_status()
    url.encoding = url.apparent_encoding

    object = etree.HTML(url.text)
    print(object)
    # 正则匹配搜索出来答案的所有网址
    # 获取词条
    head = object.xpath('/html/head//meta[@name="description"]/@content')
    # 详细内容
    para = object.xpath('/html/body//div[@class="para"]/text()')
    result = '小智：'
    for i in para:
        result += i
    if result == '小智：':
        print("小智：对不起，我不知道")
    else:
        f = open("1.txt", "r")
        s = f.read()
        if s == "1":
            print_one_by_one(result)
        else:
            print(result)
while(True):
    if os.path.exists('1.txt'):
        chuli()
    else:
        f = open("1.txt", "w")
        f.write("1")
        f.close()
        chuli()
