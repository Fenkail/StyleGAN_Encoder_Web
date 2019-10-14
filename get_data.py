# -*- coding: utf-8 -*-
# create a csv file for image_path and label

# 2019.02.17  MXY
# + get_image_label_dict
# + create_csv


import os
import glob
import pandas as pd
import argparse
import cv2


# from a root dir to get a images and labels dict
# input:
#   root_dir: images' root dir
#       root_dir/sub_dir(must be number and the number is label)/image.jpg
#       one image_path only have one label
# output:
#   image_label_dict
def get_image_label_dict(root_dir):
    # init image_label_dict
    image_label_dict = {}
    # get path_list
    path_list = [x[0] for x in os.walk(root_dir)]
    is_root_dir = True
    for sub_dirs in path_list:
        if is_root_dir:
            is_root_dir = False
            # continue will jump out to next
            continue

        # extension_name lists the figures types
        extension_name = ['jpg', 'jpeg', 'JPG', 'JPEG']
        # create a list to save fig name
        images_list = []
        for extension in extension_name:
            # join() use to contact dir and extension_name
            file_glob = os.path.join(sub_dirs, '*.' + extension)
            # use glob() to get the file name of figures
            images_list.extend(glob.glob(file_glob))

        # basename() will get the last dir name
        # like a dir as A/B/C, dir_name is C
        dir_name = os.path.basename(sub_dirs)
        # the dir_name is landmark_ID
        landmark_ID = dir_name
        # print(images_list)
        # print(landmark_ID)
        for image_path in images_list:
            image_label_dict[image_path] = landmark_ID
        print("sub dir: " + sub_dirs + ", images <----> labels have got!")
    return image_label_dict
    # pass


# create the csv with images and labels
# input:
#   root_dir
#   csv_path
# output:
#   a csv file
def create_csv(root_dir, csv_path):
    # if the csv exists no need to do so
    if os.path.exists(csv_path):
        print("images labels csv file exists!")
        return 0
    else:
        print("images labels csv file not exists!")
    image_label_dict = get_image_label_dict(root_dir)
    # get two lists
    image_list = list(image_label_dict.keys())
    # test whether images can be loaded
    for i in image_list:
        try:
            im = cv2.imread(i)
        except:
            image_list.remove(i)
            print(i + " can not be loaded!")
    label_list = [image_label_dict[image_path] for image_path in image_list]
    image_label_list_dict = {"image_list": image_list, "label_list": label_list}
    # to DataFrame
    data_frame = pd.DataFrame(image_label_list_dict)
    data_frame.to_csv(csv_path, columns=None, header=False, index=False,)
    print("images labels csv file created!")
    # pass


# if no special, default args for get_data
def get_data_parse_args():
    parser = argparse.ArgumentParser(description='Args for get_data')
    parser.add_argument('--root_dir', default='./images/paris/', help='root directory')
    parser.add_argument('--csv_path', default='./image_label.csv', help='the csv with images and labels')
    args = parser.parse_args()
    return args


# if __name__ == '__main__':
def main(root_dir, csv_path):
    # args = get_data_parse_args()
    create_csv(root_dir, csv_path)


if __name__ == '__main__':
    args = get_data_parse_args()
    main(args.root_dir, args.csv_path)

