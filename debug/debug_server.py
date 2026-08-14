from flask import Flask, Response, render_template, jsonify
from computer_vision import vision
from threading import Thread
import numpy as np
import cv2

app = Flask(__name__)

def generate():
    """Generator function that yields frames from the last captured frame in the vision module.

    Yields:
        bytes: The JPEG-encoded frame.
    """
    
    while True:
        if vision.last_frame is None:
            continue

        _, buffer = cv2.imencode(".jpg", vision.last_frame)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

@app.route("/")
def index():
    """Generate the index page for the Flask application.

    Returns:
        render_template: The rendered index page.
    """

    return render_template("index.html")

@app.route("/video")
def video():
    """Generate video stream from the last captured frame in the vision module.

    Returns:
        Response: The video stream response.
    """

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/telemetry")
def telemetry():
    """Generate telemetry data from the last vision state in the vision module.

    Returns:
        jsonify: The JSON response containing the telemetry data.
    """

    return jsonify(vision.last_state)


def start():
    """Start the Flask application in a separate thread.

    This function initializes the Flask application and runs it in a background thread,
    allowing the main thread to continue executing other code.
    """

    Thread(
        target=app.run,
        kwargs={
            "host": "0.0.0.0",
            "port": 5000,
            "threaded": True,
            "use_reloader": False
        },
        daemon=True
    ).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)


def draw_debug_frame(frame, line_contour, line_info, green_contours, fps, roi_offset_y=0):
    """Draw a debug frame with the detected line and green contours.

    Args:
        frame (numpy.ndarray): The input frame.
        line_contour (numpy.ndarray): The contour of the detected line.
        line_info (dict): Information about the detected line.
        green_contours (list): A list of contours for the detected green objects.
        fps (float): The frames per second.
        roi_offset_y (int, optional): The vertical offset for the region of interest. Defaults to 0.

    Returns:
        numpy.ndarray: The debug frame with the detected line and green contours.
    """

    debug_frame = frame.copy()

    def _offset_contour(contour, dy):
        """Offset a contour by a vertical distance.

        Args:
            contour (_type_): The contour to offset.
            dy (_type_): The vertical distance to offset by.

        Returns:
            _type_: The offset contour.
        """

        offset = np.array([[[0, dy]]], dtype=contour.dtype)
        return contour + offset

    if line_info["found"]:
        contours_to_draw = []
        if isinstance(line_contour, (list, tuple)):
            contours_to_draw = [c for c in line_contour if c is not None and hasattr(c, "shape")]
        elif hasattr(line_contour, "shape"):
            contours_to_draw = [line_contour]

        if contours_to_draw:
            shifted_contours = [_offset_contour(c, roi_offset_y) for c in contours_to_draw]
            cv2.drawContours(
                debug_frame,
                shifted_contours,
                -1,
                (255, 0, 0),
                2
            )

        cv2.circle(
            debug_frame,
            (
                line_info["center_x"],
                line_info["center_y"] + roi_offset_y
            ),
            6,
            (0, 0, 255),
            -1
        )

    if green_contours:
        MIN_GREEN_AREA = 8000
        valid_green_contours = [
            c for c in green_contours
            if c is not None and hasattr(c, "shape") and cv2.contourArea(c) >= MIN_GREEN_AREA
        ]
        if valid_green_contours:
            shifted_green_contours = [_offset_contour(c, roi_offset_y) for c in valid_green_contours]
            cv2.drawContours(
                debug_frame,
                shifted_green_contours,
                -1,
                (0, 255, 0),
                2
            )

    return debug_frame