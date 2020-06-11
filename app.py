from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
import json
import os
from werkzeug.utils import secure_filename
import boto3

app = Flask(__name__)  # app
app.secret_key = '8a96241c5f3a4360ae140ae4482fc76f'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB


@app.route('/')
def home():
    return render_template('urler.html', name='Yifan Ai', codes=session.keys())


@app.route('/short', methods=['GET', 'POST'])
def short():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('/tmp/urls.json'):
            with open('/tmp/urls.json') as uf:
                urls = json.load(uf)
        if request.form['code'] in urls.keys():
            message = 'Link already taken!'
            if 'url' in request.form.keys():
                return render_template('urler.html', url=request.form['url'], code=request.form['code'], message=message, codes=session.keys())
            else:
                return render_template('urler.html', code2=request.form['code'], message2=message, codes=session.keys())
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = secure_filename(f.filename)
            location = '/tmp/' + full_name
            f.save(location)
            s3 = boto3.resource('s3')
            s3.Bucket('urler').upload_file(location, full_name)
            urls[request.form['code']] = {'file': full_name}
        with open('/tmp/urls.json', 'w') as uf:
            json.dump(urls, uf)
            session[request.form['code']] = True
        return render_template('short.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()


@app.route('/<string:code>')
def go(code):
    if os.path.exists('/tmp/urls.json'):
        with open('/tmp/urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():  # key
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                elif 'file' in urls[code].keys():
                    return redirect('https://urler.s3-ap-southeast-2.amazonaws.com/' + urls[code]['file'])
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
