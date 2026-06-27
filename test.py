from openrdk import CommsRuntime

openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)
openrdk.list_devices(verbose=True)
openrdk.post("webview_complete")

while True:
    pass