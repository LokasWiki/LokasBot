web_type = "web".strip().lower()
press_release_type = "press_release".strip().lower()
newsgroup_type = "newsgroup".strip().lower()
news_type = "news".strip().lower()
map_type = "map".strip().lower()

list_of_template = [
    # webcite
    ["مرجع موقع", web_type],
    ["استشهاد ويب/إنجليزي", web_type],
    ["Cite web", web_type],
    ["Citeweb", web_type],
    ["مرجع وب", web_type],
    ["مرجع وب/إنجليزي", web_type],
    ["Cita web", web_type],
    ["يستشهد ويب", web_type],
    ["استشهاد بموقع", web_type],
    ["Web cite", web_type],
    ["مرجع ويب", web_type],
    ["مرجع ويب/إنجليزي", web_type],
    ["Cw", web_type],
    ["استشهاد ويب", web_type],
    # Cite press release
    ["استشهاد ببيان صحفي", press_release_type],
    ["Cite press", press_release_type],
    ["Cite pressrelease", press_release_type],
    ["Cite press release", press_release_type],
    # Cite newsgroup
    ["استشهاد بمجموعة أخبار", newsgroup_type],
    ["Cite newsgroup", newsgroup_type],
    # Cite news
    ["استشهاد بخبر", news_type],
    ["Cite news", news_type],
    ["Cite newspaper", news_type],
    ["يستشهد خبر", news_type],
    ["Cite News", news_type],
    ["Tidningsref", news_type],
    ["Cita noticia", news_type],
    # cite map
    ["استشهاد بخريطة", web_type],
    ["Cite map", web_type],


]
