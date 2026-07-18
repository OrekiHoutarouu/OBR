from openrdk import CommsRuntime
from time import sleep

# Run with "python debug/webview_test.py"

def main():
    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    try:
        while True:
            pass

    except KeyboardInterrupt:
        print("Stopping execution...")
        
        motor_1.stop()
        motor_2.stop()
        openrdk.stop()
        
        exit()

    except:
        print("An error occurred. Stopping execution...")
        
        motor_1.stop()
        motor_2.stop()
        openrdk.stop()
        
        exit()
        

if __name__ == "__main__":
    main()