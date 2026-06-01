from modules import image_processing, line_detector, utils, webcam
import cv2

def main():
    capture = webcam.get_webcam()

    while True:
        frame = webcam.get_frame(capture)
        frame_center_x = utils.get_frame_center_x(frame)

        frame_gray = image_processing.convert_to_gray(frame)

        frame_blur = image_processing.blur_frame(frame)
        gray_frame_blur = image_processing.blur_frame(frame_gray)

        _, gray_frame_threshold = image_processing.set_threshold_black_white(gray_frame_blur)

        gray_frame_contours, _ = line_detector.find_contours(gray_frame_threshold)
        
        line_center = line_detector.get_line_center(gray_frame_contours, frame)

        line_offset = utils.get_offset(frame_center_x, line_center)

        if line_offset > 0:
            print("left")
            print(line_offset)
        else:
            print("right")
            print(line_offset)

        cv2.imshow("Webcam", gray_frame_threshold)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()