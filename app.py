from flask import Flask, render_template, request, redirect
from flask import current_app
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from bp_module.module import module_bp
from bp_pbbs.pbbs import pbbs_bp
from my_utils.sendmail import sendmail
from datetime import datetime
import os, joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.register_blueprint(module_bp, url_prefix='/module')
app.register_blueprint(pbbs_bp, url_prefix='/pbbs')

@app.route('/')
def index():
    menu = {'ho':1, 'pb':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0}
    return render_template('index.html', menu=menu)

@app.route('/menu1', methods=['GET', 'POST'])
def menu1():
    menu = {'ho':0, 'm1':1, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':0}
    if request.method == 'GET':
        options = [
            {'disp':'영어', 'val':'en'},
            {'disp':'일어', 'val':'jp'},
            {'disp':'중국어', 'val':'cn'},
            {'disp':'프랑스어', 'val':'fr'},
            {'disp':'스페인어', 'val':'es'}
        ]
        return render_template('menu1.html', menu=menu, options=options)
    else:
        text = request.form['text']
        review = request.form['review'].replace('\n','<br>')
        lang = request.form['lang']
        return render_template('menu1_res.html', menu=menu,
                               text=text, review=review, lang=lang)

@app.route('/menu2')
def menu2():
    menu = {'ho':0, 'm1':0, 'm2':1, 'm3':0, 'cf':0, 'cu':0, 'ma':0}
    items = [
        {'id':1001, 'title':'HTML', 'content':'HTML is HyperText ...'},
        {'id':1002, 'title':'CSS', 'content':'CSS is Cascading ...'},
        {'id':1003, 'title':'JS', 'content':'JS is Javascript ...'},
    ]
    cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 
             'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
             'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
    now = datetime.now()
    np.random.seed(now.microsecond)
    X = np.random.rand(100)
    Y = np.random.rand(100)
    plt.figure()
    plt.scatter(X, Y, c=X+Y, cmap=cmaps[np.random.randint(0,len(cmaps))])
    if not os.path.exists(os.path.join(current_app.root_path, 'static/img')):
        os.makedirs(os.path.join(current_app.root_path, 'static/img'))
    img_file = os.path.join(current_app.root_path, 'static/img/menu2.png')
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)

    return render_template('menu2.html', menu=menu, mtime=mtime,
                            now=now.strftime('%Y-%m-%d %H:%M:%S.%f'), items=items)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    menu = {'ho':0, 'm1':0, 'm2':0, 'm3':0, 'cf':1, 'cu':0, 'ma':0}
    if request.method == 'GET':
        return render_template('classify.html', menu=menu)
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/titanic_test.csv')
        scaler = joblib.load('static/model/titanic_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, 0]
        lrc = joblib.load('static/model/titanic_lr.pkl')
        svc = joblib.load('static/model/titanic_sv.pkl')
        rfc = joblib.load('static/model/titanic_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}

        tmp = df.iloc[index, 1:].values
        value_list = []
        int_index_list = [0, 1, 3, 4, 6, 7]
        for i in range(8):
            if i in int_index_list:
                value_list.append(int(tmp[i]))
            else:
                value_list.append(tmp[i])
        org = dict(zip(df.columns[1:], value_list))
        return render_template('classify_res.html', menu=menu, res=result, org=org)

@app.route('/cluster', methods=['GET', 'POST'])
def cluster():
    menu = {'ho':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':1, 'ma':0}
    if request.method == 'GET':
        return render_template('cluster.html', menu=menu)
    else:
        k_number = int(request.form['k_number'])
        option = request.form['option']
        if not os.path.exists(os.path.join(current_app.root_path, 'static/upload')):
            os.makedirs(os.path.join(current_app.root_path, 'static/upload'))
        if option == 'direct':
            f_csv = request.files['csv']
            file_csv = os.path.join(current_app.root_path, 'static/upload/') + f_csv.filename
            f_csv.save(file_csv)
            print(f"{k_number}, {f_csv}, {file_csv}")
        else:
            file_csv = os.path.join(current_app.root_path, 'static/clus_pca_data/') + option + '.csv'
        if not os.path.exists(os.path.join(current_app.root_path, 'static/img')):
            os.makedirs(os.path.join(current_app.root_path, 'static/img'))

        df_csv = pd.read_csv(file_csv)
        # 전처리 - 정규화
        X_scaled = StandardScaler().fit_transform(df_csv.iloc[:, :-1])

        # 차원 축소(PCA)
        pca_array = PCA(n_components=2).fit_transform(X_scaled)
        df = pd.DataFrame(pca_array, columns=['pca_x', 'pca_y'])
        df['target'] = df_csv.iloc[:, -1].values

        # K-Means Clustering
        kmeans = KMeans(n_clusters=k_number, init='k-means++', max_iter=300, random_state=2022)
        kmeans.fit(X_scaled)
        df['cluster'] = kmeans.labels_

        # 시각화
        markers = ['s', 'o', '^', 'P', 'D', 'H', 'x']
        plt.figure()
        for i in df.target.unique():
            marker = markers[i]
            x_axis_data = df[df.target == i]['pca_x']
            y_axis_data = df[df.target == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.title('Original Data', fontsize=15)
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster0.png')
        plt.savefig(img_file)

        plt.figure()
        for i in range(k_number):
            marker = markers[i]
            x_axis_data = df[df.cluster == i]['pca_x']
            y_axis_data = df[df.cluster == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.title(f'{k_number} Clustering Result', fontsize=15)
        img_file = os.path.join(current_app.root_path, 'static/img/cluster1.png')
        plt.savefig(img_file)

        mtime = int(os.stat(img_file).st_mtime)
        return render_template('cluster_res.html', menu=menu, k_number=k_number, mtime=mtime)

@app.route('/mail', methods=['GET', 'POST'])
def mail():
    menu = {'ho':0, 'm1':0, 'm2':0, 'm3':0, 'cf':0, 'cu':0, 'ma':1}
    if request.method == 'GET':
        return render_template('mail.html', menu=menu)
    else:
        subject = request.form['subject']
        addr = request.form['addr']
        content = request.form['content']
        files = request.files.getlist('fields[]')
        for file in files:
            file_up = os.path.join(current_app.root_path, 'static/upload/') + file.filename
            file.save(file_up)
        sendmail(subject, addr, content, files)
        return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', debug=True)
