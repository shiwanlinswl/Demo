import pandas as pd


def get_question_answer_list():
    """
    读取Excel文件中的问题和答案
    """
    df = pd.read_excel(r"D:\GitHub\Demo\flask_full_search\faq\faq_data.xlsx", usecols=[1, 2],
                       names=None)
    df_list = df.values.tolist()
    print(df_list)
    return df_list


if __name__ == '__main__':
    get_question_answer_list()
