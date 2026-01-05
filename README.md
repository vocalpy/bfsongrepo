# bfsongrepo
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
## scripts and website for the Bengalese Finch Song Repository

## Development

### set up

We use Nox to run development tasks.

```console
brew install nox
```

Clone the repo and then run the Nox session named `"dev"` to make a virtual environment with all development dependencies.

```
nox -s dev
```

### Usage

#### Building the documentation

To build the docs locally, run the Nox session `"docs"`.

```
nox -s docs
```

It essentially runs this command:

```console
sphinx-build -nW --keep-going -b html docs docs/build/html
```

To inspect the generated docs, you can do the following: 

```console
cd docs/build/html; python -m http.server; cd ../../.. 
```

and then navigate to )http://127.0.0.1:8000 in a browser while the Python http server is running.

#### Publishing the documentation

Once you are happy with the look of the generated docs, run the `"publish-to-github"` session.

```
nox -s publish-to-github
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/melisandeteng"><img src="https://avatars.githubusercontent.com/u/34208548?v=4?s=100" width="100px;" alt="melisandeteng"/><br /><sub><b>melisandeteng</b></sub></a><br /><a href="https://github.com/vocalpy/bfsongrepo/commits?author=melisandeteng" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!