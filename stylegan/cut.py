import logging
import os
import queue
import time
import PIL
import random
from PIL import Image
import multiprocessing
from  tqdm import tqdm

path = './results_black/'
path_cut = './results_black_cut/'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a')

def cut_1024(num_a, num_b):
    filename = os.listdir(path)
    filename.sort()
    for ima in tqdm( filename[num_a:num_b] ):
        img = Image.open(path+ima)
        #
        # print(ima)
        # # 从左上角开始 剪切 200*200的图片
        img2 = img.crop((1024, 1024, 2048, 2048))
        img2.save(path_cut+ima)

def cut1024():
    filename = os.listdir(path)
    for ima in tqdm(filename):
        img = Image.open(path + ima)
        #
        # print(ima)
        # # 从左上角开始 剪切 200*200的图片
        img2 = img.crop((1024, 1024, 2048, 2048))
        img2.save(path_cut + ima)

if __name__ == '__main__':
    start_ = time.time()
    ans = [0,33,66,99,132,165,200]

    for i in range(1,7):
        p = multiprocessing.Process(target=cut_1024, args = (ans[i-1],ans[i], ))
        p.start()
    p.join()
    # cut1024()
    end_ = time.time()
    logging.info('花费时间: %.2f s' % (end_ - start_))
    print(end_ - start_)
