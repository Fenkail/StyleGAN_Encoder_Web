import logging
import os
import time

import PIL.Image
import numpy as np

start_ = time.time()
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a'
                    )

canvas = PIL.Image.new('RGB', (1024 * (2), 1024 * (2)), 'white')
    # for col, src_image in enumerate(list(src_images)):
    #     canvas.paste(PIL.Image.fromarray(src_image, 'RGB'), ((col + 1) * w, 0))
    # for row, dst_image in enumerate(list(dst_images)):
    #     canvas.paste(PIL.Image.fromarray(dst_image, 'RGB'), (0, (row + 1) * h))
    #     row_dlatents = np.stack([dst_dlatents[row]] * len(src_seeds))
    #     row_dlatents[:, style_ranges[row]] = src_dlatents[:, style_ranges[row]]
    #     row_images = Gs.components.synthesis.run(row_dlatents, randomize_noise=False, **synthesis_kwargs)
    #     for col, image in enumerate(list(row_images)):
    #         canvas.paste(PIL.Image.fromarray(image, 'RGB'), ((col + 1) * w, (row + 1) * h))

canvas2 = canvas.crop((1024,1024,2048,2048))
# end_ = time.time()
# logging.info('人脸识别剪裁部分花费时间: %f' %(end_ - start_))