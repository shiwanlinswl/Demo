from flask import Flask, current_app, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
from jieba.analyse import ChineseAnalyzer
from faq.read_data import get_question_answer_list

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:xxx@93.179.119.153:3306/Demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["QLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 配置索引名称
app.config['MSEARCH_INDEX_NAME'] = "msearch"
# 配置主键
app.config['MSEARCH_PRIMARY_KEY'] = "id"
# 配置mSearch后端为whoosh
app.config['MSEARCH_BACKEND'] = "whoosh"
# 配置自动更新索引
app.config['MSEARCH_ENABLE'] = True

db = SQLAlchemy(app)
search = Search(db=db, analyzer=ChineseAnalyzer())
search.init_app(app)


class Faq(db.Model):
    """
    FAQ模型
    """
    __tablename__ = 'faq'
    __searchable__ = ['question']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.Text)

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "question": self.question,
            "answer": self.answer
        }
        return resp_dict

    def __repr__(self):
        return '<Faq:{}>'.format(self.id)


search.create_index(Faq)


# db.create_all()
# print("创建faq表格成功")

@app.route("/insertFaq")
def insert_faq():
    """
    插入FAQ数据
    :return:
    """
    qa_list = get_question_answer_list()
    faq_list = []
    for qa in qa_list:
        qa_obj = Faq(question=qa[0], answer=qa[1])
        faq_list.append(qa_obj)
    try:
        db.session.add_all(faq_list)
        db.session.commit()
    except Exception as e:
        current_app.logger(e)
        db.session.rollback()
        return jsonify(status="failure", data=None, errmsg="操作数据库异常")
    return jsonify(status="success", data=None, errmsg="插入数据成功")


@app.route("/queryFaq")
def query_faq():
    """
    查看FAQ数据
    :return:
    """
    faq_list = Faq.query.all()
    faq_dict_list = []
    for faq in faq_list if faq_list else []:
        faq_dict_list.append(faq.to_dict())
    return jsonify(status="success", data=faq_dict_list, errmsg="查询数据成功")


@app.route("/search", methods=["post"])
def full_text_search():
    """
    全文搜索接口
    :return:
    """
    keyword = request.json.get('keyword')
    result_dict_list = []
    results = Faq.query.msearch(keyword, fields=['question'], limit=3).all()
    for r in results:
        result_dict_list.append(r.to_dict())
    return jsonify(status="success", search_keyword=keyword, data=result_dict_list, errmsg="全文搜索成功数据成功")


if __name__ == '__main__':
    app.run(port="5001")
