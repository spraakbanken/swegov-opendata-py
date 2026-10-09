# swegov-opendata

[![PyPI version](https://img.shields.io/pypi/v/swegov-opendata.svg)](https://pypi.org/project/swegov-opendata/)
[![PyPI license](https://img.shields.io/pypi/l/swegov-opendata.svg)](https://pypi.org/project/swegov-opendata/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swegov-opendata.svg)](https://pypi.org/project/swegov-opendata)

[![Maturity badge - level 2](https://img.shields.io/badge/Maturity-Level%202%20--%20First%20Release-yellowgreen.svg)](https://github.com/spraakbanken/getting-started/blob/main/scorecard.md)
[![Stage](https://img.shields.io/pypi/status/swegov-opendata.svg)](https://pypi.org/project/swegov-opendata/)

[![codecov](https://codecov.io/gh/spraakbanken/swegov-opendata-py/graph/badge.svg?token=DUV4CL6AK2)](https://codecov.io/gh/spraakbanken/swegov-opendata-py)

[![CI(check)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/check.yml/badge.svg)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/check.yml)
[![CI(release)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/release.yml/badge.svg)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/release.yml)
[![CI(scheduled)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/rolling.yml/badge.svg)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/rolling.yml)
[![CI(test)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/test.yml/badge.svg)](https://github.com/spraakbanken/swegov-opendata-py/actions/workflows/test.yml)

Pydantic models for [Riksdagens Öppna data](http://data.riksdagen.se/).

## Install

Add this to your project with

```shell
uv add swegov-opendata
```

## Minimum Supported Python Version Policy

The Minimum Supported Python Version is fixed for a given minor (1.x)
version. However it can be increased when bumping minor versions, i.e. going
from 1.0 to 1.1 allows us to increase the Minimum Supported Python Version. Users unable to increase their
Python version can use an older minor version instead. Below is a list of sparv-sbx-corpus-statistics versions
and their Minimum Supported Python Version:

- v0.1: Python 3.11.

Note however that sparv-sbx-corpus-statistics also has dependencies, which might have different MSRV
policies. We try to stick to the above policy when updating dependencies, but
this is not always possible.

## Changelog

This project keeps a [changelog](./CHANGELOG.md).

## License

This repository is licensed under the [MIT](./LICENSE) license.
