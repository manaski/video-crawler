import requests, os
from tqdm import tqdm
from threading import Thread
import ffmpy


def download_from_url(url, headers, dst):
    response = requests.get(url=url, headers=headers, stream=True)  # (1)
    file_size = int(response.headers['content-length'])  # (2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  # (3)
    else:
        first_byte = 0
    if first_byte >= file_size:  # (4)
        return file_size

    headers["range"] = f"bytes={first_byte}-{file_size}"
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=headers, stream=True)  # (5)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):  # (6)
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


def merge_video(video_path, filename):
    all_file = os.listdir(video_path)
    all_file.sort(key=lambda x: int(x[:-4]))

    with open("file_list.txt", "w+") as f:
        for file in all_file:
            f.write("file '{}'\n".format(video_path + '/' + file))

    ff = ffmpy.FFmpeg(
        global_options=['-f', 'concat', '-y'],
        inputs={"file_list.txt": None},
        outputs={video_path + '/' + filename: ['-c', 'copy']}
    )

    ff.run()

    print(filename, "合并完成！！")


def clean(video_path, file):
    all_ts = os.listdir(video_path)
    for ts in all_ts:
        os.remove(video_path + '/' + ts)

    os.remove(file)

    print("清理完成！！")


if __name__ == '__main__':
    base_url = ''
    dst = 'video.mp4'
    headers = {
    }

    th_list = []
    for i in range(5):
        url = base_url + str(i + 1) + '.mp4'
        dst = 'video/' + str(i + 1) + '.mp4'
        th = Thread(target=download_from_url, args=(url, headers, dst))
        th_list.append(th)
        th.start()
        print(str(i + 1), "finished")

    for th in th_list:
        th.join()

    print("all finished")

    merge_video('video', 'video.mp4')

    clean('video', 'file_list.txt')
