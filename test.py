from asynclib.core import Future, asyncfun
from asynclib.asynchttp import get as asyncget

@asyncfun
def http():
    responseData = yield from Future(
        lambda resolve:
            asyncget(
                url='http://gaolihai.cool/doc/README.md',
                callback=lambda response: resolve(response)
            )
    )
    print(responseData.decode('utf-8'))


for i in range(1):
    http()
