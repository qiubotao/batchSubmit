from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AiMojoAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AiMojo 提交页面...")
        driver.get('https://aimojo.io/zh-CN/submit/')

        try:
            print("等待页面加载...")
            self._wait_for_page_load(driver)

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 
                'input[data-test-dynamic="text-form-frontend-input"]', 
                self.website.user_name, 
                "Your Name"
            )
            
            self._fill_form_field(driver, 
                'input[data-test-dynamic="email-form-frontend-input"]', 
                self.website.email, 
                "Your Email"
            )
            
            # 工具名称 - 使用富文本编辑器
            self._fill_rich_text(driver, 
                '[data-test-dynamic="longtext-form-frontend-input"]:nth-child(1)', 
                self.website.name, 
                "Tool Name"
            )
            
            # 工具URL
            self._fill_form_field(driver, 
                'input[data-test-dynamic="text-form-frontend-input"]:nth-child(2)', 
                self.website.url, 
                "TOOL URLs"
            )
            
            # 工具描述 - 使用富文本编辑器
            self._fill_rich_text(driver, 
                '[data-test-dynamic="longtext-form-frontend-input"]:nth-child(2)', 
                self.website.description, 
                "Tool Description"
            )
            
            # 选择定价模型
            self._select_pricing_model(driver, self.website.pricing_model)
            
            # 上传Logo
            if self.website.image_path:
                self._upload_logo(driver, self.website.image_path)
            
            # 填写评论
            self._fill_rich_text(driver, 
                '[data-test-dynamic="longtext-form-frontend-input"]:nth-child(3)', 
                "Looking forward to being part of AiMojo community!", 
                "Comments"
            )

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 等待用户确认
            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            driver.quit()

    def _wait_for_page_load(self, driver, timeout=30):
        try:
            # 等待表单容器加载
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tw-basis-4/6"))
            )
            
            # 等待第一个输入框加载
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-dynamic="text-form-frontend-input"]'))
            )
            
        except Exception as e:
            print(f"等待页面加载时出错: {str(e)}")
            print("将尝试继续执行...")

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

    def _fill_rich_text(self, driver, selector, value, field_name):
        try:
            editor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'{selector} .ProseMirror'))
            )
            editor.clear()
            editor.send_keys(value)
            print(f"已填写 '{field_name}' 富文本字段")
        except Exception as e:
            print(f"填写 '{field_name}' 富文本字段时出错: {str(e)}")

    def _select_pricing_model(self, driver, pricing_model):
        try:
            # 点击下拉菜单
            dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-dynamic="label-form-frontend-input"] .tw-input'))
            )
            dropdown.click()
            
            # 等待选项出现并选择
            time.sleep(1)  # 给下拉菜单动画一些时间
            
            # 这里需要根据实际的选项结构进行调整
            option = driver.find_element(By.XPATH, f"//span[contains(text(), '{pricing_model}')]")
            option.click()
            
            print(f"已选择定价模型: {pricing_model}")
        except Exception as e:
            print(f"选择定价模型时出错: {str(e)}")

    def _upload_logo(self, driver, image_path):
        try:
            # 点击上传按钮
            upload_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.sidebar-value-attachment-wrapper .tw-text-center'))
            )
            upload_button.click()
            
            # 等待文件输入框出现
            time.sleep(1)
            
            # 发送文件路径
            file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_input.send_keys(image_path)
            
            print("已上传Logo")
        except Exception as e:
            print(f"上传Logo时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-wrapper .tw-button'))
            )
            
            # 滚动到按钮可见
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            
            # 点击提交
            submit_button.click()
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")
