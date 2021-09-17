from .core import loop, eventQueue, asyncRun,asyncfun, Future

# auto loop
__import__('threading').Thread(target=loop).start()