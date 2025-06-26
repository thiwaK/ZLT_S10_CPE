import os
from construct import Struct, Int8ul, Array, Byte
from bchlib import BCH


PAGE_DATA_SIZE = 2048
PAGE_OOB_SIZE = 64
PAGES_PER_BLOCK = 64
BLOCKS_COUNT = 1024
PAGE_SIZE = PAGE_DATA_SIZE + PAGE_OOB_SIZE
BLOCK_SIZE = PAGES_PER_BLOCK * (PAGE_DATA_SIZE + PAGE_OOB_SIZE)

Page = Struct(
    "Data" / Array(PAGE_DATA_SIZE, Int8ul),
    "OOB" / Array(PAGE_OOB_SIZE, Int8ul)
)
Block = Struct(
    "Pages" / Array(PAGES_PER_BLOCK, Page)
)
Flash = Struct(
    "Blocks" / Array(BLOCKS_COUNT, Block)
)

# offset, length
PARTITIONS = {
    'zloader':[0x0, 0x20000],
    'uboot':[0x20000, 0x100000],
    'uboot-mirr':[0x120000, 0x100000],
    'nvrofs': [0x220000, 0x200000],
    'imagefs': [0x420000, 0x1000000],
    'rootfs': [0x1420000, 0x1E00000],
    'userdata': [0x3220000, 0x4960000],
    'yaffs': [0x7b80000, 0x200000]
}   

def extract(file_obj):
    
    for name, (offset, size) in PARTITIONS.items():
        file_obj.seek(offset)
        data = file_obj.read(size)

        output_path = os.path.join('extracts', f"{name}.bin")
        with open(output_path, 'wb') as out_file:
            out_file.write(data)
            print(f"Extracted {name}: offset=0x{offset:X}, size=0x{size:X} to {output_path}")

def create_clean_dump(file_obj, clean_dump_file, clean_dump_bb_file):

    file_obj.seek(0)
    if os.path.isfile(clean_dump_file):
        os.remove(clean_dump_file)
    if os.path.isfile(clean_dump_bb_file):
        os.remove(clean_dump_bb_file)

    with open(clean_dump_file, 'ab') as clean_dump, open(clean_dump_bb_file, 'ab') as clean_dump_bb:
        for block_index in range(BLOCKS_COUNT):
            block_data = file_obj.read(BLOCK_SIZE)

            if len(block_data) < BLOCK_SIZE:
                raise ValueError(f"[e] block {block_index + 1} is incomplete. {len(block_data)} != {BLOCK_SIZE}")

            for page_offset in range(0, BLOCK_SIZE, PAGE_SIZE):

                page = block_data[page_offset: page_offset+PAGE_SIZE]
                if len(page) != PAGE_SIZE:
                    raise ValueError(f"[e] invalid page size. {int(page_offset/PAGE_SIZE)} != {len(page)}")

                data, oob = page[:PAGE_DATA_SIZE], page[PAGE_DATA_SIZE:]
                if (len(data) != PAGE_DATA_SIZE) or (len(oob) != PAGE_OOB_SIZE):
                    raise ValueError("[e] invalid data and/or oob length.")
                
                if is_bad_block(oob):
                    if all(byte == 0 for byte in data):
                        # print("Badblock")
                        clean_dump_bb.write(data)
                    continue

                clean_dump.write(data)
                clean_dump_bb.write(data)

            # print(f"Block {block_index + 1} | {block_data[:10]}...{block_data[-10:]}")

    return clean_dump_file

def has_oob(file_obj):
    # Verify dump
    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    expected_size_oob = BLOCKS_COUNT * PAGES_PER_BLOCK * (PAGE_DATA_SIZE + PAGE_OOB_SIZE)
    expected_size = BLOCKS_COUNT * PAGES_PER_BLOCK * PAGE_DATA_SIZE
    
    if file_size == expected_size_oob:
        return True
    elif file_size == expected_size:
        return False
    else:
        raise ValueError(f"[e] invalid or corrupted dump")

def is_bad_block(oob):
    bad_block = False

    # bad_block_marker = oob[6:7]
    # if bad_block_marker != b'\xff':
    #   bad_block = True

    if oob[0:3] != b'\xff\xff\xff':
        bad_block = True

    return bad_block

def preprocess(file):

    print("Block Size:", BLOCK_SIZE)
    
    clean_dump_bb_file = os.path.join('preprocess', 'clean_dump_with_badblock.bin')
    clean_dump_file = os.path.join('preprocess', 'clean_dump.bin')

    with open(raw_dump, 'rb') as file_obj:

        dump_has_oob = has_oob(file_obj)
        
        if (dump_has_oob):
            print("creating dump without oob and badblocks")
            create_clean_dump(file_obj, clean_dump_file, clean_dump_bb_file)

        else:
            raise ValueError(f"[e] your dump does not contains oob data.")

def extract_partitions():

    clean_dump_file = os.path.join('preprocess', 'clean_dump.bin')
    with open(clean_dump_file, 'rb') as f:
        extract(f)

def hamming_ecc(data_chunk):
    """
    Calculate a 3-byte Hamming ECC over 512 bytes (classic 1-bit correct ECC).
    Algorithm based on Linux MTD implementation.
    """
    if len(data_chunk) != 512:
        raise ValueError("ECC expects 512-byte chunk")

    par = [0, 0, 0]
    for i, b in enumerate(data_chunk):
        for j in range(8):
            bit = (b >> j) & 1
            if bit:
                par[0] ^= i
                par[1] ^= ~i & 0xFF
                par[2] ^= 1

    return bytes([(par[0] & 0xFF), (par[1] & 0xFF), (par[2] & 0xFF)])

def verify_hamming_ecc(page_data, page_oob):
    """
    Verifies ECC for a full 2048-byte page using Hamming.
    Assumes OOB has ECC in first 16 bytes (4 x 3 bytes ECC)
    """
    if len(page_data) != 2048 or len(page_oob) < 16:
        raise ValueError("Invalid page size or OOB")

    result = []
    for i in range(4):  # 4 chunks of 512 bytes
        chunk = page_data[i * 512 : (i + 1) * 512]
        expected_ecc = page_oob[i * 4 : i * 4 + 3]
        calc_ecc = hamming_ecc(chunk)
        match = calc_ecc == expected_ecc
        result.append((i, match, expected_ecc.hex(), calc_ecc.hex()))

    return result


'''
t — Error Correction Strength(required)
t = 8 can correct up to 8 bit errors in a given block of data (usually 512 bytes).
common values: 4, 8, 12, 15.

poly — Primitive Polynomial
This is a low-level parameter mostly needed for custom or non-standard BCH codes.

m — Galois Field Size
Must be between 5 and 15, inclusive.
This affects how many bits (and bytes) of ECC are generated.

swap_bits — Bit Order Reversal
If True, reverses the bits in each byte of data and ECC before encoding/decoding.
'''

# bch = BCH(t=5, m=12, swap_bits=False)
# bch = BCH(t=6, m=10, swap_bits=True)
# bch = BCH(t=7, m=9, swap_bits=True)
bch = BCH(t=8, m=8, swap_bits=True)

def ecc_check(data: bytes, oob: bytes):
    
    if len(data) != PAGE_DATA_SIZE or len(oob) != PAGE_OOB_SIZE:
        raise ValueError(f"Invalid input sizes. Expecting {PAGE_DATA_SIZE} bytes data and {PAGE_OOB_SIZE} bytes OOB.")

    new_oob = bytearray()


    for i in range(4):
        
        new_oob.extend(b'\xff' * 8)
        
        # Encode ECC for this 512-byte chunk (should be 13 bytes)
        data_chunk = data[i * 512 : (i + 1) * 512]
        ecc_bytes = bch.encode(data_chunk)
        
        if len(ecc_bytes) != bch.ecc_bytes:
            raise ValueError(f"ECC length mismatch: expected {bch.ecc_bytes}, got {len(ecc_bytes)}")
        
        new_oob.extend(ecc_bytes)


    print(oob.hex())
    print(new_oob.hex())
    print()

def repack_to_nand_image(partition_dir='extracts', output_path='repacked_nand.bin', include_oob=True):
    
    total_blocks = BLOCKS_COUNT
    page_size = PAGE_DATA_SIZE + (PAGE_OOB_SIZE if include_oob else 0)
    block_size = page_size * PAGES_PER_BLOCK
    total_image_size = total_blocks * block_size

    print(f"[i] Repacking to NAND image ({'with' if include_oob else 'without'} OOB)...")

    nand_image = bytearray([0xFF] * total_image_size)

    for name, (offset, size) in PARTITIONS.items():
        bin_path = os.path.join(partition_dir, f"{name}.bin")
        if not os.path.isfile(bin_path):
            raise ValueError(f"[!] missing partition file: {bin_path}")

        with open(bin_path, 'rb') as part_file:
            data = part_file.read()

        if len(data) > size:
            raise ValueError(f"[e] Partition {name} is too large: {len(data)} > {size}")

        start = offset
        end = offset + len(data)
        i = 0

        while start < end:
            page_data = data[i:i+PAGE_DATA_SIZE]
            oob = b'\xFF' * PAGE_OOB_SIZE if include_oob else b''
            page = page_data + oob
            nand_image[start:start + len(page)] = page

            i += PAGE_DATA_SIZE
            start += len(page)

        print(f"[i] Inserted {name} at 0x{offset:X} (size={len(data)} bytes)")

    with open(output_path, 'wb') as f:
        f.write(nand_image)
        print(f"\n[i] NAND image written to {output_path}")

def repack(original_dump_path, partition_dir='extracts', output_path='repacked_nand_with_oob.bin', include_oob=True):
    
    print(f"[i] Repacking...")

    with open(original_dump_path, 'rb') as f:
        raw_data = bytearray(f.read())

    for name, (part_offset, part_size) in PARTITIONS.items():
        bin_path = os.path.join(partition_dir, f"{name}.bin")
        if not os.path.isfile(bin_path):
            raise ValueError(f"[!] missing partition file: {bin_path}")

        with open(bin_path, 'rb') as pf:
            partition_data = pf.read()

        if len(partition_data) > part_size:
            raise ValueError(f"[e] Partition {name} too large: {len(partition_data)} > {part_size}")

        print(f"[i] writing partition: {name} at offset 0x{part_offset:X}")

        data_written = 0
        nand_offset = 0

        for block_index in range(BLOCKS_COUNT):
            block_base = block_index * BLOCK_SIZE

            for page_idx in range(PAGES_PER_BLOCK):
                page_offset = block_base + page_idx * PAGE_SIZE
                data_offset = page_offset
                oob_offset = page_offset + PAGE_DATA_SIZE

                oob = raw_data[oob_offset : oob_offset + PAGE_OOB_SIZE]
                if is_bad_block(oob):
                    continue  # skip bad block

                if part_offset <= nand_offset < part_offset + part_size:
                    chunk_size = min(PAGE_DATA_SIZE, part_offset + part_size - nand_offset)
                    chunk = partition_data[data_written : data_written + chunk_size]

                    # ecc_check(chunk, oob)
                    
                    raw_data[data_offset : data_offset + len(chunk)] = chunk
                    data_written += len(chunk)

                nand_offset += PAGE_DATA_SIZE

                if data_written >= len(partition_data):
                    break
            if data_written >= len(partition_data):
                break

        
        print(f"[i] Wrote {data_written} bytes to {name}")

    if os.path.isfile(output_path):
        os.remove(output_path)

    with open(output_path, 'wb') as out:
        out.write(raw_data)

    print(f"[i] Final image written to {output_path} (OOB and bad blocks preserved)")

    with open(output_path, 'rb') as f:
        create_clean_dump(f, 'repacked_nand_without_oob_and_bb.bin', 'repacked_nand_without_oob.bin')



# "E:\Softawers\Windows\Router\ZLT S10\S10_Dialog_407_v1.12_ch341_dump\S10_Dump1.bin"
# "E:\Softawers\Windows\Router\ZLT S10\S10_Dialog_407_v1.12_ch341_dump\S10_Dump3_with_spare.bin"

raw_dump = r"E:\Softawers\Windows\Router\ZLT S10\S10_Dialog_407_v1.12_ch341_dump\S10_Dump3_with_spare.bin"

os.makedirs('preprocess', exist_ok=True)
os.makedirs('extracts', exist_ok=True)

# preprocess(raw_dump)
# extract_partitions()
# repack_to_nand_image()
repack(raw_dump)