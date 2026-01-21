#!/bin/bash

# Configuration
SOURCE_DIR=".claude/skills"
TARGET_DIR=".agent/skills"
PROJECT_ROOT="$(pwd)"

# Ensure we are in the project root
if [ ! -d ".claude" ]; then
    echo "Error: .claude directory not found. Please run this script from the project root."
    exit 1
fi

# Check if source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Ensure .agent directory exists
if [ ! -d ".agent" ]; then
    mkdir -p ".agent"
    echo "Created .agent directory."
fi

# Check target status
if [ -L "$TARGET_DIR" ]; then
    # It's a symlink, check where it points
    CURRENT_LINK=$(readlink "$TARGET_DIR")
    if [[ "$CURRENT_LINK" == *".claude/skills"* ]]; then
        echo "Success: $TARGET_DIR is already symlinked to .claude/skills."
        ls -l "$TARGET_DIR"
        exit 0
    else
        echo "Updating symlink..."
        rm "$TARGET_DIR"
    fi
elif [ -d "$TARGET_DIR" ]; then
    # It's a real directory
    echo "Warning: $TARGET_DIR is a real directory."
    echo "Backing up to ${TARGET_DIR}.backup..."
    mv "$TARGET_DIR" "${TARGET_DIR}.backup"
fi

# Create the symlink
# We use a relative path for the link to be portable
# .agent/skills -> ../.claude/skills
cd .agent
ln -s ../.claude/skills skills
cd ..

echo "Comparison:"
ls -dF .claude/skills .agent/skills
ls -l .agent/skills

echo "Done. .agent/skills is now a symlink to .claude/skills."
