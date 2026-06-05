from modules import green_detector, image_processing, line_detector, track_features, utils, webcam
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
        frame_red_mask = image_processing.apply_red_mask(frame_hsv_blur)

        frame_black_mask = cv2.bitwise_and(
            frame_black_mask,
            cv2.bitwise_not(
                cv2.bitwise_or(frame_green_mask, frame_red_mask)
            )
        )

        frame_green_mask = cv2.bitwise_and(
            frame_green_mask,
            cv2.bitwise_not(
                cv2.bitwise_or(frame_black_mask, frame_red_mask)
            )
        )

        frame_red_mask = cv2.bitwise_and(
            frame_red_mask,
            cv2.bitwise_not(
                cv2.bitwise_or(frame_black_mask, frame_green_mask)
            )
        )

        line_contours, _ = utils.find_contours(frame_black_mask)
        green_contours, _ = utils.find_contours(frame_green_mask)
        red_contours, _ = utils.find_contours(frame_red_mask)

        line_info = line_detector.get_line_info(line_contours, frame_center_x, 15000)
        green_center_x = green_detector.get_green_center_x(green_contours, 3000)

        green_offset = utils.get_offset(line_info["center_x"], green_center_x)

        if green_offset == line_info["center_x"]:
            green_offset = 0

        # DEBUG

        possible_gap = track_features.detect_possible_gap(frame_black_mask, line_contours)
        print(f"Possible gap: {possible_gap}")
        
        intersection = track_features.detect_intersection(frame_black_mask,line_contours, line_info)
        print(f"Intersection: {intersection}")

        cv2.imshow("Black mask", frame_black_mask)
        cv2.imshow("Green mask", frame_green_mask)
        cv2.imshow("Red mask", frame_red_mask)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()