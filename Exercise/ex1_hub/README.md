# ryu - ex1 Hub

## 目標

從這個範例會學到最基本的ryu架構以及基本的function該怎麼使用。

這次要做一個簡單的hub,並且默認action為Flooding(轉傳封包至所有除了來源port以外的port)

![](https://img2018.cnblogs.com/blog/1309518/201910/1309518-20191024105802987-842471749.png) [來源](https://www.cnblogs.com/ssyfj/p/11731565.html)

---

## 定義controller - 初始化動作

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%28171%2C+184%2C+195%2C+1%29&t=seti&wt=none&l=python&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=133%25&si=false&es=2x&wm=false&code=from%2520ryu.base%2520import%2520app_manager%250A%250Aclass%2520Hub%28app_manager.RyuApp%29%253A%250A%2520%2520%2520%2520OFP_VERSIONS%2520%253D%2520%255Bofproto_v1_3.OFP_VERSION%255D%250A%250A%2520%2520%2520%2520def%2520__init__%28self%252C%2520*args%252C%2520**kwargs%29%253A%250A%2520%2520%2520%2520%2520%2520%2520%2520super%28Hub%252C%2520self%29.__init__%28*args%252C%2520**kwargs%29"
  style="width: 1024px; height: 473px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin"
  align="right">
</iframe>