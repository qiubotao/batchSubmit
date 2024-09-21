from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
import os

class SupertoolsAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Supertools 提交页面...")
        driver.get('https://supertools.therundown.ai/submit')

        try:
            print("等待页面加载...")
            self._wait_for_page_load(driver)

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, "//input[@placeholder='Tool name ']", self.website.name, "Tool name")
            self._fill_form_field(driver, "//textarea[@placeholder='One to two sentences max.']", self.website.description, "Tool description")
            self._fill_form_field(driver, "//input[@placeholder='Free, paid, or both']", self.website.pricing_model, "Price")
            self._fill_form_field(driver, "//input[@placeholder='Which category fits your tool best?']", self.website.category, "Category")
            self._fill_form_field(driver, "//input[@placeholder='Link to your tool home page']", self.website.url, "Tool link")
            self._fill_form_field(driver, "//input[@placeholder='Optional']", '', "Affiliate registration link")
            self._fill_form_field(driver, "//input[@placeholder='@companytwitterhandle ']", '', "Tool Twitter handle")
            self._fill_form_field(driver, "//input[@placeholder='Tool creator email']", self.website.email, "Tool creator email")
            self._upload_image(driver, self.website.image_path)

            print("表单填写完成")

            # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _wait_for_page_load(self, driver, timeout=30):
        try:
            # 等待页面标题
            WebDriverWait(driver, timeout).until(EC.title_contains("Submit"))
            
            # 等待表单出现
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            
            # 使用JavaScript检查页面加载状态
            is_ready = driver.execute_script("return document.readyState") == "complete"
            
            if not is_ready:
                print("页面加载可能未完成，但将继续执行...")
            
        except Exception as e:
            print(f"等待页面加载时出错: {str(e)}")
            print("将尝试继续执行...")

    def _fill_form_field(self, driver, xpath, value, field_name):
        try:
            # 增加等待时间和重试逻辑
            for _ in range(3):  # 尝试3次
                try:
                    field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    field.clear()
                    field.send_keys(value)
                    print(f"已填写 '{field_name}' 字段")
                    break
                except:
                    print(f"填写 '{field_name}' 字段失败，正在重试...")
                    time.sleep(2)
            else:
                print(f"填写 '{field_name}' 字段失败")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _upload_image(self, driver, image_path):
        try:
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(os.path.abspath(image_path))
            print("已上传缩略图")
        except Exception as e:
            print(f"上传缩略图时出错: {str(e)}")

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

    def _check_submission_success(self, driver):
        try:
            # 这里需要根据实际情况调整成功消息的选择器
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.success-message'))
            )
            if success_message:
                print("提交成功")
            else:
                print("提交失败或未找到成功消息")
        except Exception as e:
            print(f"检查提交成功时出错: {str(e)}")