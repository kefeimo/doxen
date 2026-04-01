#!/bin/bash
# Clone expansion projects (6 more) for experimental evaluation

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="$SCRIPT_DIR/../projects"

echo "🚀 Cloning expansion projects (Phase 2)"
echo "Target directory: $PROJECTS_DIR"
echo ""

# Expansion project configurations: "org/repo:local_name:description"
PROJECTS=(
    "pallets/flask:flask:Python micro-framework"
    "rails/rails:rails:Ruby full-stack framework"
    "vuejs/core:vue:JavaScript progressive framework"
    "pallets/click:click:Python CLI framework"
    "psf/requests:requests:Python HTTP library"
    "moby/moby:docker:Container platform"
)

echo "📋 Expansion Projects:"
echo "  1. Flask (Python) - Micro-framework, compare to FastAPI/Django"
echo "  2. Rails (Ruby) - Full-stack, different language"
echo "  3. Vue.js (JavaScript) - Frontend framework"
echo "  4. Click (Python) - CLI domain"
echo "  5. Requests (Python) - Pure library"
echo "  6. Docker (Go) - Infrastructure/containers"
echo ""

for project in "${PROJECTS[@]}"; do
    IFS=':' read -r repo name description <<< "$project"

    target_dir="$PROJECTS_DIR/$name/repo"

    if [ -d "$target_dir/.git" ]; then
        echo "✓ $name already cloned, skipping..."
    else
        echo "📥 Cloning $name ($description) from $repo..."
        git clone --depth 1 "https://github.com/$repo" "$target_dir"
        echo "✅ $name cloned successfully"
    fi
    echo ""
done

echo "✅ All expansion projects cloned!"
echo ""
echo "Summary:"
for project in "${PROJECTS[@]}"; do
    IFS=':' read -r repo name description <<< "$project"
    target_dir="$PROJECTS_DIR/$name/repo"
    if [ -d "$target_dir" ]; then
        file_count=$(find "$target_dir" -type f | wc -l)
        echo "  • $name: $file_count files ($description)"
    fi
done

echo ""
echo "Total projects: 10 (4 pilot + 6 expansion)"
