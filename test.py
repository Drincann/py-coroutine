from asynclib import loop, Future, asynchttp, asyncfun

@asyncfun
def http():
    responseData = yield from Future(
        lambda resolve:
            asynchttp.get(
                url='http://gaolihai.cool/doc/README.md',
                callback=lambda response: resolve(response)
            )
    )
    print(responseData.decode('utf-8'))


for i in range(1):
    http()
