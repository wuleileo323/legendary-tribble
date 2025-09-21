import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# --- 配置 ---
EXCEL_FILE_PATH = 'processed_data.xlsx'  # <-- 修改为你的Excel文件路径
CHROMEDRIVER_PATH = 'D:/Trae/chromedriver-win64/chromedriver.exe'  # <-- 修改为你的chromedriver路径
OUTPUT_COLUMN_NAME = '是否公开'  # 新增列的名称
WAIT_TIME_BETWEEN_URLS = 10  # 访问每个URL之间的等待时间（秒）
PAGE_LOAD_TIMEOUT = 15  # 页面加载超时时间（秒）
ELEMENT_WAIT_TIMEOUT = 10  # 等待特定元素出现的超时时间（秒）
CHECK_TEXT = "内容暂时无法显示"  # 要检查的文本
# --- 配置结束 ---


def check_single_facebook_page(driver, url):
    """
    访问单个 Facebook 页面并检查内容。
    Args:
        driver (webdriver.Chrome): 已连接的 WebDriver 实例。
        url (str): 要访问的 Facebook 页面 URL。
    Returns:
        str: 检查结果 ("私密", "公开", "访问失败", "未知错误")。
    """
    try:
        print(f"正在访问: {url}")
        # 设置页面加载超时
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.get(url)
        print("页面加载中...")

        # 等待页面基本加载完成
        WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 等待一段时间让动态内容加载（可根据需要调整）
        #time.sleep(5) 

        # 尝试查找包含特定文本的元素
        try:
            element = WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{CHECK_TEXT}')]"))
            )
            print(f"  -> 检测到: '{CHECK_TEXT}'")
            return "私密"
        except TimeoutException:
            print(f"  -> 未检测到: '{CHECK_TEXT}'")
            return "公开"

    except TimeoutException:
        print(f"  -> 错误: 访问 {url} 超时。")
        return "访问失败"
    except WebDriverException as e:
        print(f"  -> 错误: 访问 {url} 时 WebDriver 出错: {e}")
        return "访问失败"
    except Exception as e:
        print(f"  -> 错误: 检查 {url} 时发生未知错误: {e}")
        return "未知错误"


def main():
    """
    主函数：读取Excel，处理URL，更新结果并保存。
    """
    # 1. 读取Excel文件
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        print(f"成功读取Excel文件: {EXCEL_FILE_PATH}")
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return

    # 检查是否存在 'facebook' 列
    if 'facebook' not in df.columns:
        print("错误: Excel文件中未找到名为 'facebook' 的列。")
        return

    # 2. 初始化 WebDriver
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = None

    try:
        print("正在连接到 Chrome 实例...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("连接成功。")

        # 3. 确保输出列存在
        if OUTPUT_COLUMN_NAME not in df.columns:
            df[OUTPUT_COLUMN_NAME] = '' # 初始化为空字符串

        # 4. 遍历 'facebook' 列中的每个URL
        total_urls = len(df['facebook'])
        for index, url in enumerate(df['facebook']):
            print(f"\n--- 处理第 {index + 1}/{total_urls} 个URL ---")
            
            if pd.isna(url) or not isinstance(url, str) or not url.strip():
                 print(f"跳过无效URL: {url}")
                 df.at[index, OUTPUT_COLUMN_NAME] = "无效URL"
                 # 仍然等待，保持节奏
                 if index < total_urls - 1: # 最后一个URL后不需要等待
                    print(f"等待 {WAIT_TIME_BETWEEN_URLS} 秒...")
                    time.sleep(WAIT_TIME_BETWEEN_URLS)
                 continue

            # 检查页面
            result = check_single_facebook_page(driver, url.strip())
            # 将结果写入DataFrame
            df.at[index, OUTPUT_COLUMN_NAME] = result

            # 在访问下一个URL前等待指定时间（除了最后一个）
            if index < total_urls - 1:
                print(f"等待 {WAIT_TIME_BETWEEN_URLS} 秒...")
                time.sleep(WAIT_TIME_BETWEEN_URLS)

        # 5. 保存更新后的DataFrame回Excel文件
        # 为了避免覆盖原文件，可以保存为新文件，或确认覆盖
        # output_file_path = EXCEL_FILE_PATH # 覆盖原文件
        output_file_path = 'facebook_urls_with_results.xlsx' # 保存为新文件
        try:
            df.to_excel(output_file_path, index=False)
            print(f"\n结果已保存到: {output_file_path}")
        except Exception as e:
            print(f"保存Excel文件失败: {e}")

    except Exception as e:
        print(f"初始化WebDriver或处理过程中发生错误: {e}")
    finally:
        # 关闭 WebDriver 会话
        if driver:
            driver.close() # 仅关闭当前标签页，保持浏览器运行
            print("已关闭 WebDriver 会话。")

if __name__ == "__main__":
    main()




