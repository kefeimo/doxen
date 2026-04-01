# Environment Setup - Detailed Reference

## Python Virtual Environment (CRITICAL)

### Why venv is Required
- Doxen has specific dependency versions that conflict with system packages
- System Python lacks isolation for development dependencies
- Virtual environments prevent dependency conflicts between projects

### Setup Commands
```bash
# Create venv (one-time)
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -e .

# Verify installation
./venv/bin/python -c "import doxen; print('OK')"
```

### Usage Patterns
```bash
# Method 1: Direct execution (preferred)
./venv/bin/python script.py
./venv/bin/pip install package

# Method 2: Activate first
source venv/bin/activate
python script.py  # Now uses venv
deactivate  # When done
```

### Common Issues
- **"ModuleNotFoundError"** → Using system Python instead of venv
- **"Permission denied"** → Missing executable permissions on venv/bin/*
- **"No such file"** → Run from project root where venv/ exists

## Ruby Environment (rbenv) (CRITICAL)

### Why rbenv is Required
- Discourse requires Ruby 3.4.1 specifically
- System Ruby versions vary by OS and may be incompatible
- rbenv provides automatic version switching per project

### Setup Commands (One-time)
```bash
# Install rbenv
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash

# Add to shell
echo 'eval "$(~/.rbenv/bin/rbenv init - bash)"' >> ~/.bashrc
source ~/.bashrc

# Install Ruby version
rbenv install 3.4.1

# Install bundler
gem install bundler

# Install project gems
bundle install --path vendor/bundle
```

### Usage Patterns
```bash
# Check version (should auto-switch)
ruby --version  # Should show 3.4.1

# Run Ruby scripts
ruby src/doxen/extractors/ruby_parser_yard.rb file.rb

# Run with bundler (when gems needed)
bundle exec ruby script.rb
```

### YARD Extraction Details
- **Purpose:** Extract Ruby API documentation (classes, modules, methods)
- **Tags:** @param, @return, @example, @see, @deprecated
- **Output:** Structured JSON with method signatures and documentation
- **Usage:** `yard doc --list-undoc` to find undocumented methods

## Docker Alternative

### When to Use Docker
- CI/CD environments where venv/rbenv setup is complex
- Isolated testing environments
- Production deployment isolation

### Docker Commands
```bash
# Build image
docker build -t doxen .

# Run analysis
docker run -v $(pwd):/app doxen python /app/src/analyze.py

# Interactive shell
docker run -it -v $(pwd):/app doxen bash
```