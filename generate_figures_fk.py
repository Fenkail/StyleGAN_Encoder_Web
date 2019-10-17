# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for reproducing the figures of the StyleGAN paper using pre-trained generators."""
import logging
import os
import pickle
import time

import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config

#----------------------------------------------------------------------------
# Helpers for loading and using pre-trained generators.

url_ffhq        = 'https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ' # karras2019stylegan-ffhq-1024x1024.pkl
url_celebahq    = 'https://drive.google.com/uc?id=1MGqJl28pN4t7SAtSrPdSRJSQJqahkzUf' # karras2019stylegan-celebahq-1024x1024.pkl
url_bedrooms    = 'https://drive.google.com/uc?id=1MOSKeGF0FJcivpBI7s63V9YHloUTORiF' # karras2019stylegan-bedrooms-256x256.pkl
url_cars        = 'https://drive.google.com/uc?id=1MJ6iCfNtMIRicihwRorsM3b7mmtmK9c3' # karras2019stylegan-cars-512x384.pkl
url_cats        = 'https://drive.google.com/uc?id=1MQywl0FNt6lHu8E_EUqnRbviagS7fbiJ' # karras2019stylegan-cats-256x256.pkl

synthesis_kwargs = dict(output_transform=dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True), minibatch_size=8)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )
_Gs_cache = dict()

def load_Gs(url):
    if url not in _Gs_cache:
        with dnnlib.util.open_url(url, cache_dir=config.cache_dir) as f:
            _G, _D, Gs = pickle.load(f)
        _Gs_cache[url] = Gs
    return _Gs_cache[url]

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Figure 3: Style mixing.

def draw_style_mixing_figure(png, Gs, w, h, src_dlatents, dst_dlatents, style_ranges, flag, start_):

    print('generating.....   '+png)

    src_images = Gs.components.synthesis.run(src_dlatents, randomize_noise=False, **synthesis_kwargs)
    dst_images = Gs.components.synthesis.run(dst_dlatents, randomize_noise=False, **synthesis_kwargs)
    src_seeds = [1]
    dst_seeds = [1]
    canvas = PIL.Image.new('RGB', (w * (len(src_seeds) + 1), h * (len(dst_seeds) + 1)), 'white')
    for col, src_image in enumerate(list(src_images)):
        canvas.paste(PIL.Image.fromarray(src_image, 'RGB'), ((col + 1) * w, 0))
    for row, dst_image in enumerate(list(dst_images)):
        canvas.paste(PIL.Image.fromarray(dst_image, 'RGB'), (0, (row + 1) * h))
        row_dlatents = np.stack([dst_dlatents[row]] * len(src_seeds))
        row_dlatents[:, style_ranges[row]] = src_dlatents[:, style_ranges[row]]
        row_images = Gs.components.synthesis.run(row_dlatents, randomize_noise=False, **synthesis_kwargs)
        for col, image in enumerate(list(row_images)):
            canvas.paste(PIL.Image.fromarray(image, 'RGB'), ((col + 1) * w, (row + 1) * h))


    if flag == True:
        print('generating the result and the source images.....')
        canvas.save(png)
    else:
        print('putting out only result.....')
        canvas_single = canvas.crop((1024, 1024, 2048, 2048))
        canvas_single.save(png)

    end_ = time.time()
    logging.info('The time it takes for generating the result: %.2f s' % (end_ - start_))


#----------------------------------------------------------------------------
# Main program.

def style_mixing(path_A, path_B, result_path, flag):
    start_ = time.time()
    tflib.init_tf()
    os.makedirs(result_path, exist_ok=True)
    name_A = os.path.basename(os.path.splitext(path_A)[0])
    name_B = os.path.basename(os.path.splitext(path_B)[0])


    src_dlatents = np.load('latent_representations/'+name_A+'.npy').reshape(1, 18, 512)  # [seed, layer, component]
    dst_dlatents = np.load('latent_representations/'+name_B+'.npy').reshape(1, 18, 512)  # [seed, layer, component]


    draw_style_mixing_figure((os.path.join(result_path, name_A+'_'+name_B+'_mixing.png')), load_Gs(url_ffhq), w=1024,
                             h=1024, src_dlatents = src_dlatents, dst_dlatents = dst_dlatents,
                             style_ranges=[range(0, 4)] * 3 + [range(4, 8)] * 2 + [range(8, 18)], flag = flag , start_=start_)


#----------------------------------------------------------------------------
