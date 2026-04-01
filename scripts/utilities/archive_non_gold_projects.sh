#!/bin/bash
# Archive 22 non-gold-standard projects to projects-archive/
# Keep only the 15 gold standard projects in projects/ for focused work

set -e

PROJECTS_DIR="experimental/projects"
ARCHIVE_DIR="experimental/projects-archive"

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

echo "Archiving 22 non-gold-standard projects..."
echo "=" * 80

# Gold standard 15 (keep in projects/):
# gitlabhq, grafana, wagtail, metabase, mui, electron, pytest, celery,
# pandas, scikit-learn, sphinx, discourse, django-rest-framework, superset, fastapi-users

# Projects to archive (22):
ARCHIVE_PROJECTS=(
    # Minimal doc folders (6)
    "airflow"
    "mastodon"
    "cal.com"
    "plane"
    "ghost"
    "kubernetes"

    # External docs (9)
    "django"
    "rails"
    "vue"
    "nextjs"
    "sentry"
    "saleor"
    "home-assistant"
    "fullstack-fastapi"
    "webpack"

    # Small libraries (7)
    "click"
    "flask"
    "requests"
    "redis"
    "docker"
    "express"
    "fastapi"
)

# Move projects to archive
for project in "${ARCHIVE_PROJECTS[@]}"; do
    if [ -d "$PROJECTS_DIR/$project" ]; then
        echo "Archiving: $project"
        mv "$PROJECTS_DIR/$project" "$ARCHIVE_DIR/"
    else
        echo "Skipping (not found): $project"
    fi
done

echo ""
echo "=" * 80
echo "Archive complete!"
echo ""
echo "Gold standard projects remaining in $PROJECTS_DIR/:"
ls -1 "$PROJECTS_DIR/" | wc -l
ls -1 "$PROJECTS_DIR/"

echo ""
echo "Archived projects in $ARCHIVE_DIR/:"
ls -1 "$ARCHIVE_DIR/" | wc -l
ls -1 "$ARCHIVE_DIR/"
