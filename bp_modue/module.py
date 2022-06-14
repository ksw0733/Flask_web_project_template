from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for
import os, random
from datetime import datetime

module_bp = Blueprint('module_bp', __name__)
menu = {'ho':0, 'm1':0, 'm2':0, 'm3':1, 'cf':0, 'cu':0, 'ma':0}
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

@module_bp.route('/sub1', methods=['GET', 'POST'])
def sub1():
    if request.method == 'GET':
        #print('Get /sub1')
        return render_template('module/audio.html', menu=menu)
    else:
        #print('Post /sub1')
        file = request.files['audio_blob']
        filename = 'static/img/file.wav'
        file.save(filename)

        text = '자세한 설명은 카카오 SSML 가이드를 참고하세요.'
        audio_file = os.path.join(current_app.root_path, filename)
        mtime = int(os.stat(audio_file).st_mtime)
        return render_template('module/audio_res.html', menu=menu, text=text, mtime=mtime)

@module_bp.route('/sub1_res')
def sub1_res():
        #print('Get /sub1_res')
        text = '자세한 설명은 카카오 SSML 가이드를 참고하세요.'
        audio_file = os.path.join(current_app.root_path, 'static/img/file.wav')
        mtime = int(os.stat(audio_file).st_mtime)
        return render_template('module/audio_res.html', menu=menu, text=text, mtime=mtime)

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