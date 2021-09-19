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

通过 `Promise` 类包装异步过程, 将会辅助 `GeneratorExcutor` 驱动协程在 IO 时挂起, 完成后恢复和继续执行。

- `asynclib.core.eventQueue` 低层级, 事件队列实现
- `asynclib.core.eventloop` 低层级, 事件循环、协程执行器、事件循环 Manager 的实现
- `asynclib.core.model` 相关类型的实现：`Promise`(高层级, 异步 api 包装器)、`Emitter`(低层级, 一个事件订阅发布器)、`Coroutine`(低层级, 生成器迭代器的包装器)、`AsyncapiWrapper`(低层级, 异步 I/O 库的 api 装饰器)、`AsyncfunWrapper`(低层级, 开发者用户协程的装饰器)
- `asynclib.asynchttp.api` 高层级, 非阻塞 socket 实现的 HTTP 协议接口
- `asynclib.asynchttp.model` 相关类型的实现：`Response`(高层级,http 响应报文的解析类)


## todo

- 复用 selector