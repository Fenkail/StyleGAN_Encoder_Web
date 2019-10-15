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


def align(args, other_args, path_A, path_B):
    start_ = time.time()

    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """

    landmarks_model_path = unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
                                               LANDMARKS_MODEL_URL, cache_subdir='temp'))
    RAW_IMAGES_DIR = [path_A,path_B]
    ALIGNED_IMAGES_DIR = args.aligned_dir
    os.makedirs(ALIGNED_IMAGES_DIR, exist_ok=True)

    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in list(RAW_IMAGES_DIR):
        print('Aligning %s ...' % img_name)
        try:
            if args.find_faces:
                print('Getting landmarks...')
                landmarks = list(landmarks_detector.get_landmarks(img_name))
                assert len(landmarks)==1
            else:
                landmarks = [[(89, 230), (90, 258), (91, 287), (93, 317), (104, 344), (122, 368), (144, 387), (171, 406),
                     (203, 414), (236, 409), (262, 392), (284, 370), (302, 345), (310, 317), (312, 289), (312, 260),
                     (311, 233), (114, 214), (129, 199), (149, 192), (170, 193), (190, 202), (228, 201), (248, 192),
                     (268, 190), (287, 196), (299, 210), (210, 222), (211, 241), (212, 260), (212, 280), (184, 290),
                     (197, 294), (211, 300), (225, 294), (238, 288), (144, 227), (155, 223), (167, 222), (179, 228),
                     (167, 232), (154, 231), (241, 227), (251, 222), (264, 221), (275, 226), (265, 230), (252, 230),
                     (153, 323), (174, 321), (194, 320), (211, 323), (226, 319), (243, 320), (261, 323), (244, 344),
                     (227, 350), (211, 352), (194, 350), (173, 343), (159, 324), (195, 326), (211, 327), (226, 326),
                     (255, 324), (226, 340), (211, 342), (194, 341)]]
            for i, face_landmarks in enumerate(landmarks, start=1):
                try:
                    face_img_name = '%s.png' % (os.path.basename(os.path.splitext(img_name)[0]))
                    aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)
                    print('Starting face alignment...')
                    image_align(img_name, aligned_face_path, face_landmarks, output_size=args.output_size,
                                x_scale=args.x_scale, y_scale=args.y_scale, em_scale=args.em_scale,
                                alpha=args.use_alpha, find_faces=args.find_faces)
                    print('Wrote result %s' % aligned_face_path)
                except Exception as e:
                    print("Exception in face alignment!",str(e))
        except Exception as e:
            print("Exception in landmark detection!",str(e))

    end_ = time.time()
    logging.info('The time it takes for the face recognition clipping  : %.2f s' % (end_ - start_))
