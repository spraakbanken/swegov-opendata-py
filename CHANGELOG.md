# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### 🚀 Features

- Improve Dataset model

## [0.3.1] - 2026-10-26

### 🐛 Bug Fixes

- Readd Dokument methods

### 🧪 Testing

- Fix export command

## [0.3.0] - 2026-10-26

### 🚀 Features

- Merge dataset.dokument and dokument.dokument to dokument
- Merge dataset.dokument_status and dokument.dokument_status to dokument

## [0.2.0] - 2026-10-23

### 🚜 Refactor

- Split dataset and dokument
- Rename shared.py to validators.py
- Move value objects from dokument and dataset to value_objects
- Extract DokumentBase from dokument.Dokument and dataset.Dokument
- Rename and clean validators

### 🧪 Testing

- Update test requirements

### 💼 Other

- _(deps-dev)_ Update uv-build requirement

## [0.1.4] - 2026-10-22

### 🐛 Bug Fixes

- Write error messages to logger instead of print

## [0.1.3] - 2026-10-22

### 🐛 Bug Fixes

- Allow `DokReferens.ref_dok_typ` to be None

## [0.1.2] - 2026-10-09

### ⚙️ Miscellaneous Tasks

- Add project.classifiers och project.urls

## [0.1.0] - 2026-10-09

### 🚀 Features

- Onyl keep swegov_opendata data models
- Import from kb-labb/kb_sb_stack

### New Contributors

- @kod-kristoff made their first contribution in [#29](https://github.com/spraakbanken/swegov-opendata-py/pull/29)
- @dependabot[bot] made their first contribution
