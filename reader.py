from collections import deque
from pathlib import Path
from win32com.client import (
    Dispatch,
    CDispatch,
)
from block import Block
from channel import Channel

PGImportLib = Dispatch("PGImportLib.PGImport")  # Создаём экземпляр PGImport.


def read_file(path: Path) -> deque[Block]:
    # Открываем файл с данными
    is_opened, _, file = PGImportLib.OpenFile(path)

    if not is_opened:
        raise FileNotFoundError(f'file "{path}" not found')

    blocks_count = file.BlockCount
    return _read_blocks(file, blocks_count)


def _read_blocks(file: CDispatch, blocks_count: int) -> deque[Block]:
    # Метод получения данных требует список. Значения в него на python не возвращает.
    no_data_list = []
    blocks = deque()
    for i in range(blocks_count):
        # Получаем экземпляр PGIBlock. Объект был возвращён в виде кортежа, почему-то.
        pg_block, _ = file.Block(i + 1)
        block = _read_block(pg_block, no_data_list)
        blocks.append(block)
    return blocks


def _read_block(pg_block: CDispatch, no_data_list: list) -> Block:
    # Получаем количество значений в канале
    channel_size = pg_block.SizeChannel
    # Получаем 2-мерный список с данными (в текущем случае содержит все данные)
    _, data = pg_block.GetDataSingleArray(1, channel_size, no_data_list)
    channels = deque()
    for i in range(len(data)):
        channel_data = data[i]
        channel = _read_channel(channel_data, channel_size)
        channels.append(channel)
    return Block(channels)


def _read_channel(channel_data: list[float], channel_size: int) -> Channel:
    values = deque()
    for j in range(channel_size):
        value = channel_data[j]
        values.append(value)
    return Channel(values)

def save_this_shit(save_path, blocks):    
    output_path = save_path
    output_path.mkdir(exist_ok=True)
    for i, block in enumerate(blocks):
        block_number = i + 1
        for j, channel in enumerate(block.channels):
            channel_number = j + 1
            path = output_path / f'block_{block_number}_channel_{channel_number}.txt'
            values = '\n'.join(map(str, channel.values))
            with open(path, 'w') as file:
                file.write(values)
