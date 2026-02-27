import webview
import threading
from app import app

def start_flask():
    app.run()

if __name__ == '__main__':
    # Start Flask in background
    threading.Thread(target=start_flask).start()

    # Open window
    webview.create_window("Demon Monk AI", "http://127.0.0.1:5000")
    webview.start()