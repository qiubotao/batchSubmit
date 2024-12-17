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
    url="https://videosummarizers.ai/",
    name="Video Summarizers AI",
    description="AI-powered video summarization tools to streamline content discovery and enhance learning",
    email="bertoltwork@gmail.com",
    category="AI, Video Summarization",
    user_name="Bertolt",
    user_first_name="Q",
    pricing_model="Freemium",
    image_path="/Users/viola/ai/videosummarizer/public/logo.png",  # 替换为实际的文件路径
    content="""keyFeature:
- Upload any video and instantly generate a detailed summary with AI-powered analysis. This includes a mind map, video timeline, and key moments.
- Generate interactive mind maps that organize video content into easy-to-understand, hierarchical structures.
- View an AI-generated video timeline that breaks down content into specific moments, allowing users to jump to key points instantly.
- Engage with the video content through smart Q&A, where the AI answers questions based on the video's content, providing a deeper understanding.
- Freemium model allows users to try out basic features for free and offers premium features for more advanced needs.
""",
    category_for_aitoolnet="Video Summarization"
)
