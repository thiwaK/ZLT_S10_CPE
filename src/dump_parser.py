import os
from construct import Struct, Int8ul, Array, Byte
import argparse

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

def create_clean_dump(file_obj, clean_dump_file, keep_badblocks=False):

    file_obj.seek(0)
    if os.path.isfile(clean_dump_file):
        os.remove(clean_dump_file)
    
    clean_dump = open(clean_dump_file, 'ab')

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
                    if not keep_badblocks:
                        continue

            clean_dump.write(data)


        # print(f"Block {block_index + 1} | {block_data[:10]}...{block_data[-10:]}")
    
    clean_dump.close()

    return clean_dump_file

def has_oob(file_obj):

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

def preprocess(raw_dump):
    
    # clean_dump_bb_file = os.path.join('preprocess', 'clean_dump_with_badblock.bin')
    clean_dump_file = os.path.join('preprocess', 'clean_dump.bin')

    with open(raw_dump, 'rb') as file_obj:

        dump_has_oob = has_oob(file_obj)
        
        if (dump_has_oob):
            print("[i] creating dump without oob and badblocks")
            create_clean_dump(file_obj, clean_dump_file)

        else:
            raise ValueError(f"[e] your dump does not contains oob data.")

def extract_partitions():

    clean_dump_file = os.path.join('preprocess', 'clean_dump.bin')
    
    with open(clean_dump_file, 'rb') as file_obj:
        for name, (offset, size) in PARTITIONS.items():
            file_obj.seek(offset)
            data = file_obj.read(size)

            output_path = os.path.join('extracts', f"{name}.bin")
            with open(output_path, 'wb') as out_file:
                out_file.write(data)
                print(f"[i] extracted {name:<10} offset=0x{offset:08X} size=0x{size:08X} -> {output_path}")

def repack(original_dump_path, partition_dir='extracts', output_path=''):
    
    with open(original_dump_path, 'rb') as file_obj:
        dump_has_oob = has_oob(file_obj)
        if not dump_has_oob:
            raise ValueError(f"[e] your dump does not contains oob data.")
            

    with open(original_dump_path, 'rb') as f:
        raw_data = bytearray(f.read())

    for name, (part_offset, part_size) in PARTITIONS.items():
        bin_path = os.path.join(partition_dir, f"{name}.bin")
        
        if not os.path.isfile(bin_path):
            raise ValueError(f"[e] missing partition file: {bin_path}")

        with open(bin_path, 'rb') as pf:
            partition_data = pf.read()

        if len(partition_data) > part_size:
            raise ValueError(f"[e] partition {name} too large: {len(partition_data)} > {part_size}")

        print(f"[i] writing partition: {name:<10} at offset 0x{part_offset:X}")

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

        
        # print(f"[i] Wrote {data_written} bytes to {name}")

    out_with_oob = os.path.join(output_path, 'repacked_nand_with_oob.bin')
    
    if os.path.isfile(out_with_oob):
        os.remove(out_with_oob)

    with open(out_with_oob, 'wb') as out:
        out.write(raw_data)

    print(f"[i] image written to {out_with_oob} (OOB and bad blocks preserved)")

    out_without_oob = os.path.join(output_path, 'repacked_nand_without_oob.bin')
    with open(out_with_oob, 'rb') as f:
        create_clean_dump(f, out_without_oob, True)

    print(f"[i] image written to {out_without_oob} (OOB excluded)")

def main():

    parser = argparse.ArgumentParser(
        description="ZLT S10 Firmware dump parser tool",
        usage="python dump_parser.py firmware_dump [--unpack | --repack]"
    )

    parser.add_argument(
        'firmware_dump',
        help="Path to the firmware dump file"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--unpack',
        action='store_true',
        help="Unpack the firmware"
    )
    group.add_argument(
        '--repack',
        action='store_true',
        help="Repack the firmware"
    )

    args = parser.parse_args()

    if args.unpack:
        print(f"Unpacking...")
        preprocess(args.firmware_dump)
        extract_partitions()
        
    elif args.repack:
        print(f"Repacking...")
        repack(args.firmware_dump)

if __name__ == "__main__":
    os.makedirs('preprocess', exist_ok=True)
    os.makedirs('extracts', exist_ok=True)
    
    main()

