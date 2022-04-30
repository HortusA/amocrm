import sqlite3
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from openpyxl import *


path_to_base = '/home/alex/Документы/amocrm/app.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    start_d = DateField("start", format='%m/%d/%y')
    finish_d = DateField("end", format='%m/%d/%y')
    submit = SubmitField("Загрузка файла")


@app.route('/', methods=['GET', "POST"])
def home():

    return render_template('index2.html')


@app.route('/upload', methods=['GET', "POST"])
def upload():
    form = UploadFileForm()
    start_data = form.start_d.data
    end_data = form.finish_d.data
    file = request.files['file']
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                             secure_filename(file.filename))
    file.save(file_path)
    d = EmailList(file_path)
    res = d.list_pyxl()
    return render_template('report.html', form=form, data=res)


class EmailList:
    def __init__(self, file_path):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.file_path = file_path

    def list_pyxl(self):
        new_xls_email_list = []
        wb = load_workbook(self.file_path)
        for sheet in wb.worksheets:
            if sheet.sheet_state == 'visible':
                column = sheet["A"]
                for one_email in range(len(column)):
                    data_email = str(column[one_email].value)
                    if '@' in data_email:
                        new_xls_email_list.append(data_email)

        sql = "','".join(new_xls_email_list)
        self.cursor.execute(f"""SELECT
                                    username, sum(amount) as sum
                                    FROM f_lk_payments
                                    WHERE username in ('{sql}')
                                    and time > '2022-02-01 00:00:01' and time < '2022-02-28 23:59:59'
                                    group by username
                                    """)
        res = self.cursor.fetchall()
        return res











app.run()