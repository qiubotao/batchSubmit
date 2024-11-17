from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AiHunterAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AI Hunter 提交页面...")
        driver.get('https://ai-hunter.io/submit-ai-tool/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'forminator-module-20773'))
            )

            print("页面已加载，正在填写表单...")

            # 填写名字
            self._fill_form_field(
                driver, 
                'input[name="name-1"]', 
                self.website.user_first_name,
                "First Name"
            )

            # 填写邮箱
            self._fill_form_field(
                driver, 
                'input[name="email-1"]',
                self.website.email,
                "Email"
            )

            # 填写AI工具名称
            self._fill_form_field(
                driver, 
                'input[name="name-3"]',
                self.website.name,
                "AI Tool Name"
            )

            # 填写网站URL
            self._fill_form_field(
                driver, 
                'input[name="url-1"]',
                self.website.url,
                "AI Tool Website"
            )

            # 选择AI工具类别
            self._select_category(
                driver, 
                'select[name="select-1"]',
                "Chat",  # 这里可以根据实际需要修改类别
                "AI Tool Category"
            )

            # 选择定价模式
            self._select_pricing(
                driver, 
                'select[name="select-2"]',
                "45",  # 45 对应 Freemium
                "Pricing"
            )

            # 填写描述
            self._fill_form_field(
                driver, 
                'textarea[name="textarea-1"]',
                self.website.description,
                "AI Tool Description"
            )

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 检查提交结果
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
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _select_category(self, driver, selector, value, field_name):
        try:
            # 点击下拉框打开选项
            select = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].click();", select)
            time.sleep(1)
            
            # 选择选项
            option = driver.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
            option.click()
            print(f"已选择 '{field_name}': {value}")
        except Exception as e:
            print(f"选择 '{field_name}' 时出错: {str(e)}")

    def _select_pricing(self, driver, selector, value, field_name):
        try:
            # 点击下拉框打开选项
            select = driver.find_element(By.CSS_SELECTOR, selector)
            driver.execute_script("arguments[0].click();", select)
            time.sleep(1)
            
            # 选择选项
            option = driver.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
            option.click()
            print(f"已选择 '{field_name}': {value}")
        except Exception as e:
            print(f"选择 '{field_name}' 时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(
                By.CSS_SELECTOR, 
                'button.forminator-button-submit'
            )
            
            # 滚动到按钮可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)  # 等待滚动完成
            
            # 点击提交按钮
            submit_button.click()
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            # 等待5秒观察结果
            time.sleep(5)
            
            # 检查成功消息
            success_messages = driver.find_elements(
                By.CSS_SELECTOR, 
                '.forminator-response-message.forminator-success'
            )
            if success_messages:
                print("提交成功")
            else:
                # 检查错误消息
                error_messages = driver.find_elements(
                    By.CSS_SELECTOR, 
                    '.forminator-response-message.forminator-error'
                )
                if error_messages:
                    print("提交失败:", error_messages[0].text)
                else:
                    print("提交状态未知，请手动检查")
        except Exception as e:
            print(f"检查提交结果时出错: {str(e)}")
