# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [2.0.2] - 2024-01-06
### Fixed
 - Fix documentation links in docstrings by @amureki
### Added
 - Share session between requests by @allburov in #31

## [2.0.1] - 2020-02-02
### Fixed
 - Updated requirements.txt to reflect compatibility with pyjwt 2

## [2.0.0] - 2019-11-25
### Added
 - Support for `HTTP_PROXY` environment variables. This should enable use of the
   SDK on the PythonAnywhere platform (see issue #24)

## [1.1.0] - 2019-02-06
### Added
 - Support for "Authenticated Users" feature: `publish_to_users`, `generate_token` and `delete_user`

### Changed
 - `publish` renamed to `publish_to_interests` (`publish` method deprecated).

## [1.0.3] - 2019-01-16
### Fixed
 - Updated python runtime version requirements in setup.py to reflect the versions
   we actually support.

## [1.0.2] - 2019-01-04
### Fixed
 - Relaxed version requirements of dependencies to increase compatibility

## [1.0.1] - 2018-11-19
### Fixed
 - Updated requests version to include fix for CVE-2018-18074

## [1.0.0] - 2018-07-31
### Added
 - Changelog for GA release
