`snip` is a command-line interface (CLI) tool written in Python. It
manages snippets and place them into the pasteboard (AKA clipboard on
some operating systems.)

# Installation

Currently, we do not publish this package to [PyPI] so the installation
step is a little involved.

1. Navigate the the [Releases] page
2. Click to select a release, preferably the latest
3. Download the .whl file and install

# Usage

## Create a New Snippet

Issue the following command:

    snip put <filename>

For example:

    snip put logvar.py

At this point, `snip` will invoke the text editor (as defined by the
`$EDITOR` environment variable) and the user can start adding content
to this file. `snip` uses a template engine which is similar to
`Jinja`. Bedlow is a sample of file `logvar.py` after editing:

    {% raw %}
    logging.debug("{{label}}=%r", {{var_name}})
    {% endraw %}

The snippet file `logvar.py` resides in the data directory which
defaults to `~/.local/share/snip`. More about this directory later in
the configuration section.

## Retrieve a Snippet

To retrieve a snippet, issue the following

    snip get -f <filename>

For example:

    snip get -f logvar.py

In this example, `snip` will ask the user for the values of `label` and
`var_name`, which are defined in `logvar.py`. User can supply the values
from the command line:

    
    snip get -f logvar.py -d label="Port number" -d var_name=port_number

With the above command, `snip` will not ask for those values. It will
output the following to the console as well as placing it into the
pasteboard:

    logging.debug("Port number=%r", port_number)

# Configuration

Upon the first run, `snip` will create a configuration file
`~/.config/snip.json` which looks like this:

```json
{
    "data-dir": "/home/user/.local/share/snip"
}
```

`snip` stores snippets into the `data-dir` directory. User can edit this
file and choose a different location, such as a folder within a Dropbox
directory to allow synchronization accross many hosts.


[PyPI]: https://pypi.org/
[Releases]: https://github.com/htv2012/snip/releases

