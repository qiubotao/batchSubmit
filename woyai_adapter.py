from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class WoyAIAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Woy AI 提交页面...")
        driver.get('https://woy.ai/submit')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Woy AI"]')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'textarea[placeholder="Woy AI"]', self.website.name, "Website Name")
            self._fill_form_field(driver, 'textarea[placeholder="https://woy.ai/"]', self.website.url, "Website URL")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 等待并捕获结果
            # self._capture_submission_result(driver)

            # 检查提交是否成功
            self._check_submission_success(driver)

            # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[class*="button-bg"]')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class*="button-bg"]')))
            
            # 使用 JavaScript 直接点击元素
            driver.execute_script("arguments[0].click();", submit_button)
            
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _capture_submission_result(self, driver):
        print("等待页面变化...")
        time.sleep(5)  # 等待5秒，给页面一些时间来响应

        print("当前页面 URL:", driver.current_url)
        
        # 尝试查找可能的成功或错误消息
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, '.success-message, .error-message, .notification, .alert')
            if messages:
                for message in messages:
                    print("找到可能的结果消息:", message.text)
            else:
                print("未找到明确的成功或错误消息")
        except Exception as e:
            print(f"查找结果消息时出错: {str(e)}")

        # 捕获并打印页面标题
        print("页面标题:", driver.title)

        # 尝试执行JavaScript来获取页面状态
        try:
            page_state = driver.execute_script("return document.readyState;")
            print("页面状态:", page_state)
        except Exception as e:
            print(f"获取页面状态时出错: {str(e)}")

        # 尝试捕获控制台日志
        logs = driver.get_log('browser')
        if logs:
            print("浏览器控制台日志:")
            for log in logs:
                print(log)
        else:
            print("没有捕获到浏览器控制台日志")

    def _check_submission_success(self, driver):
        try:
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.w-form-done'))
            )
            if success_message and "Thank you! Your submission has been received!" in success_message.text:
                print("提交成功")
            else:
                print("提交失败或未找到成功消息")
        except Exception as e:
            print(f"检查提交成功时出错: {str(e)}")