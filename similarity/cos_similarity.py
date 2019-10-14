# -*- coding: utf-8 -*-
# calculate cosine similarity

# 2019.02.18 MXY
# + load_npy_csv
# + get_cos_similarity

# 2019.02.27 MXY
# * get_cos_similarity: directly use np.dot not use cosine_similarity

import pandas as pd
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
import argparse


# load npy and csv
# input:
#   npy_path
#   csv_path
# output:
#   imagepath_label
#   features_npy
def load_npy_csv(npy_path, csv_path):
    image_path_label_pd = pd.read_csv(csv_path, sep=',', encoding='utf-8', names=['image_path', 'label'])
    features_npy = np.load(npy_path)
    return image_path_label_pd, features_npy


# use sklearn to calculate cos distance
# input:
#   image_feature: [1, feature_size]
#   features_npy: [images_num, feature_size]
#   ipl_pd: image_path_label_pd
# output:
#   all_pd: "image_path", "label", "similarity"
def get_cos_similarity(image_feature, features_npy, ipl_pd):
    # # init similarity_npy
    # similarity_npy = np.zeros((features_npy.shape[0], 1))
    # # get cosine distance
    # for i in range(0, features_npy.shape[0]):
    #     Y = features_npy[i][:].reshape(-1, 1)
    #     similarity_npy[i][0] = cosine_similarity(image_feature, Y.T)
    #     if i % 5000 == 0:
    #         print('Cos match: ' + str(i))
    similarity_npy = np.dot(features_npy, image_feature.T)

    # print(similarity_npy.shape)
    # print(ipl_pd.shape)
    index = list(ipl_pd.index)
    # print(index)
    similarity_pd = pd.DataFrame(similarity_npy, columns=["similarity"], index=index)
    all_pd = pd.concat([ipl_pd, similarity_pd], axis=1)
    # all_pd = pd.concat([ipl_pd, similarity_pd], axis=1).round({'similarity': 4})
    # sort by cosine distance
    all_pd_sort = all_pd.sort_values("similarity", ascending=False)
    return all_pd_sort


def main(image_feature, npy_path, csv_path):
    image_path_label_pd, features_npy = load_npy_csv(npy_path, csv_path)
    all_pd = get_cos_similarity(image_feature, features_npy, image_path_label_pd)
    return all_pd


# if no special, default args for delf_extract_features_from_imagelabelcav
def cos_similarity_parse_args():
    parser = argparse.ArgumentParser(description='Args for delf_extract_features_from_imagelabelcav')
    # parser.add_argument('--root_dir', default='../images/paris/', help='root directory')
    parser.add_argument('--root_dir', default='/home/dengxi/Desktop/MXY/DataSet/paris_single/', help='root directory')
    parser.add_argument(
        '--single_image_path',
        default='/home/macxy/桌面/paris/paris_single/0/paris_defense_000000_0.jpg',
        help='single image_path')
    parser.add_argument('--csv_path', default='../image_label.csv', help='the csv with images and labels')
    parser.add_argument('--npy_path', default='../features.npy', help='the csv with images and labels')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    from vision_delf import feature_extractor
    args = cos_similarity_parse_args()
    # init delf
    delf = feature_extractor.DELF()
    image_feature = delf.extract_feature_singleimage(args.single_image_path)
    all_pd = main(image_feature, args.npy_path, args.csv_path)
    pass
