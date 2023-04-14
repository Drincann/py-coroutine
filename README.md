# py-coro-impl

一个小目标，Python 基于生成器的协程实现，带有简单的事件循环、以及可能的 Promise 实现。

同时提供异步计时器(timer)、一套 socket 异步 api，以及可能的其他异步 api。

## 参考资料

异步 socket api 实现参考

[aosabook a-web-crawler-with-asyncio-coroutines](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

非自旋的阻塞的事件队列参考

[StackOverflow how-would-you-implement-a-basic-event-loop](https://stackoverflow.com/questions/658403/how-would-you-implement-a-basic-event-loop)

js 异步实现参考

[知乎 手写 JavaScript Promise Generator async/await](https://zhuanlan.zhihu.com/p/338009998)

## 原理

这是一个使用事件循环的协程调度器实现, 异步 api IO 时会复用事件循环线程的 selector, I/O 状态由事件循环负责监听, 完成后回调。

通过 `Promise` 类包装异步过程, 将会辅助 `GeneratorExcutor` 驱动协程在 IO 时挂起, 完成后恢复和继续执行。

- `asynclib.core.eventQueue` 低层级, 事件队列实现:
  - class `_EventQueue`: 低层级, 事件队列实现
  - class `EventQueueManager`: 低层级抽象层, 事件队列单例的管理器
- `asynclib.core.eventloop` 低层级, 事件循环、协程执行器、事件循环 Manager 的实现
  
  在事件循环中, 每次首先检查 timer 最小堆, 执行已经超时的任务。
  
  然后检查事件队列, 执行所有事件。
  
  最后等待 I/O, 超时时间为即将发生的 timer 到现在的时间间隔，如果没有 timer, 则阻塞时间为 2^31 - 1。
  - class `Loop`: 低层级, 事件循环的实现
  - class `LoopManager`: 高层级, 用于管理事件循环单例的执行, 负责所有协程和异步任务的计数, 以及向外暴露协程函数和异步 api 的装饰器
- `asynclib.core.model` 相关类型的实现：
  - class `Promise`: 高层级, 异步 api 包装器
  - class `Emitter`: 低层级, 一个事件订阅发布器
  - class `Coroutine`: 低层级, 生成器迭代器的包装器
  - class `AsyncapiWrapper`: 低层级, 异步 I/O 库的 api 装饰器
  - class `AsyncfunWrapper`: 低层级, 协程函数的装饰器
  - class `MinHeap`: 通用的最小堆实现
- `asynclib.core.timer` 异步计时器实现:
  - class `TimerHeap`: timer 最小堆
  - class `Timer`: timer 的实现
- `asynclib.asynchttp.api` 高层级, 非阻塞 socket 实现的 HTTP 协议接口
  - method `get`: 异步 HTTP GET 请求实现
- `asynclib.asynchttp.model` 相关类型的实现
  - class `Response`: 高层级, http 响应报文的解析类 @BBQ293
