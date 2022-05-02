import sqlite3
from flask import Flask, render_template
from elasticsearch import Elasticsearch
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

es = Elasticsearch('http://192.168.0.111:9200')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_COOKIE_SECURE'] = False
bootstrap = Bootstrap(app)

path_to_base = '/home/alex/Документы/amocrm/app.db'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()
list_body = []


class ElasticAddForm(FlaskForm):
    id_doc = StringField("id", validators=[DataRequired()])
    elastic_search = StringField("elastic_search", validators=[DataRequired()])
    submit = SubmitField("ок")


class ElasticSearchForm(FlaskForm):
    elastic_search = StringField("elastik_search", validators=[DataRequired()])
    submit = SubmitField("ok")


@app.route('/', methods=['GET', "POST"])
def elastic():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        resp = search_text(field_form)
        return render_template('elastic.html', form=form, search_result=resp.body['hits']['hits'])
    return render_template('elastic.html', form=form)


@app.route('/add_id', methods=['GET', "POST"])
def add_id():
    form = ElasticAddForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        id_d = form.id_doc.data
        resp = add_id_es(id_d, field_form)
        return render_template('add_id.html', form=form, search_result=resp)
    return render_template('add_id.html', form=form)


@app.route('/get_id', methods=['GET', "POST"])
def get_id():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        resp = get_id_one(field_form)
        return render_template('search_id.html', form=form, search_result=resp)
    return render_template('search_id.html', form=form)

@app.route('/del_id', methods=['GET', "POST"])
def del_id():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        resp = del_id_one(field_form)
        return render_template('delete_id.html', form=form, search_result=resp)
    return render_template('delete_id.html', form=form)


def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


def execute_all():
    cursor.execute("SELECT article_id, content FROM cms_article_content")
    return cursor.fetchall()


def create_index_es():
    for cont in execute_all():
        es.index(index='my_index', id=cont[0], document={'text': (cont[1])})


def search_text(text):
    resp = es.search(index="my_index", body={'query': {'match': {'text': text}}})
    print(resp)
    return resp


def add_id_es(id_dic, text):
    resp = es.index(index="my_index", id=id_dic, document={'text': text})
    return resp


def get_id_one(id_d):
    resp = es.get(index="my_index", id=id_d)
    return resp


def del_id_one(id_d):
    resp = es.delete(index="my_index", id=id_d)
    return resp

app.run()
