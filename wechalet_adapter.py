from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class WechaletAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Wechalet 提交页面...")
        driver.get('https://wechalet.cn/appstore/add')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'webEmail')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'webEmail', self.website.email, "邮件地址")
            self._fill_form_field(driver, 'webLink', self.website.url, "网站地址")
            self._fill_form_field(driver, 'webInfo', self.website.description, "网站介绍")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 检查提交是否成功
            # self._check_submission_success(driver)

            # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, field_id, value, field_name):
        try:
            field = driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.ID, 'submit')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit')))
            
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