# ryu - ex1 Hub

## 目標

從這個範例會學到最基本的ryu架構以及基本的function該怎麼使用。

這次要做一個簡單的hub,並且默認action為Flooding(轉傳封包至所有除了來源port以外的port)

![](https://img2018.cnblogs.com/blog/1309518/201910/1309518-20191024105802987-842471749.png) [來源](https://www.cnblogs.com/ssyfj/p/11731565.html)

---

## 定義controller - 初始化動作

![](https://imgur.com/jV5nfZk.jpg)