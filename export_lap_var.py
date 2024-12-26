# import the necessary packages
from imutils import paths
import argparse
import csv
import cv2
from tqdm import tqdm

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
help="path to input directory of images")
args = vars(ap.parse_args())

with open('lap_var_values.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['lap_var','actual','phone', 'width'])
    # loop over the input images
    with tqdm(total=17040) as pbar:
        for image_path in paths.list_images(args["images"]):
            image_name = image_path.rsplit('\\', 1)[-1]
            # if the image contains Mb (motion blur) or Ob(out-of-focus blur)
            if ("Mb" in image_name or "Ob" in image_name):
                actu = "Blurry"
            else:
                actu = "Not"

            # if the image contains Mb (motion blur) or Ob(out-of-focus blur)
            if ("WP" in image_name):
                phone = "Nokia"
            else:
                phone = "Samsung"

            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method
            image = cv2.imread(image_path)
            original_height, original_width, _ = image.shape
            aspect_ratio = original_height / original_width
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            pbar.update(1)

            for image_width in [original_width, 400, 1600]:
                resized = cv2.resize(gray, 
                    (image_width, int(image_width * aspect_ratio)))
                fm = variance_of_laplacian(resized)

                # prints the focus measure and clasification
                writer.writerow([fm, actu, phone, image_width])
                pbar.update(1)

print("Finished exporting Laplacian variance values from dataset.")
