# Doorplates Microservice

This microservice generates a doorplate.

## Example usage

### Generate one doorplate using JSON

```bash
curl --location --request POST 'http://localhost:8080/doorplates/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "roomnumber": "301",
  "description": "Bla bla bla bla",
  "personname": "Max Mueller",
  "template": "13x13.svg"
}'
```

### Generate many doorplate using CSV

```bash
curl --request POST 'http://localhost:8080/doorplates/' \
--header 'Content-Type: text/csv' \
--data-raw '301;bla bla bla;Max Mueller;13x13.svg
302;whatever;Heinz Strunk;13x13.svg'
```

`--data-raw '...'` can be replaced by `--data-binary @rooms.csv` to read data from a file.

## Notes

### Rendering backends
There are some different backends to render your input data into a PDF:

#### Inkscape Microservice
`inkscape-microservice` uses the [inkscape-converter-microservice](https://github.com/debuglevel/inkscape-converter-microservice) to call Inkscape.
`inkscape-converter-microservice` obviously needs Inkscape installed.
But there is a docker image available (see `docker-compose.yml`) and
actually might just be the easiest variant.

It gives you the best results and especially can handle Inkscape's "flowed text",
which the other backends will probably not handle well (black boxes or just missing text; see https://superuser.com/questions/1030072/why-do-i-have-black-boxes-in-svgs-created-with-inkscape).

Furthermore, it is the only backend which could handle other input than SVG (although never tested).

#### Inkscape
`inkscape` calls Inkscape without the microservice above.

`apk add inkscape` installs about 99 packages, and fonts are not yet included (if available at all).
But on a Debian based docker image (or just a Debian machine), this might work quite well.

#### svglib
`svglib` uses the [svglib](https://pypi.org/project/svglib/) library, which is purely written
in Python. Unfortunately it seems to produce rather poor results
(e.g. the embedded image in `hogwarts_13x13.svg` is just not rendered at all, and the "flowed text" problem exists.)

It's just there for testing purposes (and not even enabled in `requirements.txt` by default).

#### CairoSVG
`cairosvg` uses the [CairoSVG](https://cairosvg.org/) package around `libcairo`.
It produces better results than `svglib` although it suffers from the "flowed text" problem.

But even without this, it's a major pain to install into an Alpine docker image; switching to
the Debian based python docker image would reduce the pain,
but IMHO is still not worth it as a default.

It might although work if your SVGs do not contain Inkscape's "flowed text", or you always
remember to convert it (see above).

Feel free to customize the docker image for your needs; the `apt` command would be this:
```bash
# Install the cairo library on the python Debian image
RUN apt-get update && apt-get install -y libcairo2 && rm -rf /var/lib/apt/lists/*
```

For Alpine, there is a `cairo` package available. But `pip` does not provide wheels for Alpine,
and so, `pip` has to compile the stuff itself. Therefore, you have to install some `-dev` and `build` packages.
```bash
# Install dependencies for CairoSVG on Alpine
RUN apk add --no-cache \
    build-base cairo-dev cairo cairo-tools \
    # pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
```

It's just there for testing purposes (and not even enabled in `requirements.txt` by default).

#### CairoSVG


# TODO
## OpenAPI clients
With inkscape microservice port 8081 on the host:
```
# actually used variant:
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli:v5.2.0 generate -i http://host.docker.internal:8081/openapi.json -g python -o /local/inkscape-client/ --additional-properties=generateSourceCodeOnly=true,packageName=app.library.inkscape_converter_client

# but asyncio does not seem to have any effect
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli:v5.2.0 generate -i http://host.docker.internal:8081/openapi.json -g python -o /local/inkscape-client/ --additional-properties=library=asyncio,generateSourceCodeOnly=true,packageName=app.library.inkscape_converter_client

# seems to be a regular argument, but only works with python-legacy
# and it actually does not work with async/await.
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli:v5.2.0 generate -i http://host.docker.internal:8081/openapi.json -g python-legacy -o /local/inkscape-client/ --additional-properties=generateSourceCodeOnly=true,packageName=app.library.inkscape_converter_client --library=asyncio
```


# Python Microservice Template

Python microservice template, inspired by my Kotlin based microservice
template https://github.com/debuglevel/greeting-microservice, but with way less enthusiasm; and I'm not too sure that
too much works here, because I just copied a bunch of stuff from my various other projects to have them at one place at
least.

## Development environment

* Python environment
    * Python 3.8
    * venv
* Code quality
    * Formatting
        * black
    * Type annotations
        * mypy
    * Testing
        * pytest
        * tox
* REST
    * FastAPI
* Configuration
  * [Pydantic Settings Management](https://fastapi.tiangolo.com/advanced/settings/)
* Deployment
    * Docker
    * docker-compose
* IDE
    * PyCharm Community

### TODO

* Logging that does not completely suck
    * would nice to be configurable via ENV
* Testing?
    * tox (which seems to test against different Python versions. WTF compatibility? But it does not install those
      environments/python versions!)
* linting?
* Formatting?

## Development

### Environment

#### Initialize virtual environment (using venv)

```sh
python3 -m venv venv
```

#### Activate virtual environment

```sh
source ./venv/Scripts/activate
```

```powershell
.\venv\Scripts\Activate.ps1
```

### Dependencies

#### Install dependencies

```sh
pip install -r requirements-dev.txt
```

#### Dependency updates

`pip list --outdated` shows outdated (transitive) dependencies.

#### Formatting / Linting

##### black

`black` is used for formatting, because `black` does not ask about your opinion about how Python code should be formatted.

```bash
black .
```

##### mypy

mypy checks the type annotations:

```sh
mypy app tests
```

### Testing

#### Run tests

```sh
pytest
```

#### Run tests on every file change

```sh
pytest-watch -c # -c clears terminal before pytest runs
```

#### Run test against different environments

```sh
tox
```

### Documentation

#### OpenAPI documentation

* Open [Swagger UI](http://localhost:8080/docs) or [ReDoc](http://localhost:8080/redoc)
* OpenAPI specs are available (as JSON) at http://localhost:8080/openapi.json 
* Update `openapi.json` via `python update-openapi.py`

### All-in-one
`tox.ini` is also configured to run some additional commands (like a Makefile):
* `black .` for formatting
* `python update-openapi.py` to update `openapi.yaml`
* `pytest` for testing

### Deployment

#### Development (with auto reloading changed files)

```sh
uvicorn app.rest.main:fastapi --port=8080 --reload --log-config=app/logging-config.yaml
```

#### Production

This should be quite okay:

```sh
uvicorn app.rest.main:fastapi --port=8080 --log-config=app/logging-config.yaml
```

But some docs mention that `gunicorn` can be used as a manager.

#### Production (via docker compose)

```sh
docker compose up --build
```


