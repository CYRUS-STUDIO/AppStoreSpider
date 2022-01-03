import jieba
import collections
import re
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import pandas as pd


# 去除分词结果中的无用词汇
def deal_txt(seg_list_exact):
    result_list = []

    with open('stop_words.txt', encoding='utf-8') as f:

        con = f.readlines()
        stop_words = set()

        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)

        for word in seg_list_exact:
            # 设置停用词并去除单个词
            if word not in stop_words and len(word) > 1:
                result_list.append(word)
        return result_list


# 渲染词云
def render_cloud(word_counts_top100, path):
    word1 = WordCloud(init_opts=opts.InitOpts(width='1350px', height='750px', theme=ThemeType.MACARONS))
    word1.add('词频', data_pair=word_counts_top100, word_size_range=[15, 108], textstyle_opts=opts.TextStyleOpts(font_family='cursive'), shape=SymbolType.DIAMOND)
    word1.set_global_opts(title_opts=opts.TitleOpts('评论云图'), toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical'), tooltip_opts=opts.TooltipOpts(is_show=True, background_color='red', border_color='yellow'))
    # 渲染在html页面上
    word1.render(path)


def word_clound_from_string(data: str, path: str):
    # 文本预处理 去除一些无用的字符  只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
    new_data = " ".join(new_data)
    # jieba分词将整句切成分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    # 去掉无用词汇
    final_list = deal_txt(seg_list_exact)
    # 筛选后统计
    word_counts = collections.Counter(final_list)
    # 获取前100最高频的词
    word_counts_top100 = word_counts.most_common(100)
    # 可以打印出来看看统计的词频
    # print(word_counts_top100)
    # 渲染词云
    render_cloud(word_counts_top100, path)


def word_cloud_form_txt(txt: str, output: str):
    """
    解析txt文件并生成词云
    :param txt: txt文件路径
    :param output: 词云文件输出路径
    """
    # 读取弹幕文件
    with open(txt, encoding='utf-8') as f:
        data = f.read()
        word_clound_from_string(data, output)


def word_cloud_form_excel(excel: str, output: str):
    """
    解析excel文件并生成词云
    :param excel: excel文件路径
    :param output: 词云文件输出路径
    """
    df = pd.read_excel(excel)
    data = '\n'.join(df["评论"])
    word_clound_from_string(data, output)


def word_cloud_form_kuchuan_excel(excel: str, output: str, combined: str = None):
    """
    解析酷传网excel文件并生成词云
    :param excel:   酷传excel文件路径
    :param output:  词云文件输出路径
    :param combined:  酷传各应用商店评论数据汇总的文件输出路径
    """
    xl = pd.ExcelFile(excel)

    df_combined = pd.DataFrame()

    # 将不同应用商店的评论数据合并到一个DataFrame
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)

        # 将列名设置为第一行
        cols = df.ix[0, :]
        df.columns = cols
        # 删除列名
        df.drop(index=df.index[0], axis=0, inplace=True)

        df['来源'] = sheet_name

        df_combined = pd.concat([df_combined, df])
        df_combined = df_combined.append(df)

    if combined:
        df_combined.to_excel(combined, index=False)

    comment = df_combined["内容"].astype(str, copy=False)

    data = '\n'.join(comment)

    word_clound_from_string(data, output)


if __name__ == '__main__':
    # word_cloud_form_excel('../spider/华为应用商店评论.xlsx')
    # word_cloud_form_kuchuan_excel('../spider/潮汐_评论详情_20210101-20211231.xls', '潮汐词云2021.html', '潮汐安卓应用商店评论汇总2021.xlsx')
    # word_cloud_form_kuchuan_excel('../spider/小睡眠_评论详情_20210101-20211231.xls', '小睡眠词云2021.html', '小睡眠安卓应用商店评论汇总2021.xlsx')
    # word_cloud_form_kuchuan_excel('../spider/Now冥想_评论详情_20210101-20211231.xls', 'Now冥想词云2021.html', 'Now冥想安卓应用商店评论汇总2021.xlsx')
