import socket
import urllib.parse
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from threading import Thread
from ..core.eventQueue import eventQueue


def get(*, url, callback):
    urlObj = urllib.parse.urlparse(url)
    selector = DefaultSelector()
    sock = socket.socket()
    sock.setblocking(False)

    def connected():
        selector.unregister(sock.fileno())
        selector.register(sock.fileno(), EVENT_READ, responded)
        sock.send(
            f"""GET {urlObj.path if urlObj.path != '' else '/'}{'?' if urlObj.query != '' else '' + urlObj.query} HTTP/1.0\r\n\r\n"""
            .encode('ascii')
        )

    responseData = bytes()

    def responded():
        nonlocal responseData
        chunk = sock.recv(4096)
        if chunk:
            responseData += chunk
        else:
            selector.unregister(sock.fileno())
            eventQueue.pushCallback(lambda: callback(responseData))
            nonlocal __stop
            __stop = True
    __stop = False

    def loop():
        while True:
            events = selector.select()
            for event_key, event_mask in events:
                cbk = event_key.data
                cbk()
            if __stop:
                break

    selector.register(sock.fileno(), EVENT_WRITE, connected)
    try:
        sock.connect(
            (urlObj.hostname, urlObj.port if urlObj.port != None else 80)
        )
    except BlockingIOError:
        pass
    Thread(target=loop).start()
