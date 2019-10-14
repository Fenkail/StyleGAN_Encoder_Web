# -*- coding: utf-8 -*-

# 2019.02.18 MXY
# * change import bof to for_html

import os
# import posixpath
from stylegan import setup
# import re

from flask import (current_app, flash, redirect, render_template, request,
                   send_from_directory, url_for, send_file)
from werkzeug.utils import secure_filename

from utils import download

from . import main
# from .. import bof
from .forms import ImgForm
import config
# from for_html import for_html


# for_html_real = for_html()
from .. import for_html_real
import request_for_location


@main.route('/', methods=['GET', 'POST'])
def index():
    # imgform2 = ImgForm2()
    imgform = ImgForm()
    # urlform = URLForm()
#TODO
    # if imgform2.validate_on_submit():
    #     file2 = imgform2.fileimg2.data
    #     filename2 = secure_filename(file2.filename)
    #     filepath2 = os.path.join(current_app.config['UPLOAD_DIR'], filename2)
    #     if not os.path.exists(filepath2):
    #         file2.save(filepath2)
    #     print('filename2_1: {}'.format(filename2))
    if imgform.validate_on_submit():
        # file
        file = imgform.fileimg.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_DIR'], filename)
        if not os.path.exists(filepath):
            file.save(filepath)
        # file2
        file2 = imgform.fileimg2.data
        filename2 = secure_filename(file2.filename)
        filepath2 = os.path.join(current_app.config['UPLOAD_DIR'], filename2)
        if not os.path.exists(filepath2):
            file2.save(filepath2)
        print('filename: {}'.format(filename))
        print('filename2_2: {}'.format(filename2))
        return redirect(url_for('.result', filename=filename, filename2=filename2))
    # elif urlform.validate_on_submit():
    #     url = urlform.txturl.data
    #     filename = secure_filename(url.split('/')[-1])
    #     filepath = os.path.join(current_app.config['UPLOAD_DIR'], filename)
    #     download(url, current_app.config['UPLOAD_DIR'], filename)
    #     if not os.path.exists(filepath):
    #         flash('无法取回指定URL的图片')
    #         return redirect(url_for('.index'))
    #     else:
    #         return redirect(url_for('.result', filename=filename))
    return render_template('index.html')


@main.route('/result', methods=['GET'])
def result():
    filename = request.args.get('filename')
    uri = os.path.join(current_app.config['UPLOAD_DIR'], filename)
    filename2 = request.args.get('filename2')
    uri2 = os.path.join(current_app.config['UPLOAD_DIR'], filename2)
    result_path = 'stylegan/results/'
    setup.mixing_image(path_A= uri, path_B=uri2, result_path =result_path, flag = False)

    name_A = os.path.basename(os.path.splitext(uri)[0])
    name_B = os.path.basename(os.path.splitext(uri2)[0])


    result_url = os.path.join(current_app.config['UPLOAD_DIR'], result_path+name_A + '_' + name_B + '_mixing.png')


    images = for_html_real.match(uri=result_url)
    # from <lng>,<lat> to <lat>,<lng>
    location = images[0]['label']
    location_r = location.split(',')
    location_r = location_r[1] + ',' + location_r[0]
    print(location_r)
    try:
        address = request_for_location.main(location_r)
    except:
        address = None
    print(address)
    print(location)
    return render_template(
        'result.html',
        filename=filename,
        images=images,
        address=address,
        location=location
        # labels=labels,
        # similarity=similarity
    )


@main.route(config.config_retrieval['images_root_dir'] + '<path:uri>')
def download_file(uri):
    # return send_from_directory(current_app.config['BASE_DIR'],
    #                            uri, as_attachment=False)
    return send_from_directory(
        config.config_retrieval['images_root_dir'],
        uri,
        as_attachment=False)
    # print(type(uri))
    # return send_file(uri)
