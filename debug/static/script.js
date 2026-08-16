async function updateTelemetry() {
            try {
                const response = await fetch("/telemetry");
                const data = await response.json();

                document.getElementById("feature").textContent =
                    data.current_feature;

                document.getElementById("resolution").textContent =
                    data.webcam_resolution;

                document.getElementById("latency").textContent =
                    data.latency + " ms";

                document.getElementById("fps").textContent =
                    data.fps;

                document.getElementById("offset").textContent =
                    data.line_info.offset_from_frame_center + " px";

                document.getElementById("center-x").textContent =
                    data.line_info.center_x + " px";

                document.getElementById("center-y").textContent =
                    data.line_info.center_y + " px";

                document.getElementById("area").textContent =
                    data.line_info.area + " px²";

                document.getElementById("touches-left").textContent =
                    data.line_info.touches_left;

                document.getElementById("touches-right").textContent =
                    data.line_info.touches_right;

                document.getElementById("touches-top").textContent =
                    data.line_info.touches_top;

                document.getElementById("touches-bottom").textContent =
                    data.line_info.touches_bottom;
                
                document.getElementById("top-left").textContent =
                    data.green_dispersion.top_left;

                document.getElementById("top-right").textContent =
                    data.green_dispersion.top_right;

                document.getElementById("bottom-left").textContent =
                    data.green_dispersion.bottom_left;

                document.getElementById("bottom-right").textContent =
                    data.green_dispersion.bottom_right;
            }

            catch (error) {
                console.error("Telemetry error:", error);
            }
        }

        setInterval(updateTelemetry, 100);

        updateTelemetry();