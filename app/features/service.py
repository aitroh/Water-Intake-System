from app.features.repository import WaterRepository

class WaterService:
    def __init__(self):
        self.repo = WaterRepository()

    def add_water(self, amount: int):
        self.repo.add_log(amount)

    def get_today_total(self):
        return self.repo.get_total_today()

    def get_today_logs(self):
        return self.repo.get_today_logs()