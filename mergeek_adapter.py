from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class MergeekAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 Mergeek 提交页面...")
        driver.get('https://mergeek.com/publish_project')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'publish_project_card')))

            print("页面已加载，正在填写表单...")

            # 处理标签
            tags = self.website.category if isinstance(self.website.category, list) else [self.website.category]
            tags = [tag.strip() for tag in tags if tag.strip()]  # 移除空白标签
            tags = tags[:5]  # 限制为5个标签
            tags_string = ",".join(tags)

            self._fill_form_field(driver, 'publish_project_name', self.website.name, "产品名称")
            self._fill_form_field(driver, 'publish_project_website', self.website.url, "相关产品网址")
            self._fill_form_field(driver, 'publish_project_desc', self.website.description[:200], "产品介绍")
            self._fill_form_field(driver, 'publish_project_codes', "", "高级权益兑换码")
            self._fill_form_field(driver, 'publish_project_tags', tags_string, "标签")
            self._fill_form_field(driver, 'publish_project_email_address', self.website.email, "电子邮件地址")

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
            submit_button = driver.find_element(By.CLASS_NAME, 'publish_project_submit_btn')
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 等待元素可点击
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'publish_project_submit_btn')))
            
            # 使用 JavaScript 直接点击元素
            driver.execute_script("arguments[0].click();", submit_button)
            
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")