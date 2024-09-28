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
    description="Discover the latest AI video generation technologies and tools, including Minimax AI and Luma AI. Create high-quality videos from text prompts and explore how AI is transforming video production. Join our platform for insights, tutorials, and more.",
    email="bertoltwork@gmail.com",
    category="AI,Video Generator",
    user_name= "Bertolt",
    user_first_name="Q",
    pricing_model="Freemium",
    image_path="/Users/viola/Downloads/logo6.png",  # 替换为实际的文件路径
    content="keyFeature:\n -Discover various AI video generation platforms and their technologies. For instance, Minimax AI excels in generating high-quality, expressive videos from complex text, while Luma AI shines in 3D generation and animation. Learn about their features, underlying technologies, advantages, and limitations. \n - Explore AI video generation tools like Minimax AI and Luma AI, which offer a range of powerful tools and features to help users easily create high-quality video content. Compare the results of different AI video generation tools. ",
    #  不同网站的定制化
    category_for_aitoolnet="Video"

)


         