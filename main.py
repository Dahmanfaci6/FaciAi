from flet import *
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)
def main(page:Page):
    page.window.width = 360
    page.window.height = 640
    page.padding = 10
    page.bgcolor = "#100b36"
    page.appbar = CupertinoAppBar(leading=IconButton(icon=Icons.PERSON,icon_color="#100b36"),trailing=IconButton(icon=Icons.CAMERA_ALT,icon_color="#100b36"),title=Text("Welcome to FaciAi",color="#100b36"),automatic_background_visibility=False,bgcolor="white",brightness=Brightness.LIGHT)
    
    ac = Column(scroll=ScrollMode.ALWAYS,expand=True)
    
    def Utext(e):
        ac.controls.append(Row([Icon(icon=Icons.PERSON,color="white"),Text(value=us.value,color="white",)],vertical_alignment=CrossAxisAlignment.START,rtl=True))
    
    def chat(e):
        a = Text(value="",expand=True,color="white",selectable=True)
        ac.controls.append(Row([Icon(icon=Icons.SMART_TOY,color="white"),Container(content=a,border_radius=20,padding=10,bgcolor="#20f4f4f4",blur=Blur(10,10,BlurTileMode.MIRROR),shadow=BoxShadow(1,15,Colors.BLUE_GREY_300,Offset(2,2),BlurStyle.OUTER),expand=True)],vertical_alignment=CrossAxisAlignment.START))
        page.update()
        
        messages = [{"role": "system", "content": "You are a helpful ai"}]
    
        user_input = us.value
        
        messages.append({"role": "user", "content": user_input})
        #groq/compound
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
            )
            
            reply = response.choices[0].message.content
            a.value = reply
                    
            page.update()
            
        except Exception as ex:
            a.value = "Try Later"
            page.update()
        page.update()
    
    us = TextField(hint_text="Type Any Thing",hint_style=TextStyle(color="grey"),expand=True,border_radius=30,border_color="white",color="white",border_width=2)
    
    
    page.add(ac,Row(controls=[us,IconButton(icon=Icons.SEND,on_click=lambda e:(Utext(e),chat(e)),bgcolor="white",icon_color="black")],margin=Margin.only(bottom=25),))
    
if __name__ == "__main__":
    run(main)
