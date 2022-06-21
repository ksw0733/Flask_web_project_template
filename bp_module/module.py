from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for, flash
import os, random
import urllib3, json, base64
from datetime import datetime

module_bp = Blueprint('module_bp', __name__)
menu = {'ho':0, 'pb':0, 'm1':0, 'm2':0, 'm3':1, 'cf':0, 'cu':0, 'ma':0}

title = 'CKEditor 사용 예(표와 이미지)'
content = '''
<table border="1" cellpadding="1" cellspacing="1" style="width:500px">
	<tbody>
		<tr>
			<td><strong>개</strong></td>
			<td><strong>고양이</strong></td>
		</tr>
		<tr>
			<td><img alt="" src="/static/upload/202205111700298986.jpg" style="height:200px; width:300px" /></td>
			<td><img alt="" src="/static/upload/202205111659327849.jpg" style="height:198px; width:300px" /></td>
		</tr>
	</tbody>
</table>
<p></p>'''

@module_bp.route('/recog', methods=['GET', 'POST'])
def recog():
    global recog_text
    if request.method == 'GET':
        return render_template('module/audio.html', menu=menu)
    else:
        file = request.files['audio_blob']
        filename = 'static/img/recog.wav'
        file.save(filename)
        return '0'

@module_bp.route('/recog_res', methods=['POST'])
def recog_res():
        lang_code = request.form['lang']
        with open('static/keys/etriaikey.txt') as kf:
            ai_key = kf.read()
        filename = 'static/img/recog.wav'
        with open(filename, 'rb') as af:
            audio_contents = base64.b64encode(af.read()).decode('utf8')
        request_json = {
            "access_key": ai_key,
            "argument": {
                "language_code": lang_code,
                "audio": audio_contents
            }
        }
        open_api_url = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            open_api_url,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json)
        )
        result = json.loads(str(response.data,"utf-8"))
        #print(result)
        if result["result"] != 0:
            recog_text = f'실패: {result["reason"]}'
        else:
            recog_text = result["return_object"]["recognized"]
        audio_file = os.path.join(current_app.root_path, filename)
        mtime = int(os.stat(audio_file).st_mtime)
        return render_template('module/audio_res.html', menu=menu, text=recog_text, mtime=mtime)

@module_bp.route('/sub2')
def sub2():
    return redirect('/')

@module_bp.route('/read')
def read():
    return render_template('module/read.html', menu=menu, title=title, content=content)

@module_bp.route('/write', methods=['GET', 'POST'])
def write():
    global title, content
    if request.method == 'GET':
        return render_template('module/write.html', menu=menu)
    else:
        title = request.form['title']
        content = request.form['content']
        return redirect('/module/read')

@module_bp.route('/update', methods=['GET', 'POST'])
def update():
    global title, content
    if request.method == 'GET':
        return render_template('module/update.html', menu=menu, title=title, content=content)
    else:
        title = request.form['title']
        content = request.form['content']
        return redirect('/module/read')
    
def gen_rnd_filename():
    filename_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

@module_bp.route('/ckupload', methods=['POST','OPTIONS'])
def ckupload():
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        if not os.path.exists(os.path.join(current_app.root_path, 'static/upload')):
            os.makedirs(os.path.join(current_app.root_path, 'static/upload'))
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        dirname = os.path.dirname(filepath)
        fileobj.save(filepath)
        url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response