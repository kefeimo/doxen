#!/bin/bash
# Clone pilot projects for experimental evaluation

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="$SCRIPT_DIR/../projects"

echo "🚀 Cloning pilot projects for experimental evaluation"
echo "Target directory: $PROJECTS_DIR"
echo ""

# Project configurations: "org/repo:local_name"
PROJECTS=(
    "tiangolo/fastapi:fastapi"
    "expressjs/express:express"
    "django/django:django"
    "vercel/next.js:nextjs"
)

for project in "${PROJECTS[@]}"; do
    IFS=':' read -r repo name <<< "$project"

    target_dir="$PROJECTS_DIR/$name/repo"

    if [ -d "$target_dir/.git" ]; then
        echo "✓ $name already cloned, skipping..."
    else
        echo "📥 Cloning $name from $repo..."
        git clone --depth 1 "https://github.com/$repo" "$target_dir"
        echo "✅ $name cloned successfully"
    fi
    echo ""
done

echo "✅ All projects cloned!"
echo ""
echo "Summary:"
for project in "${PROJECTS[@]}"; do
    IFS=':' read -r repo name <<< "$project"
    target_dir="$PROJECTS_DIR/$name/repo"
    if [ -d "$target_dir" ]; then
        file_count=$(find "$target_dir" -type f | wc -l)
        echo "  • $name: $file_count files"
    fi
done
