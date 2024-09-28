import requests
from submission_adapter import SubmissionAdapter

class AiNavigationAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        data = {
            'url': self.website.url,
            'name': self.website.name,
            'email': self.website.email
        }
        
        response = requests.post('https://www.ai-navigation.net/api/submit', json=data)
        
        if response.status_code == 200:
            print('提交到 AI Navigation 成功!')
            print(f'响应内容: {response.text}')
        else:
            print(f'提交到 AI Navigation 失败。错误代码: {response.status_code}')
            print(f'错误信息: {response.text}')
