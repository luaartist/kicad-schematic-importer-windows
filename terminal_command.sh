# For Windows users (convert LF to CRLF on checkout, convert CRLF to LF on commit)
git config --global core.autocrlf true

# For macOS/Linux users (don't convert on checkout, convert CRLF to LF on commit)
git config --global core.autocrlf input

# For a specific repository only (instead of --global)
git config core.autocrlf true  # or 'input'