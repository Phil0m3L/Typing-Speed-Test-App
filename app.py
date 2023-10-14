import time
from tkinter import messagebox

import customtkinter as ctk
from wonderwords import RandomWord


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speed Typing Test")  # Set window title
        self.word_generator = RandomWord()  # Initialize the word generator

        self.entry_word = None
        self.current_word = ""
        self.words_typed = 0
        self.correct_words_typed = 0
        self.start_time = None
        self.remaining_time = 60  # The test lasts for 60 seconds
        self.wpm = 0
        self.accuracy = 0.0

        self.lbl_title = None
        self.lbl_instruction = None
        self.lbl_word = None
        self.lbl_metrics = None
        self.btn_start = None

        self.initialize_widgets()

    def initialize_widgets(self):
        """
        Function to initialize the various widgets of the application.
        :return:
        """

        # Set application header
        self.lbl_title = ctk.CTkLabel(
            master=self,
            text="Typing Speed Test",
            font=ctk.CTkFont(family="Algerian", size=28, weight="bold", underline=True),
        )
        self.lbl_title.pack(pady=20)

        # Set application description / usage instructions
        self.lbl_instruction = ctk.CTkLabel(
            master=self,
            text="Welcome to the typing speed test application!\n"
            "This is my first golden project for the CodeClause internship.\n"
            "The test lasts for a total of 60 seconds.\n"
            'Type the words as shown on the screen and press the spacebar to proceed to the next word.\n'
            "The metrics will be shown in real-time as well as at the end of the test.\n"
            "You can exit the test at any time.",
            font=ctk.CTkFont(family="Helvetica", size=14, slant="italic"),
        )
        self.lbl_instruction.pack(pady=10)

        # Placeholder for the word to be typed
        self.lbl_word = ctk.CTkLabel(
            master=self,
            text="",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
        )
        self.lbl_word.pack(pady=10)

        # Placeholder for the metrics (wpm, accuracy, remaining time) display
        self.lbl_metrics = ctk.CTkLabel(
            master=self,
            text="",
            font=ctk.CTkFont(family="Helvetica", size=16, slant="italic"),
        )
        self.lbl_metrics.pack(pady=10)

        # Start button
        self.btn_start = ctk.CTkButton(
            master=self, text="Start Test", command=self.start_test
        )
        self.btn_start.pack(pady=20)

        # Set fixed window size
        self.geometry("600x400")

        # Set the callback for the window exit event
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def start_test(self):
        """
        Function to start the typing test.
        :return:
        """

        self.btn_start.configure(state=ctk.DISABLED)  # Disable the "Start Test" button
        self.btn_start.pack_forget()  # Hide the "Start Test" button
        self.words_typed = 0
        self.correct_words_typed = 0
        self.start_time = time.time()
        self.update_word()  # Display the first word
        self.update_metrics()  # Display the initial metrics

        # Input box
        self.entry_word = ctk.CTkEntry(
            master=self, font=ctk.CTkFont(family="Helvetica", size=20)
        )
        self.entry_word.pack(pady=10)

        # Perform post-input tasks when the user presses the "Space" key
        self.entry_word.bind("<space>", self.check_word)
        self.entry_word.focus()  # Focus the cursor on the input box

    # noinspection PyUnusedLocal
    def update_word(self):
        """
        Function to generate and update the word to be typed in.
        :return:
        """

        self.current_word = self.word_generator.word(word_max_length=8)
        self.lbl_word.configure(text=self.current_word)

    # noinspection PyUnusedLocal
    def check_word(self, event):
        """
        Function to validate the input by the user against the word to be typed in.
        :param event: placeholder variable
        :return:
        """

        user_input = self.entry_word.get().strip()

        if user_input == self.current_word:
            self.entry_word.configure(
                fg_color="green"
            )  # Flash the input box green for correct input
            self.correct_words_typed += (
                1  # Increment the number of correct words (accuracy calculation)
            )

        else:
            self.entry_word.configure(
                fg_color="red"
            )  # Flash the input box red for incorrect input

        self.words_typed += 1  # Increment the number of words typed (wpm calculation)

        self.remaining_time += 0.2  # Compensate for the input box flash
        self.after(
            200, self.clear_input_and_update_word
        )  # Clear the input box and update word after 200 ms

    def update_metrics(self):
        """
        Function to update the metrics (wpm, accuracy and remaining time).
        :return:
        """

        elapsed_time = int(time.time() - self.start_time)  # Calculate elapsed time
        self.remaining_time = max(60 - elapsed_time, 0)  # Calculate remaining time

        # Calculate words per minute (wpm)
        self.wpm = (
            int(self.correct_words_typed / (elapsed_time / 60))
            if elapsed_time > 0
            else 0
        )

        # Calculate accuracy
        self.accuracy = (
            (self.correct_words_typed / self.words_typed) * 100
            if self.words_typed > 0
            else 0
        )

        # Update the metrics display
        self.lbl_metrics.configure(
            text=f"WPM: {self.wpm} | Accuracy: {round(self.accuracy)}% | Remaining Time: {self.remaining_time} seconds"
        )

        # Update the metrics each second until the remaining time for the test is 0
        if self.remaining_time > 0:
            self.after(1000, self.update_metrics)

        else:
            self.show_metrics_popup()  # Display the final metrics as popup
            self.btn_start.pack()  # Show the "Start Test" button again
            self.btn_start.configure(state=ctk.NORMAL)  # Enable the "Start Test" button
            self.lbl_word.configure(text="")  # Reset the word to be typed in
            # Replace the metrics display with a test completion message
            self.lbl_metrics.configure(text="Test Complete!")
            # Hide the input box
            self.entry_word.pack_forget()

    def clear_input_and_update_word(self):
        """
        Function to clear the input box, and update the word to be typed in.
        :return:
        """

        self.entry_word.configure(fg_color="black")  # Reset box color to black
        self.entry_word.delete(0, ctk.END)
        self.update_word()

    def show_metrics_popup(self):
        """
        Function to show a popup message with the metrics.
        :return:
        """

        popup_text = f"Typing Speed: {self.wpm} WPM\nAccuracy: {round(self.accuracy)}%"

        # If the exit was made mid-test, show the remaining time
        if self.remaining_time > 0:
            popup_text += f"\nRemaining Time: {self.remaining_time} seconds"

        messagebox.showinfo("Test Completed!", popup_text)

    def on_exit(self):
        """
        Function to perform pre-exit steps.
        :return:
        """

        if self.btn_start.winfo_ismapped():  # If the "Start Test" button is visible
            # Prompt the user for exit confirmation
            if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
                self.destroy()

        else:
            self.show_metrics_popup()  # If the test was ongoing, show the final metrics.
            self.destroy()


def main():
    # Set default theme and color scheme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    # Run the application
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
