from .eventQueue import eventQueue

def asyncRun(gen):
    eventQueue.pushCallback(gen)