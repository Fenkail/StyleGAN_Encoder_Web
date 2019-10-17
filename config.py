# -*- coding: utf-8 -*-
import argparse
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
    'server': 'http://10.1.20.91:20200/'
}

os.environ["CUDA_VISIBLE_DEVICES"] = config_retrieval['gpu_list']

result_dir = 'results'
data_dir = 'datasets'
cache_dir = 'cache'
run_dir_ignore = ['results', 'datasets', 'cache']

# experimental - replace Dense layers with TreeConnect
use_treeconnect = False
treeconnect_threshold = 1024

#----------------------------------------------------------------------------
# aligned 设置部分
parser = argparse.ArgumentParser(description='Align faces from input images',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--raw_dir', help='Directory with raw images for face alignment', default='raw_images')
parser.add_argument('--aligned_dir', help='Directory for storing aligned images', default='aligned_images')
parser.add_argument('--output_size', default=1024, help='The dimension of images for input to the model', type=int)
parser.add_argument('--x_scale', default=1, help='Scaling factor for x dimension', type=float)
parser.add_argument('--y_scale', default=1, help='Scaling factor for y dimension', type=float)
parser.add_argument('--em_scale', default=0.1, help='Scaling factor for eye-mouth distance', type=float)
parser.add_argument('--use_alpha', default=False, help='Add an alpha channel for masking', type=bool)
parser.add_argument('--find_faces', default=True, type=bool)

#----------------------------------------------------------------------------
# Style Encoder 部分的设置

# parser = argparse.ArgumentParser(description='Find latent representation of reference images using perceptual losses',
#                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--src_dir', help='Directory with images for encoding', default='aligned_images')
parser.add_argument('--generated_images_dir', help='Directory for storing generated images', default='generated_images')
parser.add_argument('--dlatent_dir', help='Directory for storing dlatent representations',
                    default='latent_representations')
parser.add_argument('--data_dir', default='data', help='Directory for storing optional models')
parser.add_argument('--mask_dir', default='masks', help='Directory for storing optional masks')
parser.add_argument('--load_last', default='', help='Start with embeddings from directory')
parser.add_argument('--dlatent_avg', default='',
                    help='Use dlatent from file specified here for truncation instead of dlatent_avg from Gs')
parser.add_argument('--model_url', default='https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ',
                    help='Fetch a StyleGAN model to train on from this URL')  # karras2019stylegan-ffhq-1024x1024.pkl
parser.add_argument('--model_res', default=1024, help='The dimension of images in the StyleGAN model', type=int)
parser.add_argument('--batch_size', default=1, help='Batch size for generator and perceptual model', type=int)

# Perceptual model params
parser.add_argument('--image_size', default=256, help='Size of images for perceptual model', type=int)
parser.add_argument('--resnet_image_size', default=256, help='Size of images for the Resnet model', type=int)
parser.add_argument('--lr', default=0.02, help='Learning rate for perceptual model', type=float)
parser.add_argument('--decay_rate', default=0.9, help='Decay rate for learning rate', type=float)
parser.add_argument('--iterations', default=100, help='Number of optimization steps for each batch', type=int)
parser.add_argument('--decay_steps', default=10,
                    help='Decay steps for learning rate decay (as a percent of iterations)', type=float)
parser.add_argument('--load_effnet', default='data/finetuned_effnet.h5',
                    help='Model to load for EfficientNet approximation of dlatents')
parser.add_argument('--load_resnet', default='data/finetuned_resnet.h5',
                    help='Model to load for ResNet approximation of dlatents')

# Loss function options
parser.add_argument('--use_vgg_loss', default=0.4, help='Use VGG perceptual loss; 0 to disable, > 0 to scale.',
                    type=float)
parser.add_argument('--use_vgg_layer', default=9, help='Pick which VGG layer to use.', type=int)
parser.add_argument('--use_pixel_loss', default=1.5, help='Use logcosh image pixel loss; 0 to disable, > 0 to scale.',
                    type=float)
parser.add_argument('--use_mssim_loss', default=100, help='Use MS-SIM perceptual loss; 0 to disable, > 0 to scale.',
                    type=float)
parser.add_argument('--use_lpips_loss', default=100, help='Use LPIPS perceptual loss; 0 to disable, > 0 to scale.',
                    type=float)
parser.add_argument('--use_l1_penalty', default=1, help='Use L1 penalty on latents; 0 to disable, > 0 to scale.',
                    type=float)

# Generator params
parser.add_argument('--randomize_noise', default=False, help='Add noise to dlatents during optimization', type=bool)
parser.add_argument('--tile_dlatents', default=False, help='Tile dlatents to use a single vector at each scale',
                    type=bool)
parser.add_argument('--clipping_threshold', default=2.0,
                    help='Stochastic clipping of gradient values outside of this threshold', type=float)

# Masking params
parser.add_argument('--load_mask', default=False, help='Load segmentation masks', type=bool)
parser.add_argument('--face_mask', default=False, help='Generate a mask for predicting only the face area', type=bool)
parser.add_argument('--use_grabcut', default=True,
                    help='Use grabcut algorithm on the face mask to better segment the foreground', type=bool)
parser.add_argument('--scale_mask', default=1.5, help='Look over a wider section of foreground for grabcut', type=float)

# Video params
parser.add_argument('--video_dir', default='videos', help='Directory for storing training videos')
parser.add_argument('--output_video', default=False, help='Generate videos of the optimization process', type=bool)
parser.add_argument('--video_codec', default='MJPG', help='FOURCC-supported video codec name')
parser.add_argument('--video_frame_rate', default=24, help='Video frames per second', type=int)
parser.add_argument('--video_size', default=512, help='Video size in pixels', type=int)
parser.add_argument('--video_skip', default=1, help='Only write every n frames (1 = write every frame)', type=int)




