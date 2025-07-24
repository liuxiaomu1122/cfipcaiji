import requests
from bs4 import BeautifulSoup
import re
import os
import sys

# 目标URL列表
urls = ['https://www.wetest.vip/page/cloudflare/address_v4.html',
        'https://cf.090227.xyz/',
        'https://ip.164746.xyz'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    # 尝试删除已存在的IP文件，不存在则忽略
    try:
        os.remove('ip.txt')
    except FileNotFoundError:
        print("ip.txt文件不存在，无需删除")

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        print(f"正在获取{url}的IP地址")
        try:
            # 添加网络请求异常处理
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # 检查HTTP错误状态码
        except requests.exceptions.RequestException as e:
            print(f"获取{url}失败: {str(e)}")
            continue  # 跳过错误URL继续执行
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
            
        elif url == 'https://www.wetest.vip/page/cloudflare/address_v4.html':
            elements = soup.find_all('tr')
        elif url == 'https://cf.090227.xyz/':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        num = 0 
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            if url == 'https://cf.090227.xyz/':
                num += 1
                if num > 13:
                    continue

            
            # 如果找到IP地址,则写入文件
            for ip in ip_matches:
                print(ip)
                file.write(ip + '\n')

print('IP地址已保存到ip.txt文件中。')
