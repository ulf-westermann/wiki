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
            # check if line contains a url
            result = urllib.parse.urlparse(line)

            if all((result.scheme, result.netloc)):
                with urllib.request.urlopen(line) as url:
                    soup = bs4.BeautifulSoup(url)
                    lines[count] = f"[{soup.title.string}]({line}) <small>{datetime.datetime.utcnow().isoformat('T', 'seconds')}</small><br>"

        lines = "\n".join(lines)

        return name, lines


    def post_put_source_file(self, source_file_path: pathlib.Path, www_file_path: pathlib.Path) -> None:
        """Called after source files have been written and processed."""
        print(f"plugin1. source_file_path: {source_file_path}, www_file_path: {www_file_path}")
