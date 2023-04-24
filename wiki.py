#! /usr/bin/env python3

import argparse
import datetime
import pathlib
import subprocess

# todo: add put/delete of files into ./static/files directory, so that they can be referenced
# in html pages (e.g. css, images)


import fastapi
import fastapi.responses
import fastapi.staticfiles
import pydantic
import uvicorn
#import html_sanitizer


class SourceData(pydantic.BaseModel):
    data : str


SOURCES_DIR = "./sources"
PAGES_DIR = "./static"


app = fastapi.FastAPI()


@app.get("/api/sources")
async def get_sources():
    """get list of source page names"""
    source_path = pathlib.Path(SOURCES_DIR)

    sources = []
    sources.extend(source_path.glob("*.md"))
    sources.extend(source_path.glob("*.rst"))
    sources.extend(source_path.glob("*.txt"))
    sources.extend(source_path.glob("*.html"))

    return [source.name for source in sources]


@app.get("/api/sources/{name}")
async def get_source(name: str):
    """get source for a html page"""
    source_path = pathlib.Path(SOURCES_DIR) / name

    if not source_path.is_relative_to(pathlib.Path(SOURCES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    with open(source_path, "r", encoding="utf-8") as file:
        return file.read()


@app.delete("/api/sources/{name}")
async def delete_source(name: str):
    """delete source and html page"""
    html_path = pathlib.Path(PAGES_DIR).joinpath(name).with_suffix(".html")

    if not html_path.is_relative_to(pathlib.Path(PAGES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if html_path.name == "manage.html": # manage.html is special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    source_path = pathlib.Path(SOURCES_DIR).joinpath(name)

    if not source_path.is_relative_to(pathlib.Path(SOURCES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    html_path.unlink(missing_ok=True)
    source_path.unlink()


#@app.put("/api/sources/{name}", response_class=fastapi.responses.HTMLResponse)
@app.put("/api/sources/{name}")
async def put_source(name: str, source: SourceData) -> None:
    """put source for a html page"""
    source_path = pathlib.Path(SOURCES_DIR) / name

    if not source_path.is_relative_to(pathlib.Path(SOURCES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_path.name == "manage.md": # manage.html is a special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_path.suffix not in (".md", ".rst", ".txt", ".html"):
        raise fastapi.HTTPException(status_code=400, detail="file type not supported")

    try:
        source_path.rename(source_path.parent / pathlib.Path(source_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
    except FileNotFoundError:
        pass

    with open(source_path, "w", encoding="utf-8") as file:
        #sanitized_html = html_sanitizer.Sanitizer({"keep_typographic_whitespace": True}).sanitize(source.data)
        # todo: sanitizer removes whitespaces
        sanitized_html = source.data
        file.write(sanitized_html)

    if not _create_html_page(name, source_path):
        raise fastapi.HTTPException(status_code=400, detail="error in source")


def _create_html_page(name: str, path: pathlib.Path) -> bool:
    result = subprocess.run(["pandoc", "--standalone", "--to", "html5", path], capture_output=True, check=True, shell=False)

    if result.returncode != 0:
        return False

    html_data = result.stdout.decode("utf-8")

    html_path = pathlib.Path(PAGES_DIR).joinpath(name).with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_data)

    return True


# make fastapi serve static (html) files
app.mount("/", fastapi.staticfiles.StaticFiles(directory=PAGES_DIR, html=True), name="static")


if __name__ == "__main__":
    # create directories if not present
    pathlib.Path(SOURCES_DIR).mkdir(exist_ok=True)
    pathlib.Path(PAGES_DIR).mkdir(exist_ok=True)

    # parse command line arguments
    parser = argparse.ArgumentParser(description="pandoc based wiki")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="listening address")
    parser.add_argument("-p", "--port", type=int, default=8081, help="listening port")
    args = parser.parse_args()

    # start uvicorn webserver with reference to fastapi app
    config = uvicorn.Config("wiki:app", host=args.ip, port=args.port, log_level="info")
    server = uvicorn.Server(config)
    server.run()
