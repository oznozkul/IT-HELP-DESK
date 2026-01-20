import json


def LoadJson(text):
    if not text.strip().endswith(']'):
        last_complete_item = text.rfind('},')
        if last_complete_item != -1:
            text = text[:last_complete_item + 1] + ']'
        else:
            last_bracket = text.rfind('}')
            text = text[:last_bracket + 1] + ']'

    try:
        return json.loads(text)
    except Exception as e:
        print(f"Otomatik tamir başarısız: {e}")
        return None