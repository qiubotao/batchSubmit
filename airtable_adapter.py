from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AirtableAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Airtable 提交页面...")
        driver.get('https://airtable.com/appcN6nvv5n1GpABK/pagzZyGl6fEI2RWDq/form')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="stackedLabel"]'))
            )

            print("页面已加载，正在填写表单...")

            # 填写名称
            self._fill_form_field(driver, 
                'textarea[id="fb47ff7edff10a5334cc8b56b24d6f9b"]', 
                self.website.name, 
                "Name")

            # 填写描述
            self._fill_form_field(driver,
                'textarea[id="c3299079154d3a1a91781d7fe83d9031"]',
                self.website.description,
                "Description")

            # 填写网站 URL
            self._fill_form_field(driver,
                'input[id="3e24d48ea09d1597866f49d75c6e3505"]',
                self.website.url,
                "Website")

            # 填写仓库地址（如果有的话）
            if hasattr(self.website, 'repository'):
                self._fill_form_field(driver,
                    'input[id="f6da826a02047d1186a06b0befc8cc60"]',
                    self.website.repository,
                    "Repository")

            # 选择类别
            self._click_category_selector(driver)

            print("表单填写完成")

            # 等待用户确认
            input("请检查填写的内容并手动完成分类选择，完成后按回车继续...")

            # 检查提交结果
            self._check_submission_success(driver)

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

    def _click_category_selector(self, driver):
        try:
            category_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '[aria-label="Add category to Category field"]')
                )
            )
            category_button.click()
            print("已点击类别选择器")
        except Exception as e:
            print(f"点击类别选择器时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            # 这里需要根据实际的成功提示来调整选择器
            success_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.success-message'))
            )
            if success_element:
                print("提交成功")
            else:
                print("未检测到成功提示")
        except Exception as e:
            print(f"检查提交结果时出错: {str(e)}")
