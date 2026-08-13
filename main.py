# pip install opencv-python numpy sys
import sys
import cv2
import numpy as np


def order_points(pts):
    """Return the 4 corners in order: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]          # smallest x+y  -> top-left
    rect[2] = pts[np.argmax(s)]          # largest  x+y  -> bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]       # smallest y-x  -> top-right
    rect[3] = pts[np.argmax(diff)]       # largest  y-x  -> bottom-left
    return rect


def four_point_transform(image, pts):
    """Bird's-eye view of the region defined by 4 points."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))

    dst = np.array([[0, 0],
                    [width - 1, 0],
                    [width - 1, height - 1],
                    [0, height - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (width, height))


def find_document(image):
    """Return the 4 corners of the largest quadrilateral, or None."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 50, 150)
    edged = cv2.dilate(edged, np.ones((3, 3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)   # simplify to fewer vertices
        if len(approx) == 4:
            return approx.reshape(4, 2).astype("float32"), edged
    return None, edged


def scan(image):
    corners, edged = find_document(image)
    if corners is None:
        return None, edged, image

    outlined = image.copy()
    cv2.drawContours(outlined, [corners.astype(int)], -1, (0, 255, 0), 3)

    warped = four_point_transform(image, corners)
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    paper = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 21, 10)
    return paper, edged, outlined


def run_image(path):
    image = cv2.imread('test.jpg')
    if image is None:
        print(f"Could not read {path}")
        return
    scale = 700 / image.shape[0]
    image = cv2.resize(image, None, fx=scale, fy=scale)

    paper, edged, outlined = scan(image)
    cv2.imshow("1. Edges", edged)
    cv2.imshow("2. Detected page", outlined)
    if paper is not None:
        cv2.imshow("3. Scanned", paper)
        cv2.imwrite("scanned_output.png", paper)
        print("Saved scanned_output.png")
    else:
        print("No page found — try a plain background with good contrast.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam():
    cap = cv2.VideoCapture(0)
    print("Hold a page in front of the camera. 's' = save, 'q' = quit")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        paper, _, outlined = scan(frame)
        cv2.imshow("Live scanner", outlined)
        if paper is not None:
            cv2.imshow("Scanned", paper)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s') and paper is not None:
            cv2.imwrite("scanned_output.png", paper)
            print("Saved scanned_output.png")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_image(sys.argv[1]) if len(sys.argv) > 1 else run_webcam()