from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)  # app
app.secret_key = 'r9qy-T2c1-ieO8-a951-dBVj-kAo8'


@app.route('/')
def home():
    return 'Home!'


@app.route('/urler')
def urler():
    return render_template('urler.html', name='Yifan Ai', codes=session.keys())


@app.route('/short', methods=['GET', 'POST'])
def short():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as uf:
                urls = json.load(uf)
        if request.form['code'] in urls.keys():
            flash('Code already taken')
            return redirect(url_for('urler'))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = secure_filename(f.filename)
            f.save('/Users/ayfallen/urler/static/media/' + full_name)
            urls[request.form['code']] = {'file': full_name}
        with open('urls.json', 'w') as uf:
            json.dump(urls, uf)
            session[request.form['code']] = True
        return render_template('short.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()


@app.route('/<string:code>')
def go(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():  # key
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                elif 'file' in urls[code].keys():
                    return redirect(url_for('static', filename='media/' + urls[code]['file']))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
