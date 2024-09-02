# Nice to Have
- Integration with fzf
- Integration with bat
- Integration with jq
- Tags
- Keep a database for metadata (tags, ...)
- I would be nice if we can display the file using `bat`

# Backlog
- Add github workflow to `hatchling build` package for the release
- Add docs for the tool
- Add github workflow to upload doc to `readthedocs.com`

# History

2024-09-01

- Create an installable package
- Implement simple put, get
- Copy to clipboard
- Add simple template expansion

2024-09-02

- Fix the required Python version -> 3.9
- Add config file
- Include first run, which create the config file if not found
- Sensible default
    - config file: `~/.config/snip.json`
    - data dir: `~/.local/share/snip`
