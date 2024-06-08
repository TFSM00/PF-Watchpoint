class Asset:
    def __init__(self, name, description, currency, institution) -> None:
        self.name = name
        self.description = description
        self.currency = currency
        self.institution = institution

class Deposit(Asset):
    def __init__(self, name, description, nominal, currency, institution, interest_rate) -> None:
        super().__init__(name, description, currency, institution)
        self.nominal = nominal
        self.interest_rate = interest_rate
        self.is_checking_account = (interest_rate == 0)

class ETF(Asset):
    def __init__(self, name, description, currency, institution, ticker) -> None:
        super().__init__(name, description, currency, institution)
        self.ticker = ticker

class Pension(Asset):
    def __init__(self, name, description, currency, institution, monthly_contribution, contributors) -> None:
        super().__init__(name, description, currency, institution)
        self.monthly_contribution = monthly_contribution
        self.contributors = contributors
        
        