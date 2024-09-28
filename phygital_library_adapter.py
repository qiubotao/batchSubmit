from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter

class PhygitalLibraryAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
   
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开网页...")
        driver.get('https://library.phygital.plus/tool-submission')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, "//input[@placeholder='Link to the tool']", self.website.url, "Try out")
            self._fill_form_field(driver, "//textarea[contains(@placeholder, 'Describe the tool')]", self.website.description, "Description")
            self._fill_form_field(driver, "//textarea[contains(@placeholder, 'Share your social media handle')]", self.website.email, "Submitted by")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)


            # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, xpath, value, field_name):
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Send')]"))
            )
            submit_button.click()
            print("表单已提交")

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '.spinner-border'))
            )
            
            print("提交成功！")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")
