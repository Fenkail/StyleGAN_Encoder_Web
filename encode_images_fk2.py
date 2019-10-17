import os
import argparse
import pickle
from tqdm import tqdm
import PIL.Image
import numpy as np
import dnnlib
import dnnlib.tflib as tflib
import config
from encoder_old.generator_model import Generator
from encoder_old.perceptual_model import PerceptualModel, load_images
from keras.models import load_model
import time
import logging

def split_to_batches(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def styleGAN_encoder(path_A, path_B):
    args, other_args = config.parser.parse_known_args()
    start_ = time.time()
    args.decay_steps *= 0.01 * args.iterations # Calculate steps as a percent of total iterations

    src_dir = args.src_dir
    name_A = src_dir+'/%s.png' %os.path.basename(os.path.splitext(path_A)[0])
    name_B = src_dir+'/%s.png' %os.path.basename(os.path.splitext(path_B)[0])
    ref_images = [name_A,name_B]
    ref_images = list(filter(os.path.isfile, ref_images))


    os.makedirs(args.data_dir, exist_ok=True)
    os.makedirs(args.dlatent_dir, exist_ok=True)

    # Initialize generator and perceptual model
    tflib.init_tf()
    with dnnlib.util.open_url(args.model_url, cache_dir=config.cache_dir) as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)

    generator = Generator(Gs_network, args.batch_size, clipping_threshold=args.clipping_threshold, tiled_dlatent=args.tile_dlatents, model_res=args.model_res, randomize_noise=args.randomize_noise)

    perc_model = None
    if (args.use_lpips_loss > 0.00000001):
        with dnnlib.util.open_url('https://drive.google.com/uc?id=1N2-m9qszOeVC9Tq77WxsLnuWwOedQiD2', cache_dir=config.cache_dir) as f:
            perc_model =  pickle.load(f)
    perceptual_model = PerceptualModel(args, perc_model=perc_model, batch_size=args.batch_size)
    perceptual_model.build_perceptual_model(generator)

    ff_model = None

    # Optimize (only) dlatents by minimizing perceptual loss between reference and generated images in feature space
    for images_batch in tqdm(split_to_batches(ref_images, args.batch_size), total=len(ref_images)//args.batch_size):
        names = [os.path.splitext(os.path.basename(x))[0] for x in images_batch]

        perceptual_model.set_reference_images(images_batch)
        dlatents = None
        if (args.load_last != ''): # load previous dlatents for initialization
            for name in names:
                dl = np.expand_dims(np.load(os.path.join(args.load_last, f'{name}.npy')),axis=0)
                if (dlatents is None):
                    dlatents = dl
                else:
                    dlatents = np.vstack((dlatents,dl))
        else:
            if (ff_model is None):
                if os.path.exists(args.load_resnet):
                    print("Loading ResNet Model:")
                    ff_model = load_model(args.load_resnet)
                    from keras.applications.resnet50 import preprocess_input
            if (ff_model is None):
                if os.path.exists(args.load_effnet):
                    import efficientnet
                    print("Loading EfficientNet Model:")
                    ff_model = load_model(args.load_effnet)
                    from efficientnet import preprocess_input
            if (ff_model is not None): # predict initial dlatents with ResNet model
                dlatents = ff_model.predict(preprocess_input(load_images(images_batch,image_size=args.resnet_image_size)))
        if dlatents is not None:
            generator.set_dlatents(dlatents)
        op = perceptual_model.optimize(generator.dlatent_variable, iterations=args.iterations)
        pbar = tqdm(op, leave=False, total=args.iterations)

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



        # Generate images from found dlatents and save them
        generator.set_dlatents(best_dlatent)
        generated_images = generator.generate_images()
        generated_dlatents = generator.get_dlatents()
        for img_array, dlatent, img_name in zip(generated_images, generated_dlatents, names):
            np.save(os.path.join(args.dlatent_dir, f'{img_name}.npy'), dlatent)

        generator.reset_dlatents()
    end_ = time.time()
    logging.info('The time it takes for the StyleGAN Encoder: %.2fs' % (end_ - start_))

if __name__ == '__main__':
    styleGAN_encoder('22','26')