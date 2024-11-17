from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AiToolNavigationAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AI Tool Navigation 页面...")
        driver.get('https://www.aitoolnavigation.com/')

        try:
            print("等待页面加载...")
            # 等待"Submit a tool"按钮出现
            submit_tool_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'button.bg-gray-700.text-white.hover\\:bg-black.rounded-3xl[data-v-dea5d471]'
                ))
            )
            
            print("点击'Submit a tool'按钮...")
            submit_tool_button.click()
            
            # 等待提交表单出现
            print("等待提交表单加载...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    'div[data-v-dea5d471] input.block.w-full.mt-1.rounded-2xl'
                ))
            )

            print("页面已加载，正在填写表单...")

            # 填写网站链接
            self._fill_form_field(
                driver, 
                'input.block.w-full.mt-1.rounded-2xl.p-1.px-4', 
                self.website.url,
                "Website URL",
                index=0
            )

            # 填写问题解决说明
            self._fill_form_field(
                driver, 
                'textarea.block.w-full.mt-1.rounded-2xl.p-1.px-4',
                self.website.description,
                "Problem Description"
            )

            # 填写邮箱
            self._fill_form_field(
                driver,
                'input.block.w-full.mt-1.rounded-2xl.p-1.px-4',
                self.website.email,
                "Email",
                index=1
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

    def _fill_form_field(self, driver, selector, value, field_name, index=None):
        try:
            if index is not None:
                fields = driver.find_elements(By.CSS_SELECTOR, selector)
                field = fields[index]
            else:
                field = driver.find_element(By.CSS_SELECTOR, selector)
            
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(
                By.CSS_SELECTOR, 
                'button.bg-blue-600.text-white.p-2.w-full.sm\\:w-20.my-3.rounded-3xl'
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
            
            # 检查URL变化或成功消息
            current_url = driver.current_url
            if "success" in current_url or "thank-you" in current_url:
                print("提交成功")
            else:
                # 尝试查找可能的成功提示
                try:
                    success_elements = driver.find_elements(
                        By.CSS_SELECTOR, 
                        '.success-message, .text-green-500, [data-success]'
                    )
                    if success_elements:
                        print("提交成功")
                    else:
                        print("提交状态未知，请手动检查")
                except:
                    print("提交状态未知，请手动检查")
        except Exception as e:
            print(f"检查提交结果时出错: {str(e)}")
