import os
import pathlib

import nox

DIR = pathlib.Path(__file__).parent.resolve()
VENV_DIR = pathlib.Path('./.venv').resolve()


@nox.session
def dev(session: nox.Session) -> None:
    """
    Sets up a python development environment for the project.

    This session will:
    - Create a python virtualenv for the session
    - Install the `virtualenv` cli tool into this environment
    - Use `virtualenv` to create a global project virtual environment
    - Invoke the python interpreter from the global project environment to install
      the project and all it's development dependencies.
    """

    session.install("virtualenv")
    # VENV_DIR here is a pathlib.Path location of the project virtualenv
    # e.g. .venv
    session.run("virtualenv", os.fsdecode(VENV_DIR), silent=True)

    python = os.fsdecode(VENV_DIR.joinpath("bin/python"))

    # Use the venv's interpreter to install the project along with
    # all it's dev dependencies, this ensures it's installed in the right way
    session.run(python, "-m", "pip", "install", "-e", ".[dev]", external=True)


DOCS_SRC_DIR = "docs"
DOCS_BUILD_DIR = "docs/build/html"


@nox.session
def docs(session: nox.Session) -> None:
    """
    Build the docs.

    To run ``sphinx-autobuild``,  do:

    .. code-block::console

       nox -s docs -- autobuild

    Otherwise the docs will be built once using sphinx-build
    """
    session.install(".[docs]")
    if session.posargs:
        if "autobuild" in session.posargs:
            print("Building docs at http://127.0.0.1:8000 with sphinx-autobuild -- use Ctrl-C to quit")
            session.run("sphinx-autobuild", DOCS_SRC_DIR, DOCS_BUILD_DIR)
        else:
            print("Unsupported argument to docs")
    else:
        session.run("sphinx-build", "-nW", "--keep-going", "-b", "html", DOCS_SRC_DIR, DOCS_BUILD_DIR)


@nox.session(name='publish-to-github')
def publish_to_github(session: nox.Session) -> None:
    """Publish built site to GitHub
    
    Uses 'ghp-import' to push contents of DOCS_BUILD_DIR to branch 'gh-pages'"""
    session.install("ghp-import")
    session.run("ghp-import", "-n", "-p", "-o", DOCS_BUILD_DIR)
