# py-coro-impl

一个小目标，Python 基于生成器的协程实现，带有简单的事件循环、以及可能的 Promise 实现。

同时提供一套 socket 异步 api，以及可能的其他异步 api。

## 参考资料

异步 socket api 实现参考

[aosabook a-web-crawler-with-asyncio-coroutines](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

非自旋的阻塞的事件队列参考

[StackOverflow how-would-you-implement-a-basic-event-loop](https://stackoverflow.com/questions/658403/how-would-you-implement-a-basic-event-loop)

js 异步实现参考

[知乎 手写 JavaScript Promise Generator async/await](https://zhuanlan.zhihu.com/p/338009998)

## 原理

这是一个生产者消费者模型下的协程实现, 异步 api IO 时会交由其他线程完成, 完成后将负责向事件队列中 "生产" 一个回调函数, 事件循环将会在未来消费它。

通过 `Future` 类包装异步过程, 将会辅助 `GeneratorExcutor` 驱动协程在 IO 时挂起, 完成后恢复和继续执行。

- `asynclib.eventQueue.eventQueue` 是一个线程安全的阻塞队列实例的包装.
- `asynclib.eventloop.loop` 是主线程的事件循环入口，开发者需要在合适的位置 (例如主调用栈的同步过程结束后) 调用, 从而开始协程的调度
- `asynclib.eventloop.__GeneratorExcutor` 是协程的驱动器, 配合 `Future` 实例对协程进行驱动,
- `asynclib.Future.Future` 是用来辅助协程驱动器执行协程的类。它有点类似 `Promise`
- `asynclib.asynchttp.*` 这是一个子包, 暂时仅实现了非常基本的基于 HTTP/1.0 的 GET method 的异步接口
  - `asynclib.asynchttp.get` 基于 HTTP/1.0 的 GET method 的异步接口

`asynclib` 暴露了三个接口

- `loop` 事件循环入口
- `asyncRun` 向事件队列中压入一个协程
- `Future` 异步过程的包装器, 用于挂起协程
  这是一个类似 Promise 的类, 该类将接收一个回调函数, 并提供一个 `resolve` 参数, 在异步过程完成时调用并传入结果, `GeneratorExcutor` 将会进一步自动驱动协程恢复并将异步过程的返回值传递到协程挂起位置
- `asynchttp.*` 子包, 实现了基于 HTTP/1.0 的的异步接口
