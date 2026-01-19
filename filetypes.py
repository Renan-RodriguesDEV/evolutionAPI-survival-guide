from dataclasses import dataclass


@dataclass
class Type:
    mediatype: str
    mimetype: str


class FileTypes:
    """Classe de tipos de arquivos e seus MIMETypes"""

    PDF = Type("document", "application/pdf")
    XLSX = Type(
        "document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    PNG = Type("image", "image/png")
    JPEG_AND_JPG = Type("image", "image/jpeg")
