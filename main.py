from flet import *
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)
def main(page:Page):
    page.window.width = 360
    page.window.height = 640
    page.rtl = True
    page.padding = padding.only(bottom=10, left=20, right=20, top=10)
    page.appbar = CupertinoAppBar(title="FaciAi")
    
    ac = Column(scroll=ScrollMode.ALWAYS,expand=True)
    
    def chat(e):
        a = Text(value="",expand=True)
        ac.controls.append(Container(bgcolor="blue",content=a,border_radius=20,padding=10))
        page.update()
        
        messages = [{"role": "system", "content": "You are a helpful ai"}]
    
        user_input = us.value
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="groq/compound",
                messages=messages,
                #stream=True
            )
            
            reply = response.choices[0].message.content
            a.value = reply
                    
            page.update()
            
        except Exception as ex:
            a.value = "Try Later"
            page.update()
    
    us = TextField("Type Any Thing",expand=True)
    
    
    page.add(ac,Row([us,IconButton(icon=Icons.SEND,on_click=chat)]))
    
if __name__ == "__main__":
    run(main)
