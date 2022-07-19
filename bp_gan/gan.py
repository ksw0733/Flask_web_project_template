from flask import Blueprint, render_template, request, Response
from gan_util import animeGAN

gan_bp = Blueprint('gan_bp', __name__)
menu = {'ho':0, 'pb':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0, 'mp':0, 'gn':1}

@gan_bp.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'GET':
        return render_template('gan/anime.html', menu=menu)
    else:
        pass
