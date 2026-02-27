from abc import ABC

from tasks.infobox_football_biography.src.data_extraction.data_extractor import DataExtractor
from tasks.infobox_football_biography.src.logger.abstract_logger import AbstractLogger


class InfoboxFootballBiography(DataExtractor, ABC):
    def __init__(self, text_page: str, logger: AbstractLogger):
        super().__init__(text_page=text_page, logger=logger)

    def template_name(self) -> str:
        return "Infobox football biography"

    def parameters_list(self) -> list:
        return [
            "position",
            "years1", "clubs1", "caps1", "goals1",
            "years2", "clubs2", "caps2", "goals2",
            "years3", "clubs3", "caps3", "goals3",
            "years4", "clubs4", "caps4", "goals4",
            "years5", "clubs5", "caps5", "goals5",
            "years6", "clubs6", "caps6", "goals6",
            "years7", "clubs7", "caps7", "goals7",
            "years8", "clubs8", "caps8", "goals8",
            "years9", "clubs9", "caps9", "goals9",
            "years10", "clubs10", "caps10", "goals10",
            "years11", "clubs11", "caps11", "goals11",
            "years12", "clubs12", "caps12", "goals12",
            "years13", "clubs13", "caps13", "goals13",
            "years14", "clubs14", "caps14", "goals14",
            "years15", "clubs15", "caps15", "goals15",
            "years16", "clubs16", "caps16", "goals16",
            "years17", "clubs17", "caps17", "goals17",
            "years18", "clubs18", "caps18", "goals18",
            "years19", "clubs19", "caps19", "goals19",
        ]
