import socket
import urllib.parse
from selectors import EVENT_WRITE, EVENT_READ
from ..core.eventloop import Loop, LoopManager
from .response import HttpResponse
from ..core.eventQueue import EventQueueManager


@LoopManager.asyncapi
def get(*, url, callback, asyncDone):
    urlObj = urllib.parse.urlparse(url)
    selector = Loop.getInstance().selector
    sock = socket.socket()
    sock.setblocking(False)

    def connected():
        selector.unregister(sock.fileno())
        selector.register(sock.fileno(), EVENT_READ, responded)
        sock.send(
            (f"""GET {urlObj.path if urlObj.path != '' else '/'}{'?' if urlObj.query != '' else '' + urlObj.query} HTTP/1.0\r\n""" +
             f"""Host: {urlObj.hostname}\r\n\r\n""")
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
            responseObj = HttpResponse(responseData.decode())
            EventQueueManager.getCurrentEventQueue().pushCallback(
                lambda: (callback(responseObj), asyncDone(responseObj)))
            nonlocal __stop
            __stop = True
    __stop = False

    selector.register(sock.fileno(), EVENT_WRITE, connected)
    try:
        sock.connect(
            (urlObj.hostname, urlObj.port if urlObj.port != None else 80)
        )
    except BlockingIOError:
        pass
