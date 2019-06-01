from flask import Flask, request, flash, redirect, render_template, url_for
import requests
import re

app = Flask(__name__)
app.secret_key = '$#^%^&*(IOPUGHJHFXHGHJGK'

ALLOWED_EXTENSIONS = ['txt']


def check_card(text_with_numbers):
    regex_pattern = re.compile(pattern=r'\d{16}')
    card_numbers = regex_pattern.findall(string=text_with_numbers)
    result_list = []
    for card_number in card_numbers:
        response = requests.post('https://psm7.com/bin/worker.php', data={'bin-input': card_number[:6]})
        issuer = response.json().get('issuer')
        result_list.append((card_number, issuer,))
    return result_list


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template(template_name_or_list='form.html')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
        else:
            return redirect(url_for('upload_file'))
        if file.filename != '' and file and allowed_file(file.filename):
            text = file.read()
            data = check_card(text_with_numbers=str(text))
            return render_template(template_name_or_list='result.html', data=data)
        else:
            return redirect(url_for('upload_file'))

    else:
        return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run()
