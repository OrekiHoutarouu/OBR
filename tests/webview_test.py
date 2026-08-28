import traceback
from open_rdk import CommsRuntime
from time import sleep

# Run with "python debug/webview_test.py"

def main():
    """Start the OpenRDK webview and keep it running until interrupted."""

    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    try:
        while True:
            pass

    except KeyboardInterrupt:
            print("KeyboardInterrupt received. Stopping execution...")
            
            openrdk.stop()  
            exit()
        
    except Exception as e:
        tb = e.__traceback__
        error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

        print(f"Error {e} occurred in {error_file} at function {function} at line {error_line}: {text}")
        print("Stopping execution...")

        openrdk.stop()
        exit()
        

if __name__ == "__main__":
    main()