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
            print("KeyboardInterrupt received. Stopping execution...")
            
            openrdk.stop()  
            exit()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Stopping execution...")

        openrdk.stop()
        exit()
        

if __name__ == "__main__":
    main()