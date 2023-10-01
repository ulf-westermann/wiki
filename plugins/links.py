import pathlib
import urllib.parse
import urllib.request
import datetime

import bs4

import plugin


print("hello from plugin1")


class Plugin(plugin.PluginBase):
    def pre_put_source_file(self, name: str, data: str) -> tuple[str, str]:
        """Called before source files are written or processed."""
        lines = data.split("\n")

        for count, line in enumerate(lines):
            url_string = line.strip()

            # check if line contains a url
            result = urllib.parse.urlparse(url_string)

            if all((result.scheme, result.netloc)):
                try:
                    with urllib.request.urlopen(urllib.request.Request(url_string, headers={"User-Agent": "Mozilla/5.0"})) as url:
                        soup = bs4.BeautifulSoup(url, features="html.parser")
                        lines[count] = f"[{soup.title.string}]({url_string}) <small>{datetime.datetime.utcnow().isoformat('T', 'seconds')}</small><br>"
                except Exception as exc:
                    print(exc)
                    lines[count] = f"[{url_string}]({url_string}) <small>{datetime.datetime.utcnow().isoformat('T', 'seconds')}</small><br>"

        lines = "\n".join(lines)

        return name, lines


    def post_put_source_file(self, source_file_path: pathlib.Path, www_file_path: pathlib.Path) -> None:
        """Called after source files have been written and processed."""
        print(f"plugin1. source_file_path: {source_file_path}, www_file_path: {www_file_path}")
