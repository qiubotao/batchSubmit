from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
from selenium.webdriver.common.action_chains import ActionChains

# 问题： 未选选择好复选框

class AILibToolsAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AILib 提交页面...")
        driver.get('https://ailib.ru/en/add-ai/free/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'jet-form-builder')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'input[name="ai-email"]', self.website.email, "联系邮箱")
            self._fill_form_field(driver, 'input[name="ai-name"]', self.website.name, "AI 工具名称")
            self._fill_form_field(driver, 'input[name="ai-link"]', self.website.url, "AI 工具链接")
            self._fill_form_field(driver, 'textarea[name="ai-description"]', self.website.description, "AI 工具描述")

            # 选择 Industry
            self._select_form_field(driver, 'select[name="ai-specs[]"]', ["202"], "行业")

            # 选择 Task
            self._select_form_field(driver, 'select[name="ai-task[]"]', ["55"], "任务")
            
            # 选择 Tag
            self._select_form_field(driver, 'select[name="ai-tag[]"]', ["89"], "标签")


            # 选择其他选项
            # self._check_form_field(driver, 'input[name="ai_paid"]', False, "付费")
            # self._check_form_field(driver, 'input[name="ai_free"]', self.website.free, "免费")
            # self._check_form_field(driver, 'input[name="ai_trial"]', True, "试用")
            # self._check_form_field(driver, 'input[name="ai_api"]', self.website.api, "API")

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
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填 '{field_name}' 字段时出错: {str(e)}")

    def _select_form_field(self, driver, selector, values, field_name):
        try:
            select = driver.find_element(By.CSS_SELECTOR, selector)
            for value in values:
                option = select.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
                option.click()
            print(f"已选择 '{field_name}' 字段")
        except Exception as e:
            print(f"选择 '{field_name}' 字段时出错: {str(e)}")

    def _check_form_field(self, driver, selector, should_check, field_name):
        try:
            checkbox = driver.find_element(By.CSS_SELECTOR, selector)
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            
            # 使用 JavaScript 直接点击元素
            if should_check and not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
            elif not should_check and checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
            
            print(f"已设置 '{field_name}' 复选框")
        except Exception as e:
            print(f"设置 '{field_name}' 复选框时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            
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
            messages = driver.find_elements(By.CSS_SELECTOR, '.jet-form-builder-messages-wrap')
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

