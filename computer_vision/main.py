from modules import webcam
import cv2

def main():
    capture = webcam.get_webcam()

    while True:
        frame = webcam.get_frame(capture)
        frame_rgb = frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         
        cv2.imwrite("teste.jpg", frame)

        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    main()