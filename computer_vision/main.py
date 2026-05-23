from modules import webcam, image_processing
import cv2

def main():
    capture = webcam.get_webcam()

    while True:
        frame = webcam.get_frame(capture)

        frame_gray = image_processing.convert_to_gray(frame)
        frame_blur = image_processing.blur_frame(frame_gray)
        _, frame_threshold = image_processing.set_threshold(frame_blur)
        frame_contours, _ = image_processing.find_contours(frame_threshold)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()