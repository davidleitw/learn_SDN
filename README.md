# learn_SDN

此專案用來整理一些學習 SDN 的相關知識以及參考資料。
由於剛開始學習沒多久，所以會著重於個人學習的**順序**，希望在寫心得的同時也可以幫助到一些想要研究 SDN 的朋友。

當然，由於我也是剛開始學習，所以整理的心得如果有誤也請各位前輩們指點

## 預備知識

在學習 SDN 之前我準備先複習了一輪 [computer networking a top-down approach 7th](https://www.ucg.ac.me/skladiste/blog_44233/objava_64433/fajlovi/Computer%20Networking%20_%20A%20Top%20Down%20Approach,%207th,%20converted.pdf)，之前大學學過的很多部份已經有點忘記了，所以先把傳統的網路概論複習一輪，之後進入SDN的學習時，才會比較清楚知道為什麼要提出SDN的概念，SDN具體來說是要解決哪些傳統架構無法解決的問題。

之後會陸續整理一點網路的基礎理論心得，讓之後SDN的一些概念比較好解釋。

## 什麼是 SDN 以及 SDN 的發展歷史

> 參考文章
> - [SDN 簡介](https://feisky.gitbooks.io/sdn/content/sdn/)
> - [SDN 發展趨勢](https://hackmd.io/@cnsrl/SJur_2twL)

傳統網路的一些特點:
- 每個節點是由設備單獨控制，屬於分散式架構。
- 控制面以及轉接面放在同一個設備上。
- 管理員無法直接的操作封包轉送行為，僅能控制設備的通訊協定，再藉由通訊協定的規則去操作設備。
- 通訊協定對於設備的影響是固定的，無法控制非自己協定內的規則。

SDN 想要採取集中式控制，要求轉接面跟控制面分離，實際上由遠端的 controller 計算以及分送每一個路由器的轉送表，管理員可以直接操作設備轉接封包的行為。

![](http://i.imgur.com/uF2pcH0.jpg)

SDN 並非一種技術，而是一種設計的理念，只要符合**控制面以及轉接面的分離**，以及開放的**可程式化**設計界面，就可以稱為 SDN 架構。通常 SDN 也伴隨著**集中控制**的特性，藉由在 controller 獲得的網路全局資料(並非傳統只能獲得局部資料)，根據其業務邏輯進行調整及優化。


## 常用名詞解釋

![](https://sites.google.com/a/cnsrl.cycu.edu.tw/da-shu-bi-ji/_/rsrc/1565708281052/sdn/sdn_architecture.png)


### Network Device 網路設備
網路設備不僅限於實體的設備(例如 switch ,路由器等等)，也有可能是虛擬的 switch (例如 OVS)，封包在網路設備之前被處理以及轉送。網路設備藉由 Southbound Interface 接收 controller 發過來的指令配置轉送的規則，也可以透過 Southbound Interface 來將一些資料回傳給 controller。

有時候網路設備也被稱為 **Data Plane**。

支援 OpenFlow 的 switch 會有以下功能
- 對於接收到的封包進行修改或針對指定的 port 進行轉送。
- 對於接收到的封包進行轉送到 Controller 的動作(Packet-In)。
- 對於接收到來自 Controller 的封包轉送到指定的連接埠(Packet-Out)。

### 南向界面(Southbound Interface/ Control Data Plane Interface)
南向界面是指 Data Plane 以及 Controller 之間的界面，在 SDN 架構中，希望南向界面是標準化的，這樣才可以讓軟體可以不受硬體的限制，在任何設備上都能執行，不過現在還只是理想。

目前主流的南向界面標準是 OpenFlow 協定，雖然還有其他各種南向界面，不過還是 OpenFlow 為大宗。

> 因為我也還是新手的緣故，所以也是從 OpenFlow 開始學習 SDN 的，此篇心得文也會著重在 OpenFlow 協定上。

### 控制器(Controller)
**Controller** 是 SDN 的核心，北向有應用程式提供業務邏輯經由 Controller 將轉送的規則藉由 Southbound Interface 傳給網路設備，屬於 SDN 架構中最重要的部份。

目前 Controller 百家爭鳴，有很多開源的 controller (例如 Ryu, FloodLight, NOX/POX)等等，也有很多公司開發的商用版本，本篇心得文會使用 Ryu 去做一些 OpenFlow 相關的實驗。

### 北向界面(Northbound Interface)
北向界面是指應用程式以及 Controller 之間溝通的界面，目前還沒有一個統一的標準，通常會因為狀況不同而採用不同的方案。

### Application(Services)
這裡的 Application 是指幾乎所有網路的應用，包含load balancing, security, monitoring 等等.. 應用程式的業務邏輯就透過 Controller 傳送規則給網路設備，讓設備彈性的執行我們要的功能。


## OpenFlow 協定
OpenFlow 為最有代表性的南向界面，被視為第一個 SDN 的標準之一。它最初在 SDN 環境中定義了通信協定，使 SDN 控制器能夠與物理和虛擬的交換機和路由器等網路裝置的轉發平面直接進行互動，從而更好地適應不斷變化的業務需求。

### 概述([維基百科](https://zh.wikipedia.org/wiki/OpenFlow))

OpenFlow 能夠啟動遠端的控制器，經由網路交換器，決定網路封包要由何種路徑通過網路交換機。這個協定的發明者，將它當成軟體定義網路（Software-defined networking）的啟動器。

OpenFlow 允許從遠端控制網路交換器的封包轉送表，透過新增、修改與移除封包控制規則與行動，來改變封包轉送的路徑。比起用存取控制列表 (ACLs) 和路由協定，允許更複雜的流量管理。同時，OpenFlow 允許不同供應商用一個簡單，開源的協定去遠端管理交換機（通常提供專有的介面和描述語言)。

### 協定內容

因為 OpenFlow 算是一個很有指標性的 SDN 協定，所以對於要學習 SDN 的人來說，他的 specification 也非常值得一看，我們會就 **OpenFlow** 獨立一個章節來談論。請點以下連結:

- [OpenFlow協定](https://github.com/davidleitw/learn_SDN/blob/master/OpenFlow.md)

--- 

> 參考資料
> - [OpenFlow 1.0 spec](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.0.0.pdf)
> - [OpenFlow: Enabling Innovation in Campus Networks](https://www.researchgate.net/publication/220195143_OpenFlow_Enabling_innovation_in_campus_networks)
> - [協定心得](https://www.cnblogs.com/ssyfj/tag/SDN/)


## 使用工具版本

* mininet: 2.3.0d6
* ryu-manager: 4.34

## 參考資料

* [Mininet Python API Reference](http://mininet.org/api/annotated.html)