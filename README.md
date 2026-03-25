# Doxen

**Where code becomes knowledge.**

Doxen is a knowledge layer for code that transforms codebases into structured, testable, and AI-ready documentation.

## Overview

Doxen analyzes your codebase, extracts structured understanding, and turns it into testable, AI-ready knowledge—so both humans and machines can truly understand how your system works.

### Key Features

- **Hybrid Analysis**: Combines AST parsing (structure) with LLM analysis (intent)
- **Structured Output**: Generates machine-usable documentation with metadata
- **Git Traceability**: Links documentation to git history
- **RAG-Native**: Optimized for vector embeddings and semantic retrieval
- **Multi-Language**: Supports Python and JavaScript (more coming)

## Installation

```bash
# Install from source (development)
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Analyze a repository
doxen analyze /path/to/repo --output .doxen/docs

# Scan repository statistics
doxen scan /path/to/repo

# Get help
doxen --help
```

## Project Status

**Current Version:** 0.1.0 (MVP in development)

### Week 1 MVP (In Progress)
- [x] Project structure
- [x] CLI skeleton
- [x] Placeholder modules
- [ ] AST parsing implementation
- [ ] LLM integration
- [ ] Markdown generation
- [ ] Git history extraction

See [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) for full roadmap.

## Architecture

```
doxen/
├── src/doxen/
│   ├── analyzer/          # AST + LLM analysis
│   ├── extractor/         # Language-specific extractors
│   ├── generator/         # Documentation generators
│   └── utils/             # Git, metadata utilities
└── tests/                 # Test suite
```

## Documentation

- [Product Vision](docs/VISION.md) - Product positioning and strategy
- [Requirements](docs/REQUIREMENTS.md) - Feature requirements and roadmap
- [Development](docs/DEVELOPMENT.md) - Architecture decisions
- [Progress](docs/PROGRESS.md) - Current work status
- [Claude Guide](CLAUDE.md) - AI collaboration conventions

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests (coming soon)
pytest

# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Contributing

This is currently a solo project. Contributions welcome once MVP is stable.

## License

MIT

## Contact

- GitHub: [@kefeimo](https://github.com/kefeimo)
- Repository: [kefeimo/doxen](https://github.com/kefeimo/doxen)
