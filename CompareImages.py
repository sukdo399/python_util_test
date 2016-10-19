from skimage.measure import structural_similarity as ssim
import numpy as np
import cv2

import math


from skimage.measure import compare_ssim



def cal_entropy(img):
    """ Adapted from:
        http://areshopencv.blogspot.com/2011/12/computing-entropy-of-image.html
        and
        https://en.wikipedia.org/wiki/Entropy
    """
    freqs = cv2.calcHist([img], [0], None, [255], [0, 255]).T[0]
    row_sum = np.sum(freqs)
    freqs = freqs * 1.0 / row_sum
    return sum([-x * math.log(x, 2) for x in freqs.tolist() if x > 0])

def get_entropy(path, region_list):

    img = cv2.imread(path, 0)

    for i in region_list:
        x = int(round(i[0]))
        y = int(round(i[1]))
        w = int(round(i[2]))
        h = int(round(i[3]))
        print(x, y, w, h)
        crop_img = img[y:y + h, x:x + w]

        entropy = cal_entropy(crop_img)

        print("entropy: %.2f" % entropy)




def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(imageA, imageB):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    print("MSE: %.2f, SSIM: %.2f" % (m, s))

def CompareImage(file1, file2, regionList):
    # test.
    # file1 = '../screenshot/temp.jpg'
    # file2 = '../screenshot/temp2.jpg'

    orgImage1 = cv2.imread(file1, cv2.IMREAD_COLOR)
    orgImage2 = cv2.imread(file2, cv2.IMREAD_COLOR)

    # test.
    # regions = [[0, 0, 1280, 720]]
    # numpy.float64 x, y, w, h
    for i in regionList:
        x = i[0]
        y = i[1]
        w = i[2]
        h = i[3]
        crop_image1 = orgImage1[y:y + h, x:x + w]
        crop_image2 = orgImage2[y:y + h, x:x + w]

        crop_image1 = cv2.cvtColor(crop_image1, cv2.COLOR_BGR2GRAY)
        crop_image2 = cv2.cvtColor(crop_image2, cv2.COLOR_BGR2GRAY)

        # compare_images(crop_image1, crop_image1) # Test.
        compare_images(crop_image1, crop_image2)

        # TODO: if different, save the image file.
        # cv2.imwrite('../screenshot/main_temp2.jpg', crop_image)


# test.
# CompareImage(None, None, None)
