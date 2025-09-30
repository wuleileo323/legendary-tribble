import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.service import Service


def setup_chrome_debugging_driver():
    """
    连接到已经通过命令行启动的Chrome实例
    命令: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\selenium_chrome_profile"
    """
    # 配置Chrome选项以连接到现有的调试实例
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(executable_path='D:/Trae/chromedriver-win64/chromedriver.exe') # <-- 修改这里

    # 创建WebDriver实例连接到已启动的Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options) # <-- 修改这里
    
    return driver

def get_cookies_from_existing_chrome(driver, url):
    """
    从已连接的Chrome实例获取认证信息
    """
    print(f"正在访问 {url} 获取认证信息...")
    driver.get(url)
    
    # 等待页面加载
    time.sleep(5)
    
    # 获取cookies
    cookies = driver.get_cookies()
    print(f"获取到 {len(cookies)} 个cookies")
    
    # 获取CSRF token (如果存在)
    csrf_token = None
    try:
        # 尝试从页面源码查找CSRF token或其他认证信息
        page_source = driver.page_source
        import re
        csrf_match = re.search(r'"csrf_token":\s*"([^"]+)"', page_source)
        if csrf_match:
            csrf_token = csrf_match.group(1)
        
        # 也可以尝试查找特定的meta标签
        if not csrf_token:
            try:
                csrf_element = driver.find_element(By.NAME, "csrfmiddlewaretoken")
                csrf_token = csrf_element.get_attribute("value")
            except:
                pass
        
        # 或者从HTTP头部查找
        if not csrf_token:
            for header in driver.execute_script("return Object.keys(window.performance.getEntries());"):
                if "csrf" in header.lower():
                    csrf_token = driver.execute_script(f"return window.performance.getEntries()['{header}'];")
                    break
    
    except Exception as e:
        print(f"获取CSRF token时出错: {e}")
    
    # 转换cookies为requests格式
    session_cookies = {}
    for cookie in cookies:
        session_cookies[cookie['name']] = cookie['value']
    
    return session_cookies, csrf_token

def make_rocketreach_request_with_existing_chrome():
    """
    使用已连接的Chrome实例获取认证信息并调用RocketReach API
    """
    # 连接到已启动的Chrome实例
    driver = setup_chrome_debugging_driver()
    
    try:
        # 访问网站获取认证信息
        session_cookies, csrf_token = get_cookies_from_existing_chrome(driver, "https://rocketreach.co/person")
        
        # API端点
        url = "https://rocketreach.co/v2/services/search/person"
        
        # 使用从Chrome获取的认证信息构建请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://rocketreach.co',
            'priority': 'u=1, i',
            'referer': 'https://rocketreach.co/person?start=1&pageSize=10&employer%5B%5D=Tencent',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"140.0.7339.81"',
            'sec-ch-ua-full-version-list': '"Chromium";v="140.0.7339.81", "Not=A?Brand";v="24.0.0.0", "Google Chrome";v="140.0.7339.81"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-csrftoken': csrf_token or 'r0WzJQAdxvCczQxsGrGHCg61dAn3RSlXYcJsNHOTjtYNfMoDHPveoSpFVzIiilvb',
            'x-rr-for': 'd3b946e2a7ace9368d6ec674dec4a770',
            'x-source-page': '/person'
        }
        
        # 构建请求数据
        data = {
            "start": 1,
            "pageSize": 10,
            "excludeContacts": False,
            "searchEventsSessionId": "4c36dbfa-515c-48b2-b566-ab3c9f786258",
            "name": "",
            "geo": [],
            "current_title": [],
            "normalized_title": [],
            "department": [],
            "management_levels": [],
            "job_change_range_days": None,
            "skills": [],
            "years_experience": None,
            "health_specialization": [],
            "health_npi": "",
            "health_license": "",
            "health_credentials": [],
            "gender": [],
            "veteran_status": [],
            "ethnicity": [],
            "employer": ["Tencent"],
            "company_intent": [],
            "company_competitors": [],
            "company_id": [],
            "company_size": None,
            "company_revenue": None,
            "company_news_timestamp": [],
            "company_industry": [],
            "company_industry_keywords": [],
            "company_sic_code": [],
            "company_naics_code": [],
            "contact_method": "",
            "email_grade": "",
            "major": [],
            "school": [],
            "degree": [],
            "contact_info": "",
            "link": "",
            "keyword": "",
            "company_tag": ""
        }
        
        # 创建requests会话并设置cookies
        session = requests.Session()
        for name, value in session_cookies.items():
            session.cookies.set(name, value)
        
        try:
            print("正在发送请求到 RocketReach API...")
            response = session.post(url, headers=headers, json=data)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 请求成功!")
                
                # 解析响应数据结构
                print(f"响应字段: {list(result.keys())}")
                
                # 解析 people 字段
                if 'people' in result:
                    people = result['people']
                    print(f"\n📊 找到 {len(people)} 个人员记录")
                    
                    # 解析并显示人员数据
                    for i, person in enumerate(people[:5]):  # 只显示前5条记录
                        print(f"\n--- 人员记录 {i+1} ---")
                        
                        # 基本信息
                        print(f"姓名: {person.get('first_name', 'N/A')} {person.get('last_name', 'N/A')}")
                        print(f"当前职位: {person.get('jobs')[0]}")

                        
                        # 工作经历


                        
                        # 其他字段
                        print(f"ID: {person.get('id', 'N/A')}")
                        print(f"头像: {person.get('profile_image_url', 'N/A')}")
                        print(f"公开档案: {person.get('public_profile_url', 'N/A')}")
                        
                        print("-" * 30)
                    
                    # 如果记录数超过5，提示还有更多
                    if len(people) > 5:
                        print(f"... 还有 {len(people) - 5} 条记录未显示")
                    
                    return people
                else:
                    print("❌ 响应中未找到 'people' 字段")
                    return []
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ 请求过程中发生错误: {e}")
            return []
    
    finally:
        # 不关闭Chrome，因为它是由用户手动启动的
        print("Chrome实例保持打开状态，由用户手动管理...")

def search_with_different_params_and_existing_chrome(employer="Tencent", start=1, page_size=10):
    """
    使用不同参数进行搜索的函数，结合现有Chrome实例获取认证信息
    """
    # 连接到已启动的Chrome实例
    driver = setup_chrome_debugging_driver()
    
    try:
        # 访问网站获取认证信息
        session_cookies, csrf_token = get_cookies_from_existing_chrome(driver, "https://rocketreach.co/person")
        
        url = "https://rocketreach.co/v2/services/search/person"
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://rocketreach.co',
            'priority': 'u=1, i',
            'referer': f'https://rocketreach.co/person?start={start}&pageSize={page_size}&employer%5B%5D={employer}',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"140.0.7339.81"',
            'sec-ch-ua-full-version-list': '"Chromium";v="140.0.7339.81", "Not=A?Brand";v="24.0.0.0", "Google Chrome";v="140.0.7339.81"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-csrftoken': csrf_token or 'r0WzJQAdxvCczQxsGrGHCg61dAn3RSlXYcJsNHOTjtYNfMoDHPveoSpFVzIiilvb',
            'x-rr-for': 'd3b946e2a7ace9368d6ec674dec4a770',
            'x-source-page': '/person'
        }
        
        data = {
            "start": start,
            "pageSize": page_size,
            "excludeContacts": False,
            "searchEventsSessionId": "4c36dbfa-515c-48b2-b566-ab3c9f786258",
            "name": "",
            "geo": [],
            "current_title": [],
            "normalized_title": [],
            "department": [],
            "management_levels": [],
            "job_change_range_days": None,
            "skills": [],
            "years_experience": None,
            "health_specialization": [],
            "health_npi": "",
            "health_license": "",
            "health_credentials": [],
            "gender": [],
            "veteran_status": [],
            "ethnicity": [],
            "employer": [employer],
            "company_intent": [],
            "company_competitors": [],
            "company_id": [],
            "company_size": None,
            "company_revenue": None,
            "company_news_timestamp": [],
            "company_industry": [],
            "company_industry_keywords": [],
            "company_sic_code": [],
            "company_naics_code": [],
            "contact_method": "",
            "email_grade": "",
            "major": [],
            "school": [],
            "degree": [],
            "contact_info": "",
            "link": "",
            "keyword": "",
            "company_tag": ""
        }
        
        # 创建requests会话并设置cookies
        session = requests.Session()
        for name, value in session_cookies.items():
            session.cookies.set(name, value)
        
        try:
            print(f"正在搜索公司: {employer}, 从第{start}页开始，每页{page_size}条...")
            response = session.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 搜索成功! 获取到 {len(result.get('people', [])) if 'people' in result else 0} 条记录")
                
                if 'people' in result:
                    return result['people']
                else:
                    return []
            else:
                print(f"❌ 搜索失败，状态码: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索过程中发生错误: {e}")
            return []
    
    finally:
        # 不关闭Chrome，因为它是由用户手动启动的
        print("Chrome实例保持打开状态，由用户手动管理...")

def parse_people_data(people_list):
    """
    解析 people 数据并提取关键信息
    """
    parsed_data = []
    
    for person in people_list:
        parsed_person = {
            'id': person.get('id'),
            'first_name': person.get('first_name', ''),
            'last_name': person.get('last_name', ''),
            'full_name': f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
            'current_title': person.get('current_title', ''),
            'current_employer': person.get('current_employer', ''),
            'current_geo': person.get('current_geo', ''),
            'profile_image_url': person.get('profile_image_url', ''),
            'public_profile_url': person.get('public_profile_url', ''),
            'contact_info': person.get('contact_info', {}),
            'summary': person.get('summary', ''),
            'work_history': person.get('work_history', []),
            'education': person.get('education', []),
            'social_profiles': person.get('social_profiles', []),
            'skills': person.get('skills', []),
            'languages': person.get('languages', [])
        }
        
        parsed_data.append(parsed_person)
    
    return parsed_data

def save_people_to_file(people_list, filename="rocketreach_people.json"):
    """
    将解析后的人员数据保存到文件
    """
    parsed_data = parse_people_data(people_list)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 人员数据已保存到 {filename}，共 {len(parsed_data)} 条记录")

def get_pagination_info(result):
    """
    获取分页信息
    """
    if 'pagination' in result:
        pagination = result['pagination']
        return {
            'total': pagination.get('total', 0),
            'current_page': pagination.get('current_page', 1),
            'page_size': pagination.get('page_size', 10),
            'pages': pagination.get('pages', 1)
        }
    return {}

def analyze_people_data(people_list):
    """
    分析人员数据
    """
    if not people_list:
        print("没有数据可分析")
        return
    
    print(f"\n📈 人员数据分析:")
    print(f"- 总人数: {len(people_list)}")
    
    # 统计职位
    titles = {}
    for person in people_list:
        title = person.get('current_title', 'N/A')
        if title in titles:
            titles[title] += 1
        else:
            titles[title] = 1
    
    print(f"- 职位分布 (前5):")
    sorted_titles = sorted(titles.items(), key=lambda x: x[1], reverse=True)
    for title, count in sorted_titles[:5]:
        print(f"  * {title}: {count}")
    
    # 统计地理位置
    locations = {}
    for person in people_list:
        location = person.get('current_geo', 'N/A')
        if location in locations:
            locations[location] += 1
        else:
            locations[location] = 1
    
    print(f"- 地理分布 (前5):")
    sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
    for loc, count in sorted_locations[:5]:
        print(f"  * {loc}: {count}")

def main():
    """
    主函数 - 演示如何使用已启动的Chrome实例获取认证信息并调用API
    """
    print("=== 适配Chrome调试端口的RocketReach API调用和解析演示 ===")
    print("请确保已通过以下命令启动Chrome:")
    print('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\\selenium_chrome_profile"')
    print("\n等待Chrome实例连接...\n")
    
    # 等待用户确认Chrome已启动
    input("请确认Chrome已按上述命令启动并登录到RocketReach，然后按Enter继续...")
    
    # 1. 基本搜索 - 搜索腾讯员工
    print("1. 搜索腾讯员工并解析people字段:")
    people_data = make_rocketreach_request_with_existing_chrome()
    
    print("\n" + "="*50 + "\n")
    
    # 2. 保存数据到文件
    if people_data:
        save_people_to_file(people_data, "tencent_employees_debug.json")
        analyze_people_data(people_data)
    
    # 3. 不同参数搜索 - 搜索谷歌员工

    # 5. 综合数据处理
    print("4. 综合数据处理示例:")
    combined_people = people_data 
    print(f"合并后的总数据量: {len(combined_people)} 条记录")
    
    if combined_people:
        save_people_to_file(combined_people, "combined_employees_debug.json")
        analyze_people_data(combined_people)
    
    print("\n=== 演示完成 ===")
    print("Chrome实例保持打开状态，可继续在浏览器中使用...")

if __name__ == "__main__":
    main()



