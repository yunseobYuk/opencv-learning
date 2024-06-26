import cv2
import pytesseract
import numpy as np


def reorderPts(pts):
    # print(pts)
    '''
        [[903. 199.]
         [179. 200.]
         [159. 593.]
         [938. 581.]]

        [[179. 200.]
        [159. 593.]
        [938. 581.]
        [903. 199.]]
    '''
    # print(pts[:, 1])
    # print(pts[:, 0])
    idx = np.lexsort((pts[:, 1], pts[:, 0]))
    pts = pts[idx]
    # print(idx)

    if pts[0, 1] > pts[1, 1]:
        pts[[0, 1]] = pts[[1, 0]]

    if pts[2, 1] < pts[3, 1]:
        pts[[2, 3]] = pts[[3, 2]]
    print(pts)
    return pts


src = cv2.imread('./namecard.jpg')

dw, dh = 700, 400
srcQuad = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32)
dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)
dst = np.zeros((dh, dw), np.uint8)

src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, src_bin = cv2.threshold(src_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cpy = src.copy()
for pts in contours:
    if cv2.contourArea(pts) < 1000:
        continue

    approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True) * 0.02, True)
    # print(approx)

    # 영상에 다각형을 그림
    # polylines(영상, 꼭지점 좌표, 폐곡선 여부, 선색상, 선두께)
    cv2.polylines(cpy, [approx], True, (0, 255, 0), 2)

    srcQuad = reorderPts(approx.reshape(4, 2).astype(np.float32))
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    dst = cv2.warpPerspective(src, pers, (dw, dh))
    dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    print(pytesseract.image_to_string(dst_gray, lang='kor+eng'))

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()









