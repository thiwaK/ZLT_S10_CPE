# Let's Hacking Into ZLT S10 4G CAT4 CPE

[img]

The ZLT S10 4G CAT4 CPE is a widely used, low-cost router offered by ISPs for home broadband connections in Sri Lanka (also in other countries too). This device manufacturered by Tozed Kangwei, providing customized versions to meet specific ISP's requirements.

Although the manufacturers advertise the ZLT S10 with an extensive list of specifications, the versions provided to end users often come with significant limitations, such as restricted frequency bands and reduced functionality.

In Sri Lanka, certain ISPs like Mobitel and Hutch supply ZLT S10 routers that can relatively easily unlocked or openlined by tweaking system configurations. However, routers provided by Dialog Axiata include additional layers of restrictions, going beyond standard configuration settings and making it more challenging for users to unlock or modify the device.



## Device Specifications

### Hardware Specifications

**Hardware**
|   |   |
| ------------------------ | --------------------------- |
| Chipset                  | ZX297520V3E                 |
| RAM                      | 64Mb (?)                    |
| Flash                    | 128Mb (DS35M1GA-IB) (NAND)  |
| Architecture             | ARMv7                       |
| Ports                    | USBx1; RJ45x1               |
| Buttons                  | WPS; WIFI; Reset            |

**Frequency Bands**
|   |   |
| ------------------------ | ------------------------------------- |
| LTE Bands (TDD)          | 38, 39, 40, 41                        |
| LTE Bands (FDD)          | 1, 2, 3, 4, 5, 7, 8, 20, 28           |
| LTE Bands (FDD)\*\*      | 12, 13, 17, 66                        |
| HSPA/UMTS Bands          | B1, B2, B5, B9                        |
| GSM Bands                | 850MHz; 900MHz; 1800MHz; 1900MHz      |
| LTE MIMO                 | Tx 1; Rx 2                            |
| LTE Antenna              | Built-in 2(3dBi); External 2(5dBi)    |
| LTE Max Throughput       | Up 150Mbps; Down 50Mbps               |

**WiFi**
|  |  |
| ------------------------ | ------------------------------------- |
| Wi-Fi Frequency          | 2.4 GHz                               |
| Wi-Fi Antenna            | Build-in 2(3dBi); External None       |
| Wi-Fi protocols          | ??                                    |
| Wi-Fi MIMO               | Tx 2; Rx 2                            |

#### Band Info (LK)

**Note**: This list includes only the frequency bands actively used by Sri Lankan ISPs for GSM, HSPA/HSPA+/UMTS, and LTE technologies.

##### *GSM*
| Band Name          | Used By                     |
| ------------------ | --------------------------- | 
| B? 900MHz (E-GSM)  | Mobitel/Dialog/Hutch/Airtel |
| B? 1800MHz (DCS)   | Mobitel/Dialog/Hutch/Airtel |

##### *HSPA/UMTS*
| Band Name  | Used By                     |
| ---------- | --------------------------- | 
| B1 2100MHz | Mobitel/Dialog/Hutch/Airtel | 

##### *LTE FDD*
| Band Name      | Used By              |
| -------------- | -------------------- |
| B1 (2100MHz)   | Mobitel/Airtel       |
| B3 (1800MHz +) | Mobitel/Dialog/Hutch |
| B5 (850MHz)    | Airtel               |
| B7 (2600MHz)   | Airtel               |
| B8 (900MHz)    | Mobitel/Hutch        |

##### *LTE TDD*
| Band Name   | Used By |
| ----------- | ------- |
| B40 2300MHz | Dialog  |
| B41 2500MHz | Mobitel |

---


### Software Specifications

|  |  |
| ----------------- | -------------- |
|  Kernal           | Linux-3.4      |
|  2nd Stage Loader | U-Boot 2011.09 |
|  Machine          | TSP ZX297520V3 |
|  File System      | UBI            |

---




## Debugging

### Hardware Debugging

#### UART (Universal Asynchronous Receiver-Transmitter)
UART is used to access a serial console for low-level interaction, such as bootloader access or kernel debugging. To access this interface, disassembling the router is required.

As shown in Picture A, there are set of three pinholes. You can solder header pins, attach wires, or use clip connectors to access them. Once connected, you need a USB-to-TTL converter, such as the CP2102 (Picture B), which is an inexpensive and reliable option.

For software, you can use terminal applications like PuTTY on Windows, screen on Linux, or other similar tools to interact with the UART interface.


#### JTAG (Joint Test Action Group)
JTAG is typically used for debugging at the processor or memory level. It provides full control over hardware, including the ability to read/write registers and memory.

There are pads that appear to be for JTAG (as shown in the picture). However, since I don't have JTAG debugging hardware, this interface could not be verified.

---

### Software Debugging

#### ADB
ADB is a software debugging interface that allows access to the device’s file system, running commands, and debugging at the OS level.

This interface can be accessed via USB or over the network. While direct access to ADB over the network is not  available, there are workarounds to do so. Over USB, ADB access is possible if you modify the system configurations to support it.

In older firmware versions, there was an option in the web configuration interface to enable ADB. However, this option is not available in newer firmware versions. To access ADB in such cases, you need to manually modify the system configuration, which requires shell access.

---

## Accessing Shell
Still, there are seveeral ways you can gain a shell access to the device over several methods.

### Exploits

### Hardware Debugging

## NAND Flash


## Dumping Firmware

