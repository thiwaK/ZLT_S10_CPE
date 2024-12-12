from construct import Struct, Array, Int8ul, Int16ul, Int32ul
import os

BLOCK_DATA_SIZE = 2048
BLOCK_OOB_SIZE = 64
PAGES_PER_BLOCK = 64
BLOCKS_COUNT = 1024
PAGE_SIZE = BLOCK_DATA_SIZE + BLOCK_OOB_SIZE

# Define structures
Page = Array(PAGE_SIZE, Int8ul)
Block = Array(PAGES_PER_BLOCK, Page)


def is_bad_block(page, block_num, page_num):

	data, oob = page[0:BLOCK_DATA_SIZE], page[BLOCK_DATA_SIZE:BLOCK_DATA_SIZE + BLOCK_OOB_SIZE]
	bad_block_marker = oob[6:7]

	if bytes(bad_block_marker).hex() == '00': # good blocks: ff
		print(block_num, page_num, bytes(bad_block_marker).hex())
		return None
	return data

def parse_raw_dump(raw_data):

	clean_dump = b''

	# Verify dump
	num_blocks = len(raw_data) // (PAGES_PER_BLOCK * PAGE_SIZE)
	if BLOCKS_COUNT and num_blocks != BLOCKS_COUNT:
		print(f"[e] {num_blocks} != {BLOCKS_COUNT}")
		exit()

	# Extract blocks
	blocks = []
	print(f"[i] Extracting Blocks")
	for i in range(BLOCKS_COUNT):

		end_offset = (i + 1) * (PAGES_PER_BLOCK * PAGE_SIZE)
		start_offset = i * (PAGES_PER_BLOCK * PAGE_SIZE)

		block_data = raw_data[start_offset:end_offset]
		block = Block.parse(block_data)
		blocks.append(block)

		# print(f"{start_offset}:{end_offset}")

		if end_offset == file_size:
			print("[i] Final block")

	# Validate pages
	valid_blocks = []
	print(f"[i] Validating Pages")
	for block_num, block in enumerate(blocks):
		for page_num, page in enumerate(block):
			valid_data = is_bad_block(page, block_num, page_num)
			if valid_data:
				valid_blocks.append(valid_data)
			else:
				print(f"Block {block_num} is bad and skipped.")

	# Write clean dump
	with open("clean_dump.bin", "wb") as f:
		block_structure = Struct("block_data" / Array(BLOCK_DATA_SIZE, Int8ul))
		for block in valid_blocks:
			block_data = block_structure.build({"block_data": block})
			f.write(block_data)


# Dump with spare data
raw_dump = 'raw_dump.bin'
file_size = os.path.getsize(raw_dump)

with open(raw_dump, 'rb') as f:
	raw_data = f.read()

parse_raw_dump(raw_data)