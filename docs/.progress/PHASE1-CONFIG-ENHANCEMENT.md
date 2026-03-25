# Phase 1 Configuration Extraction Enhancement

## Problem

Current Phase 1 discovery doesn't extract concrete configuration details (ports, startup commands, environment variables), leading to hallucinated content in generated documentation.

## Example Issues

- README says "http://localhost:3000" but port is not verified
- README says "python main.py" but actual command may differ
- README says "npm start" but script name not confirmed

## Solution: Extract Configuration from Discovery

### 1. Docker Configuration
**From `docker-compose.yml` / `docker-compose.yaml`:**
```yaml
services:
  backend:
    ports:
      - "8000:8000"    # Extract this
  frontend:
    ports:
      - "3000:3000"    # Extract this
```

**From `Dockerfile`:**
```dockerfile
EXPOSE 8000
CMD ["python", "main.py"]
ENTRYPOINT [...]
```

### 2. Package Manager Scripts
**From `package.json`:**
```json
{
  "scripts": {
    "start": "vite",          # Extract scripts
    "dev": "vite dev",
    "build": "vite build"
  }
}
```

**From `pyproject.toml` / `setup.py`:**
```toml
[tool.poetry.scripts]
start = "app.main:main"
```

### 3. Environment Configuration
**From `.env.example` / `.env.template`:**
```bash
PORT=8000
HOST=0.0.0.0
API_KEY=your_key_here
```

### 4. Startup Scripts
**From `start.sh`, `run.sh`, `Makefile`:**
```bash
#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Implementation Plan

### Add to `RepositoryAnalyzer`

```python
def _extract_configuration(self, repo_path: Path) -> Dict[str, Any]:
    """Extract runtime configuration from various sources."""
    config = {
        "ports": [],
        "scripts": {},
        "environment": {},
        "startup_commands": [],
    }

    # 1. Docker Compose
    config["ports"].extend(self._extract_docker_ports(repo_path))

    # 2. Package.json scripts
    config["scripts"].update(self._extract_npm_scripts(repo_path))

    # 3. Environment templates
    config["environment"].update(self._extract_env_template(repo_path))

    # 4. Startup scripts
    config["startup_commands"].extend(self._extract_startup_scripts(repo_path))

    return config
```

### Update Discovery Output

Add to `REPOSITORY-ANALYSIS.md`:

```markdown
## Runtime Configuration

### Ports
- Backend: 8000 (from docker-compose.yml)
- Frontend: 3000 (from docker-compose.yml)

### Startup Commands
- Backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000` (from backend/start.sh)
- Frontend: `npm run dev` (from package.json)

### Environment Variables
- `OPENAI_API_KEY`: Required (from .env.example)
- `PORT`: Optional, defaults to 8000 (from .env.example)
```

## Benefits

1. **No hallucinations**: Only state verified facts
2. **Accurate setup guides**: Real commands users can copy
3. **Confidence tracking**: Know what's verified vs. inferred
4. **Better Quick Start**: Executable, tested instructions

## Implementation Priority

**Phase 1 (High Priority):**
- [ ] Extract Docker Compose ports
- [ ] Extract npm/pip scripts
- [ ] Parse .env.example files

**Phase 2 (Medium Priority):**
- [ ] Parse Dockerfile EXPOSE/CMD
- [ ] Extract Makefile targets
- [ ] Scan startup scripts (.sh, .bat)

**Phase 3 (Low Priority):**
- [ ] Parse systemd/supervisor configs
- [ ] Extract Kubernetes manifests
- [ ] Terraform/CloudFormation outputs

## Quality Markers

Until Phase 1 enhancement is complete, mark uncertain content:

```markdown
## Quick Start

> ⚠️ **Setup instructions not yet verified from codebase.**
> Refer to component README files for accurate setup steps.

### Prerequisites
- Python 3.8+ (detected from codebase)
- Node.js (detected from package.json)
- OpenAI API key (detected from .env.example)

### Installation

Refer to component-specific documentation:
- Backend: See `backend/README.md`
- Frontend: See `frontend/README.md`
```

## References

- Issue: Hallucinated port numbers and commands
- Root cause: Phase 1 doesn't extract configuration
- Solution: Configuration extraction in RepositoryAnalyzer
