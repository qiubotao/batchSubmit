from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class TallyAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Tally 提交页面...")
        driver.get('https://tally.so/r/nPpyBV')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'form')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'input[placeholder="jasper AI"]', self.website.name, "Tool Name")
            self._fill_form_field(driver, 'input[placeholder="https://jasper.ai/"]', self.website.url, "Tool URL")
            self._fill_form_field(driver, 'input[placeholder="email address"]', self.website.email, "Email")
            self._fill_form_field(driver, 'textarea[placeholder="Tool Description"]', self.website.description, "Description")
            self._fill_form_field(driver, 'input[placeholder="Pls mention categories that fit ur tool"]', self.website.category, "Categories")
            
            # 选择 Pricing 选项
            self._select_pricing(driver, "Freemium")

            # 上传文件
            self._upload_file(driver, 'input[type="file"]', self.website.image_path, "Tool image")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

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

    def _upload_file(self, driver, selector, file_path, field_name):
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, selector)
            file_input.send_keys(file_path)
            print(f"已上传 '{field_name}' 文件")
        except Exception as e:
            print(f"上传 '{field_name}' 文件时出错: {str(e)}")

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

    def _select_pricing(self, driver, option):
        try:
            # 找到 Pricing 输入框
            pricing_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Pricing"]')
            
            # 使用 JavaScript 设置输入框的值并触发 change 事件
            script = f"""
            arguments[0].value = "{option}";
            var event = new Event('change', {{ bubbles: true }});
            arguments[0].dispatchEvent(event);
            """
            driver.execute_script(script, pricing_input)
            
            # 等待一下，确保值已经被设置
            time.sleep(1)
            
            print(f"已选择 Pricing 选项: {option}")
        except Exception as e:
            print(f"选择 Pricing 选项时出错: {str(e)}")

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