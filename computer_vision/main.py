from modules import image_processing, line_detector, utils, webcam
import cv2

def main():
    capture = webcam.get_webcam()

    while True:
        frame = webcam.get_frame(capture)
        frame_center_x = utils.get_frame_center_x(frame)

        frame_grayscale = image_processing.convert_to_grayscale(frame)
        frame_hsv = image_processing.convert_to_hsv(frame)

        frame_grayscale_blur = image_processing.blur_frame(frame_grayscale)
        frame_hsv_blur = image_processing.blur_frame(frame_hsv)

        _, frame_black_mask = image_processing.apply_black_mask(frame_grayscale_blur)
        frame_green_mask = image_processing.apply_green_mask(frame_hsv_blur)

        line_contours, _ = utils.find_contours(frame_black_mask)
        green_contours, _ = utils.find_contours(frame_green_mask)

        line_center_x = line_detector.get_line_center(line_contours)

        line_offset = utils.get_offset(frame_center_x, line_center_x)

        if line_offset > 0:
            print("left")
            print(line_offset)
        else:
            print("right")
            print(line_offset)

        cv2.imshow("Webcam", frame_black_mask)
        cv2.imshow("Green mask", frame_green_mask)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()