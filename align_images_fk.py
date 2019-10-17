import os
import bz2
from keras.utils import get_file
from ffhq_dataset.face_alignment import image_align
from ffhq_dataset.landmarks_detector import LandmarksDetector
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )

LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
# 定位人脸并进行截图 python align_images.py raw_images/ aligned_images/

def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, 'wb') as fp:
        fp.write(data)
    return dst_path


def align(path_A, path_B):
    start_ = time.time()

    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """

    landmarks_model_path = unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
                                               LANDMARKS_MODEL_URL, cache_subdir='temp'))
    RAW_IMAGES_DIR = [path_A,path_B]
    ALIGNED_IMAGES_DIR = 'aligned_images'
    os.makedirs(ALIGNED_IMAGES_DIR, exist_ok=True)

    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in list(RAW_IMAGES_DIR):
        print('Aligning %s ...' % img_name)
        try:
            print('Getting landmarks...')
            landmarks = list(landmarks_detector.get_landmarks(img_name))
            assert len(landmarks)==1

            for i, face_landmarks in enumerate(landmarks, start=1):
                try:
                    face_img_name = '%s.png' % (os.path.basename(os.path.splitext(img_name)[0]))
                    aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)
                    print('Starting face alignment...')
                    image_align(img_name, aligned_face_path, face_landmarks, output_size=1024,
                                x_scale=1, y_scale=1, em_scale=0.1,
                                alpha=False, find_faces=True)
                    print('Wrote result %s' % aligned_face_path)
                except Exception as e:
                    print("Exception in face alignment!",str(e))
        except Exception as e:
            print("Exception in landmark detection!",str(e))

    end_ = time.time()
    logging.info('The time it takes for the face recognition clipping  : %.2f s' % (end_ - start_))
