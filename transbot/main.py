import argparse
import time

from pydantic import BaseModel
from pynput import keyboard
import pyperclip
import openai


context = "Please translate the following text into Japanese" \
    " if it is in English, or into simple English if it is in Japanese." \
    "\n===\n{message}"


class ResponseFormat(BaseModel):
    translation_message: str


class KeyboardMonitor:

    def __init__(self, action_duration: float = 1.0):
        self.COMBINATION: set[keyboard.KeyCode] = {
            keyboard.Key.cmd, keyboard.KeyCode.from_char('c')}
        self.current_keys: set[keyboard.KeyCode] = set()
        self.last_command_c_time: float = 0.
        self.action_duration: float = action_duration
        self.client = openai.OpenAI()

    def on_press(self, key: keyboard.KeyCode):
        if key in self.COMBINATION:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.COMBINATION):
                current_time = time.time()
                duration = current_time - self.last_command_c_time
                if duration < self.action_duration:
                    self.process_clipboard()
                self.last_command_c_time = current_time

    def on_release(self, key: keyboard.KeyCode):
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass

    def process_clipboard(self):
        print("===== # Translating # =====")
        clipboard_content = str(pyperclip.paste())
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are an excellent translator."},
                {
                    "role": "user",
                    "content": context.format(message=clipboard_content)
                }],
            response_format=ResponseFormat)
        message = completion.choices[0].message
        if message.parsed:
            print(message.parsed.translation_message)
        else:
            print(message.refusal)
        print("")

    def start_monitoring(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action_duration", type=float, default=1.0,
        help="Duration of the action in seconds.")
    args = parser.parse_args()

    monitor = KeyboardMonitor(action_duration=args.action_duration)
    print("Running Translation Bot... Press Cmd + C twice to translate!")
    monitor.start_monitoring()


if __name__ == "__main__":
    main()
