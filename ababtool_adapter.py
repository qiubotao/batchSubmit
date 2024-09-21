from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
#  有不少流量，但未成功

class AbabToolsAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 ABABTOOLS 提交页面...")
        driver.get('https://ababtools.com/?post=1292')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            # 额外等待，确保页面完全加载
            time.sleep(15)
            
            # 检查是否存在表单元素
            if not driver.find_elements(By.CSS_SELECTOR, 'form.ant-form'):
                print("警告：未找到预期的表单元素")

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'input[name="field_1"]', self.website.name, "产品名称")
            self._fill_form_field(driver, 'textarea[name="field_4"]', self.website.description, "产品介绍、功能特征、产品定价")
            self._fill_form_field(driver, 'input[name="field_13"]', self.website.url, "网址")
            self._fill_form_field(driver, 'input[name="field_3"]', self.website.email, "联系方式")

            # 上传附件（如果有的话）
            if hasattr(self.website, 'image_path'):
                self._upload_file(driver, 'input[type="file"]', self.website.image_path)

            # 填写补充信息（如果有的话）
            if hasattr(self.website, 'additional_info'):
                self._fill_form_field(driver, 'textarea[name="field_12"]', self.website.additional_info, "补充信息")

            print("表单填写完成")

            # 提交表单
            # self._submit_form(driver)

            # 检查提交是否成功
            # self._check_submission_success(driver)

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

    def _upload_file(self, driver, selector, file_path):
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, selector)
            file_input.send_keys(file_path)
            print("已上传附件")
        except Exception as e:
            print(f"上传附件时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="button"].ant-btn-primary')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"].ant-btn-primary')))
            
            # 使用 JavaScript 直接点击元素
            driver.execute_script("arguments[0].click();", submit_button)
            
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            # 这里需要根据实际情况调整成功提交的判断条件
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-message-success'))
            )
            if success_message:
                print("提交成功")
            else:
                print("提交失败或未找到成功消息")
        except Exception as e:
            print(f"检查提交成功时出错: {str(e)}")