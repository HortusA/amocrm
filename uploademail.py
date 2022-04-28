import pandas as pd
import re
import sqlite3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

path_to_base = '/home/alex/Документы/amocrm/app.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Загрузка файла")


@app.route('/', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))
        return "Файл загружен."
    return render_template('index.html', form=form)


class EmailList:
    def __init__(self, sh_name):
        self.data = pd.read_excel(r'nris.xlsx', sheet_name=sh_name)
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()

    @property
    def list_email(self):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        l_email = self.data["E-mail"].tolist()
        list_e = []
        for email in l_email:
            if re.fullmatch(regex, str(email)):
                list_e.append(email)
        return list_e

    def get_test(self):
        self.cursor.execute(f"""SELECT username, sum(amount) as sum
                                FROM f_lk_payments
                                WHERE username in ('ms.vysotckaia@yandex.ru')
                                and time > '2022-02-01 00:00:01' and time < '2022-02-28 23:59:59'
                                group by username
                            """)
        print(self.cursor.fetchall())

    def get_data_email(self):
        sql = "','".join(self.list_email)
        self.cursor.execute(f"""SELECT
                            username, sum(amount) as sum
                            FROM f_lk_payments
                            WHERE username in ('{sql}')
                            and time > '2022-02-01 00:00:01' and time < '2022-02-28 23:59:59'
                            group by username
                            """)
        res = self.cursor.fetchall()
        print(f"result is {res}")


fl = EmailList('Физ.лица')
fl.get_data_email()
fl.get_test()

app.run()