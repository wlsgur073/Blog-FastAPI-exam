def truncate_text(text, limit=150) -> str:
    if text is not None: # DB에서 not null로 설정했기 때문에 None은 없으나, 혹시 모르니 체크
        if len(text) > limit:
            return text[:limit] + "..."
        return text
    return ""
   
def newline_to_br(newline: str) -> str:
    return newline.replace("\n", "<br>") # DB의 개행문자를 HTML에 맞게 번역해야 함.

def none_to_null(text, is_sqote=False): # DB에 None을 넣으면 'None'으로 들어가는 문제를 해결하기 위함
    if text is None:
        return "NULL"
    else:
        if is_sqote:
            return f"'{text}'"
    return text