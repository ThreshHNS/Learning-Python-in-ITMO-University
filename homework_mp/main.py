import os
import glob
import tinify
from multiprocessing import Queue
from config import TINIFY_KEY
from pool import ProcessPool
tinify.key = TINIFY_KEY


def compress_resize(filename, test_run=False):
    base_filename, file_extension = os.path.splitext(filename)
    base_filename = base_filename.split("/")[1]
    resized_filename = f"{base_filename}-compressed{file_extension}"
    image_to_resize = tinify.from_file(filename)
    resized_image = image_to_resize.resize(method="fit", width=500, height=500)
    resized_image.to_file(f'compressed/{resized_filename}')
    if not test_run:
        print(f"- {base_filename}{file_extension} ...")
    else:
        print(f"• Calculating memory usage in test running ...")


if __name__ == '__main__':
    image_files = glob.glob("files/*.jpg")
    q = Queue()
    pool = ProcessPool()
    for i in image_files:
        q.put(i)
    result = pool.map(compress_resize, q)
