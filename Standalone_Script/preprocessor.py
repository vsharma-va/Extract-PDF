import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path


class Preprocessor:
    def __init__(self) -> None:
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(
            filetypes=(("pdf", "*.pdf"), ("photos", ["*.jpg", "*.png"]))
        )
        self.file_name = self.file_path.split("/")[-1].split(".")[0]
        self.file_extension = self.file_path.split("/")[-1].split(".")[-1]

        if self.file_extension == "pdf":
            pages = convert_from_path(self.file_path, 500, poppler_path="./poppler/bin")
            self.file_extension = "jpg"
            self.file_path = (
                f"./assets/converted/{self.file_name}.{self.file_extension}"
            )
            pages[0].save(self.file_path, "JPEG")

    def get_file_info(self) -> dict:
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_extension": self.file_extension,
        }
