from pathlib import Path
from reader import read_file


def pgc_to_txt(input_file_path):
    blocks = read_file(input_file_path)
def save_this_shit():    
    output_path = project_root / 'output'
    output_path.mkdir(exist_ok=True)
    for i, block in enumerate(blocks):
        block_number = i + 1
        for j, channel in enumerate(block.channels):
            channel_number = j + 1
            path = output_path / f'block_{block_number}_channel_{channel_number}.txt'
            values = '\n'.join(map(str, channel.values))
            with open(path, 'w') as file:
                file.write(values)
