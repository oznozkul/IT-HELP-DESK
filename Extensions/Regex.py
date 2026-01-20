import re

def RegexIntent(intent):
    hata_pattern = r"(sorun|hata|çalışmıyor|ulaşılamıyor|problem)"
    istek_pattern = r"(talep|istek|ekleme|kurulum)"
    category = ""
    if re.search(hata_pattern, intent.lower()):
        category = "Hata"
    elif re.search(istek_pattern, intent.lower()):
        category = "İstek"
    else:
        category = "Bilinmiyor"

    return {"orjinal_text": intent,"category":category}


