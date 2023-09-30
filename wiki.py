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

import plugin


class SourceData(pydantic.BaseModel):
    data : str


_SOURCE_PATH = pathlib.Path("./source")
_WWW_PATH = pathlib.Path("./www")
_WWW_MEDIA_PATH = _WWW_PATH / "media"
_PLUGIN_PATH = pathlib.Path("./plugins")

_PANDOC_FILE_SUFFIXES = (".md", ".rst")
_BACKUP_FILE_SUFFIX = ".bak"


app = fastapi.FastAPI()


@app.get("/api/source")
async def get_source_files():
    """get list of source file names"""
    return [file.name for file in _SOURCE_PATH.glob("*") if file.is_file() and file.name[0] != "."]


@app.get("/api/source/{name}")
async def get_source(name: str):
    """get source source for a html page"""
    source_file_path = _SOURCE_PATH / name

    if not source_file_path.is_relative_to(_SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    return source_file_path.read_text()


@app.delete("/api/source/{name}")
async def delete_source_file(name: str):
    """delete source file and corresponding html page"""

    # check if source file is valid
    source_file_path = _SOURCE_PATH / name

    if not source_file_path.is_relative_to(_SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    www_file_path = None

    if source_file_path.suffix in _PANDOC_FILE_SUFFIXES:
        # check if html file is valid
        www_file_path = _WWW_PATH.joinpath(name).with_suffix(".html")

    else:
        www_file_path = _WWW_PATH / name

    if not www_file_path.is_relative_to(_WWW_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # delete files
    www_file_path.unlink(missing_ok=True)
    source_file_path.unlink()


@app.put("/api/source/{name}")
async def put_source_file(name: str, source: SourceData):
    """put source file and create corresponding html page"""
    name, data = plugin.pre_put_source_file(name, source.data)

    # check if source file path is valid
    source_file_path = _SOURCE_PATH / name

    if not source_file_path.is_relative_to(_SOURCE_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # backup old source file with same name, if present
    try:
        source_file_path.rename(source_file_path.parent / pathlib.Path("~" + source_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + _BACKUP_FILE_SUFFIX))
    except FileNotFoundError:
        pass

    # write source file
    source_file_path.write_text(data, encoding="utf-8")

    # process new source file
    www_file_path = _process_source_file(source_file_path)

    plugin.post_put_source_file(source_file_path, www_file_path)

    return source_file_path.read_text(encoding="utf-8")


@app.get("/api/media")
async def get_media_files():
    """get list of media files"""
    return [file.name for file in _WWW_MEDIA_PATH.glob("*")]


@app.put("/api/media")
async def upload_media_files(files: list[fastapi.UploadFile]):
    """upload multiple media files"""
    for remote_file in files:
        local_file_path = _WWW_MEDIA_PATH / remote_file.filename

        # check if media file path is valid
        if not local_file_path.is_relative_to(_WWW_MEDIA_PATH):
            raise fastapi.HTTPException(status_code=403, detail="not allowed")

        # backup old media file with same name, if present
        try:
            local_file_path.rename(local_file_path.parent / pathlib.Path("~" + local_file_path.name + "_" + datetime.datetime.utcnow().isoformat() + _BACKUP_FILE_SUFFIX))
        except FileNotFoundError:
            pass

        local_file_path.write_bytes(await remote_file.read())


@app.delete("/api/media/{name}")
async def delete_media_file(name: str):
    """delete media file"""
    # check if media file is valid
    file_path = _WWW_MEDIA_PATH.joinpath(name)

    if not file_path.is_relative_to(_WWW_MEDIA_PATH):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    # delete media file
    file_path.unlink()


def _process_source_file(source_file_path: pathlib.Path) -> pathlib.Path:
    """create html files from markup sources, then copy files to www directory"""
    www_file_path = pathlib.Path()

    # check if we need go generate html by invoking pandoc
    if source_file_path.suffix in _PANDOC_FILE_SUFFIXES:
        # create html page with currently available css files
        css_files = [css_file.name for css_file in _SOURCE_PATH.glob("*.css")]
        html = _create_html(source_file_path, css_files)

        www_file_path = _WWW_PATH.joinpath(source_file_path.stem).with_suffix(".html")
        www_file_path.write_text(html, encoding="utf-8")
    elif source_file_path.suffix != _BACKUP_FILE_SUFFIX:
        # other, non-backup files are simply copied to www directory
        www_file_path = _WWW_PATH / source_file_path.name
        www_file_path.write_bytes(source_file_path.read_bytes())

    return www_file_path


def _create_html(source_file_path: pathlib.Path, css_files: list[str]) -> str:
    run_params = ["pandoc", "--standalone", "--to", "html5"]

    for css_file in css_files:
        run_params.extend(["--css", css_file])

    run_params.append(source_file_path)

    result = subprocess.run(run_params, capture_output=True, check=True, shell=False)

    if result.returncode != 0:
        return False

    html_data = result.stdout.decode("utf-8")

    return html_data


# create directories if not present
_SOURCE_PATH.mkdir(exist_ok=True)
_WWW_PATH.mkdir(exist_ok=True)
_WWW_MEDIA_PATH.mkdir(exist_ok=True)

# load plugins
plugin.load(_PLUGIN_PATH, _SOURCE_PATH, _WWW_PATH, _WWW_MEDIA_PATH)

# make fastapi serve static (html) files
app.mount("/", fastapi.staticfiles.StaticFiles(directory=_WWW_PATH, html=True), name="www")

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
