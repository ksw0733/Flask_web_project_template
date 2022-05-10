from flask import Blueprint, render_template, request, redirect

module_bp = Blueprint('module_bp', __name__)
menu = {'ho':0, 'm1':0, 'm2':0, 'm3':1, 'cf':0, 'cu':0}

@module_bp.route('/sub1')
def sub1():
    return render_template('module/sub1.html', menu=menu)

@module_bp.route('/sub2')
def sub2():
    return redirect('/')

@module_bp.route('/sub3')
def sub3():
    return render_template('module/sub3.html', menu=menu)