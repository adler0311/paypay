def is_chosung_only(s):
    chosungs = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    for char in s:
        if char not in chosungs:
            return False
    return True


def get_chosung(word):
    chosungs = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    result = ""

    for char in word:
        if "가" <= char <= "힣":
            chosung_index = (ord(char) - ord("가")) // 588
            result += chosungs[chosung_index]
        else:
            result += char
    return result
