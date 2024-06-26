import cv2
import numpy as np
import sys

src = cv2.imread('./namecard.jpg')
# (1008, 756, 3) 중 h,w,채널 중 h,w 지정
h, w = src.shape[:2]
dh = 500
# A4용지 크기: 210*297cm
dw = round(dh * 297 / 210)

# 변경전/변경후 좌표 설정
srcQuad = np.array([[30, 30], [30, h-30], [w-30, h-30], [w-30, 30]], np.float32)
dstQuad = np.array([[0, 0], [0, dh], [dw, dh], [dw, 0]], np.float32)

dragSrc = [False, False, False, False]
# img를 복사하여 corners위치에 기반한 점 및 선을 그리는 코드
def drawROI(img, corners):
    cpy = img.copy()
    c1 = (192, 192, 255) # 색상1
    c2 = (128, 128, 255) # 색상2
    # 해당 점에 4개의 점 그리기
    for pt in corners:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1)
    # 각 점을 잇는 라인
    cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2)
    cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2)
    cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2)
    cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2)

    return cpy


def onMouse(event, x, y, flags, param):
    global srcQuad, dragSrc, ptOld, src
    # 왼쪽버튼 눌렸을 때
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break

    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]
                srcQuad[i] += (dx, dy)
                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy)
                ptOld = (x, y)
                break

disp = drawROI(src, srcQuad)
cv2.imshow('img', disp)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey()
    if key == 13:
        break
    elif key == 27:
        sys.exit()


pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
dst = cv2.warpPerspective(src, pers, (dw,dh), flags=cv2.INTER_CUBIC)
cv2.imshow('dst',dst)
cv2.waitKey()