import threading
import uvicorn

def run_uvicorn(host, port):
    uvicorn.run("app:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    run_uvicorn('26.52.35.245', 8000)
    # hosts = [
    #     ['192.168.1.140', 8000],
    #     ['26.52.35.245', 8005]
    # ]

    # threads = []

    # for host in hosts:
    #     thread = threading.Thread(target=run_uvicorn, args=(host[0], host[1]))
    #     threads.append(thread)
    #     thread.start()

    # for thread in threads:
    #     thread.join()
