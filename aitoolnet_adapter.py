from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AitoolnetAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AIToolNet 提交页面...")
        driver.get('https://www.aitoolnet.com/submit')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'dr_title')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'dr_title', self.website.name, "Name")
            self._fill_form_field(driver, 'dr_website', self.website.url, "Website")
            self._select_category(driver, self.website.category_for_aitoolnet)
            self._select_pricing(driver, self.website.pricing_model)
            self._fill_form_field(driver, 'dr_description', self.website.description, "Description")
            self._fill_form_field(driver, 'dr_content', self.website.content, "Content")
            self._fill_form_field(driver, 'dr_email', self.website.email, "Email")

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

    def _fill_form_field(self, driver, field_id, value, field_name):
        try:
            field = driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _select_category(self, driver, category):
        try:
            select = Select(driver.find_element(By.ID, 'dr_category'))
            select.select_by_visible_text(category)
            print("已选择类别")
        except Exception as e:
            print(f"选择类别时出错: {str(e)}")

    def _select_pricing(self, driver, pricing):
        try:
            select = Select(driver.find_element(By.ID, 'dr_pricingremark'))
            select.select_by_visible_text(pricing)
            print("已选择定价")
        except Exception as e:
            print(f"选择定价时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.ID, 'btnSubmit')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnSubmit')))
            
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