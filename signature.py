import cv2
from skimage.metrics import structural_similarity as ssim

def match(path1, path2):
    # Read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize images for comparison
    gray1 = cv2.resize(gray1, (300, 300))
    gray2 = cv2.resize(gray2, (300, 300))

    # Display both images
    cv2.imshow("Image 1", gray1)
    cv2.imshow("Image 2", gray2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calculate SSIM (Structural Similarity Index)
    similarity_value, diff = ssim(gray1, gray2, full=True)
    similarity_value = "{:.2f}".format(similarity_value * 100)

    # Calculate contours for enhanced accuracy
    ret1, thresh1 = cv2.threshold(gray1, 127, 255, 0)
    ret2, thresh2 = cv2.threshold(gray2, 127, 255, 0)

    contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img1, contours1, -1, (0, 255, 0), 3)
    cv2.drawContours(img2, contours2, -1, (0, 255, 0), 3)

    # Display images with contours
    cv2.imshow("Image 1 with Contours", img1)
    cv2.imshow("Image 2 with Contours", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return float(similarity_value)
