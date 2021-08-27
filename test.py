from asynclib import asyncRun, loop, Future, asynchttp


def http():
    responseData = yield from Future(
        lambda resolve:
            asynchttp.get(
                url='http://gaolihai.cool/doc/README.md',
                callback=lambda response: resolve(response.decode('utf-8'))
            )
    )
    # print(responseData)


for i in range(10):
    asyncRun(http())

loop()
