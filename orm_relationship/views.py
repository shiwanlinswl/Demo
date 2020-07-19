import logging

from flask import jsonify
from flask import request

from Demo.orm_relationship.orm_one_to_many import app, Author, Book, db


@app.route("/authors")
def query_author():
    """
    查看作者
    :return:
    """
    authors = Author.query.all()
    data = {
        "authors": [author.name for author in authors]
    }

    return jsonify(data=data, msg="查看作者", status_code=200)


@app.route("/author_book", methods=["GET", "POST"])
def author_book():
    """
    查看&新增数据
    :return:
    """
    if request.method == "GET":
        authors = Author.query.all()
        data = {
            "ahthors": [author.name for author in authors]
        }
        return jsonify(data=data, msg="查看作者", status_code=200)
    else:
        author = request.json.get("author")
        book = request.json.get("book")
        if not all([book, author]):
            return jsonify(data=None, msg="参数不足", status_code=200)

        # 作者是否存在
        author_obj = Author.query.filter(Author.name == author).first()
        if author_obj:
            author_book = Book.query.filter(Book.au_book == author_obj.id, Book.name == book).first()
            # 图书是否存在
            if author_book:
                return jsonify(data=None, msg="图书已存在", status_code=200)
            else:
                b = Book(name=book, au_book=author_obj.id)
                try:
                    db.session.add(b)
                    db.session.commit()
                except Exception as ex:
                    logging.error(ex)
                    db.rollback()
                    return jsonify(data=None, msg="新增图书异常", status_code=500)
                data = {
                    "book": book,
                    "author": author
                }
                return jsonify(data=data, msg="新增图书成功", status_code=201)
        # 作者不存在，直接新增
        else:
            # 先添加作者
            new_author = Author(name=author.encode('utf-8'))
            new_book = Book(name=book.encode('utf-8'))
            new_book.au_book = new_author.id
            try:
                db.session.add(new_book)
                db.session.commit()
            except Exception as ex:
                logging.error(ex)
                db.session.rollback()
                return jsonify(data=None, msg="新增图书异常", status_code=500)
            data = {
                "book": book,
                "author": author
            }
            return jsonify(data=data, msg="新增图书成功", status_code=201)