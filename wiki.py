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


SOURCE_PATH = pathlib.Path("./source")
WWW_PATH = pathlib.Path("./www")
WWW_MEDIA_PATH = WWW_PATH / "media"


app = fastapi.FastAPI()


@app.get("/api/source")
async def get_source_files():
    """get list of source file names"""
    return [file.name for file in SOURCE_PATH.glob("*")]


@app.get("/api/source/{name}")
async def get_source(name: str):
    """get source source for a html page"""
    source_file_path = SOURCE_PATH / name

    if not source_file_path.is_relative_to(SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    with open(source_file_path, "r", encoding="utf-8") as file:
        return file.read()


@app.delete("/api/source/{name}")
async def delete_source_file(name: str):
    """delete source file and corresponding html page"""
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

    # delet files
    html_file_path.unlink(missing_ok=True)
    source_file_path.unlink()


#@app.put("/api/source/{name}", response_class=fastapi.responses.HTMLResponse)
@app.put("/api/source/{name}")
async def put_source_file(name: str, source: SourceData) -> None:
    """put source file and create corresponding html page"""
    # check if source file path is valid
    source_file_path = SOURCE_PATH / name

    if not source_file_path.is_relative_to(SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_file_path.name == "manage.md": # manage.html is a special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # backup old source file with same name, if present
    try:
        source_file_path.rename(source_file_path.parent / pathlib.Path(source_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
    except FileNotFoundError:
        pass

    # sanitize input and write source file
    with open(source_file_path, "w", encoding="utf-8") as file:
        # todo: sanitizer removes whitespaces
        #sanitized_html = html_sanitizer.Sanitizer({"keep_typographic_whitespace": True}).sanitize(source.data)
        #sanitized_html = source.data
        file.write(source.data)

    # process new source file
    _process_source_file(source_file_path)

    #if source_file_path.suffix != ".css":
    #    css_files = [css_file.name for css_file in SOURCE_PATH.glob("*.css")]

    #    if not _create_html_page(name, source_file_path, css_files):
    #        raise fastapi.HTTPException(status_code=400, detail="error in source")



@app.get("/api/media")
async def get_media_files():
    """get list of media files"""
    return [file.name for file in WWW_MEDIA_PATH.glob("*")]


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


def _process_source_file(source_file_path: pathlib.Path) -> bool:
    """create html files from markup sources, then copy files to www directory"""

    # check if we need go generate html by invoking pandoc
    if source_file_path.suffix  in (".md", ".rst"):
        # get all currently availabe css files
        css_files = [css_file.name for css_file in SOURCE_PATH.glob("*.css")]

        return _create_html_page(source_file_path, css_files)

    # copy other files to www directory
    www_file_path = WWW_PATH / source_file_path.name
    www_file_path.write_bytes(source_file_path.read_bytes())
    return True


def _create_html_page(source_file_path: pathlib.Path, css_files: list[str]) -> bool:
    run_params = ["pandoc", "--standalone", "--to", "html5"]

    for css_file in css_files:
        run_params.extend(["--css", css_file])

    run_params.append(source_file_path)

    result = subprocess.run(run_params, capture_output=True, check=True, shell=False)

    if result.returncode != 0:
        return False

    html_file_data = result.stdout.decode("utf-8")

    html_path = WWW_PATH.joinpath(source_file_path.stem).with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_file_data)

    return True


# create directories if not present
SOURCE_PATH.mkdir(exist_ok=True)
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
