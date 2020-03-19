from bs4 import BeautifulSoup, element, NavigableString
import requests
import csv
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('-export', nargs='?', help="If you want the program to export the data to CSV")
args = argparser.parse_args()

def request_site(url):
    # Spoof a typical browser header. HTTP Headers are case-insensitive.
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "referer": "www.google.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "cache-control": "no-cache",
        "upgrade-insecure-requests": "1",
        "DNT": "1",
    }
    if "://" in url:
        url = url.split("://", 1)[1]
    if "www." in url:
        url = url.split("www.", 1)[1]

    url = "https://" + url

    response = requests.get(url, headers=headers)

    if response.status_code not in [200, 202, 301, 302]:
        print(f"Failed request; status code is: {response.status_code}")
        return None

    parsed = BeautifulSoup(response.content, "html.parser")
    return parsed


if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Outline_of_science"

    parsed = request_site(url)

    containing_div = parsed.find("div", {"id": "toc"})

    all_toctext_spans = containing_div.find_all("span", {"class": "toctext"})

    output_lod = []
    for n, toctext_span in enumerate(all_toctext_spans):
        print(toctext_span.get_text())
        output_lod.append({
            "Section": toctext_span.get_text(),
            "Input_URL": url
        })

    if args.export:
        with open('output.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, output_lod[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(output_lod)
            print("Finished writing data to output.csv")
