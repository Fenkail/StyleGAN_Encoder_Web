import os
import argparse
import pickle
from tqdm import tqdm
import PIL.Image
import numpy as np
import dnnlib
import dnnlib.tflib as tflib
import config
from encoder.generator_model import Generator
from encoder.perceptual_model import PerceptualModel, load_images
from keras.models import load_model
import time
import logging

def split_to_batches(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def styleGAN_encoder(path_A, path_B):
    start_ = time.time()
    decay_steps =10
    decay_steps *= 0.01 * 100 # Calculate steps as a percent of total iterations

    src_dir = 'aligned_images'
    name_A = src_dir+'/%s.png' %os.path.basename(os.path.splitext(path_A)[0])
    name_B = src_dir+'/%s.png' %os.path.basename(os.path.splitext(path_B)[0])
    ref_images = [name_A,name_B]
    ref_images = list(filter(os.path.isfile, ref_images))


    os.makedirs('data', exist_ok=True)
    os.makedirs('masks', exist_ok=True)

    # Initialize generator and perceptual model
    tflib.init_tf()
    with dnnlib.util.open_url('https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ', cache_dir='cache') as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)

    generator = Generator(Gs_network, 1, clipping_threshold=2.0, tiled_dlatent=False, model_res=1024, randomize_noise=False)
    print(generator.model_scale)

    perc_model = None
    if (100 > 0.00000001):
        with dnnlib.util.open_url('https://drive.google.com/uc?id=1N2-m9qszOeVC9Tq77WxsLnuWwOedQiD2', cache_dir='cache') as f:
            perc_model =  pickle.load(f)
    perceptual_model = PerceptualModel(perc_model=perc_model, batch_size=1)
    perceptual_model.build_perceptual_model(generator)

    ff_model = None

    # Optimize (only) dlatents by minimizing perceptual loss between reference and generated images in feature space
    for images_batch in tqdm(split_to_batches(ref_images, 1), total=len(ref_images)//1):
        names = [os.path.splitext(os.path.basename(x))[0] for x in images_batch]

        perceptual_model.set_reference_images(images_batch)
        dlatents = None


        if (ff_model is None):
            if os.path.exists('data/finetuned_resnet.h5'):
                print("Loading ResNet Model:")
                ff_model = load_model('data/finetuned_resnet.h5')
                from keras.applications.resnet50 import preprocess_input


        if (ff_model is not None): # predict initial dlatents with ResNet model
            dlatents = ff_model.predict(preprocess_input(load_images(images_batch,image_size=256)))
        if dlatents is not None:
            generator.set_dlatents(dlatents)

        op = perceptual_model.optimize(generator.dlatent_variable, iterations=100)
        pbar = tqdm(op, leave=False, total=100)

        best_loss = None
        best_dlatent = None
        for loss_dict in pbar:
            pbar.set_description(" ".join(names) + ": " + "; ".join(["{} {:.4f}".format(k, v)
                    for k, v in loss_dict.items()]))
            if best_loss is None or loss_dict["loss"] < best_loss:
                best_loss = loss_dict["loss"]
                best_dlatent = generator.get_dlatents()

            generator.stochastic_clip_dlatents()
        print(" ".join(names), " Loss {:.4f}".format(best_loss))

        print(best_dlatent)

        # Generate images from found dlatents and save them
        generator.set_dlatents(best_dlatent)
        generated_images = generator.generate_images()
        generated_dlatents = generator.get_dlatents()
        print(generator.initial_dlatents)



        for img_array, dlatent, img_name in zip(generated_images, generated_dlatents, names):
            np.save(os.path.join('latent_representations', f'{img_name}.npy'), dlatent)

        generator.reset_dlatents()

    end_ = time.time()
    logging.info('The time it takes for the StyleGAN Encoder: %.2fs' % (end_ - start_))

if __name__ == '__main__':
    styleGAN_encoder('22','26')