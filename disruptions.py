from src.archive import ArchiveScraper
from src.upload import upload_resource

CSV_FILE = 'disruptions.csv'

def main():
    scraper = ArchiveScraper()
    scraper.scrape(CSV_FILE)
    upload_resource(CSV_FILE)

if __name__ == '__main__':
    main()
