import numpy as np
import cv2
import math

def main():

    img_path = r'data\00.jpg'#path to images

    img = cv2.imread(img_path)
    scale = img.shape[0] / 1000
    width = int(img.shape[1] / scale)
    height = int(img.shape[0] / scale)
    new_dim = (width, height)
    resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_LANCZOS4)

    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv_img)

    mean = np.mean(val)
    gamma = math.log(1 * 255) / math.log(mean)

    val_gamma = np.power(val, gamma).clip(0, 255).astype(np.uint8)
    hsv_img = cv2.merge([hue, sat, val_gamma])
    resized_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    def search_contours(mask, col):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        contour_number = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if col == (0, 0, 255) and area > 100:
                cv2.drawContours(resized_img, [contour], -1, col, 2)
                contour_number = contour_number + 1
            elif col == (128, 0, 128) and area > 60:
                cv2.drawContours(resized_img, [contour], -1, col, 2)
                contour_number = contour_number + 1
            elif col == (0, 255, 255) and area > 50:
                cv2.drawContours(resized_img, [contour], -1, col, 2)
                contour_number = contour_number + 1
            elif col == (0, 255, 0) and area > 125:
                cv2.drawContours(resized_img, [contour], -1, col, 2)
                contour_number = contour_number + 1

        return contour_number

    kernel = np.ones((3, 3), np.uint8)

    avg_ = int(np.mean(hsv_img[:, :, 1]))

    # utworzenie maski do zliczania zielonych cukierkow
    green_lower1  = np.array([28, 185,
                            20])  # tu środek był 185, 175 i 195 do bani, tu prawo było 20, 10 do bani, 30 też do bani, lewo było 28 i mnie jest do bani
    green_upper1 = np.array([65, 255, 255])
    green_mask1 = cv2.inRange(hsv_img, green_lower1, green_upper1)
    green_lower2 = np.array([40, 45, 90])
    green_upper2 = np.array([53, 190, 255])
    green_mask2 = cv2.inRange(hsv_img, green_lower2, green_upper2)
    green_mask=green_mask1+green_mask2 ###to potem sprawdzić
    #green_mask = green_mask1
    kernel = np.ones((5, 5), np.uint8)
    green_mask = cv2.erode(green_mask, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    # utworzenie maski do zliczania żółtych cukierkow
    yellow_lower = np.array([18, 180,
                             60])  # tu po lewej było 18, 15 to samo, 20 do bani, prawe było 120 110 to samo 130 do bani, 100 to samo, 60 to samo
    yellow_upper = np.array([28, 255,
                             255])  # tu po lewej było 30, lewe 25 do bani, obniżenie prawego jest do bani, środek niższy niż 255 to tragedia !!!! sprawdzić lewe 26
    yellow_mask = cv2.inRange(hsv_img, yellow_lower, yellow_upper)
    yellow_mask = cv2.erode(yellow_mask, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    # utworzenie maski do zliczania fioletowych cukierkow
    purple_lower = np.array([150, 30, 20])  # tu środkowe było 40 30 tyle samo 20 do bani
    purple_upper = np.array([176, 255, 245])  # tu prawe było 245, 240 to samo, 230 do bani
    purple_lower2 = np.array([0, 0, 0])
    purple_upper2 = np.array(
        [7, 100, 70])  # tu lewe było 6 przy 7 tyle samo, prawe było na 30 przy 40 to samo przy 50 to samo 70 to samo
    purple_mask = cv2.inRange(hsv_img, purple_lower, purple_upper)
    purple_mask2 = cv2.inRange(hsv_img, purple_lower2, purple_upper2)
    purple_mask3 = purple_mask + purple_mask2
    purple_mask3 = cv2.erode(purple_mask3, kernel)
    purple_mask3 = cv2.morphologyEx(purple_mask3, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((5, 5), np.uint8)

    # utworzenie maski do zliczania czerwonych cukierkow
    red_lower = np.array([0, 130, 40])  #### tu srodkowe bylo 100, 120 ok,!!!!!!!!!!!
    red_upper = np.array([5, 255, 255])
    red_lower2 = np.array([175, 120, 10])  # tu prawe było po 30, 10 to samo
    red_upper2 = np.array([185, 255, 255])
    red_mask = cv2.inRange(hsv_img, red_lower, red_upper)
    red_mask2 = cv2.inRange(hsv_img, red_lower2, red_upper2)
    red_mask3 = red_mask + red_mask2
    red_mask3 = red_mask3
    red_mask3 = cv2.erode(red_mask3, kernel)
    red_mask3 = cv2.morphologyEx(red_mask3, cv2.MORPH_OPEN, kernel)

    cv2.imshow('HSV_Pic', hsv_img)

    color_selected=[0,0,0]

    def select_color(event, x, y, flags, param):
        H = hsv_img[y, x][0]
        S = hsv_img[y, x][1]
        V = hsv_img[y, x][2]
        if event == cv2.EVENT_LBUTTONDOWN:
            color_selected[:] = (H, S, V)
            print(color_selected)
    cv2.setMouseCallback('HSV_Pic', select_color)
    while True:
        cv2.imshow('Green', green_mask)
        cv2.imshow('Yellow', yellow_mask)
        cv2.imshow('Purple', purple_mask3)
        cv2.imshow('Red', red_mask3)

        green_number = search_contours(green_mask,(0, 255, 0))
        cv2.putText(resized_img, f'Green: {green_number}', (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        yellow_number = search_contours(yellow_mask,(0, 255, 255))
        cv2.putText(resized_img, f'Yellow: {yellow_number}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        purple_number = search_contours(purple_mask3,(128, 0, 128))
        cv2.putText(resized_img, f'Purple: {purple_number}', (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 0, 128), 2, cv2.LINE_AA)
        red_number = search_contours(red_mask3,(0, 0, 255))
        cv2.putText(resized_img, f'Red: {red_number}', (5, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('Original', resized_img)
        key_code = cv2.waitKey(10)
        if key_code == 27:
            # escape key pressed
            break

if __name__ == '__main__':
    main()