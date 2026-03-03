# 1.0.0 (2026-03-03)


### Features

* initial commit ([33a224a](https://github.com/amirkhonov/metatrader5-mcp/commit/33a224aa5dfa55194a40244ae9c65dc797c0f65f))

# 1.0.0 (2026-03-01)


### Features

* initial commit ([33a224a](https://github.com/amirkhonov/metatrader5-mcp/commit/33a224aa5dfa55194a40244ae9c65dc797c0f65f))

# [1.2.0](https://github.com/amirkhonov/metatrader5-mcp/compare/v1.1.0...v1.2.0) (2026-02-24)


### Features

* introduce Pydantic schemas and tools for MetaTrader 5 market data, positions, and trading operations. ([6cd80e4](https://github.com/amirkhonov/metatrader5-mcp/commit/6cd80e41b847fd781d66f9adc1ecf2b6ece55837))

# [1.1.0](https://github.com/amirkhonov/metatrader5-mcp/compare/v1.0.0...v1.1.0) (2026-02-24)


### Features

* Implement initial MetaTrader 5 FastMCP server with CLI argument parsing, predefined prompts, and Pydantic schema validation for tool parameters. ([b7792e0](https://github.com/amirkhonov/metatrader5-mcp/commit/b7792e0442ae5671a7e45119b5b69720512dce30))

# 1.0.0 (2026-02-15)


### Features

* Add GitHub Actions workflow for automated releases using semantic-release. ([0f70eae](https://github.com/amirkhonov/metatrader5-mcp/commit/0f70eae5023c739251f3c000fe29c73c865edf86))

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- LICENSE file (MIT)
- requirements.txt for pip users
- requirements-dev.txt for development dependencies
- setup.py for pip installation
- .env.example for configuration template
- CHANGELOG.md for version tracking
- CONTRIBUTING.md with contribution guidelines
- Enhanced error handling and validation
- Environment variable support for configuration
- Quick installation script
- Docker support with Dockerfile and docker-compose.yml
- Comprehensive documentation

### Changed
- Updated README with quick start guide
- Improved project metadata in pyproject.toml and setup.py
- Enhanced logging configuration

### Fixed
- Package metadata placeholders

## [0.1.0] - 2024-01-01

### Added
- Initial release
- 32 MCP tools for MetaTrader 5 integration
- Connection and account management tools
- Market data retrieval tools
- Trading operations tools
- Position and order management tools
- FastMCP-based server implementation
- CLI support with auto-initialization
- Comprehensive README documentation

[Unreleased]: https://github.com/amirkhonov/metatrader5-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/amirkhonov/metatrader5-mcp/releases/tag/v0.1.0
