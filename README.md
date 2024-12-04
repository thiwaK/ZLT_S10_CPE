# Let's Hacking Into ZLT S10 4G CAT4 CPE

The ZLT S10 4G CAT4 CPE is a widely used, low-cost router offered by ISPs in Sri Lanka and many other countries. This device is designed as a generic model, with manufacturers like Tozed providing customized versions to meet specific ISP requirements.

Although the manufacturers advertise the ZLT S10 with an extensive list of specifications (see the tables below), the versions provided to end users often come with significant limitations, such as restricted frequency bands and reduced functionality.

In Sri Lanka, certain ISPs like Mobitel and Hutch supply ZLT S10 routers that can be relatively easily unlocked or openlined by tweaking system configurations. However, routers provided by Dialog Axiata include additional layers of restrictions, going beyond standard configuration settings and making it more challenging for users to unlock or modify the device.

[[toc]]

## Device Specifications

### Hardware Specifications

**Hardware**
|   |   |
| ------------------------ | ------------------------------------- |
| Chipset                  |           ZX297520V3E                 |
| RAM                      |            64Mb (?)                   |
| Flash                    |           128Mb (DS35M1GA-IB) (NAND)  |
| Architecture             |           ARMv7                       |
| Ports                    | USBx1; RJ45x1  |
| Buttons                  | WPS; WIFI; Reset |

**Frequency Bands**
|   |   |
| ------------------------ | ------------------------------------- |
| LTE Bands (TDD)          |           38, 39, 40, 41              |
| LTE Bands (FDD)          |           1, 2, 3, 4, 5, 7, 8, 20, 28 |
| LTE Bands (FDD) IDK      |           12, 13, 17, 66              |
| HSPA/UMTS Bands          | B1, B2, B5, B9                        |
| GSM Bands                | 850MHz; 900MHz; 1800MHz; 1900MHz      |
| LTE MIMO                 |           Transmit 1; Receive 2       |  
| LTE Antenna              | Built-in 2(3dBi); External 2(5dBi)    | 
| LTE Max Throughput       | Up 150Mbps; Down 50Mbps               |

**WiFi**
|  |  |
| ------------------------ | ------------------------------------- |
| Wi-Fi Frequency          | 2.4 GHz                               |
| Wi-Fi Antenna            | Build-in 2(3 dBi); External None         |
| Wi-Fi protocols          |           ??                          |
| Wi-Fi MIMO               | Transmit 2; Receive 2                 |

#### Band Info
Note: Inlcude only bands used by Sri Lankan ISPs only.

**Band Frequencies**

| GSM |
| Band Name          | Used By                     |
| ------------------ | --------------------------- | 
| B? 900MHz (E-GSM)  | Mobitel/Dialog/Hutch/Airtel |
| B? 1800MHz (DCS)   | Mobitel/Dialog/Hutch/Airtel |

| HSPA/UMTS |
| Band Name  | Used By                     |
| ---------- | --------------------------- | 
| B1 2100MHz | Mobitel/Dialog/Hutch/Airtel | 

| LTE TDD |
| Band Name   | Used By |
| ----------- | ------- |
| B40 2300MHz | Dialog  |
| B41 2500MHz | Mobitel |

| LTE FDD |
| Band Name      | Used By              |
| -------------- | -------------------- |
| B1 (2100MHz)   | Mobitel/Airtel       |
| B3 (1800MHz +) | Mobitel/Dialog/Hutch |
| B5 (850MHz)    | Airtel               |
| B7 (2600MHz)   | Airtel               |
| B8 (900MHz)    | Mobitel/Hutch        |



 

### Software Specifications

|  |  |
| ----------------- | --------------- |
|  Kernal           | Linux-3.4       |
|  2nd Stage Loader | U-Boot 2011.09  |
|  Machine          | TSP ZX297520V3  |
|  File System      | UBI             |

## Debugging

### Hardware Debugging
UART, JTAG

### Software Debugging
ADB


## NAND Flash