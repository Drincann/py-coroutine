# py-coro-impl

一个小目标，Python 基于生成器的协程实现，带有简单的事件循环、以及可能的 Promise 实现。

同时提供一套 socket 异步 api，以及可能的其他异步 api。

## 参考资料

[aosabook a-web-crawler-with-asyncio-coroutines](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

[StackOverflow how-would-you-implement-a-basic-event-loop](https://stackoverflow.com/questions/658403/how-would-you-implement-a-basic-event-loop)

[知乎 手写 JavaScript Promise Generator async/await](https://zhuanlan.zhihu.com/p/338009998)


## 待解决的问题

### 应该暴露什么样的接口？

### 如何在单线程中驱动事件循环？

### JavaScript 协程与 Python 协程的主要区别在哪？

### Promise 对应 Python 协程的哪一层，Promise 是更高级的包装吗
