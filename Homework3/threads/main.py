import os
import time
import shutil
import logging
from pathlib import Path
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

extensions = {'archives': ('.ZIP', '.GZ', '.TAR', '.RAR', '.7Z'),
              'audio': ('.MP3', '.OGG', '.WAV', '.AMR'),
              'video': ('.AVI', '.MP4', '.MOV', '.MKV'),
              'documents': ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
              'images': ('.JPEG', '.PNG', '.JPG', '.SVG')}

unknown = 'unknown'


def time_it(func):
    def wrapper(*args):
        start = time.time()
        func(*args)
        finish = time.time()
        logging.debug(f'Function {func.__name__}\texecuted in {finish - start:.4f} seconds.')
    return wrapper


def new_file_name(file: Path) -> Path:
    counter = 1
    file_stem = file.stem
    while file.exists():
        new_name = f"{file_stem}({counter}){file.suffix}"
        file = file.parent / new_name
        counter += 1
    return file


def move_file(file: Path) -> None:
    time.sleep(0.1)
    for dest_folder, extension in extensions.items():
        if file.suffix.upper() in extension:
            dest_file = file.parents[len(file.parents) - 2] / dest_folder / file.name
            if dest_file.exists():
                dest_file = new_file_name(dest_file)
            shutil.move(file, dest_file)
            # logging.debug(f'File {file.name} moved to {dest_folder} folder.')
            break
    else:
        dest_file = file.parents[len(file.parents) - 2] / unknown / file.name
        if dest_file.exists():
            dest_file = new_file_name(dest_file)
        shutil.move(file, dest_file)
        # logging.debug(f'File {file.name} moved to {unknown} folder.')


def mk_folders(folder: Path):
    for dest in extensions:
        dest_folder = folder/dest
        if not dest_folder.exists():
            dest_folder.mkdir()
    dest_folder = folder / 'unknown'
    if not dest_folder.exists():
        dest_folder.mkdir()


def rm_folders(path: Path) -> None:
    for iter_folder in path.iterdir():
        if iter_folder.is_dir():
            rm_folders(iter_folder)
            if not os.listdir(iter_folder):
                os.rmdir(iter_folder)


def sort_files_regular(folder: Path) -> None:
    mk_folders(folder)
    for directory in folder.glob('**/*'):
        if directory.is_file() and directory.parent.name not in extensions and directory.parent.name != unknown:
            move_file(directory)
    rm_folders(folder)


def sort_files_threading(folder: Path) -> None:
    threads = []
    mk_folders(folder)
    for directory in folder.glob('**/*'):
        if directory.is_file() and directory.parent.name not in extensions and directory.parent.name != unknown:
            thread = Thread(target=move_file, args=(directory,))
            threads.append(thread)
            thread.start()
            # move_file(directory)
    [el.join() for el in threads]
    rm_folders(folder)


def sort_files_threadpool(folder: Path) -> None:
    files = []
    mk_folders(folder)
    for directory in folder.glob('**/*'):
        if directory.is_file() and directory.parent.name not in extensions and directory.parent.name != unknown:
            files.append(directory)
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(move_file, files))
    rm_folders(folder)


@time_it
def sort_regular(path: str) -> None:
    path = Path(path)
    sort_files_regular(path)


@time_it
def sort_threading(path: str) -> None:
    path = Path(path)
    sort_files_threading(path)


@time_it
def sort_threadpool(path: str):
    path = Path(path)
    sort_files_threadpool(path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    sort_regular('test_pack')
    sort_threading('test_pack_2')
    sort_threadpool('test_pack_3')
