import webbrowser
import threading
import time
import uvicorn

def open_browser():
    time.sleep(1)  # espera o servidor subir (ajuste o tempo se precisar)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
