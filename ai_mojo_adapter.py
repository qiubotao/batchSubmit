from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
# 不成功，后面再看
class AiMojoToolsAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AiMojo 提交页面...")
        driver.get('https://app.startinfinity.com/form/74803cbc-5cf6-4e0e-8f53-42a367d5d59d')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'input[placeholder="Enter"][type="text"]', self.website.user_name, "Your Name")
            self._fill_form_field(driver, 'input[placeholder="Enter"][type="email"]', self.website.email, "Your Email")
            self._fill_form_field(driver, 'div[data-test-dynamic="longtext-form-frontend-input"] .ProseMirror', self.website.name, "Tool Name")
            self._fill_form_field(driver, 'input[data-test-dynamic="text-form-frontend-input"][type="text"]', self.website.url, "TOOL URLs")  # 更新选择器
            self._fill_form_field(driver, 'div[data-test-dynamic="longtext-form-frontend-input"] .ProseMirror', self.website.description, "Tool Description")
            self._fill_form_field(driver, 'div[data-test-dynamic="longtext-form-frontend-input"] .ProseMirror', self.website.description, "Any Comments")
            self._fill_form_field(driver, 'input[placeholder="Enter"][type="text"]', self.website.pricing_model, "Pricing Model")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 等待并捕获结果
            self._capture_submission_result(driver)

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"找到 '{field_name}' 字段，选择器: {selector}")
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段，值为: {value}")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.tw-button')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.tw-button')))
            
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
