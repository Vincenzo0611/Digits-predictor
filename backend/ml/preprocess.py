import cv2
import numpy as np

TARGET_SIZE = (100, 100)


def preprocess_image(
    img,
    return_visual=False
):

    img = cv2.resize(
        img,
        TARGET_SIZE,
        interpolation=cv2.INTER_AREA
    )

    blurred = cv2.GaussianBlur(img, (9, 9), 0)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (15, 15)
    )

    th_color = cv2.morphologyEx(
        blurred,
        cv2.MORPH_TOPHAT,
        kernel
    )

    bh_color = cv2.morphologyEx(
        blurred,
        cv2.MORPH_BLACKHAT,
        kernel
    )

    th_gray = cv2.cvtColor(
        th_color,
        cv2.COLOR_BGR2GRAY
    )

    bh_gray = cv2.cvtColor(
        bh_color,
        cv2.COLOR_BGR2GRAY
    )

    s_top = np.sum(th_gray, dtype=np.float64)
    s_black = np.sum(bh_gray, dtype=np.float64)

    L_top = np.count_nonzero(th_gray > 8)
    L_black = np.count_nonzero(bh_gray > 8)

    if s_top > s_black and L_top > L_black:
        chosen_gray = th_gray

    elif s_black > s_top and L_black > L_top:
        chosen_gray = bh_gray

    else:

        if (
            (s_top > s_black)
            and (s_top < s_black * 1.5)
            and (L_black > L_top)
        ):
            chosen_gray = bh_gray

        elif (
            (s_black > s_top)
            and (s_black < s_top * 1.5)
            and (L_top > L_black)
        ):
            chosen_gray = th_gray

        else:

            chosen_gray = cv2.addWeighted(
                th_gray,
                0.5,
                bh_gray,
                0.5,
                0
            )

    _, details_clean = cv2.threshold(
        chosen_gray,
        4,
        255,
        cv2.THRESH_TOZERO
    )

    normalized = cv2.normalize(
        details_clean,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    _, thresh = cv2.threshold(
        normalized,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    final_img = cv2.medianBlur(
        thresh,
        3
    )

    visual_image = final_img.copy()

    final_img = final_img.astype(np.float32) / 255.0

    final_img = final_img.reshape(
        1,
        100,
        100,
        1
    )

    if return_visual:
        return final_img, visual_image

    return final_img