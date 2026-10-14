from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transactions:
    amount:float
    type:str
    category:str
    payment_method:str
    date:str
    id:int | None=None

    def __post_init__(self):
        if self.id is not None:
            if type(self.id) is not int or self.id <=0:
                raise ValueError("Transaction ID must be positive integer.")
        
        if not isinstance(self.amount,(int,float)) or isinstance(self.amount,bool):
            raise ValueError("Amount must be number.")
        if self.amount<=0:
            raise ValueError("Amount must be greater than zero.")
        
        self.type=self.type.strip().lower()
        if self.type not in ("income","expense"):
            raise ValueError("Type must be income or expense.")

        for fields in ("category","payment_method","date"):
            value=getattr(self,fields)
            if not isinstance(value,str) or not value.strip():
                raise ValueError(
                    f"{fields} cannot be empty."
                )
            
            value=value.strip()

            if fields in ("category","payment_method"):
                if not any(char.isalpha() for char in value):
                    raise ValueError(f"{fields} must contain at least one letter.")

            setattr(self,fields,value.strip())

        try:
            parsed_date=datetime.strptime(self.date,"%Y-%m-%d")
            if parsed_date.strftime("%Y-%m-%d") != self.date:
                raise ValueError
        except ValueError:
            raise ValueError("Date must be a valid calendar date in YYYY-MM-DD format.")

        self.amount=float(self.amount)