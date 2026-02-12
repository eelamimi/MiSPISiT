class Result:
    def __init__(self, r: tuple):
        self.full_section: str = r[0]
        self.pol_c: int = r[1]
        self.chl_c: int = r[2]
        self.umn_c: int = r[3]
        self.pol: float = r[4]
        self.chl: float = r[5]
        self.umn: float = r[6]

    def __str__(self):
        return f"Result(section='{self.full_section}', pol_c={self.pol_c}, chl_c={self.chl_c}, umn_c={self.umn_c}, pol={self.pol:.2f}, chl={self.chl:.2f}, umn={self.umn:.2f})"

    def __repr__(self):
        return self.__str__()
