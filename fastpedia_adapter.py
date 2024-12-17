from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
import os

class FastpediaAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Fastpedia 提交页面...")
        driver.get('https://fastpedia.io/submit-tool/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'wpcf7-form')))

            print("页面已加载，正在填写表单...")

            # 基本信息
            self._fill_form_field(driver, 'input[name="text-136"]', self.website.name, "Tool Name")
            self._fill_form_field(driver, 'input[name="text-974"]', self.website.url, "Official Website")
            self._fill_form_field(driver, 'input[name="email-716"]', self.website.email, "Contact Email")
            
            # 选择类别
            self._select_form_field(driver, 'select[name="menu-85"]', "Video generator", "Tool Category")
            
            # 价格模型
            self._select_radio_field(driver, 'input[name="radio-784"]', self.website.pricing_model, "Pricing Model")
            
            # 描述信息
            self._fill_form_field(driver, 'textarea[name="textarea-671"]', self.website.description[:300], "Short Description")
            self._fill_form_field(driver, 'textarea[name="textarea-676"]', self.website.content, "Purpose")
            self._fill_form_field(driver, 'input[name="text-959"]', self.website.category, "Tags")

            # 上传图片
            if self.website.image_path:
                self._upload_file(driver, 'input[name="file-641"]', self.website.image_path, "Logo")
                # self._upload_file(driver, 'input[name="file-232"]', self.website.image_path, "Screenshot")

            print("表单填写完成")
            input("wait")

            # 提交表单
            self._submit_form(driver)

            # 等待用户确认
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            driver.quit()

    def _upload_file(self, driver, selector, file_path, field_name):
        try:
            if os.path.exists(file_path):
                file_input = driver.find_element(By.CSS_SELECTOR, selector)
                file_input.send_keys(os.path.abspath(file_path))
                print(f"已上传 {field_name}")
            else:
                print(f"文件不存在: {file_path}")
        except Exception as e:
            print(f"上传 {field_name} 时出错: {str(e)}")

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            field.clear()
            field.send_keys(value)
            print(f"已填写 {field_name}")
        except Exception as e:
            print(f"填写 {field_name} 时出错: {str(e)}")

    def _select_form_field(self, driver, selector, value, field_name):
        try:
            select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            for option in select.find_elements(By.TAG_NAME, 'option'):
                if option.text == value:
                    option.click()
                    print(f"已选择 {field_name}: {value}")
                    break
        except Exception as e:
            print(f"选择 {field_name} 时出错: {str(e)}")

    def _select_radio_field(self, driver, selector, value, field_name):
        try:
            radio_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            for radio in radio_buttons:
                if radio.get_attribute('value') == value:
                    if not radio.is_selected():
                        radio.click()
                    print(f"已选择 {field_name}: {value}")
                    break
        except Exception as e:
            print(f"选择 {field_name} 时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.wpcf7-submit'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            submit_button.click()
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")
