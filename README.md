<div align="center">
      <h1 align="center">Let's Hacking Into ZLT S10 4G CAT4 CPE 🔓</h1>
      <i>A Comprehensive Guide to Unlocking, Dumping, and Modifying Firmware on ZX297520 based Routers</i>
</div>

---

<tt> This repository provides a technical walkthrough for modding the `ZLT S10` Router, which is powered by the `ZX297520V3E` SoC. Whether you're a security researcher, embedded systems enthusiast, or simply exploring how to unlock and debrand carrier-locked devices, this guide offers directions for gaining shell access to reflashing modified firmware dumps.
</tt>

---

![\*Device Image\*](/assets/images/ZLT_S10.png)
<br>
<details>
<summary>Story</summary>
<br>
The ZLT S10 4G CAT4 CPE is a widely used, low-cost router offered by several ISPs for home broadband connections in Sri Lanka. This device (distributed in Sri Lanka), manufactured by Tozed Kangwei, provides customized versions to meet specific ISPs’ requirements.
<br><br>
Although the manufacturer (Tozed Kangwei) advertises the ZLT S10 with an extensive list of specifications, the versions provided to home users often come with significant limitations, such as restricted frequency bands and reduced functionality.
<br><br>
In Sri Lanka, ISPs like `SLTMobitel` and `Hutchison Telecommunications Lanka` supply ZLT S10 routers that can be easily unlocked or openlined by tweaking system configurations. However, routers provided by `Dialog Axiata` include additional layers of restrictions, going beyond standard configuration settings and making it more challenging for users to unlock or modify the device.
<br>
</details>
<br>

> [!NOTE]
> ⚠️ ***This content is provided strictly for educational and research purposes. Modifying firmware or hardware may void warranties or violate local regulations. Proceed at your own risk.***

<hr>

**Contents**

<ul>
	<li><a href="#device-specifications">Device Specifications</a></li>
		<ul>
			<li><a href="#hardware-specifications">Hardware Specifications</a></li>
				<ul>
					<li><a href="#frequency-bands">Frequency Bands</a></li>
					<li><a href="#wifi">WiFi</a></li> 
	            </ul>
            <li><a href="#software-specifications">Software Specifications</a></li>
        </ul>
	<li><a href="#mobile-network-info-lk">Mobile Network Info (LK)</a></li>
		<ul>
			<li><a href="#frequency-bands">Frequency Bands</a></li>
			<li><a href="#mcc-and-mnc-code">MCC and MNC Code</a></li> 
	    </ul>
    <li><a href="#getting-shell-access">Getting Shell Access</a></li>
        <ul>
			<li><a href="#over-debug-interfaces">Over Debug Interfaces</a></li>
				<ul>
					<li><a href="#adb-android-debug-bridge">ADB (Android Debug Bridge)</a></li>
					<li><a href="#uart-universal-asynchronous-receiver-transmitter">UART (Universal Asynchronous Receiver-Transmitter)</a></li>
					<li><a href="#u-boot-Shell-over-uart">U-Boot Shell over UART</a></li>
				</ul>
			<li><a href="#exploiting-code-execution-vulnerabilities">Exploiting Code Execution Vulnerabilities</a></li>
        </ul>
    <li><a href="#openline-unlock-debrand">Openline/Unlock/Debrand</a></li>
    	<ul>
			<li><a href="#method-one">Method One (Config)</a></li>
            <li><a href="#method-two">Method Two (NVRAM)</a></li>
        </ul>
    <li><a href="#dumping-firmware">Dumping Firmware</a></li>
        <ul>
            <li><a href="#accessing-nand-flash">Accessing NAND Flash</a></li>
        </ul>
    <li><a href="#parsing-the-raw-dump">Parsing the Raw Dump</a></li>
        <ul>
            <li><a href="#unpackingrepacking">Unpacking/Repacking</a></li>
        </ul>
    <li><a href="#firmware-configuration-update">Firmware/Configuration Update</a></li>
        <ul>
            <li><a href="#update-methods">Update Methods</a></li>
                <ul>
	                <li><a href="#management-server-cwmp">Management Server (CWMP)</a></li>
	                <li><a href="#tftp-recovery-mode">TFTP (Recovery Mode)</a></li>
	                <li><a href="#web-interface">Web Interface</a></li>
                </ul>
            <li><a href="#firmware-bundle-contents">Firmware Bundle Contents</a></li>
                <ul>
                    <li><a href="#required-files-in-firmware-bundles">Required Files in Firmware Bundles</a></li>
                    <li><a href="#additional-required-files-in-newer-firmware-versions">Additional Required Files in Newer Firmware Versions</a></li>
                    <li><a href="#configuration-updates">Configuration Updates</a></li>
                </ul>
        </ul>     
</ul>

## Device Specifications

### Hardware Specifications

|    |    |
| ------------------------ | --------------------------- |
| Chipset                           | ZX297520V3E                         |
| RAM                                 | 64Mb (?)                              |
| Flash                              | 128Mb (DS35M1GA-IB) (NAND)   |
| Architecture                   | ARMv7                                  |
| Ports                              | USB x1; RJ45 x1                   |
| Buttons                           | WPS; WIFI; Reset                  |

#### Frequency Bands
|    |    |
| ------------------------ | ------------------------------------- |
| LTE Bands (TDD)               | 38, 39, 40, 41                                    |
| LTE Bands (FDD)               | 1, 2, 3, 4, 5, 7, 8, 20, 28                |
| LTE Bands (FDD)\*\* | 12, 13, 17, 66                                    |
| HSPA/UMTS Bands               | B1, B2, B5, B9                                    |
| GSM Bands                        | 850MHz; 900MHz; 1800MHz; 1900MHz         |
| LTE MIMO                         | Tx 1; Rx 2                                          |
| LTE Antenna                     | Built-in 2(3dBi); External 2(5dBi)      |
| LTE Max Throughput          | Up 150Mbps; Down 50Mbps                      |

#### WiFi
|   |   |
| ------------------------ | ------------------------------------- |
| Wi-Fi Frequency               | 2.4 GHz                                              |
| Wi-Fi Antenna                  | Build-in 2(3dBi); External None          |
| Wi-Fi protocols               | ??                                                      |
| Wi-Fi MIMO                      | Tx 2; Rx 2                                          |

<details>
<summary>Mobile Network Info (LK)</summary>

## Mobile Network Info (LK)

### Frequency Bands

#### GSM
| Band Name               | Used By                               |
| ------------------ | --------------------------- | 
| B? 900MHz (E-GSM)   | Mobitel/Dialog/Hutch/Airtel |
| B? 1800MHz (DCS)    | Mobitel/Dialog/Hutch/Airtel |

#### HSPA/UMTS
| Band Name   | Used By                               |
| ---------- | --------------------------- | 
| B1 2100MHz | Mobitel/Dialog/Hutch/Airtel | 

#### LTE FDD
| Band Name         | Used By                     |
| -------------- | -------------------- |
| B1 (2100MHz)    | Mobitel/Airtel          |
| B3 (1800MHz +) | Mobitel/Dialog/Hutch |
| B5 (850MHz)      | Airtel                      |
| B7 (2600MHz)    | Airtel                      |
| B8 (900MHz)      | Mobitel/Hutch            |

#### LTE TDD
| Band Name    | Used By |
| ----------- | ------- |
| B40 2300MHz | Dialog   |
| B41 2500MHz | Mobitel |

### MCC and MNC Code

</details>

---


### Software Specifications

|                            |   |
| ----------------- | -------------- |
|   Kernel                | Linux-3.4         |
|   2nd Stage Loader | U-Boot 2011.09 |
|   Machine               | TSP ZX297520V3 |
|   File System         | UBI                  |

---


## Getting Shell Access

> [!NOTE]
> There are several ways to gain shell access to the device. Depending on your current firmware version, some methods may or may not work as expected.

### Over Debug Interfaces

#### ADB (Android Debug Bridge)

> ADB provides high-level access to the device’s command-line interface, enabling you to run shell commands, transfer files, and debug the device. It can be accessed over USB or, with some workarounds, over the network.

To access ADB over USB.
1. You must modify the system configurations to support it 
2. You must have a USB male-to-male cable
3. You must install ADB drivers and have the ADB executable
4. You may need to log in to the router as the admin

In older firmware versions (older than 1.13.x), there was an option in the web configuration interface to enable ADB. However, this option is no longer available. In such cases, you can send the following requests to modify the system configuration to support ADB.

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

> UART provides lower-level access to the device’s software (bootloader, kernel, etc.). It allows serial communication and is useful for debugging, monitoring/logging. However, as it is not possible to interrupt bootup due to the bootloader configuration, the functionality of the UART is limited.

> [!CAUTION]
> Disassembling the router is required to access this interface. Disassembling the device may void your warranty. Proceed with caution.

To access the UART;
1. You must have a USB-to-TTL converter/adapter
2. You must correctly connect Rx, Tx, and GND cables

On the device, the pins are organized as
```
[ Rx | GND | Tx ]
```

As shown in the image (orange box), there is a set of three pinholes. You can solder header pins, attach wires, or use clip connectors to access them. 

For software, you can use terminal applications like PuTTY on Windows, screen on Linux, or other similar tools to interact with the UART interface.


#### U-Boot Shell over UART

During the device boot process, `U-Boot` (the second stage loader) is responsible for performing file system checks and loading the Linux kernel. If there is an error, such as a checksum failure or file system corruption, U-Boot will stop execution and drop into an interactive shell (hushshell), which is only accessible via UART (serial interface).

This shell provides low-level access to the device and can typically be used for diagnostics and recovery. The following commands are available to use.

| Command |   Description |
| -------- | --------------------------- |
| 0            | do nothing, unsuccessfully   |
| 1            | do nothing, successfully |
| ?            | alias for 'help' |
| badblock_query | is support bad block query |
| base       | print or set address offset |
| bbt_count | bbt_count |
| bdinfo    | print Board Info structure |
| bootm      | boot application image from memory |
| bootz      | NAND sub-system |
| cmp         | memory compare |
| compat_read | upload: compat_read [partition][offset][size] |
| compat_write | download: compat_write [partition][offset][size] |
| coninfo   | print console devices and information |
| cp          | memory copy |
| crc         | crc_check |
| crc32      | checksum calculation |
| dcache    | enable or disable data cache |
| dl          | dl : dl [sign] |
| downloader | Perform ZIXC TSP downloader |
| downver   | upgrade software downloaded from TFTP server |
| echo       | echo args to console |
| editenv   | edit environment variable |
| efuse_program | efuse_program: program [puk_hash/secure_en/chip_flag] [hash0/enable/SPE][hash1][hash2][hash3] |
| efuse_read | efuse_read: read [devid] |
| env         | environment handling commands |
| erase      | Erase nand: erase [partition] |
| exit       | exit script |
| fsinfo    | print information about filesystems |
| fsload    | load binary file from a filesystem image |
| getvar    | Downloader get information: getvar [info] |
| go          | start application at address 'addr' |
| help       | print command description/usage |
| icache    | enable or disable instruction cache |
| loop       | infinite loop on address range |
| ls          | list files in a directory (default /) |
| md          | memory display |
| mm          | memory modify (auto-incrementing address) |
| mtest      | simple RAM read/write test |
| mw          | memory write (fill) |
| nand       | NAND sub-system |
| nm          | memory modify (constant address) |
| nor         | SPINAND sub-system |
| part_bbc | partition bad block count |
| part_valid_space_query | get partition valid physics space size |
| ping       | send ICMP ECHO_REQUEST to network host |
| printenv | print environment variables |
| ram_start | ram_start: ram_start |
| read_board_type | read board type. |
| reboot    | reboot: reboot |
| reset      | Perform RESET of the CPU |
| run         | run commands in an environment variable |
| set         | set : set [module] [size] |
| setenv    | set environment variables |
| showvar   | print local hushshell variables |
| single_part_bbc | single partition bad block count |
| test       | minimal test like /bin/sh |
| testusb   | testusb: testusb [size] |
| tftp       | boot image via network using TFTP protocol |
| tftpput   | TFTP put command, for uploading files to a server |
| version   | print monitor, compiler and linker version |


### Exploiting Code Execution Vulnerabilities

Certain code execution vulnerabilities stem from improper handling (without proper sanitization) of arguments passed into the GoAhead backend. Although many of these flaws have been addressed and patched in recent firmware updates, some may still be present in older versions.

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

## Openline/Unlock/Debrand

### Method One

> [!WARNING]
> Depending on your ISP and firmware version, the following configurations may not work as expected.

> [!CAUTION]
> Improper configuration of the device may result in a state of bootloop, invalid SIM card, signal failure, or other issues.

For most S10 routers, the following modifications should give the expected result.

1. Edit `/etc_ro/default/default_parameter_sys`
```shell
tr069_app_enable=0
tz_lock_band_state=no
tz_lock_plmn_state=no
tz_lock_plmn_list=
```

2. Edit `/yaffs/apply_config.conf`
```shell
tz_lock_plmn_state_s="no"
tz_lock_plmn_list_s=""
```

> [!NOTE]
> Disabling band and PLMN locks may lead to reduced signal strength or inconsistent connectivity. It’s recommended to adjust these settings based on your specific needs for optimal performance.

> [!TIP]
> You can choose the matching PLMN for your network using this table.


### Method Two
However, there are routers (as stated above) that require additional modifications to the NVRAM to get the expected result. (Most forums and groups state that those devices are impossible to debrand/openline. But that statement is a false positive.) You can find the modified NVRAM file [here](https://mega.nz/file/eSZFxIJZ#Vf70fdWHV7z9jJTWjNl1fiSWpr_J7uXyJ0k5gIRtiN8). Replace this file with the file in `/mnt/nvrofs/`

<br>

> [!WARNING]
> Backup your current NVRAM before proceeding.

> [!CAUTION]
> The NVRAM provided here comes with the IMEI of `000000000000000` and MAC of `00:00:00:00:00:00`. Using this without changing the IMEI can lead to unknown issues.

> [!CAUTION]
> Your WIFI PSK and SSID will be changed after applying this file. Proceed with caution.

> [!NOTE]
> PLEASE DO NOT SHARE THIS FILE ON YouTube or OTHER SOCIAL MEDIA PLATFORMS.

<br>

The NVRAM provided here comes with `TDD`, `FDD`, and `WCSMA` enabled (no `GSM` and `TDS`). And with the support for LTE bands `band1`, `band3`, `band5`, `band8`, `band38`, `band39`, `band40`, `band41`, which covers all the FDD and TDD LTE bands currently used in Sri Lanka (In other words, every mobile or router SIM with LTE support should work). Although you can gain internet access via the IMEI of `000000000000000`, it is a bit risky. You should change the IMEI before use. Use the following table.

<br>

| item | offset | size |
| --- | --- | --- |
| IMEI | 0x0 | 0x8 |
| MAC | 0x7C | 0x6 |
| MAC | 0x2C0 | 0x6 |

---

## Dumping Firmware

Gaining shell access and dumping the full firmware is not always straightforward or even possible. For instance, if you're using UART, you may not be able to interrupt the bootloader. In such cases, dumping the firmware directly from the flash memory becomes an alternative, though it can be destructive.

To do this, you may need to desolder the chip, which requires specialized equipment (like a hot air station) and experience. If not done carefully, this process can damage the chip, melt nearby components, or create unwanted connections, ultimately rendering the device unusable.

Alternatively, you might try other methods, such as clipping to the pins or soldering wires directly. However, these methods don't always work and can also be destructive. When powering up the chip, other components may also activate, interfering with the process (as the NAND chip requires a small voltage, we are relatively safe). In such cases, desoldering the chip remains the most reliable solution.

> [!IMPORTANT]
> Proceed only if you have the necessary knowledge and experience.

### Accessing NAND Flash

<p float="left">
      <img src="/assets/images/Actual_DS35M1GA-IB.jpg" width="200"/>
      <img src="/assets/images/Size_DS35M1GA-IB.jpg" width="200"/>
</p>

As outlined in the hardware specifications of the device, this router is equipped with an 8-lead WSON NAND Flash chip (DS35M1GA-IB). Clipping WSON chips is extremely difficult. To access the chip, you must either solder wires directly to the chip while it is on the PCB or remove the chip for easier connection, either by soldering it to a separate PCB or using a socket.

I initially attempted the first method—soldering wires directly to the chip. While it may seem nearly impossible, using very thin copper wire can make this task feasible, and it works perfectly with careful handling.

![hooking](/assets/images/Hooking_DS35M1GA-IB.jpg)
![pinout](/assets/images/Pinout_DS35M1GA-IB.png)

To read the chip, you will need a NAND Flash chip reader, such as the CH341. Additionally, since this chip operates at 1.8V, an adapter is required to match its voltage.

> [!TIP]
> If you use *NeoProgrammer*, select W25N01GW as the Device.

> [!NOTE]
> For further info about the chip, [refer to this document](/assets/documents/Dosilicon-DS35M1GA-IB_C725999.pdf).

## Parsing the Raw Dump

### Unpacking/Repacking

> [!WARNING]
> The script is still not able to calculate the ECC. The repacked firmware after modification may not work. Use the non-OOB repack, which can work depending on the modifications.

Unpacking a SPI NAND dump requires an understanding of the physical NAND layout, including pages, blocks, out-of-band (OOB) data, and bad block management. Manually handling this process can be complex and error-prone. To simplify it, I’ve created a small utility script called [dump_parser.py](/src/dump_parser.py), which assists in unpacking and repacking NAND firmware dumps.

This script is written specifically for the NAND structure of the `DS35M1GA-IB` chip and the partition layout used in the `ZLT S10` device. As such, it is only compatible with this particular combination unless you adapt the script to match your own device's configuration.

When unpacked, the firmware is divided into the following partitions:

| Name    | File System |
| ----------- | ------- |
| zloader | No   |
| uboot | No   |
| uboot-mirr | No   |
| nvrofs | Yes   |
| imagefs | Yes   |
| rootfs | Yes   |
| userdata | Yes   |
| yaffs | Yes   |

> [!NOTE]
> Partitions without a file system contain raw binary data (bootloaders, preloaders, or low-level configuration). File system partitions can be mounted or explored using standard Linux tools once extracted.

## Firmware/Configuration Update

The ZLT S10 supports firmware and configuration updates through several methods.
- Remote update via management server (CWMP)
- TFTP-based recovery mode
- The device’s web interface

### Update Methods

#### Management Server (CWMP)

Firmware and configuration updates are often performed automatically by the ISP/Vendor using CWMP (CPE WAN Management Protocol). This is a hands-off, scheduled process controlled remotely and is not intended for manual use.

#### TFTP (Recovery Mode)
U-Boot provides a low-level recovery mechanism that allows firmware flashing via TFTP. However, this mode is only accessible when there is a critical issue, such as a corrupted file system or a kernel checksum failure. Even if you manage to access this interface, flashing via TFTP is challenging. It requires in-depth knowledge of low-level memory mapping and command-line tools within U-Boot (which I don't, unfortunately).

#### Web Interface
The device’s web interface offers a more user-friendly method for firmware or configuration updates. However, based on testing and reverse engineering, this method has several limitations. 

- It is not backward compatible.
- Firmware compatibility is tightly controlled by the ISP/Vendor.
- Even if your device has not been updated regularly, future firmware updates pushed by the CWMP or Web interface may fail to install.

This is primarily because ISPs and the Vendor frequently modify:
- Flashing procedures
- Firmware encryption mechanisms
- Integrity verification checks

##### File Format Requirements
Firmware updates through the web interface require specific file extensions (`.bin` or `.img`). The device treats these formats differently. (`.img` treated as a firmware bundle containing multiple components (see Firmware Bundle Contents below))

##### Access Requirements
To perform firmware updates via the web interface, you must log in as `admin` or `super admin`.

Super admin access is practically impossible, although you have the correct credentials. Simply, the device’s internal configurations do not allow it. However, logging in as an admin is sufficient to perform firmware and configuration updates, and it is possible.

> [!CAUTION]
> Using an incompatible firmware may brick the device or lock out access to features.

### Firmware Bundle Contents
Firmware uses the script named `updateit` in the firmware bundle to initiate the update process. After the firmware version 1.13.x, every version is encrypted by using a certificate. Which means creation of modified firmware is not possible unless you have the private certificate that is used in the encryption process.

#### Files in Firmware Bundles

| File Name | Purpose |
| --------- | ------- |
| imagefs.tgz | Contains binary images |
| rootfs.tgz | Contains the root filesystem |
| md5.txt | Verifies the integrity of the firmware files |
| set_fotaflag | Change the reboot flags (`recovery` or `normal`) |
| re_rc | Replacement script for recovery startup routines |
| rc | Replacement script for normal startup routines |
| encrypt.txt | Another firmware integrity verifier |
| updateit | Initiate the update process |

#### Configuration Updates

Some firmware bundles also include a configuration update file.

| File Name | Purpose |
| --------- | ------- |
| configupdate.zip | Contains system configuration settings |
