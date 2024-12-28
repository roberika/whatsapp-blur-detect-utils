import cv2
import numpy as np

def crop_document(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not loaded.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Edge detection using Canny
    edges = cv2.Canny(blurred, 30, 120)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and keep the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    document_contour = None
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # If the polygon has 4 sides, assume it is the document
        if len(approx) == 4:
            document_contour = approx
            break

    if document_contour is None:
        print("Error: Document contour not detected.")
        return

    # Perspective transform to get a top-down view of the document
    pts = document_contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # Order the points: top-left, top-right, bottom-right, bottom-left
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # Compute the width and height of the new image
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    # Destination points for the perspective transform
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # Apply the perspective transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Save the result
    cv2.imwrite(output_path, warped)
    print(f"Document cropped and saved to {output_path}")

# Example usage
input_image_path = "Images/M_Img_WP_D30_L4_r35_a-5_b10.jpg"
output_image_path = "cropped_document.jpg"
crop_document(input_image_path, output_image_path)
