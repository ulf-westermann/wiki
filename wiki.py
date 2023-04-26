#! /usr/bin/env python3

import argparse
import datetime
import pathlib
import subprocess


import fastapi
import fastapi.responses
import fastapi.staticfiles
import pydantic
import uvicorn
#import html_sanitizer


class SourceData(pydantic.BaseModel):
    data : str



MARKUP_PATH = pathlib.Path("./markup")
WWW_PATH = pathlib.Path("./www")
WWW_MEDIA_PATH = WWW_PATH / "media"


app = fastapi.FastAPI()


@app.get("/api/markup")
async def get_markup_files():
    """get list of markup file names"""
    sources = []

    sources.extend(MARKUP_PATH.glob("*.md"))
    sources.extend(MARKUP_PATH.glob("*.rst"))
    sources.extend(MARKUP_PATH.glob("*.txt"))
    sources.extend(MARKUP_PATH.glob("*.html"))
    sources.extend(MARKUP_PATH.glob("*.css"))

    return [source.name for source in sources]


@app.get("/api/markup/{name}")
async def get_markup(name: str):
    """get markup source for a html page"""
    markup_file_path = MARKUP_PATH / name

    if not markup_file_path.is_relative_to(MARKUP_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    with open(markup_file_path, "r", encoding="utf-8") as file:
        return file.read()


@app.delete("/api/markup/{name}")
async def delete_markup_file(name: str):
    """delete markup file and corresponding html page"""
    # check if html file is valid
    html_file_path = WWW_PATH.joinpath(name).with_suffix(".html")

    if not html_file_path.is_relative_to(WWW_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if html_file_path.name == "manage.html": # manage.html is special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # check if markup file is valid
    markup_file_path = MARKUP_PATH.joinpath(name)

    if not markup_file_path.is_relative_to(MARKUP_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # delet files
    html_file_path.unlink(missing_ok=True)
    markup_file_path.unlink()


#@app.put("/api/markup/{name}", response_class=fastapi.responses.HTMLResponse)
@app.put("/api/markup/{name}")
async def put_markup_file(name: str, source: SourceData) -> None:
    """put markup file and create corresponding html page"""
    # check if markup file path is valid
    markup_file_path = MARKUP_PATH / name

    if not markup_file_path.is_relative_to(MARKUP_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if markup_file_path.name == "manage.md": # manage.html is a special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if markup_file_path.suffix not in (".md", ".rst", ".txt", ".html", ".css"):
        raise fastapi.HTTPException(status_code=400, detail="file type not supported")

    # backup old markup file with same name, if present
    try:
        markup_file_path.rename(markup_file_path.parent / pathlib.Path(markup_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
    except FileNotFoundError:
        pass

    # sanitize input and write markup file
    with open(markup_file_path, "w", encoding="utf-8") as file:
        # todo: sanitizer removes whitespaces
        #sanitized_html = html_sanitizer.Sanitizer({"keep_typographic_whitespace": True}).sanitize(source.data)
        #sanitized_html = source.data
        file.write(source.data)

    # create html file
    if markup_file_path.suffix != ".css":
        css_files = [css_file.name for css_file in MARKUP_PATH.glob("*.css")]

        if not _create_html_page(name, markup_file_path, css_files):
            raise fastapi.HTTPException(status_code=400, detail="error in source")


@app.get("/api/media")
async def get_media_files():
    """get list of media files"""
    files = WWW_MEDIA_PATH.glob("*")

    return [file.name for file in files]


@app.put("/api/media")
async def upload_media_files(files: list[fastapi.UploadFile]):
    """upload multiple media files"""
    for remote_file in files:
        local_file_path = WWW_MEDIA_PATH / remote_file.filename

        # check if media file path is valid
        if not local_file_path.is_relative_to(WWW_MEDIA_PATH):
            raise fastapi.HTTPException(status_code=403, detail="not allowed")

        # backup old media file with same name, if present
        try:
            local_file_path.rename(local_file_path.parent / pathlib.Path(local_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
        except FileNotFoundError:
            pass

        with open(local_file_path, "wb") as local_file:
            remote_content = await remote_file.read()
            local_file.write(remote_content)


@app.delete("/api/media/{name}")
async def delete_media_file(name: str):
    """delete media file"""
    # check if media file is valid
    file_path = WWW_MEDIA_PATH.joinpath(name)

    if not file_path.is_relative_to(WWW_MEDIA_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # delete media file
    file_path.unlink()


def _create_html_page(name: str, path: pathlib.Path, css_files: list) -> bool:
    run_params = ["pandoc", "--standalone", "--to", "html5"]

    for css_file in css_files:
        run_params.extend(["--css", css_file])

    run_params.append(path)

    result = subprocess.run(run_params, capture_output=True, check=True, shell=False)

    if result.returncode != 0:
        return False

    html_file_path = result.stdout.decode("utf-8")

    html_path = WWW_PATH.joinpath(name).with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_file_path)

    return True


# create directories if not present
MARKUP_PATH.mkdir(exist_ok=True)
WWW_PATH.mkdir(exist_ok=True)
WWW_MEDIA_PATH.mkdir(exist_ok=True)

# make fastapi serve static (html) files
app.mount("/", fastapi.staticfiles.StaticFiles(directory=WWW_PATH, html=True), name="www")

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description="pandoc based wiki")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="listening address")
    parser.add_argument("-p", "--port", type=int, default=8081, help="listening port")
    args = parser.parse_args()

    # start uvicorn webserver with reference to fastapi app
    config = uvicorn.Config("wiki:app", host=args.ip, port=args.port, log_level="info")
    server = uvicorn.Server(config)
    server.run()
