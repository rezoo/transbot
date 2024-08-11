import argparse
import time

from pynput import keyboard
import pyperclip
import openai


context = """次の与えられた文章が英語であれば日本語に、日本語であれば簡単な英語に翻訳してください。ただし、「The translated and simplified version of your text in English is〜」などの言葉や、"The output is..."などの二重引用符で囲むなどの修飾は出力しないでください。単純に訳文のみ出力してください。
===
{message}"""


class KeyboardMonitor:

    def __init__(self, action_duration: float = 1.0):
        self.COMBINATION: set[keyboard.KeyCode] = {
            keyboard.Key.cmd, keyboard.KeyCode.from_char('c')}
        self.current_keys: set[keyboard.KeyCode] = set()
        self.last_command_c_time: float = 0.
        self.action_duration: float = action_duration

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
        res = openai.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "user", "content": context.format(
                message=clipboard_content)}],
        )
        print(res.choices[0].message.content)
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
