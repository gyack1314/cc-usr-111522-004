from dataclasses import dataclass

@dataclass(frozen=True)
class Period:
    start:int
    end:int
    def __post_init__(self):
        if type(self.start) is not int or type(self.end) is not int or self.start>=self.end:raise ValueError('期间非法')
    def contains(self,t):return self.start<=t<self.end
    def intersection(self,other):
        a=max(self.start,other.start);b=min(self.end,other.end)
        return None if a>=b else Period(a,b)

def row_period(row):
    if type(row.get('multiplicity')) is not int or row['multiplicity']<=0:raise ValueError('袋重数须为正整数')
    return Period(row['start'],row['end'])
