from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class DropYourAIAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 DropYourAI 提交页面...")
        driver.get('https://www.dropyourai.com/submit-tool')

        try:
            print("等待页面加载...")
            self._wait_for_page_load(driver)
            
            print("页面已加载，正在填写表单...")
            
            # 填写必填字段
            self._fill_form_field(driver, '#input_comp-lk5wclbm', self.website.name, "Project Name")
            self._fill_form_field(driver, '#input_comp-lklog3b66', self.website.email, "Email")
            self._fill_form_field(driver, '#input_comp-lkloggvo1', self.website.url, "Website URL")
            
            # 上传图片
            if self.website.image_path:
                self._upload_image(driver, self.website.image_path)
            
            # 选择定价类型
            self._select_pricing_type(driver, self.website.pricing_type)
            
            # 填写价格信息(如果是付费的)
            if self.website.pricing_type == "Paid":
                self._fill_pricing_info(driver)
            
            # 填写描述
            self._fill_form_field(driver, '#input_comp-lk5wlm9y3', self.website.short_description, "Short Description")
            self._fill_form_field(driver, '#textarea_comp-lk5wsr9b', self.website.description, "Long Description")
            
            # 选择AI分类
            self._select_ai_category(driver, self.website.category)
            
            # 可选字段
            if self.website.youtube_url:
                self._fill_form_field(driver, '#input_comp-lk5wj7iv', self.website.youtube_url, "Youtube URL")
            if self.website.twitter_url:
                self._fill_form_field(driver, '#input_comp-lkgmxpld', self.website.twitter_url, "Twitter URL")
            if self.website.linkedin_url:
                self._fill_form_field(driver, '#input_comp-lk5x4hgc4', self.website.linkedin_url, "LinkedIn URL")
            
            print("表单填写完成")
            
            # 提交表单
            self._submit_form(driver)
            
            # 检查提交结果
            self._check_submission_success(driver)
            
            input("请检查提交结果，按回车键关闭浏览器...")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            driver.quit()

    def _select_pricing_type(self, driver, pricing_type):
        try:
            radio_selector = f'input[name="comp-lkoezacg"][value="{pricing_type}"]'
            radio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, radio_selector))
            )
            radio.click()
            print(f"已选择定价类型: {pricing_type}")
        except Exception as e:
            print(f"选择定价类型时出错: {str(e)}")

    def _select_ai_category(self, driver, category):
        try:
            select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'collection_comp-lkfvfvjd'))
            )
            select.click()
            option = driver.find_element(By.CSS_SELECTOR, f'option[value="{category}"]')
            option.click()
            print(f"已选择AI分类: {category}")
        except Exception as e:
            print(f"选择AI分类时出错: {str(e)}")
