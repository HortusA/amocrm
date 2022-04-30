import sqlite3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, validators
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from openpyxl import *
from flask_bootstrap import Bootstrap


path_to_base = '/home/alex/Документы/amocrm/app.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'
bootstrap = Bootstrap(app)


class UploadFileForm(FlaskForm):
    file = FileField("file")
    start = DateField("start", format='%Y-%m-%d', validators=(validators.Optional(),))
    end = DateField("end", format='%Y-%m-%d', validators=(validators.Optional(),))
    submit = SubmitField("Загрузка файла")


@app.route('/', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        start_data = form.start.data
        end_data = form.end.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        d = EmailList(file_path)
        res = d.list_pyxl(start_data,end_data)

        return render_template('index.html', form=form, data=res)
    return render_template('index.html', form=form)


class EmailList:
    def __init__(self, file_path):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.file_path = file_path

    def list_pyxl(self, data_start, data_end):
        self.data_start = data_start
        self.data_end = data_end
        new_xls_email_list = []
        wb = load_workbook(self.file_path)
        for sheet in wb.worksheets:
            if sheet.sheet_state == 'visible':
                column = sheet["A"]
                for one_email in range(len(column)):
                    data_email = str(column[one_email].value)
                    if '@' in data_email:
                        new_xls_email_list.append(data_email)
        print(self.data_end)
        sql = "','".join(new_xls_email_list)
        self.cursor.execute(f"""SELECT
                                    username, sum(amount) as sum
                                    FROM f_lk_payments
                                    WHERE username in ('{sql}')
                                    and time > ('{self.data_start}') and time < ('{self.data_end}')
                                    group by username
                                    """)
        res = self.cursor.fetchall()
        return res











app.run()