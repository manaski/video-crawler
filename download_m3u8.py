import requests, re, time, os
from Crypto.Cipher import AES
import urllib.parse
import ffmpy


def request(url, headers, timeout):
    print('请求：', url)
    max_retry = 3
    while max_retry > 0:
        res = requests.get(url=url, headers=headers, timeout=timeout)
        if res.status_code == 200:
            return res.content
        else:
            print('请求出错, status_code:', res.status_code)
            time.sleep(1)


def parse_m3a8(m3u8_file):
    urls = []
    key_url = ''
    with open(m3u8_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.endswith(".ts\n"):
                urls.append(line.strip("\n"))
            if line.startswith("#EXT-X-KEY:"):
                matches = re.findall(r'URI="(.*?)"', line)
                if len(matches) > 0:
                    key_url = matches[0]
    if (len(urls) > 0) and key_url != '':
        print('解析m3a8成功')
        return urls, key_url
    else:
        print("解析m3a8失败")


def save_2_file(contents, file):
    with open(file, 'wb') as f:
        try:
            f.write(contents)
        except:
            print('m3u8写入异常')

    print('m3u8写入完成')


def download(video_path, base_url, ts_urls, headers, ts_key):
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    cryptor = AES.new(ts_key, AES.MODE_CBC, ts_key)

    total = len(ts_urls)
    index = 0

    for url in ts_urls:
        res = request(base_url + '/' + url, headers, 5)
        filename = video_path + '/' + url
        with open(filename, 'wb') as f:
            try:
                content = cryptor.decrypt(res)
            except:
                print(filename, '解密出错')
                break
            try:
                f.write(content)
                print('%s 下载完成(%d/%d)' % (filename, index, total))
            except:
                print(filename, '写入出错')
                break
        time.sleep(0.5)
        index += 1


def merge_video(video_path, filename):
    all_ts = os.listdir(video_path)
    all_ts.sort(key=lambda x: int(x[5:-3]))

    with open(video_path + '/' + "file_list.txt", "w+") as f:
        for file in all_ts:
            f.write("file '{}'\n".format(video_path + '/' + file))

    ff = ffmpy.FFmpeg(
        global_options=['-f', 'concat', '-y'],
        inputs={video_path + '/' + "file_list.txt": None},
        outputs={video_path + '/' + filename: ['-c', 'copy']}
    )

    ff.run()

    print(filename, "合并完成！！")


def clean(video_path, m3u8_file):
    all_ts = os.listdir(video_path)
    for ts in all_ts:
        os.remove(video_path + '/' + ts)

    os.remove(m3u8_file)

    os.remove(video_path + '/' + 'file_list.txt')

    print("清理完成！！")


# 点击进入视频播放页
def parse_m3u8_url(html):
    urls = re.findall(r'js_video_url=\'(.*?.m3u8)\'', html)
    if len(urls) == 0:
        print("failed to find m3u8 url")
        return

    m3u8_url = urls[0]

    urls = re.findall(r'(.*?)/index.m3u8', m3u8_url)
    if len(urls) == 0:
        print("failed to find video base url")
        return

    video_base_url = urls[0]

    urls = re.findall(r'(https://[0-9a-z.]+)/.*', m3u8_url)
    if len(urls) == 0:
        print("failed to find video base url")
        return

    host = urls[0]

    print("获取 m3u8 URL 成功")

    return m3u8_url, video_base_url, host


def parse_entry_url():
    filename = 'page.html'

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    urls = re.findall(r'"entry-title"><a href="(.*?)"', content)
    if len(urls) == 0:
        print("failed to get entry url")
        return

    titles = []

    for url in urls:
        title = re.findall(r'.+/([a-z0-9-%]+)/', url)
        if len(title) == 0:
            print("failed to get entry title")
            return

        t = title[0]
        if t.find('%'):
            t = urllib.parse.unquote(t)
        titles.append(t)

    return urls, titles


if __name__ == '__main__':
    m3u8_headers = {
    }

    entry_headers = {
    }

    entry_urls, entry_titles = parse_entry_url()

    for idx in range(len(entry_titles)):
        url = entry_urls[idx]
        title = entry_titles[idx]

        res = request(url, entry_headers, 5)
        html = res.decode('UTF-8')

        m3u8_url, video_base_url, host = parse_m3u8_url(html)

        m3a8_res = request(m3u8_url, m3u8_headers, 5)
        save_2_file(m3a8_res, title + '.m3u8')

        video_urls, key_url = parse_m3a8(title + '.m3u8')

        key_res = request(host + key_url, m3u8_headers, 5)
        key = key_res.decode('UTF-8')
        print('获得key成功', key)

        download(title, video_base_url, video_urls, m3u8_headers, key)

        merge_video(title, title + '.ts')

        clean(title, title + '.m3u8')
