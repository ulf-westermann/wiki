import pathlib
import urllib.parse
import urllib.request
import datetime

import bs4

import plugin


print("hello from links plugin")


class Plugin(plugin.PluginBase):
    def pre_put_source_file(self, name: str, data: str) -> tuple[str, str]:
        """Called before source files are written or processed."""
        lines = data.split("\n")

        for count, line in enumerate(lines):
            url_string = line.strip()

            # check if line contains a url
            result = urllib.parse.urlparse(url_string)

            if all((result.scheme, result.netloc)):
                timetag = datetime.datetime.now().isoformat('T', 'seconds')

                try:
                    # open url
                    with urllib.request.urlopen(urllib.request.Request(url_string, headers={"User-Agent": "Mozilla/5.0"})) as url:
                        # parse html
                        soup = bs4.BeautifulSoup(url, features="html.parser")

                        title = soup.title.string
                        description_tag = soup.find("meta", property="og:description")
                        description = ", " + description_tag["content"] if description_tag else ""

                        # substitute url by markdown link
                        lines[count] = f"[{title} <small>({timetag}, {result.netloc}{description})</small>]({url_string})"
                except Exception as exc:
                    print(exc)

        lines = "\n".join(lines)

        return name, lines
