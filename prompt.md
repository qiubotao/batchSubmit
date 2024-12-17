
# 推广词
角色：你是网站推广运营专家，能根据我的网站特点，去各个平台填写我的网站介绍，提交外链。
背景：我做的网站是AI 视频总结网站，网站链接是 https://videosummarizers.ai/
1. **上传视频**
   - 点击"选择视频"按钮
   - 选择本地视频文件（支持 MP4 格式）
   - 等待视频上传完成

2. **生成思维导图**
   - 点击"生成思维导图"按钮
   - 等待 AI 分析完成
   - 使用缩放工具查看思维导图详情

3. **生成时间线**
   - 点击"生成时间线"按钮
   - 查看视频内容时间轴
   - 点击时间点快速定位视频位置

4. **智能问答**
   - 在输入框中输入问题
   - 点击"提问"按钮
   - 查看 AI 回答结果
任务：帮我生成对应的网站介绍内容。基于这个内容修改下面的网站推广词
class Website:
    def __init__(self, url, name, description, email, category, user_name, pricing_model, user_first_name, image_path, content, category_for_aitoolnet):
        self.url = url
        self.name = name
        self.description = description
        self.email = email
        self.category = category
        self.user_name = user_name
        self.pricing_model = pricing_model
        self.user_first_name = user_first_name
        self.image_path = image_path
        self.content = content
        self.category_for_aitoolnet = category_for_aitoolnet


# 定义结构化数据
my_website = Website(
    url="https://videoaihub.ai/",
    name="VIDEO AI HUB",
    description="One-stop AI Video Generation Information and Tools Platform",
    email="bertoltwork@gmail.com",
    category="AI,Video Generator",
    user_name= "Bertolt",
    user_first_name="Q",
    pricing_model="Freemium",
    image_path="/Users/viola/Downloads/image/videoaihub/logo.png",  # 替换为实际的文件路径
    content="""keyFeature:\n 
- Discover various AI video generation platforms and their technologies. For example, Minimax AI excels in generating high-quality, expressive videos from complex text prompts, while Luma AI specializes in 3D generation and animation. Learn about their features, underlying technologies, strengths, and limitations.
- Explore AI video generation tools for text-to-video and image-to-video creation. Tools like Minimax AI and Luma AI offer a range of powerful features that help users effortlessly create high-quality video content. Compare the output of different AI video generation tools.
- Support for adding video effects, such as video effects from Pika1.5. 
- Users can earn points by logging in, with daily logins adding points. Points can be purchased on a per-use, monthly, or yearly basis, and generating videos will consume the corresponding points.
""",

    
    #  不同网站的定制化
    category_for_aitoolnet="Video"
)


【自荐】
产品：VideoSummarizers.ai
产品地址：https://videosummarizers.ai
简介：VideoSummarizers.ai 是一款基于 AI 的视频总结平台，提供上传视频、生成思维导图、生成视频时间线、以及智能问答等多种功能，帮助用户快速提炼视频核心内容。平台支持 MP4 格式的视频上传，并通过 AI 分析生成结构化内容，提升视频学习和内容发现效率。
特点：
上传视频：支持上传 MP4 格式的视频，快速生成总结。
思维导图生成：通过 AI 分析生成详细思维导图，帮助用户全面理解视频内容。
时间线功能：生成结构化时间线，快速定位视频关键内容。
智能问答：基于视频内容，用户可以提问，AI 自动生成精准回答。
