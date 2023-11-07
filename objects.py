from dataclasses import dataclass

@dataclass
class CarForRent:
    sipp: str = ""
    name: str = ""
    depo: float = 0
    rate1: float = 0
    rate3: float = 0
    rate7: float = 0
    rate14: float = 0
    rate21: float = 0
    rate30: float = 0

    def setRate(self, days: int, rate: float):
        if days == 1:
            self.rate1 = rate
            return
        if days == 3:
            self.rate3 = rate
            return
        if days == 7:
            self.rate7 = rate
            return
        if days == 14:
            self.rate14 = rate
            return
        if days == 21:
            self.rate21 = rate
            return
        if days == 30:
            self.rate30 = rate
            return

class CFR(CarForRent):
    carType: str = ""
    millage: int = 0
    url: str = ""
    MY: str = ""
    driving_experience: str = ""
    min_age: str = ""
    gear_box: str = ""
    engine: str = ""
    company: str = ""
    different_millages: bool = False