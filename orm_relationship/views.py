from flask import jsonify

from Demo.orm_relationship.orm_one_to_many import app, Author


@app.route("/authors")
def query_author():
    """
    查看作者
    :return:
    """
    authors = Author.query.all()
    data = {
        "ahthors": [author.name for author in authors]
    }

    return jsonify(data=data, msg="查看作者", status_code=200)
