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

            # 使用实际的input ID
            form_fields = {
                "486c4892-a743-40a3-ba5a-d5755a7b230a": (self.website.name, "Tool name"),
                "de8ac9df-c278-4172-a1bf-841dd34d5ed1": (self.website.description, "Tool description"),
                "2e2dc17c-809a-40e0-9dd8-5333897e2ef2": (self.website.pricing_model, "Price"),
                "44766190-9401-408d-9ea7-6aacc6e84b76": (self.website.category, "Category"),
                "3d2761a8-dee9-4b54-b3c1-667e838b29da": (self.website.url, "Tool link"),
                "5b142219-6c77-4b9b-a828-dba208afa801": ("", "Affiliate registration link"),
                "d0bb218f-706b-4ab6-899c-cfd6b9eb583d": ("", "Tool Twitter handle"),
                "b9496427-555a-41f4-88b7-b547d7036196": (self.website.email, "Tool creator email")
            }

            # 填写所有表单字段
            for field_id, (value, field_name) in form_fields.items():
                self._fill_form_field(driver, field_id, value, field_name)

            # 上传图片
            self._upload_image(driver, self.website.image_path)

            print("表单填写完成")

            # 等待用户确认后再提交表单
            input("请检查表单内容，按回车键提交...")
            self._submit_form(driver)

            # 检查提交是否成功
            self._check_submission_success(driver)

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _wait_for_page_load(self, driver, timeout=30):
        try:
            # 等待表单容器加载
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sc-c94a0b56-0"))
            )
            
            # 等待进度条加载
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "progress"))
            )
            
            # 等待第一个输入框加载
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sc-e7c900b2-0"))
            )
            
        except Exception as e:
            print(f"等待页面加载时出错: {str(e)}")
            print("将尝试继续执行...")

    def _fill_form_field(self, driver, field_id, value, field_name):
        try:
            # 使用CSS选择器通过ID定位元素
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"#{field_id}"))
            )
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _upload_image(self, driver, image_path):
        try:
            # 使用更精确的选择器
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][aria-label='Resource thumbnail image ']"))
            )
            file_input.send_keys(os.path.abspath(image_path))
            print("已上传缩略图")
        except Exception as e:
            print(f"上传缩略图时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            # 使用更精确的选择器
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-5b8353b7-1.bXEisP"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
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

    def _click_next_button(self, driver):
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
            )
            next_button.click()
            print("已点击下一页按钮")
        except Exception as e:
            print(f"点击下一页按钮时出错: {str(e)}")