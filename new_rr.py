import requests
import json
import time

def make_rocketreach_request():
    """
    使用从浏览器获取的cURL命令转换的Python代码
    直接调用RocketReach的API并解析people字段
    """
    url = "https://rocketreach.co/v2/services/search/person"
    
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
        'x-csrftoken': 'r0WzJQAdxvCczQxsGrGHCg61dAn3RSlXYcJsNHOTjtYNfMoDHPveoSpFVzIiilvb',
        'x-rr-for': 'd3b946e2a7ace9368d6ec674dec4a770',
        'x-source-page': '/person'
    }
    
    cookies = {
        'src': '201',
        'ctx': 'rocketreach.co', 
        'cj2': 'L2xvZ2lu',
        'jh': '1740960000',
        '_ga': 'GA1.1.1381607328.1757425371',
        'validation_token': 'HmX3e1oQW8wLQ61lbyZHWMtOS9vpBDko',
        'sessionid-20191028': '5unq14cd9kdsvn3z04hlolhs98v64eyd',
        'hubspotutk': 'aa29a649faf8a5239c1befa040ef467f',
        '_dd_s': 'isExpired=1&aid=9a4483f2-1e64-44bf-8a2e-3a36d094f719; _clck=5rr103^5E2^5Efzq^5E0^5E2078',
        '_gcl_au': '1.1.1505756196.1757425371.1872715732.1759145773.1759146226',
        '_cfuvid': 'UhwIq8OpxZx3yg3iBapyFo72blJstYFOav4PVIkoHMo-1759146683519-0.0.1.1-604800000',
        '__hssrc': '1',
        '__hstc': '94151554.aa29a649faf8a5239c1befa040ef467f.1757426083401.1759147034688.1759149078343.10',
        '__hssc': '94151554.3.1759149078343',
        '_ga_FB8KKHJC7E': 'GS2.1.s1759149037$o10$g1$t1759149541$j58$l0$h0',
        '_rdt_uuid': '1757425370365.8795a97e-7864-46fc-b471-332725285ef9',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Sep+29+2025+20%3A39%3A02+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d1a7fb8c-4e74-4f2f-8039-8d9a09817a01&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
        '_clsk': '1mafs3n^5E1759149542231^5E4^5E0^5Ei.clarity.ms/collect',
        '_uetsid': '1134b6109d2811f084d2010d85618d39',
        '_uetvid': '864623a08d8411f09b671961b1767c39|p6xe1j|1757426082373|1|1|bat.bing.com/p/insights/c/e'
    }
    
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
    
    try:
        print("正在发送请求到 RocketReach API...")
        response = requests.post(url, headers=headers, cookies=cookies, json=data)
        
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
                    print(f"姓名: {person.get('name', 'N/A')} {person.get('last_name', 'N/A')}")
                    print(f"当前职位: {person.get('links', 'N/A')}")
                    print(f"当前公司: {person.get('jobs', 'N/A')[0]}")
 
                    
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

def search_with_different_params(employer="Tencent", start=1, page_size=10):
    """
    使用不同参数进行搜索的函数
    """
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
        'x-csrftoken': 'r0WzJQAdxvCczQxsGrGHCg61dAn3RSlXYcJsNHOTjtYNfMoDHPveoSpFVzIiilvb',
        'x-rr-for': 'd3b946e2a7ace9368d6ec674dec4a770',
        'x-source-page': '/person'
    }
    
    cookies = {
        'src': '201',
        'ctx': 'rocketreach.co', 
        'cj2': 'L2xvZ2lu',
        'jh': '1740960000',
        '_ga': 'GA1.1.1381607328.1757425371',
        'validation_token': 'HmX3e1oQW8wLQ61lbyZHWMtOS9vpBDko',
        'sessionid-20191028': '5unq14cd9kdsvn3z04hlolhs98v64eyd',
        'hubspotutk': 'aa29a649faf8a5239c1befa040ef467f',
        '_dd_s': 'isExpired=1&aid=9a4483f2-1e64-44bf-8a2e-3a36d094f719; _clck=5rr103^5E2^5Efzq^5E0^5E2078',
        '_gcl_au': '1.1.1505756196.1757425371.1872715732.1759145773.1759146226',
        '_cfuvid': 'UhwIq8OpxZx3yg3iBapyFo72blJstYFOav4PVIkoHMo-1759146683519-0.0.1.1-604800000',
        '__hssrc': '1',
        '__hstc': '94151554.aa29a649faf8a5239c1befa040ef467f.1757426083401.1759147034688.1759149078343.10',
        '__hssc': '94151554.3.1759149078343',
        '_ga_FB8KKHJC7E': 'GS2.1.s1759149037$o10$g1$t1759149541$j58$l0$h0',
        '_rdt_uuid': '1757425370365.8795a97e-7864-46fc-b471-332725285ef9',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Sep+29+2025+20%3A39%3A02+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d1a7fb8c-4e74-4f2f-8039-8d9a09817a01&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
        '_clsk': '1mafs3n^5E1759149542231^5E4^5E0^5Ei.clarity.ms/collect',
        '_uetsid': '1134b6109d2811f084d2010d85618d39',
        '_uetvid': '864623a08d8411f09b671961b1767c39|p6xe1j|1757426082373|1|1|bat.bing.com/p/insights/c/e'
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
    
    try:
        print(f"正在搜索公司: {employer}, 从第{start}页开始，每页{page_size}条...")
        response = requests.post(url, headers=headers, cookies=cookies, json=data)
        
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
    主函数 - 演示如何使用API并解析people字段
    """
    print("=== RocketReach API 人员数据解析演示 ===\n")
    
    # 1. 基本搜索 - 搜索腾讯员工
    print("1. 搜索腾讯员工并解析people字段:")
    people_data = make_rocketreach_request()
    
    print("\n" + "="*50 + "\n")
    
    # 2. 保存数据到文件
    if people_data:
        save_people_to_file(people_data, "tencent_employees.json")
        analyze_people_data(people_data)
    

    
    print("\n" + "="*50 + "\n")
    
    # 5. 综合数据处理
    print("4. 综合数据处理示例:")
    combined_people = people_data 
    print(f"合并后的总数据量: {len(combined_people)} 条记录")
    
    if combined_people:
        save_people_to_file(combined_people, "combined_employees.json")
        analyze_people_data(combined_people)
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    main()



