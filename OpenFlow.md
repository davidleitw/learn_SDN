# OpenFlow1.0協定講解

## 前言

想要深入了解一個協定的內容，看規格書是最快的，因為剛開始學習 SDN 相關的知識，所以目前正在讀OpenFlow1.0相關的內容，這篇文章會先主要介紹**OpenFlow 1.0的架構**，以及一些 spec 的整理。

之後也會整理一些 OpenFlow 1.3版本的內容，並且簡單描述跟 OpenFlow 1.0的差異。

### 為什麼會著重在1.0與1.3兩個版本呢？

> 1.0版本與之後的版本不兼容，所以1.0要最先介紹。 **1.0以及1.3版本被選為長期支持的穩定版本** 1.3為目前的主流版本，**多數支持OpenFlow的硬體是支援OpenFlow1.3**
> 
> 參考資料: [OpenFlow 協定演進](https://blog.csdn.net/qq_29229567/article/details/88797395)

底下會依照 OpenFlow 1.0 spec 的編排，去依據介紹完整的協定。

* [**Switch Components**](#OpenFlow-1.0-架構)
  * [Flow Table(存放規則)](#Flow-Table)
    * [Header Fields](#Header-Fields)
    * [Counters](#Counters)
    * [Actions](#Actions)
* [**Matching (配對條件流程)**](#Matching)
* [**Secure Channel**](#Secure-Channel)
* [**OpenFlow Protocol Message**](#OpenFlow-Protocol-Message)
  * [Controller-to-Switch](#Controller-to-Switch)
  * [Asynchronous](#Asynchronous)
  * [Symmetric](#Symmetric)

## OpenFlow 1.0 架構

![](https://imgur.com/AioLuDj.jpg)
**OpenFlow 1.0 spec 架構圖**

--- 

## Flow Table

![](https://imgur.com/YazXiG6.jpg)

在 **OpenFlow Switch** 中存放轉發規則的表稱之為 ```Flow Table``` 

> OpenFlow 1.0 中每個Switch只能存放一個Flow Table 

```Flow Table```中每個項目被稱為 ```Flow Entry``` 
在 **OpenFlow 1.0** 中，每個 ```Flow Entry``` 中都包含三個部份

- ```Header Fields```
- ```Counters```
- ```Actions```

### Header Fields

**OpenFlow 1.0** 協定中共有12種可供匹配的條件， IP部份只支援IPv4。

分別如下，僅列出條列，細節說明請參考 **OpenFlow 1.0 spec**
- L1
    - **Ingress Port**: 封包進入 ```Switch``` 的Port
- L2
    - **Ether source**: 來源Mac Address
    - **Ether dst**: 目標Mac Address
    - **Ether type**: [乙太類型](https://zh.wikipedia.org/wiki/%E4%BB%A5%E5%A4%AA%E7%B1%BB%E5%9E%8B)
    - **VLAN ID**
    - **VLAN priority**
- L3
    - **IPv4 source**: 來源IP Address
    - **IPv4 dst**: 目標IP Address
    - **IPv4 proto**: [IP協定表](https://zh.wikipedia.org/wiki/IP%E5%8D%8F%E8%AE%AE%E5%8F%B7%E5%88%97%E8%A1%A8)
    - **IPv4 Tos bits**: [Type of service](https://en.wikipedia.org/wiki/Type_of_service)
- L4
    - **TCP/UDP source port**
    - **TCP/UDP dst port**

![](https://i.imgur.com/3BGpIr4.png)

### Counters

```Counter``` 會針對每張 ```Flow Table```, 每條 ```Flow entry```, 每個 switch 上的 port 以及每個佇列分別紀錄一些相關資訊。

![](https://i.imgur.com/exsmUoB.png)


### Actions

每一個 ```Flow entry``` 都伴隨著0或者多個 ```actions```， ```actions```代表今天封包匹配某個 ```Header fields``` 的條件成功之後會執行的動作。

假設匹配成功之後發現沒有設置 ```actions```， 此時 ```Switch``` 就會把**封包丟棄(dropped)**，匹配成功之後執行 actions list 必定會按照原本的順序**依序執行**。

> - 如果 Controller 將 Flow entry 寫入 Switch 時，Swich 不支援某些 actions，則會被拒絕寫入 Switch 並且返回錯誤。
> - 當 Controller 在與 Switch 做連結時，Switch 就會告知 Controller 哪些 **Optional Action** 指令是它支援的。

```Switch``` 並不需要支援所有在 spec 裡面提及的 ```action```， 只有標注 **Required Action** 的才是一定要支援的，標注 **Optional Action** 的則是選用。

#### Required Action: Forward(轉發封包)

轉發除了要支援基本的 Switch port 之外， 也要支援以下的 **virtual port**。

![](https://i.imgur.com/tgv3Nbj.png)

也有兩個 **Optional Action** 的 **virtual port**， ```Switch``` 可以自行選擇要不要支援。

![](https://i.imgur.com/UdCjSyJ.png)


#### Required Action: Drop(丟棄封包)

除了可以設定 Drop action 之外， 假設今天有 ```Flow entry``` 沒有設定 ```action```，switch 也會預設把封包丟棄。

#### Optional Action: Enqueue

Enqueue 可以將封包轉發至某個特定 port 的 queue 中，便於支援```QoS```。

#### Optional Action: Modify-Field(修改封包)

基本上最有彈性的 **Modify-Field** 雖然是標注為 **Optional Action**，但是 spec 有提到此功能可以大大提昇 OpenFlow 的實用性，基本上所有支援 OpenFlow 的 ```Switch``` 都會支援。

![](https://i.imgur.com/8L2cErK.png)

---

## Matching

### Packet flow in an OpenFlow switch: 封包處理流程 

![](https://i.imgur.com/QD4VWvh.png)

> Parse header fields步驟會按照下方的圖表進行

封包會按照 ```flow entry``` 的優先度依序進行匹配
- 匹配成功
    - 更新 ```Counter```，並且按照 ```actions``` 去執行
    - 假設匹配到的 ```flow entry``` 並沒有設置 ```actions```， 則**丟棄**此封包
    - 假設**沒有匹配**到任何符合條件的 ```flow entry```，則將**封包轉發至 ```Controller```**

### 解析封包獲得 Header field 用以檢索符合的 Flow entry

![](https://i.imgur.com/wJHVTOf.png)

#### 解析步驟可以簡單劃分成底下四點

- 初始化 ```Headers```
    - 設置 Ingress Port
    - 設置 Ethernet src, dst, type
    - 其餘欄位設成0
- 根據 Eth type 填寫 ```Header```
    - Eth type: 0x8100(802.1q)
        - 設置 VLAN ID 跟 優先度
    - Eth type: 0x0806(ARP) => **Optional**
        - 設置 IPv4 src, dst
    - Eth type: 0x0800(Ipv4)
        - 設置 IPv4 src, dst, toc
- 根據 IPv4 封包來確定是TCP/UDP/ICMP協定
- 寫入TCP/UDP/ICMP協定資料

## Secure Channel

作為連結 ```Switch``` 與 ```Controller``` 的橋樑。

## OpenFlow Protocol Message

> 記得,OpenFlow 是定義 Controller 與 Switch 溝通的通訊協定

OpenFlow 協定訊息分成三大類
- **Controller-to-Switch**: 此類消息通常由 ```Controller``` 主動發出
- **Asynchronous**: 此類消息通常由 ```Switch``` 主動發出
- **Symmetric**: 此類消息 ```Controller``` 以及 ```Switch``` 都可以發出

### Controller-to-Switch

- **Features** 
    ```Features message``` 是初始化建立 TLS 連線時由 ```Controller``` 發送， 要求 ```Switch``` 回覆它支援的 Option 功能。
- **Configuration**
    ```Controller``` 可以用 ```Configuration message``` 來設置或者查詢 Switch 的配置訊息。
- **Modify-State**
    ```Modify-State message``` 可以用來新增/修改/刪除位在 Switch 上的 ```Flow Table```，也可以拿來設置 Switch 上 port 的屬性。
- **Read-State**
    ```Read-State message``` 用來讀取 ```Switch's Flow Table``` 狀態/統計資料以及 ```port``` 的狀態。
- **Send-Packet**
    ```Send-Packet message``` 用來傳送資料到指定 ```Switch``` 的 ```port```。
- **Barrier**
    ```OFPT_BARRIER_REQUEST```、```OFPT_BARRIER_REPLY```。

### Asynchronous

- **Packet-in**
    ```Packet-in message``` 會在兩種情況觸發, 轉送封包去 ```Controller```。
    - 沒有 match 到任何的 ```Flow entry```
    - match 到的 ```Flow entry``` 有著 ```packet-in action```
    
    假設 Switch 還有足夠的 memory 去緩衝 packet 資料，```Switch``` 會傳送部份的 ```packet header``` (默認128 bytes) 以及 ```buffer ID``` 給 ```Controller```。
    
    對於不支援緩存的 ```Switch``` 或者 memory 空間不足的情況，```Packet-in``` 事件會把完整的 packet 轉送給 ```Controller```。
- **Flow-Removed**
    在 ```Controlle```r 傳送 ```flow modify message``` 時， 在封包裡面可以選擇填入 ```idle timeout```, ```hard timeout```。
    - ```idle timeout```: ```Counter``` 會紀錄 ```flow entry``` 最後被 match 的時間點，如果超過就刪除。
    - ```hard timeout```: ```Counter``` 會紀錄 ```flow entry``` 被建立的時間，如果超過就刪除。

    ```Flow-Removed message``` 會在 Switch 刪除某條 ```Flow entry``` 時被觸發，傳訊告知```Controller```。
    
- **Post-status**
    在 ```Switch port``` 狀態改變時，傳送狀態更新給 ```Controller```。
- **Error**
    ```Switch``` 回傳錯誤訊息。

### Symmetric

- **Hello**
    初始化 OpenFlow 連線時使用。
- **Echo**
    ```Echo request/reply messages``` 可以由 ```Controller``` 或者 ```Switch``` 發起 ```request```，收到的一方必須回覆 ```reply```，可以藉此測試延遲，頻寬還有連線的狀況。
- **Vendor**
    自定義訊息

## Reference 

> - [OpenFlow 1.0 spec](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.0.0.pdf)
> - [OpenFlow 1.3 spec](https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.0.pdf)
> - [OpenFlow：简述对OpenFlow协议的认识](https://blog.csdn.net/qq_29229567/article/details/88796456)
> - [软件定义网络基础---OpenFlow流表](https://www.cnblogs.com/ssyfj/p/11620375.html)
> - [OpenFlow 1.0 協議講解](https://blog.csdn.net/lady_killer9/article/details/104540806)