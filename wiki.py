#! /usr/bin/env python3

import pathlib
import subprocess
import datetime

import uvicorn
import fastapi
import fastapi.staticfiles
import fastapi.responses
import pydantic
import html_sanitizer


class SourcePage(pydantic.BaseModel):
    data : str


SOURCES_DIR = "./sources"
PAGES_DIR = "./html"

app = fastapi.FastAPI()


@app.get("/api/sources")
async def get_sources():
    """get list of source page names"""
    source_path = pathlib.Path(SOURCES_DIR)
    sources = source_path.glob("*.md")
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
        print(f"forbidden1: {html_path} not relative to {pathlib.Path(PAGES_DIR)}")
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if html_path.name == "manage.html": # manage.html is special page
        print(f"forbidden2: {html_path.name}")
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    source_path = pathlib.Path(SOURCES_DIR).joinpath(name)

    if not source_path.is_relative_to(pathlib.Path(SOURCES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    html_path.unlink(missing_ok=True)
    source_path.unlink()


@app.put("/api/sources/{name}", response_class=fastapi.responses.HTMLResponse)
async def put_source(name: str, source: SourcePage):
    """put source for a html page"""
    source_path = pathlib.Path(SOURCES_DIR) / name

    if not source_path.is_relative_to(pathlib.Path(SOURCES_DIR)):
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    if source_path.name == "manage.md": # manage.html is a special page
        raise fastapi.HTTPException(status_code=403, detail="not allowed")

    try:
        source_path.rename(source_path.parent / pathlib.Path(source_path.name + "_" + datetime.datetime.utcnow().isoformat() + ".backup"))
    except FileNotFoundError:
        pass

    with open(source_path, "w", encoding="utf-8") as file:
        sanitized_html = html_sanitizer.Sanitizer().sanitize(source.data)
        print(f"sanitized html: {sanitized_html}")
        file.write(sanitized_html)

    return _create_html_page(name, source_path)


def _create_html_page(name: str, path: pathlib.Path) -> str:
    result = subprocess.run(["pandoc", "--standalone", path], capture_output=True, check=True)

    html_data = result.stdout.decode("utf-8")

    html_page_path = pathlib.Path(PAGES_DIR).joinpath(name).with_suffix(".html")

    with open(html_page_path, "w", encoding="utf-8") as file:
        file.write(html_data)

    return html_data


app.mount("/", fastapi.staticfiles.StaticFiles(directory=PAGES_DIR, html=True), name="static")


if __name__ == "__main__":
    config = uvicorn.Config("wiki:app", host="0.0.0.0", port=8081, log_level="info")
    server = uvicorn.Server(config)
    server.run()
