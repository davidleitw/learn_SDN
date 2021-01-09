# OpenFlow1.0協定講解

## 前言

想要深入了解一個協定的內容，看規格書是最快的，因為剛開始學習SDN相關的知識，所以目前正在讀OpenFlow1.0相關的內容，這篇文章會先主要介紹OpenFlow 1.0的架構，以及一些spec的整理。

之後也會整理一些OpenFlow 1.3版本的內容，並且簡單描述跟OpenFlow 1.0的差異。

### 為什麼會著重在1.0與1.3兩個版本呢？

> 1.0版本與之後的版本不兼容，所以1.0要最先介紹。 **1.0以及1.3版本被選為長期支持的穩定版本**

因為OpenFlow是支援OpenFlow協定的網路設備跟Controller兩者溝通的橋樑，所以我們在探討此協定的時候也要分成兩大部份去看。

- 支援OpenFlow的switch
  - Flow Table(存放規則)
    - Header Fields
    - Counters
    - Actions
  - Matching(配對條件流程)
  - Secure Channel
- OpenFlow Protocol Message
  - Controller-to-Switch
  - Asynchronous
  - Symmetric





## Reference 

> - [OpenFlow 1.0 spec](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.0.0.pdf)
> - [OpenFlow 1.3 spec](https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf)
> - [OpenFlow：简述对OpenFlow协议的认识](https://blog.csdn.net/qq_29229567/article/details/88796456)
> - [软件定义网络基础---OpenFlow流表](https://www.cnblogs.com/ssyfj/p/11620375.html)