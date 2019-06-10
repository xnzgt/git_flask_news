
def news_hot_filter(index):
    num = ["first","second","third"]
    try:
        return num[index]
    except IndexError:
        return
