import random
import os
import json

class XiaoziGame:
    def __init__(self):
        self.pool = {
            "普通": ["丰田", "本田", "福特", "雪佛兰", "日产", "现代", "起亚", "大众", "斯巴鲁", "马自达", "三菱", "别克", "克莱斯勒", "道奇", "吉普", "GMC", "Ram", "菲亚特", "迷你", "标致"],
            "稀有": ["宝马", "奔驰", "奥迪", "雷克萨斯", "沃尔沃", "捷豹", "路虎", "保时捷", "特斯拉", "英菲尼迪"],
            "史诗": ["法拉利", "兰博基尼", "阿斯顿·马丁", "宾利", "劳斯莱斯"],
            "传奇": ["布加迪", "帕加尼", "科尼赛克", "迈凯伦", "Rimac"]
        }
        self.probabilities = [0.7, 0.2, 0.08, 0.02]
        self.total_draws = 0
        self.legendary_count = 0
        self.rarity_counts = {rarity: 0 for rarity in self.pool}
        self.brand_counts = {brand: 0 for brands in self.pool.values() for brand in brands}
        self.stats_file = os.path.join(os.path.expanduser("~"), "xiaozi_stats.json")
        self.load_stats()

    def draw(self):
        self.total_draws += 1
        rarity = random.choices(list(self.pool.keys()), self.probabilities)[0]
        result = random.choice(self.pool[rarity])
        if rarity == "传奇":
            self.legendary_count += 1
        self.rarity_counts[rarity] += 1
        self.brand_counts[result] += 1
        self.save_stats()
        return result

    def ten_draws(self):
        results = []
        for _ in range(10):
            results.append(self.draw())
        return results

    def display_stats(self):
        average_draws = self.total_draws / self.legendary_count if self.legendary_count > 0 else 0
        legendary_probability = self.legendary_count / self.total_draws if self.total_draws > 0 else 0
        return {
            "total_draws": self.total_draws,
            "average_draws_for_legendary": average_draws,
            "legendary_probability": legendary_probability,
            "legendary_count": self.legendary_count,
            "rarity_counts": self.rarity_counts,
            "brand_counts": self.brand_counts
        }

    def reset_stats(self):
        self.total_draws = 0
        self.legendary_count = 0
        self.rarity_counts = {rarity: 0 for rarity in self.pool}
        self.brand_counts = {brand: 0 for brands in self.pool.values() for brand in brands}
        self.save_stats()

    def save_stats(self):
        stats = {
            "total_draws": self.total_draws,
            "legendary_count": self.legendary_count,
            "rarity_counts": self.rarity_counts,
            "brand_counts": self.brand_counts
        }
        with open(self.stats_file, "w") as f:
            json.dump(stats, f)

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, "r") as f:
                stats = json.load(f)
                self.total_draws = stats.get("total_draws", 0)
                self.legendary_count = stats.get("legendary_count", 0)
                self.rarity_counts = stats.get("rarity_counts", {rarity: 0 for rarity in self.pool})
                self.brand_counts = stats.get("brand_counts", {brand: 0 for brands in self.pool.values() for brand in brands})
