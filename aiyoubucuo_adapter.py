from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AiyoubucuoAdapter(SubmissionAdapter):
    def __init__(self, website):
        super().__init__(website)
        self.url = "https://aiyoubucuo.com/comment.html"

    def submit(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            driver.get(self.url)
            
            # 等待评论表单加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "comment-form"))
            )
            
            # 填写评论内容
            textarea = driver.find_element(By.ID, "textarea")
            textarea.send_keys(self.website.description)
            
            # 填写称呼
            author = driver.find_element(By.ID, "author")
            author.send_keys(self.website.name)
            
            # 填写电子邮件
            email = driver.find_element(By.ID, "mail")
            email.send_keys(self.website.email)
            
            # 填写网站
            url = driver.find_element(By.ID, "url")
            url.send_keys(self.website.url)
            
            # 提交评论
            submit_button = driver.find_element(By.ID, "submit")
            # submit_button.click()
            # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")
            
            # 等待提交结果
            # time.sleep(5)
            
            # 检查提交是否成功
            try:
                success_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-success"))
                )
                if success_message:
                    print("评论提交成功")
                else:
                    print("评论提交失败或未找到成功消息")
            except Exception as e:
                print(f"检查提交成功时出错: {str(e)}")

             # 等待用户确认后再关闭浏览器
            input("请检查提交结果，按回车键关闭浏览器...")
                
        except Exception as e:
            print(f"提交过程中出错: {str(e)}")
        finally:
            driver.quit()
