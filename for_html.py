# -*- coding: utf-8 -*-
# get three lists for html: images_url, label, similarity


# 2019.02.18 MXY
# + class for_html
# as the flask needs class, so create the following classes
# + class images_class
# + class labels_class
# + class similarity_class


from config import config_retrieval
import click
import get_data
import os
import re


class for_html(object):
    def __init__(self, args=None):
        self.feature_npy_path, self.image_path_label_csv_path, self.images_root_dir = self.get_config(args)
        print(self.image_path_label_csv_path)
        print(self.feature_npy_path)
        print(self.images_root_dir)
        #
        # if config_retrieval["model_kind"] == 'delf':
        #
        #     self.delf = feature_extractor.DELF()
        # if config_retrieval['model_kind'] == 'ArcFace':
        #     pass

    def init_app(self, app):
        # extract features
        @click.command('extract')
        def extract():
            self.extract()
            # pass

        # now no use, may add later
        @click.command('evaluate')
        def evaluate():
            # queries = []
            # for i in range(0, self.n, 4):
            #     start = time.time()
            #     matches = self.match(self.ukbench[i])
            #     ap = self.ukbench.evaluate(self.ukbench[i], matches)
            #     elapse = time.time() - start
            #     print("Query %s: ap = %4f, %4fs elapsed" %
            #           (self.ukbench[i], ap, elapse))
            #     queries.append((ap, elapse))
            # mAP, mT = np.mean(queries, axis=0)
            # print("mAP of the %d images is %4f, %4fs per query" %
            #       (len(queries), mAP, mT))
            pass
        app.cli.add_command(extract)
        app.cli.add_command(evaluate)

    # change the config param from relative_path to abs_path
    # input:
    #   args: if have then use, not exists use the config_retrieval
    def get_config(self, args):
        systerm_root_dir = os.getcwd()
        if args is None:
            feature_npy_path = config_retrieval['features_npy_path']
            image_path_label_csv_path = config_retrieval['image_path_label_csv_path']
            images_root_dir = config_retrieval['images_root_dir']
            # single_image_path = config_retrieval['single_image_path']
        else:
            feature_npy_path = args.features_npy_path
            image_path_label_csv_path = args.image_path_label_csv_path
            images_root_dir = args.images_root_dir
            # single_image_path = args.single_image_path

        # change to abs root
        feature_npy_path = systerm_root_dir + '/' + feature_npy_path
        image_path_label_csv_path = systerm_root_dir + '/' + image_path_label_csv_path
        images_root_dir = images_root_dir
        # self.single_image_path = systerm_root_dir + '/' + single_image_path
        return feature_npy_path, \
               image_path_label_csv_path, \
               images_root_dir, \
               # single_image_path

    # extract all features
    def extract(self):
        get_data.main(self.images_root_dir, self.image_path_label_csv_path)

        if config_retrieval["model_kind"] == 'delf':
            self.delf.extract_feature_from_imagelabelcsv(
                self.image_path_label_csv_path,
                self.feature_npy_path
            )
        if config_retrieval['model_kind'] == 'ArcFace':
            pass

    # get match for query image
    def match(self, uri, top_k=config_retrieval['top_k']):
        # image_feature = self.delf.extract_feature_singleimage(uri)
        #
        # if config_retrieval['similarity_kind'] == 'cosine':
        #     from similarity import cos_similarity
        #     all_pd = cos_similarity.main(
        #         image_feature,
        #         self.feature_npy_path,
        #         self.image_path_label_csv_path
        #     )
        #
        # if all_pd is None:
        #     return [], [], []
        # top_k_pd = all_pd.iloc[0: top_k]
        # images_list = list(top_k_pd['image_path'])
        # label_list = list(top_k_pd['label'])
        # similarity_list = list(top_k_pd['similarity'])

        # for i in range(0, len(images_list)):
        images_list = []
        images_list.append(config_retrieval['server'] + re.sub(config_retrieval['images_root_dir'], '', uri))
        # images_list.append(config_retrieval['server'] + re.sub(config_retrieval['images_root_dir'], '', './results/22_26_mixing.png'))
        print(images_list)
        # images = images_class(config_retrieval['images_root_dir'], images_list)
        images = []
        for i in range(0, len(images_list)):
            temp_dict = dict()
            temp_dict['url'] = images_list[i]
            # temp_dict['similarity'] = round(similarity_list[i], 4)
            # temp_dict['label'] = label_list[i]
            images.append(temp_dict)
        return images


# class images_class(object):
#     def __init__(self, root_dir, image_list):
#         self.root = root_dir
#         self.uris = image_list
#
#     def __getitem__(self, index):
#         return self.uris[index]
#
#     def __iter__(self):
#         return iter(self.uris)
#
#     def __len__(self):
#         return len(self.uris)

