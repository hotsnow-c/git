
# 示例代码：获取一部分中文繁体字
# 这里只是示例，实际需要完整的繁体字列表可以从更广泛的资源中获取
import random


def 生成繁体游戏名():
    # Unicode 中文繁体字范围
    start = int('4E00', 16)  # 起始字符的Unicode码点
    end = int('9FFF', 16)  # 结束字符的Unicode码点

    # 生成繁体字列表
    chinese_characters = [chr(i) for i in range(start, end + 1)]

    # 生成100个随机网名
    random_names = []
    for _ in range(100):
        name_length = random.randint(2, 3)  # 随机确定网名长度为3到6个字
        name = ''.join(random.sample(chinese_characters, name_length))  # 随机选择指定长度的繁体字
        random_names.append(name)

    # 写入文件
    with open('random_names.txt', 'w', encoding='utf-8') as f:
        for name in random_names:
            f.write(name + '\n')


生成繁体游戏名()