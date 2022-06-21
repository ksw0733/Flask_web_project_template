from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for, flash
import os, json, math
from datetime import datetime

pbbs_bp = Blueprint('pbbs_bp', __name__)
menu = {'ho':0, 'pb':1, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0}

@pbbs_bp.route('/list/<int:page>', methods=['GET'])
def list(page):
    offset = (page - 1) * 10
    count = 3
    total_page = math.ceil(count / 10)
    start_page = math.floor((page - 1) / 10) * 10 + 1
    end_page = math.ceil(page / 10) * 10
    end_page = total_page if end_page>total_page else end_page

    rows = [
        {'pid':103, 'title':'손그림 색칠 플라스크 구현', 'org':'멀티캠퍼스', 'numAuthor':4, 'when':'2022.06', 'viewCount':3},
        {'pid':102, 'title':'표준협회 타이틀', 'org':'한국표준협회', 'numAuthor':5, 'when':'2022.01', 'viewCount':5},
        {'pid':101, 'title':'리뷰 분석을 통한 호텔 카테고리 재분류', 'org':'한경아카데미', 'numAuthor':4, 'when':'2021.07', 'viewCount':6}
    ]
    return render_template('pbbs/list.html', menu=menu, plist=rows,
                            page_no=page, start_page=start_page, 
                            end_page=end_page, total_page=total_page)

@pbbs_bp.route('/view/<int:pid>', methods=['GET'])
def view(pid):
    authors = [
        {'author':'제임스', 'email':'james@ckworld.com'},
        {'author':'마리아', 'email':'maria@ckworld.com'}
    ]
    files = ['abc.mp4', '각난닫.pdf']
    title = '손그림 색칠 플라스크 구현'
    desc = '손그림 색칠 플라스크 구현, 손그림 색칠 플라스크 구현'
    cr_year_month = '2022.06'
    view_count = 3
    course_name = '지능형 빅데이터 서비스 개발(9,10회차)'
    course_org = '멀티캠퍼스'
    hash_tags = ['#인공지능','#GAN','#파이썬','#플라스크','#웹']
    return render_template('pbbs/view.html', menu=menu)