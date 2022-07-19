from flask import Blueprint, render_template, request, current_app
from my_utils.gan_util import animeGAN
import os

gan_bp = Blueprint('gan_bp', __name__)
menu = {'ho':0, 'pb':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0, 'mp':0, 'gn':1}

@gan_bp.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'GET':
        return render_template('gan/anime.html', menu=menu)
    else:
        version = request.form['version']
        f_src = request.files['face']
        file_src = os.path.join(current_app.root_path, 'static/upload/') + f_src.filename
        f_src.save(file_src)
        return render_template('gan/spinner.html', menu=menu, 
                                src=f_src.filename, version=version)

@gan_bp.route('/anime_res', methods=['POST'])
def anime_res():
    version = request.form['version']
    src = request.form['src']
    animeGAN(src, os.path.join(current_app.root_path, 'static/upload/'), version)

    file_dst = os.path.join(current_app.root_path, 'static/upload/') + "animated_image.jpg"
    mtime = int(os.stat(file_dst).st_mtime)
    return render_template('gan/anime_res.html', menu=menu, src=src,
                            version=version, mtime=mtime)
