from pdf2image import convert_from_bytes


class Preprocessor:
    def __init__(self, file_obj) -> None:
        self.file_name = file_obj.filename.split('.')[0]
        pages = convert_from_bytes(file_obj.read(), 500, poppler_path="./helper/poppler/bin")
        self.file_extension = "jpg"
        self.file_path = (
            f"./helper/assets/converted/{self.file_name}.{self.file_extension}"
        )
        pages[0].save(self.file_path, "JPEG")

    def get_file_info(self) -> dict:
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_extension": self.file_extension,
        }
