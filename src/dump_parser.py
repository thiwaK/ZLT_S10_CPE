import os
from construct import Struct, Int8ul, Array, Byte

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


def is_bad_block(oob):
	bad_block = False

	# bad_block_marker = oob[6:7]
	# if bad_block_marker != b'\xff':
	# 	bad_block = True

	if oob[0:3] != b'\xff\xff\xff':
		bad_block = True

	return bad_block

def parse_raw_dump(file):

	print("Block Size:", BLOCK_SIZE)
	
	# Verify dump
	file.seek(0, os.SEEK_END)
	file_size = file.tell()
	expected_size = BLOCKS_COUNT * PAGES_PER_BLOCK * (PAGE_DATA_SIZE + PAGE_OOB_SIZE)
	if file_size != expected_size:
		raise ValueError(f"[e] Invalid parameters. {len(raw_data)} != {expected_size}")

	# read blocks
	file.seek(0)
	if os.path.isfile('clean_dump.bin'):
		os.remove('clean_dump.bin')
	if os.path.isfile('clean_dump_oob.bin'):
		os.remove('clean_dump_oob.bin')
	if os.path.isfile('raw_dump_oob.bin'):
		os.remove('raw_dump_oob.bin')

	with open('clean_dump.bin', 'ab') as out_data, open('clean_dump_oob.bin', 'ab') as out_oob, open('raw_dump_oob.bin', 'ab') as out_oob_raw:
		for block_index in range(BLOCKS_COUNT):
			block_data = file.read(BLOCK_SIZE)
			mark_as_badblock = False

			if len(block_data) < BLOCK_SIZE:
				raise ValueError(f"[e] Block {block_index + 1} is incomplete. {len(block_data)} != {BLOCK_SIZE}")

			for page_offset in range(0, BLOCK_SIZE, PAGE_SIZE):
				if mark_as_badblock:
					continue

				page = block_data[page_offset: page_offset+PAGE_SIZE]
				if len(page) != PAGE_SIZE:
					raise ValueError(f"[e] Invalid page size. Page: {int(page_offset/PAGE_SIZE)} Size: {len(page)}")

				data, oob = page[:PAGE_DATA_SIZE], page[PAGE_DATA_SIZE:]
				if (len(data) != PAGE_DATA_SIZE) or (len(oob) != PAGE_OOB_SIZE):
					raise ValueError("[e] Invalid data and/or oob length.")
				
				out_oob_raw.write(oob)
				if is_bad_block(oob):
					if all(byte == 0 for byte in data):
						mark_as_badblock = True
						print("Badblock")
					continue

				out_data.write(data)
				out_oob.write(oob)


			print(f"Block {block_index + 1} Data (first 10 bytes): {block_data[:10]}...{block_data[-10:]}")



raw_dump = 'raw_dump.bin'
file_size = os.path.getsize(raw_dump)

# Dump with spare data
with open(raw_dump, 'rb') as f:
	raw_data = f.read()
	parse_raw_dump(f)