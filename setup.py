import encode_images_fk as ei
import encode_images_fk2 as ee
import generate_figures_fk as gf
import align_images_fk



def mixing_image(path_A, path_B, result_path, flag):
    # 执行图像中人脸的检测与图像的剪裁
    align_images_fk.align( path_A, path_B)
    #     执行图像的StyleEncoder的编码过程
    # ei.styleGAN_encoder(path_A, path_B)
    ei.styleGAN_encoder(path_A,path_B)

    gf.style_mixing(path_A, path_B,result_path,flag)


if __name__ == '__main__':

    mixing_image(path_A= './raw_images/wr.jpg', path_B='./raw_images/wx.jpg', result_path ='./results_ff', flag = False)

