import csv
import os

from datetime import datetime, timezone


class TrendsCsvPipeline(object):
    """
    Archive trends data to CSV files
    Classified by date and language
    """

    def __init__(self):
        self.trends = {
            'daily': {},
            'weekly': {},
            'monthly': {}
        }

    def process_item(self, item, spider):
        # Add to buffer
        since = item['since']
        lang = item['lang']
        if lang not in self.trends[since]:
            self.trends[since][lang] = []
        self.trends[since][lang].append(item)
        return item

    def close_spider(self, spider):
        """
        Before spider closed, we write data to CSV files
        """
        for date_range in self.trends:
            for lang in self.trends[date_range]:
                filename = "{}.csv".format(lang)
                path = self.build_path(date_range)
                self.write_csv(os.path.join(path, filename), self.trends[date_range][lang])
                

    @staticmethod
    def build_path(date_range):
        # Make dirs
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        if date_range == "weekly":
            path = utc_now.strftime("%Y/%W")
        elif date_range == "monthly":
            path = utc_now.strftime("%Y/%m")
        else:
            path = utc_now.strftime("%Y/%m/%d")
        path = os.path.join("archive", date_range, path)
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def write_csv(path, items):
        with open(path, "w", newline='', encoding='utf-8') as fp:
            writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id",  "name", "full_name", "language", "new stars", "description", "forks_count", "stargazers_count","avatar_url"])
            # "full_name", "description", "forks_count", "stargazers_count","owner"
            for item in items:
                print("----------------------------------")
                print(item )
                primary_lang = item['primaryLanguage']['name'] if item['primaryLanguage'] else ""
                arr = [
                    item["databaseId"], 
                    item["name"], 
                    item["nameWithOwner"],
                    primary_lang, 
                    item["stars_inc"], 
                    item["description"],
                    item["forkCount"],
                    item["stargazers"]["totalCount"],
                    item["owner"]["avatarUrl"]
                  ]
                print(arr )
                # writer.writerow([item["databaseId"], item["nameWithOwner"], primary_lang, item["stars_inc"]])
                writer.writerow(arr)
