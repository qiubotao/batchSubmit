class Website:
    def __init__(self, url, name, description, email, category, user_name, 
                 pricing_model, user_first_name, image_path, content, 
                 category_for_aitoolnet, tags=None, funding_type=None, 
                 board_members=False):
        # Basic fields
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
        
        
        # New fields for LaunchingNext support
        self.tags = tags if tags is not None else []
        self.funding_type = funding_type
        self.board_members = board_members
