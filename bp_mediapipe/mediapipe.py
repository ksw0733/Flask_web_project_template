from flask import Blueprint, render_template, request, redirect
from flask import current_app, make_response, url_for, flash

mediapipe_bp = Blueprint('mediapipe_bp', __name__)
menu = {'ho':0, 'pb':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0, 'mp':1}

@mediapipe_bp.route('/hand')
def hand():
    return render_template('mediapipe/hand.html', menu=menu)

@mediapipe_bp.route('/face_detection')
def face_detection():
    return render_template('mediapipe/face_detection.html', menu=menu)

@mediapipe_bp.route('/face_mesh')
def face_mesh():
    return render_template('mediapipe/face_mesh.html', menu=menu)

@mediapipe_bp.route('/pose')
def pose():
    return render_template('mediapipe/pose.html', menu=menu)

@mediapipe_bp.route('/holistic')
def holistic():
    return render_template('mediapipe/holistic.html', menu=menu)

@mediapipe_bp.route('/selfie')
def selfie():
    return render_template('mediapipe/selfie.html', menu=menu)
