from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for, flash
import os, json, math

pbbs_bp = Blueprint('pbbs_bp', __name__)
menu = {'ho':0, 'pb':1, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0}

@pbbs_bp.route('/list/<int:page>')
def list(page):
    #offset = (page - 1) * 10
    page = 1
    count = 3
    total_page = math.ceil(count / 10)
    start_page = math.floor((page - 1) / 10) * 10 + 1
    end_page = math.ceil(page / 10) * 10
    end_page = total_page if end_page>total_page else end_page

    rows = [
        {'pid':103, 'title':'손그림 색칠 플라스크 구현', 'org':'멀티캠퍼스', 'numAuthor':4, 'term':'2022.06', 'viewCount':3},
        {'pid':102, 'title':'표준협회 타이틀', 'org':'한국표준협회', 'numAuthor':5, 'term':'2022.01', 'viewCount':5},
        {'pid':101, 'title':'리뷰 분석을 통한 호텔 카테고리 재분류', 'org':'한경아카데미', 'numAuthor':4, 'term':'2021.07', 'viewCount':6}
    ]
    return render_template('pbbs/list.html', menu=menu, plist=rows,
                            page_no=page, start_page=start_page, 
                            end_page=end_page, total_page=total_page)

@pbbs_bp.route('/view/<int:pid>')
def view(pid):
    authors = [
        {'name':'제임스', 'email':'james@ckworld.com'},
        {'name':'마리아', 'email':'maria@ckworld.com'}
    ]
    files = ['abc.mp4', '각난닫.pdf']
    title = '손그림 색칠 플라스크 구현'
    desc = '손그림 색칠 플라스크 구현, 손그림 색칠 플라스크 구현'
    term = '2022.06'
    view_count = 3
    course_name = '지능형 빅데이터 서비스 개발 과정(9,10회차)'
    course_org = '멀티캠퍼스'
    hash_tags = ['#인공지능','#GAN','#파이썬','#플라스크','#웹']
    row = {'pid':pid, 'title':title, 'desc':desc, 'term':term, 'vc':view_count,
           'cn':course_name, 'co':course_org, 'ht':hash_tags,
           'authors':authors, 'files':files}
    page = 1
    return render_template('pbbs/view.html', menu=menu, row=row, page=page)

@pbbs_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        page = 1
        return render_template('pbbs/register.html', menu=menu, page=page)
    else:
        title = request.form['title'].strip()
        term = request.form['term'].strip()
        desc = request.form['desc'].strip()
        desc = desc.replace('\n', '<br>')
        ht = request.form['ht'].strip()             # hash tag
        ht_list = [tag.strip() for tag in ht.split(',')]

        name1 = request.form['name1'].strip()
        email1 = request.form['email1'].strip()
        name2 = request.form['name2'].strip()
        email2 = request.form['email2'].strip()
        name3 = request.form['name3'].strip()
        email3 = request.form['email3'].strip()
        info = request.form['info'].strip()
        authors = []
        authors.append({'name':name1, 'email':email1 if email1 else 'unknown'})
        if name2:
            authors.append({'name':name2, 'email':email2 if email2 else 'unknown'})
        if name3:
            authors.append({'name':name3, 'email':email3 if email3 else 'unknown'})
        if info:
            info_list = [item.strip() for item in info.split(',')]
            for i in range(math.ceil(len(info_list)/2)):
                authors.append({'name':info_list[2*i], 'email':info_list[2*i+1] if info_list[2*i+1] else 'unknown'})
        print(authors)

        cn = request.form['cn'].strip()             # course name
        co = request.form['co'].strip()             # course organization
        
        files = []
        upload_path = os.path.join(current_app.root_path, 'static/project_upload')
        f_pdf = request.files['pdf']
        if f_pdf:
            f_pdf.save(f'{upload_path}/{f_pdf.filename}')
            files.append(f_pdf.filename)
        f_mp4 = request.files['mp4']
        if f_mp4:
            f_mp4.save(f'{upload_path}/{f_mp4.filename}')
            files.append(f_mp4.filename)
        file3 = request.files['file3']
        if file3:
            file3.save(f'{upload_path}/{file3.filename}')
            files.append(file3.filename)
        file4 = request.files['file4']
        if file4:
            file4.save(f'{upload_path}/{file4.filename}')
            files.append(file4.filename)
        print(files)
        #return redirect('/')

        vc = 1
        row = {'pid':999, 'title':title, 'desc':desc, 'term':term, 'vc':vc,
                'cn':cn, 'co':co, 'ht':ht_list, 'authors':authors, 'files':files}
        page = 1
        return render_template('pbbs/view.html', menu=menu, row=row, page=page)

@pbbs_bp.route('/update_file', methods=['GET','POST'])
def update_file():
    if request.method == 'GET':
        files = ['각난닫.pdf', 'abc.mp4', 'ckiekim-2021.stl']
        return render_template('pbbs/update_file.html', menu=menu, files=files)
    else:
        pass    