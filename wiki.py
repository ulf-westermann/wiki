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


# todo: use global pathlib objects
SOURCES_DIR = "./sources"
PAGES_DIR = "./static"
FILES_SUBDIR = "files"

SOURCE_PATH = pathlib.Path(SOURCES_DIR)
WWW_PATH = pathlib.Path(PAGES_DIR)
WWW_FILES_PATH = WWW_PATH / "files"


app = fastapi.FastAPI()


@app.get("/api/sources")
async def get_sources():
    """get list of source page names"""
    sources = []

    sources.extend(SOURCE_PATH.glob("*.md"))
    sources.extend(SOURCE_PATH.glob("*.rst"))
    sources.extend(SOURCE_PATH.glob("*.txt"))
    sources.extend(SOURCE_PATH.glob("*.html"))

    return [source.name for source in sources]


@app.get("/api/sources/{name}")
async def get_source(name: str):
    """get source for a html page"""
    source_file_path = SOURCE_PATH / name

    if not source_file_path.is_relative_to(SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    with open(source_file_path, "r", encoding="utf-8") as file:
        return file.read()


@app.delete("/api/sources/{name}")
async def delete_source(name: str):
    """delete source and html page"""
    # check if html file is valid
    html_file_path = WWW_PATH.joinpath(name).with_suffix(".html")

    if not html_file_path.is_relative_to(WWW_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if html_file_path.name == "manage.html": # manage.html is special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # check if source file is valid
    source_file_path = SOURCE_PATH.joinpath(name)

    if not source_file_path.is_relative_to(SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # delete files
    html_file_path.unlink(missing_ok=True)
    source_file_path.unlink()


#@app.put("/api/sources/{name}", response_class=fastapi.responses.HTMLResponse)
@app.put("/api/sources/{name}")
async def put_source(name: str, source: SourceData) -> None:
    """put source for a html page"""
    # check if source file is valid
    source_file_path = SOURCE_PATH / name

    if not source_file_path.is_relative_to(SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_file_path.name == "manage.md": # manage.html is a special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_file_path.suffix not in (".md", ".rst", ".txt", ".html"):
        raise fastapi.HTTPException(status_code=400, detail="file type not supported")

    # backup old source files with same name, if present
    try:
        source_file_path.rename(source_file_path.parent / pathlib.Path(source_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
    except FileNotFoundError:
        pass

    # sanitize input and write source file
    with open(source_file_path, "w", encoding="utf-8") as file:
        # todo: sanitizer removes whitespaces
        #sanitized_html = html_sanitizer.Sanitizer({"keep_typographic_whitespace": True}).sanitize(source.data)
        sanitized_html = source.data
        file.write(sanitized_html)

    # create html file
    if not _create_html_page(name, source_file_path):
        raise fastapi.HTTPException(status_code=400, detail="error in source")


@app.put("/api/files")
async def upload_files(files: list[fastapi.UploadFile]):
    """upload multiple files to special folder that is served by www server"""
    for remote_file in files:
        local_file_path = WWW_FILES_PATH / remote_file.filename

        # todo: check local file path  

        # todo: handle already existing files

        with open(local_file_path, "wb") as local_file:
            remote_content = await remote_file.read()
            local_file.write(remote_content)


def _create_html_page(name: str, path: pathlib.Path) -> bool:
    result = subprocess.run(["pandoc", "--standalone", "--to", "html5", path], capture_output=True, check=True, shell=False)

    if result.returncode != 0:
        return False

    html_file_path = result.stdout.decode("utf-8")

    html_path = WWW_PATH.joinpath(name).with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_file_path)

    return True


# make fastapi serve static (html) files
app.mount("/", fastapi.staticfiles.StaticFiles(directory=PAGES_DIR, html=True), name="static")


if __name__ == "__main__":
    # create directories if not present
    SOURCE_PATH.mkdir(exist_ok=True)
    WWW_PATH.mkdir(exist_ok=True)
    WWW_FILES_PATH.mkdir(exist_ok=True)

    # parse command line arguments
    parser = argparse.ArgumentParser(description="pandoc based wiki")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="listening address")
    parser.add_argument("-p", "--port", type=int, default=8081, help="listening port")
    args = parser.parse_args()

    # start uvicorn webserver with reference to fastapi app
    config = uvicorn.Config("wiki:app", host=args.ip, port=args.port, log_level="info")
    server = uvicorn.Server(config)
    server.run()
