class SubmissionAdapter:
    def __init__(self, website):
        self.website = website

    def submit(self):
        raise NotImplementedError("子类必须实现此方法")
