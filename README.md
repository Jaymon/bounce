# Bounce

It's a keyword search engine, meaning you can configure it to redirect `yt` to Youtube, so a search like `yt weird al` would redirect right to Youtube's search.


## 1 minute getting started

1. Install it

        $ pip install bounce

2. Start it:

        $ bounce serve --host "127.0.0.1:5000"

3. Query it:

        $ curl "http://127.0.0.1:5000/?q=yt weird al" 

You can also run it using any WSGI server like [uWSGI](http://projects.unbit.it/uwsgi/) using the included `bouncefile.py` as the `wsgi-file`.


## Configuration


### url configuration

Bounce has a built-in [configuration file with generic mappings](https://github.com/Jaymon/bounce/blob/master/bounce/config.py) but you can also create your own that bounce will read when starting by setting the environment variable `BOUNCE_CONFIG` with a path to your custom configuration python file:

```bash
export BOUNCE_CONFIG=/path/to/bounce_config.py
```

The file must import `bounce.config.commands`:

```python
from bounce.config import commands
```

The `commands.add()` method takes a space separated list of commands and a value:

```python
commands.add("foo bar", "http://foo.com?q={}")
```

So, if you called bounce with the input:

    foo blammo

It would redirect to:

    http://foo.com?q=blammo

You could also call it with `bar blammo` and get the same thing because we set up the command keywords as `foo bar` so either _foo_ or _bar_ would redirect.

Notice that the value is a [python format string](https://docs.python.org/2/library/string.html#formatspec).


### callback configuration

value can also be a callback:

```python
def callback(q):
    # manipulat q in some way and then return where you would like to go
    return 'http://some.url.that.needed.manipulation.q.com={}'.format(q)

commands.add("foo bar", callback)
```

That makes it so bounce can do all kinds of crazy things.


### default configuration

By default, Google is the search engine of choice, so if you don't start your request with a command, bounce will redirect to Google search with your search string. If you would like to change this just pass `default=True` to one of your custom commands:

```python
commands.add("keyword", "value", default=True)
```


### Viewing configuration


the command `ls` will list all the commands bounce supports


## Testing

To test locally from the repo:

    $ export BOUNCE_CONFIG=/path/to/bounce/config.py
    $ python -m bounce serve --host "127.0.0.1:5000"

That should produce output that ends with the bound hostname and port:

    ...
    Server is listening on 127.0.0.1:5000

Which you can then use to test:

    $ curl "http://127.0.0.1:5000/?q=..."

And that's it.

