from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class InsidrAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Insidr.ai 提交页面...")
        driver.get('https://www.insidr.ai/submit-tools/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "elementor-form"))
            )

            print("页面已加载，正在填写表单...")

            # 填写工具描述
            self._fill_form_field(
                driver, 
                '#form-field-message', 
                self.website.description, 
                "Message"
            )

            # 填写工具链接
            self._fill_form_field(
                driver, 
                '#form-field-name', 
                self.website.url, 
                "Link"
            )

            # 填写工具分类
            self._fill_form_field(
                driver, 
                '#form-field-email', 
                self.website.category,  # 使用 website 对象的 category 属性
                "Tag"
            )

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 检查提交是否成功
            self._check_submission_success(driver)

            # 等待用户确认
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            # 使用新的选择器定位提交按钮
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'button.sc-jTzLTM[type="submit"]'
                ))
            )
            
            # 如果需要填写邮箱
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'input[type="email"].sc-gZMcBi'
                ))
            )
            email_input.clear()
            email_input.send_keys(self.website.email)  # 确保 website 对象有 email 属性
            print("已填写邮箱地址")
            
            # 滚动到提交按钮可见位置
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", 
                submit_button
            )
            
            # 等待按钮可点击
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    'button.sc-jTzLTM[type="submit"]'
                ))
            )
            
            # 使用 JavaScript 点击提交按钮
            driver.execute_script("arguments[0].click();", submit_button)
            
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            # 等待成功消息出现
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'elementor-message-success')
                )
            )
            if success_message:
                print("提交成功")
            else:
                print("提交失败或未找到成功消息")
        except Exception as e:
            print(f"检查提交成功时出错: {str(e)}")
