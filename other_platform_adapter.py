import requests
from submission_adapter import SubmissionAdapter

class OtherPlatformAdapter(SubmissionAdapter):
    def submit(self):
        data = {
            'website_url': self.website.url,
            'website_name': self.website.name,
            'website_description': self.website.description,
            'contact_email': self.website.email
        }
        
        response = requests.post('https://other-platform.com/submit', json=data)
        
        if response.status_code == 200:
            print('提交到其他平台成功!')
            print(f'响应内容: {response.text}')
        else:
            print(f'提交到其他平台失败。错误代码: {response.status_code}')
            print(f'错误信息: {response.text}')
