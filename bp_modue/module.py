from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for
import os, random
from datetime import datetime

module_bp = Blueprint('module_bp', __name__)
menu = {'ho':0, 'm1':0, 'm2':0, 'm3':1, 'cf':0, 'cu':0}
title = 'CKEditor 사용 예(표와 이미지)'
content = '''
<table border="1" cellpadding="1" cellspacing="1" style="width:500px">
	<tbody>
		<tr>
			<td><strong>개</strong></td>
			<td><strong>고양이</strong></td>
		</tr>
		<tr>
			<td><img alt="" src="/static/upload/202205111409036563.jpg" style="height:200px; width:300px" /></td>
			<td><img alt="" src="/static/upload/202205111409215825.jpg" style="height:198px; width:300px" /></td>
		</tr>
	</tbody>
</table>
<p></p>'''

@module_bp.route('/sub1')
def sub1():
    return render_template('module/sub1.html', menu=menu)

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