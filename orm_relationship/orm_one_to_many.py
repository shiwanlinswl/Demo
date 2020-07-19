from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 设置连接数据
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:shi930718@93.179.119.153:3306/author_book'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 实例化SQLAlchemy对象
db = SQLAlchemy(app)


# 定义模型类-作者
class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author:%s' % self.name


# 定义模型类-书名
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    au_book = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return 'Book:%s,%s' % (self.id, self.name)


# db.create_all()
# print("创建数据库成功")


if __name__ == '__main__':
    app.run()
