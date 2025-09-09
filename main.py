from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class ContentPipelineState(BaseModel):

    # Inputs
    content_type: str = ""
    topic: str = ""
    
    # Internal
    max_length: int = 0
    score: int = 0

    blog_post: str = ""
    tweet_post: str = ""
    linkedin_post: str = ""

class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ["tweet", "blog", "linkedin"]:
            raise ValueError("The content type is wrong")
        
        if self.state.topic == "":
            raise ValueError("The topic can't be blank")

        if self.state.content_type == "tweet":
            self.state.max_length = 150
        elif self.state.content_type == "blog":
            self.state.max_length = 800
        elif self.state.content_type == "tweet":
            self.state.max_length = 500
    
    @listen(init_content_pipeline)
    def conduct_research(self):
        print("Researching...")
        return True
    
    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        elif content_type == "linkedin":
            return "make_linkedin"
    
    @listen(or_("make_blog", "redo_blog"))
    def handle_make_blog(self):
        print("Making blog...")
    
    @listen(or_("make_tweet", "redo_tweet"))
    def handle_make_tweet(self):
        print("Making tweet...")
    
    @listen(or_("make_linkedin", "redo_linkedin"))
    def handle_make_linkedin(self):
        print("Making linkedin...")
    
    @listen(handle_make_blog)
    def check_seo(self):
        print("Checking Blog SEO...")
    
    @listen(or_(handle_make_tweet, handle_make_linkedin))
    def check_virality(self):
        print("Checking virality...")

    @router(or_(check_seo, check_virality))
    def score_router(self):

        content_type = self.state.content_type
        score = self.state.score

        if score >= 8:
            return "check_passed"
        else:
            if content_type == "blog":
                return "redo_blog"
            elif content_type == 'linkedin':
                return "redo_linkedin"
            elif content_type == 'tweet':
                return 'redo_tweet'

    @listen("check_passed")
    def finalize_content(self):
        print("Finalizing content")

flow = ContentPipelineFlow()
flow.kickoff(inputs={"content_type": "tweet", "topic": "AI Dog Training",},)