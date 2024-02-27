import pathlib
import urllib.parse
import urllib.request
import datetime

import bs4

import plugin


print("hello from links.py plugin")


class Plugin(plugin.PluginBase):
    def pre_put_source_file(self, name: str, data: str) -> tuple[str, str]:
        """Called before source files are written or processed."""
        lines = data.split("\n")

        for count, line in enumerate(lines):
            url_string = line.strip()

            # check if line contains a url
            if line.startswith("http"):
                result = urllib.parse.urlparse(url_string)

                if all((result.scheme, result.netloc)):
                    timetag = datetime.datetime.now().isoformat('T', 'seconds')

                    try:
                        # open url
                        with urllib.request.urlopen(urllib.request.Request(url_string, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})) as url:
                            # parse html
                            soup = bs4.BeautifulSoup(url, features="html.parser")

                            title = soup.title.string.replace("\r", " ").replace("\n", " ").strip()

                            description_tag = soup.find("meta", property="og:description")
                            description = ", " + description_tag["content"].replace("\r", " ").replace("\n", " ").strip() if description_tag else ""

                            # substitute url by markdown link
                            lines[count] = f"[{title} <small>({timetag}, {result.netloc}{description})</small>]({url_string})"
                    except Exception as exc:
                        print(exc)
                        lines[count] = f"[{url_string} <small>({timetag}, {result.netloc})</small>]({url_string})"

        lines = "\n".join(lines)

        return name, lines
