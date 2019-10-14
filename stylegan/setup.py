import os
import numpy as np
import sys
sys.path.append('stylegan')
import encode_images_fk as ei
import stylegan.config
import generate_figures_fk as gf
import align_images_fk
from dnnlib import tflib



def mixing_pre():
    args, other_args = config.parser.parse_known_args()
    # 路径设置
    # args.raw_dir = 'raw_images'
    args.raw_dir = 'results_f'
    args.aligned_dir = 'aligned_images_f'
    args.src_dir = 'aligned_images_f'
    args.generated_images_dir = 'generated_images'
    args.dlatent_dir = "latent_representations"

    # 执行图像中人脸的检测与图像的剪裁
    align_images_fk.align(args, other_args)
    #     执行图像的StyleEncoder的编码过程
    ei.styleGAN_encoder(args)



def mixing_image(path_A, path_B, result_path, flag):
    args, other_args = stylegan.config.parser.parse_known_args()
    # 执行图像中人脸的检测与图像的剪裁
    align_images_fk.align(args, other_args, path_A, path_B)
    #     执行图像的StyleEncoder的编码过程
    ei.styleGAN_encoder(args,path_A, path_B)

    gf.style_mixing(path_A, path_B,result_path,flag)




if __name__ == '__main__':

    mixing_image(path_A= './raw_images/wr.jpg', path_B='./raw_images/wx.jpg', result_path ='./results_ff', flag = False)

