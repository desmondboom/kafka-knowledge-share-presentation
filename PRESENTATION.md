## Stage 1：村庄里的原始相亲方式

在一个村庄里，年轻人想找对象，但没有任何媒介和工具，他们只能面对面交流。

### 场景

- 年轻人只能面对面交流
- 每个人重复描述自己的需求
- 信息不会被保存，也不会传播

### 结构示意

```
A <-> B
C <-> D
```

### 类比到系统

- 年轻人 = Producer & Consumer
- 没有中间系统
- 强耦合、低效率

### 问题

如果人越来越多，信息如何被集中保存和复用？

---

## Stage 2：出现相亲角（Topic）

### 场景

- 村口出现公告板
- 每个人把需求贴上去
- 想找对象的人来看公告

### 结构示意

```
Producer --> [ 相亲角 ]
```

### 类比到系统

- 相亲角 = Topic
- 张贴信息的人 = Producer
- 看公告的人 = Consumer

### 问题

谁来管理公告板？如果乱贴、丢失怎么办？

---

## Stage 3：引入管理员（Broker）

### 场景

- 指定一个管理员负责相亲角
- 维护秩序、记录信息、防止丢失

### 结构示意

```
Producer --> [ Broker : Topic ] --> Consumer
```

### 类比到系统

- 管理员 = Broker
- 相亲角仍然是 Topic
- Broker 负责存储和分发数据

### 问题

排队贴告示的队伍过长，怎么办？
如果管理员一个人忙不过来，怎么办？

---

## Stage 4：分区管理（Partition）

### 场景

- 相亲角被分成多个板块：
  - 男找女
  - 女找男
  - 男找男
  - 女找女
  - 同性恋
  - 其他偏好

### 结构示意

```
Producer
   |
   | - key -> hash
   ↓
[ Topic ]
   |-- Partition 1
   |-- Partition 2
   |-- Partition 3
   |-- Partition 4
   |-- Partition 5
```

### 类比到系统

- 板块 = Partition
- Topic 被拆成多个 Partition
- 每个 Partition 内部有顺序

### 问题

如果一个管理员出问题，这些数据是否会丢失？

---

## Stage 5：多个管理员（Replica & Leader）

### 场景

- 再来一个管理员
- 两人分别管理不同板块
- 同时互相备份数据

### 结构示意

```
Partition 1 -> Leader Broker 1
            -> Replica Broker 2

Partition 2 -> Leader Broker 2
            -> Replica Broker 1
```

### 类比到系统

- 主管理员 = Leader Replica
- 备份管理员 = Follower Replica
- 副本机制保证数据安全

### 问题

谁来真正处理撮合工作？所有人看公告效率较低

---

## Stage 6：红娘出现（Consumer）

### 场景

- 出现红娘专门读取相亲信息
- 负责匹配双方并联系他们

### 结构示意

```
Producer -> Topic -> Consumer(红娘)
```

### 类比到系统

- 红娘 = Consumer
- 撮合 = 业务处理逻辑
- Consumer 专门负责处理数据

### 问题

如果一个红娘忙不过来怎么办？

---

## Stage 7：红娘群组（Consumer Group）

### 场景

- 出现两个红娘
- 一个负责异性恋，一个负责同性恋
- 分工协作

### 结构示意

```
Partition 1 -> Consumer A
Partition 2 -> Consumer B
```

### 类比到系统

- 红娘群 = Consumer Group
- 一个 Partition 只能被一个 Consumer 消费
- 实现负载均衡

### 问题

如果红娘中途请假，系统如何重新分配工作？

---

## Stage 8：完整自动化系统（Kafka）

### 场景

- 相亲角高度自动化
- 管理员、红娘、分区协同工作
- 稳定运行

### 结构示意

```
Producer
   |
[ Topic ]
   |-- Partition 1 (Leader + Replica)
   |-- Partition 2 (Leader + Replica)
   |
Consumer Group
```

### 类比到系统

- Producer = 发消息的人
- Broker = 管理员
- Topic = 相亲角
- Partition = 分类板块
- Consumer Group = 红娘团队

---

## 总结：Kafka 系统完整结构

### 整体结构图

```
                    Producer
                        |
                        v
+------------------- Topic -----------------------+
| Partition 1 (Leader B1 Replica B2 Replica B3)   |
| Partition 2 (Leader B2 Replica B1 Replica B3)   |
| Partition 3 (Leader B3 Replica B1 Replica B2)   |
+-------------------------------------------------+
                        |
                        v
                  Consumer Group
                /        |        \
            Consumer1  Consumer2  Consumer3
```

### 核心思想

- 解耦生产与消费
- 用 Partition 提升吞吐量
- 用 Replica 提供容错
- 用 Consumer Group 提供并行处理

### 一句话总结

Kafka 是一个：
可扩展、可容错、可并行的消息分发系统

---

## 总结：Kafka 核心概念速览

### 概念清单

- Topic：消息分类的“频道”
- Partition：Topic 的并行分片，保持分片内有序
- Broker：Kafka 节点，负责存储与转发
- Leader：分区主副本，处理读写
- Replica：分区副本，保障容错
- Consumer Group：并行消费的“工班”
- ZooKeeper：旧版集群协调（元数据/选主）
- KRaft：新一代内置元数据管理（替代 ZooKeeper）

### 一句话

Kafka = Topic + Partition + Broker + Replica + Consumer Group 的协作系统

---

## 总结：常见关键参数

### 主题与副本

- `num.partitions`：分区数（并行度）
- `replication.factor`：副本数（容错级别）
- `min.insync.replicas`：最小同步副本数（写入安全）

### 生产与消费

- `acks`：生产者确认级别（0/1/all）
- `max.in.flight.requests.per.connection`：在途请求数
- `enable.idempotence`：幂等写入
- `max.poll.records`：单次拉取条数

### 存储与保留

- `retention.ms`：保留时间
- `retention.bytes`：保留大小
- `segment.bytes`：日志段大小

### 经验法则

- 分区数决定吞吐上限
- 副本数决定稳定性成本
- `min.insync.replicas` + `acks=all` 决定数据安全底线

---

## 另外：集群的特点

当我们谈到kafka集群的时候，我们在谈什么？

- 高可用(Availability)
  - 防止单点故障带来的系统瘫痪
- 横向扩展(Scalability)
  - 单机能力有物理极限，那么两个呢？十个呢？
  - CPU，内存，IO，带宽
- 性能(Throughput)
  - 吞吐 <-> 并行
- 治理能力(Manageability)
  - 选主，心跳，同步，编排

> 数量换质量，用结构换稳定，用分布换确定性。
