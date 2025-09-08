from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class MyFirstFlowState(BaseModel):

    user_id: int = 1
    is_admin: bool = False

class MyFirstFlow(Flow[MyFirstFlowState]):

    @start()
    def first(self):
        print(self.state.user_id)
        print("Hello")
    
    @listen(first)
    def second(self):
        self.state.is_admin = True
        print("World")

    @listen(first)
    def third(self):
        print("!")
    
    @listen(and_(second, third))
    def final(self):
        print(":)")

    @router(final)
    def route(self):
        a = 3
        if self.state.is_admin:
            return 'admin'
        else:
            return 'not admin'
    
    @listen("admin")
    def handle_even(self):
        print("admin")
    
    @listen("not admin")
    def handle_odd(self):
        print("not admin")

flow = MyFirstFlow()

flow.kickoff()