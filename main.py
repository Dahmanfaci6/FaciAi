import threading
import requests
import pyttsx3
from flet import *

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "FaciAI/1.0 (Python chatbot; educational project)"}


def wikipedia_answer(question: str) -> str:
    """Search Wikipedia and return the best matching article extract."""
    question = question.strip()
    if not question:
        return "Please type a question."

    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": question,
        "srlimit": 1,
    }
    response = requests.get(
        WIKIPEDIA_API, params=search_params, headers=HEADERS, timeout=20
    )
    response.raise_for_status()
    results = response.json().get("query", {}).get("search", [])
    if not results:
        return "I couldn't find a matching Wikipedia article."

    title = results[0]["title"]
    extract_params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "extracts",
        "explaintext": 1,
        "exchars": 3000,
        "titles": title,
    }
    response = requests.get(
        WIKIPEDIA_API, params=extract_params, headers=HEADERS, timeout=20
    )
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", [])
    if pages and pages[0].get("extract"):
        return f"Wikipedia result: {title}\n\n{pages[0]['extract']}"
    return f"I found '{title}', but Wikipedia did not return article text."


def speak_text(text: str):
    """Speak text with pyttsx3 without blocking the Flet interface."""
    if not text.strip():
        return

    def worker():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as exc:
            print("Voice error:", exc)

    threading.Thread(target=worker, daemon=True).start()


def main(page: Page):
    page.window.width = 360
    page.window.height = 640
    page.padding = 10
    page.bgcolor = "#100b36"
    page.appbar = CupertinoAppBar(
        leading=IconButton(icon=Icons.PERSON, icon_color="#100b36"),
        trailing=IconButton(icon=Icons.CAMERA_ALT, icon_color="#100b36"),
        title=Text("Welcome to FaciAi", color="#100b36"),
        automatic_background_visibility=False,
        bgcolor="white",
        brightness=Brightness.LIGHT,
    )

    chat_area = Column(scroll=ScrollMode.ALWAYS, expand=True)

    def add_user_message(message: str):
        chat_area.controls.append(
            Row(
                [
                    Icon(icon=Icons.PERSON, color="white"),
                    Text(value=message, color="white", selectable=True, expand=True),
                ],
                vertical_alignment=CrossAxisAlignment.START,
                rtl=True,
            )
        )

    def add_answer_message(message: str):
        answer_text = Text(value=message, color="white", selectable=True, expand=True)
        voice_button = IconButton(
            icon=Icons.VOLUME_UP,
            tooltip="Read answer aloud",
            icon_color="white",
            on_click=lambda e, spoken=message: speak_text(spoken),
        )
        chat_area.controls.append(
            Row(
                [
                    Icon(icon=Icons.SMART_TOY, color="white"),
                    Container(
                        content=Column(
                            [answer_text, Row([voice_button], alignment=MainAxisAlignment.END)],
                            spacing=4,
                        ),
                        border_radius=20,
                        padding=10,
                        bgcolor="#20f4f4f4",
                        expand=True,
                    ),
                ],
                vertical_alignment=CrossAxisAlignment.START,
            )
        )
        page.update()

    def chat(e):
        question = user_input.value.strip()
        if not question:
            return

        add_user_message(question)
        user_input.value = ""
        user_input.disabled = True
        page.update()

        try:
            answer = wikipedia_answer(question)
        except requests.exceptions.Timeout:
            answer = "Wikipedia took too long to respond. Please try again."
        except requests.exceptions.RequestException:
            answer = "Could not connect to Wikipedia. Check your internet connection."
        except (ValueError, KeyError, TypeError) as exc:
            answer = f"Couldn't read Wikipedia's response: {exc}"
        finally:
            user_input.disabled = False

        add_answer_message(answer)
        page.update()
        user_input.focus()

    user_input = TextField(
        hint_text="Ask anything...",
        hint_style=TextStyle(color="grey"),
        expand=True,
        border_radius=30,
        border_color="white",
        color="white",
        border_width=2,
        on_submit=chat,
    )
    send_button = IconButton(
        icon=Icons.SEND,
        on_click=chat,
        bgcolor="white",
        icon_color="black",
    )

    page.add(
        chat_area,
        Row(controls=[user_input, send_button], margin=Margin.only(bottom=25)),
    )


if __name__ == "__main__":
    run(main)
    
