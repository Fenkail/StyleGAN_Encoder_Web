# -*- coding: utf-8 -*-

import os
# os.environ["CUDA_VISIBLE_DEVICES"] = '-1'


class Config:
    DEBUG = False
    # 路径配置
    BASE_DIR = os.path.dirname(__file__)
    UPLOAD_DIR = os.path.join(BASE_DIR, 'app/static/uploads')
    # 秘钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'it is a secret'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

config_retrieval = {
    'gpu_list': '0',
    'model_kind': "delf",
    'similarity_kind': "cosine",
    # 'images_root_dir': '/home/dengxi/Desktop/MXY/DataSet/paris_single',
    # 'images_root_dir': '/media/dengxi/娱乐/MXY/BaiduStaticViewer/Nanjing_new',
    'images_root_dir': '/media/macxy/Documents/Nanjing_landmark/Nanjing_new',
    'features_npy_path': 'features.npy',
    'image_path_label_csv_path': 'image_label.csv',
    'single_image_path': 'querry.jpg',
    'top_k': 121,
    'server': 'http://0.0.0.0:20200/'
}

os.environ["CUDA_VISIBLE_DEVICES"] = config_retrieval['gpu_list']

