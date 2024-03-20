import time

import requests
from lxml import html
import openpyxl
from requests.adapters import HTTPAdapter
import urllib3

def getSubUrlData(url,session):
    print("开始请求子链接:%s" %url)
    start_time = time.time()
    resp = session.get(url=url, verify=False, timeout=30).text
    end_time = time.time()
    print("请求子链接完成，耗时%.2f秒"% (end_time - start_time))
    etree = html.etree  # 获取etree
    content = etree.HTML(resp)  # 获取xpath对象
    content = content.xpath("/html//div[@class='basic-info cmn-clearfix']")
    dir = {}
    for con in content:
        k = con.xpath("./dl/dt/text()")
        v = con.xpath("./dl/dd/text()")
        if len(k) != 0 and len(k) == len(v):
            for i in range(len(k)):
                dir[k[i]] = v[i]
    return dir

def getData(url, session):
    resData = []
    count = 0
    print("请求链接：%s" %url)
    resp = session.get(url=url, verify=False).text
    print("%s请求完成" % url)
    etree = html.etree  # 获取etree
    content = etree.HTML(resp)  # 获取xpath对象
    content = content.xpath("/html//div[@class='row']/div[@class='panel panel-default post']")
    # 遍历每一个div
    for div in content:
        data = []
        num = div.xpath(".//span[@class='line11']/text()")
        data.append(' '.join(num))
        title = div.xpath(".//div[@class='page-header']//span/text()")[0]
        subUrl = div.xpath(".//div[@class='page-header']//a[@target='_blank']/@href")[0]
        dir={}
        try:
            dir = getSubUrlData(subUrl, session)
        except Exception as e:
            print("请求失败", e)
            print("--------------------------------------", subUrl)
        data.append(title)
        infos = div.xpath("./div/div/div[2]//div[@class='media media-inner']")
        count = count + 1
        for info in infos:
            titleName = info.xpath('.//span/text()')[0]
            titleContent = info.xpath('.//div[@class="media-body"]//text()')[0]
            dir[titleName.strip()] = titleContent.strip()
        data.append(dir.get('英文名称', ''))
        data.append(dir.get('专业范围', ''))
        data.append(dir.get('对口/相关联国际组织', ''))
        data.append(dir.get('秘书处承担单位', ''))
        data.append(dir.get('秘书处所在地', ''))
        data.append(dir.get('委员会全称', ''))
        data.append(dir.get('英文全称', ''))
        data.append(dir.get('委员会简称', ''))
        data.append(dir.get('委员会编号', ''))
        data.append(dir.get('负责专业范围', ''))
        data.append(dir.get('本届届号', ''))
        data.append(dir.get('筹建单位', ''))
        data.append(dir.get('业务指导单位', ''))
        data.append(dir.get('对口/相关联国际组织', ''))
        data.append(dir.get('现任秘书长', ''))
        data.append(dir.get('秘书处所在单位', ''))
        data.append(dir.get('所在省（市）', ''))
        data.append(dir.get('通讯地址', ''))
        data.append(dir.get('邮编', ''))
        data.append(dir.get('联系人', ''))
        data.append(dir.get('电话', ''))
        data.append(dir.get('邮箱', ''))
        data.append(dir.get('传真', ''))
        resData.append(data)
    return resData

if __name__ == '__main__':
    urllib3.disable_warnings()
    workBook = openpyxl.Workbook();
    sheet = workBook.active
    sheet['A1'] = '编号'
    sheet['B1'] = '标题'
    sheet['C1'] = '英文名称'
    sheet['D1'] = '专业范围'
    sheet['E1'] = '对口/相关联国际组织'
    sheet['F1'] = '秘书处承担单位'
    sheet['G1'] = '秘书处所在地'
    sheet['H1'] = '委员会全称'
    sheet['I1'] = '英文全称'
    sheet['J1'] = '委员会简称'
    sheet['K1'] = '委员会编号'
    sheet['L1'] = '负责专业范围'
    sheet['M1'] = '本届届号'
    sheet['N1'] = '筹建单位'
    sheet['O1'] = '业务指导单位'
    sheet['P1'] = '对口/相关联国际组织'
    sheet['Q1'] = '现任秘书长'
    sheet['R1'] = '秘书处所在单位'
    sheet['S1'] = '所在省（市）'
    sheet['T1'] = '通讯地址'
    sheet['U1'] = '邮编'
    sheet['V1'] = '联系人'
    sheet['W1'] = '电话'
    sheet['X1'] = '邮箱'
    sheet['Y1'] = '传真'
    # with ThreadPoolExecutor(40) as t:
        # t.submit(fun, *args)
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=3))
    session.mount("https://", HTTPAdapter(max_retries=3))
    for i in range(1,12):
        url = 'https://std.samr.gov.cn/search/orgPage?q=&op=TABLE_NAME%3A%22BV_COMMITEE_INFO%22%2CG_SECRETARIAT_UNIT_PROVINCE%3A%22%E4%B8%8A%E6%B5%B7%E5%B8%82%22&pageNo=' + str(i)
        resData = getData(url, session)
        for res in resData:
            sheet.append(res)
        # for i in range(1, 12):
        #     url = 'https://std.samr.gov.cn/search/orgPage?q=&op=TABLE_NAME%3A%22BV_COMMITEE_INFO%22%2CG_SECRETARIAT_UNIT_PROVINCE%3A%22%E4%B8%8A%E6%B5%B7%E5%B8%82%22&pageNo=' + str(i)
        #     resData = t.submit(getData, url=url)
        #     for res in resData.result():
        #         sheet.append(res)
    workBook.save("xxx.xlsx")
