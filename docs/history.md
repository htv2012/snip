# History

2024-09-01

- Create an installable package
- Implement simple put, get
- Copy to clipboard
- Add simple template expansion

version 0.3 2024-09-02

- Fix the required Python version -> 3.9
- Add config file
- Include first run, which create the config file if not found
- Sensible default
    - config file: `~/.config/snip.json`
    - data dir: `~/.local/share/snip`

Version 0.4.1 2024-09-03
- Integration with fzf
- Add `--version` flags

Version 0.4.2 2024-09-03
- Fix pyproject.toml to work with `hatchling build`
