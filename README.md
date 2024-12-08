# Let's Hacking Into ZLT S10 4G CAT4 CPE

![\*Device Image\*](/assets/images/ZLT_S10.png)

The ZLT S10 4G CAT4 CPE is a widely used, low-cost router offered by ISPs for home broadband connections in Sri Lanka (also in other countries too). This device manufacturered by Tozed Kangwei, providing customized versions to meet specific ISP's requirements.

Although the manufacturers advertise the ZLT S10 with an extensive list of specifications, the versions provided to end users often come with significant limitations, such as restricted frequency bands and reduced functionality.

In Sri Lanka, certain ISPs like Mobitel and Hutch supply ZLT S10 routers that can relatively easily unlocked or openlined by tweaking system configurations. However, routers provided by Dialog Axiata include additional layers of restrictions, going beyond standard configuration settings and making it more challenging for users to unlock or modify the device.

[[toc]]

## Device Specifications

### Hardware Specifications

**Hardware**
|   |   |
| ------------------------ | --------------------------- |
| Chipset                  | ZX297520V3E                 |
| RAM                      | 64Mb (?)                    |
| Flash                    | 128Mb (DS35M1GA-IB) (NAND)  |
| Architecture             | ARMv7                       |
| Ports                    | USB x1; RJ45 x1             |
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

<details>
<summary><h4>Band Info (LK)</h4></summary>

> [!NOTE]
> This list includes only the frequency bands actively used by Sri Lankan ISPs for GSM, HSPA/HSPA+/UMTS, and LTE technologies.

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

</details>

---


### Software Specifications

|  |  |
| ----------------- | -------------- |
|  Kernal           | Linux-3.4      |
|  2nd Stage Loader | U-Boot 2011.09 |
|  Machine          | TSP ZX297520V3 |
|  File System      | UBI            |

---


## Getting Shell Access

> [!NOTE]
> There are several ways you can gain a shell access to the device. Depending on your current firmware version, some methods may or may not work as expected.

### Over Debug Interfaces

#### ADB
> Provide high-level access to the command-line interface.

* Debugging
* Running shell commands
* Transferring files
* Over network or USB

This interface can be accessed via USB or over the network. Direct access over the network is not available, but there are workarounds. Over USB access is possible if you modify the system configurations to support it and you have USB male-to-male cabale.

In older firmware versions, there was an option in the web configuration interface to enable ADB. However, this option is no available in newer firmware versions. To access ADB in such cases, you need to manually modify the system configuration, which requires shell access or manual request crafting.

Since you don't have shell access, you have to send these requests to the device after login in to enable ADB

```shell
# Enable USB Port
url: http://[HOST]/goform/goform_get_cmd_process
method: POST
payload: {'isTest': 'false', 'goformId': 'TZ_SET_USB_STATUS', 'usbPortEnable': '1', 'usbDownloadEnable': '1'}

# Enable ADB
url: http://[HOST]/goform/goform_get_cmd_process
method: POST
payload: {'isTest': 'false', 'goformId': 'TZ_CMD_SECURE_LOGIN', 'telnetdEnable': 'n', 'adbEnable': 'y', 'dropbearEnable': 'n'}
```
> [!NOTE]
> Optionally, you can enable telnet and/or dropbeer by setting the corresponding values to `'y'`, which also you can gain shell access but with password (which we may never find) ;-(.


#### UART (Universal Asynchronous Receiver-Transmitter)
> Lower-level access to the device's hardware and software (bootloader, kernel)

* Serial communication
* Simple text based in and out
* Basic debugging and monitoring

To access this interface, disassembling the router is required.

As shown, there are set of three pinholes. You can solder header pins, attach wires, or use clip connectors to access them. Once connected, you need a USB-to-TTL converter, such as the CP2102 (Picture B), which is an inexpensive and reliable option.

For software, you can use terminal applications like PuTTY on Windows, screen on Linux, or other similar tools to interact with the UART interface.

#### JTAG (Joint Test Action Group)
> Very low-level access to the device's hardware.

* Debugging at hardware level
* Access to memory and registers
* Single stepping through code

JTAG is typically used for debugging at the processor or memory level. It provides full control over hardware, including the ability to read/write registers and memory.

There are pads that appear to be for JTAG (as shown in the picture). However, since I don't have JTAG debugging hardware, this interface could not be verified.


### Exploits

### Debug interfaces

## NAND Flash


## Dumping Firmware

