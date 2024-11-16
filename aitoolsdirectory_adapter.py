from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AitoolsdirectoryAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AI Tools Directory 提交页面...")
        driver.get('https://aitoolsdirectory.com/submit-tool')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form[data-testid="livefieldsection"]'))
            )

            print("页面已加载，正在填写表单...")

            # 填写产品名称
            self._fill_form_field(driver, 'input[name="Name of product"]', 
                                self.website.name, "产品名称")
            
            # 填写URL
            self._fill_form_field(driver, 'input[name="URL"]', 
                                self.website.url, "URL")
            
            # 选择定价模式 (Freemium)
            self._select_pricing(driver)
            
            # 填写简短描述 (需要至少130字符)
            short_desc = self.website.description[:150]
            if len(short_desc) < 130:
                short_desc = self.website.description[:130]
            self._fill_form_field(driver, 'input[name="Short description (20-30 words)"]', 
                                short_desc, "简短描述")
            
            # 填写详细描述 (需要至少300字符)
            long_desc = self.website.description
            if len(long_desc) < 300:
                long_desc = self.website.description * 2  # 重复内容以达到最小长度要求
            self._fill_form_field(driver, 'input[name="Long description (50-500 words)"]', 
                                long_desc, "详细描述")
            
            # 填写标签
            self._fill_form_field(driver, 'input[name="Tags / Keywords / Hashtags"]', 
                                "#ai #tool", "标签")
            
            # 填写姓名
            self._fill_form_field(driver, 'input[name="Your name"]', 
                                self.website.user_name, "姓名")
            
            # 填写邮箱
            self._fill_form_field(driver, 'input[name="Your email"]', 
                                self.website.email, "邮箱")

            print("表单填写完成，准备提交...")
            
            # 等待用户确认
            input("请检查表单内容，按回车键继续提交...")

            # 提交表单
            # self._submit_form(driver)

            # 等待提交结果
            # self._check_submission_result(driver)

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            input("按回车键关闭浏览器...")
            driver.quit()

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

    def _select_pricing(self, driver):
        try:
            pricing_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.Select-value-label'))
            )
            pricing_div.click()
            
            freemium_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Freemium')]"))
            )
            freemium_option.click()
            print("已选择定价模式: Freemium")
        except Exception as e:
            print(f"选择定价模式时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-primary'))
            )
            submit_button.click()
            print("已点击提交按钮")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _check_submission_result(self, driver):
        try:
            time.sleep(5)  # 等待提交响应
            # 这里需要根据实际情况添加成功提交的判断逻辑
            print("正在检查提交结果...")
            
            # 可以通过URL变化、成功消息等来判断
            current_url = driver.current_url
            print(f"当前页面URL: {current_url}")
            
        except Exception as e:
            print(f"检查提交结果时出错: {str(e)}")