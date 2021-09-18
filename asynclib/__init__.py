from .core import loop, asyncfun, Future

# auto loop
__import__('threading').Thread(target=loop).start()
