#!/usr/bin/env python3
"""
Generate conventional commit messages based on change type and content.

Supports standardized English prefixes:
- Docs: Documentation changes
- Feat: New features
- Fix: Bug fixes
- Refactor: Code refactoring
- Style: Code style changes
- Chore: Build tools, dependencies
- Test: Test additions/changes
- Config: Configuration changes
- License: License file updates
"""

import subprocess
import re
import argparse
from typing import List, Dict


# Category to commit type mapping
CATEGORY_TO_TYPE = {
    'deps': 'Chore',
    'docs': 'Docs',
    'license': 'License',
    'config': 'Config',
    'test': 'Test',
    'chore': 'Chore',
    'feat': 'Feat',
    'fix': 'Fix',
    'refactor': 'Refactor',
    'style': 'Style',
    'code': 'Style',  # Default for uncategorized code
    'other': 'Chore',
}

# Common commit message templates by category
MESSAGE_TEMPLATES = {
    'deps': {
        'patterns': [
            (r'package\.json', 'Update JavaScript dependencies'),
            (r'requirements\.txt', 'Update Python dependencies'),
            (r'go\.(mod|sum)', 'Update Go dependencies'),
            (r'Gemfile', 'Update Ruby dependencies'),
            (r'Cargo\.toml', 'Update Rust dependencies'),
        ],
        'default': 'Update dependencies',
    },
    'docs': {
        'patterns': [
            (r'README', 'Update README documentation'),
            (r'CHANGELOG', 'Update changelog'),
            (r'CONTRIBUTING', 'Update contributing guidelines'),
            (r'ARCHITECTURE', 'Update architecture documentation'),
        ],
        'default': 'Update documentation',
    },
    'license': {
        'default': 'Update license file',
    },
    'config': {
        'default': 'Update configuration',
    },
    'test': {
        'default': 'Update tests',
    },
    'chore': {
        'patterns': [
            (r'\.gitignore', 'Update gitignore'),
            (r'Dockerfile', 'Update Docker configuration'),
            (r'\.github/', 'Update GitHub workflows'),
        ],
        'default': 'Update tooling',
    },
    'feat': {
        'default': 'Add new feature',
    },
    'fix': {
        'default': 'Fix bug',
    },
    'refactor': {
        'default': 'Refactor code',
    },
    'style': {
        'default': 'Update code style',
    },
}


def get_file_changes(filepath: str) -> str:
    """Get git diff for a specific file."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', filepath],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def analyze_changes(files: List[str], category: str) -> str:
    """
    Analyze file changes to generate a descriptive message.

    Returns a brief description of what was changed.
    """
    if not files:
        return ""

    # Try to match patterns
    if category in MESSAGE_TEMPLATES:
        templates = MESSAGE_TEMPLATES[category]
        if 'patterns' in templates:
            for pattern, message in templates['patterns']:
                for filepath in files:
                    if re.search(pattern, filepath):
                        return message

        # Use default template
        if 'default' in templates:
            # Enhance with file-specific info if available
            base_msg = templates['default']

            # For docs, mention specific doc
            if category == 'docs' and len(files) == 1:
                filename = files[0].split('/')[-1]
                if filename.endswith('.md'):
                    doc_name = filename.replace('.md', '').replace('_', ' ').title()
                    return f"Update {doc_name} documentation"

            return base_msg

    # Fallback: generic message based on category
    return f"Update {category} files"


def generate_commit_message(category: str, files: List[str]) -> str:
    """
    Generate a conventional commit message.

    Format: <Type>: <description>

    Args:
        category: Change category (deps, docs, feat, etc.)
        files: List of changed files in this category

    Returns:
        Formatted commit message
    """
    # Get commit type
    commit_type = CATEGORY_TO_TYPE.get(category, 'Chore')

    # Generate description
    description = analyze_changes(files, category)

    # Format: Type: Description
    return f"{commit_type}: {description}"


def generate_commit_messages(groups: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Generate commit messages for all groups.

    Args:
        groups: Dictionary mapping category to list of files

    Returns:
        Dictionary mapping category to commit message
    """
    messages = {}
    for category, files in groups.items():
        messages[category] = generate_commit_message(category, files)
    return messages


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Generate conventional commit messages'
    )
    parser.add_argument(
        '--category',
        type=str,
        help='Change category (deps, docs, feat, etc.)'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        help='List of changed files'
    )

    args = parser.parse_args()

    if args.category and args.files:
        msg = generate_commit_message(args.category, args.files)
        print(msg)
    else:
        print("Usage: generate_commit_message.py --category <type> --files <file1> [file2...]")


if __name__ == '__main__':
    main()
