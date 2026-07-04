from flask import Flask, Response
import cv2
from computer_vision import vision
from threading import Thread

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