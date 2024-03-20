import datetime

import requests
from lxml import html


def get_qrcode_url(url, password):
    res = requests.post(url, data={'secret_key': password}).text
    etree = html.etree  # 获取etree
    content = etree.HTML(res)
    # ele = content.xpath("/html//img[@alt='微信扫一扫，获取，验证码']/@src")
    return content


if __name__ == '__main__':
    # 二维码图片地址
    qrcode_url = 'https://www.ajihuo.com/wp-content/uploads/2023/08/jiagouwang.jpg'
    # 请求地址
    access_url = 'https://www.ajihuo.com/idea/4222.html'
    passworld_list = []
    for pre in ('66', '88', '99', '11', '22', '33', '44', '55', '77'):
        month = datetime.datetime.now().strftime('%m')
        for i in range(1, 32):
            if i < 10:
                passworld_list.append(pre + month + '0' + str(i))
            else :
                passworld_list.append(pre + month + str(i))
    for passworld in passworld_list:
        content = get_qrcode_url(access_url, passworld)
        xpath = content.xpath("/html//img[@alt='微信扫一扫，获取，验证码']/@src")

        is_failed = bool() # bool()默认false
        for e in xpath:
            # 如果返回结果中包含了二维码，说明失败了，需要重新请求
            if e == qrcode_url:
                print(e)
                is_failed = bool(True)

        if is_failed:
            print('请求失败，错误验证码: %s' % passworld)
            continue
        else :
            res = content.xpath("/html//div[@class=' old-record-id-doxcnpkXyrUwChfXnvQ0K9RwEKb']")
            for r in res:
                print('请求成功， 激活码为：%s' % r.text)
            break
