# History

version 0.5.1 2024-12-10
- Switch tooling to uv
- Introduce the ls sub command

Version 0.4.2 2024-09-03
- Fix pyproject.toml to work with `hatchling build`

Version 0.4.1 2024-09-03
- Integration with fzf
- Add `--version` flags

version 0.3 2024-09-02

- Fix the required Python version -> 3.9
- Add config file
- Include first run, which create the config file if not found
- Sensible default
    - config file: `~/.config/snip.json`
    - data dir: `~/.local/share/snip`

2024-09-01

- Create an installable package
- Implement simple put, get
- Copy to clipboard
- Add simple template expansion

