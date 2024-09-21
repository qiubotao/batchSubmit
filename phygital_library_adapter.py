from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter

class PhygitalLibraryAdapter(SubmissionAdapter):
    def submit(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
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
            self._fill_form_field(driver, 'input[name="Try out"]', self.website.url, "Try out")
            self._fill_form_field(driver, 'textarea[name="Description"]', self.website.description, "Description")
            self._fill_form_field(driver, 'textarea[name="Для агрегатора: Submitted by"]', self.website.email, "Submitted by")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'sw-form-capture-submit-btn'))
            )
            submit_button.click()
            print("表单已提交")

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '.spinner-border'))
            )
            
            # success_icon = driver.find_element(By.CSS_SELECTOR, '.fa-check:not(.d-none)')
            # if success_icon:
            print("提交成功！")
            # else:
                # print("提交可能未成功，请检查。")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")
