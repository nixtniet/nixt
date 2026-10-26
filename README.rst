**NAME**


::

    NIXT - write your own commands.


**SYNOPSIS**


::

    nixt <cmd> [-option] [--option] [arg=val] [arg==val] [arg-=val]


**INSTALL**


::

    due to lost access to my pypi account, use the latest from github

        $ git clone https://github.com/nixtniet/nixt
        $ cd nixt
        $ pipx install . --force


**DESCRIPTION**


::

    NIXT has it's modules in the ~/.nixt/mods directory so for a
    hello world command you would edit a file in ~/.nixt/mods/hello.py
    and add the following:


        def hello(msg):
            msg.reply("hello world !!")


    typing the hello command would result into a hello world !!:


        $ nixt hello
        hello world !!

**MANUAL**

::

    usage: nixt [options] [cmd] [key=val] [key==val] [key-=val] [arguments]

    NIXT

    options:
      -h, --help         show this help message and exit
      -c, --console      start a console.
      -d, --daemon       run as background daemon.
      -s, --service      run as service.

      -a, --all          load all modules.
      -l, --level level  set loglevel.
      -v, --verbose      enable verbose.
      -w, --wait         wait for services to start.

      -m, --mods m1,m2   modules to load.
      -p, --path path    path to modules directory.

      --admin            enable admin mode.
      --scanner          do full modules scan on boot.
      --wdr WDR          set modules directory.

    use "nixt cmd" for a list of commands.


**FILES**

::

    ~/.nixt
    ~/.local/bin/nixt
    ~/.local/share/pipx/venvs/nixt/*


**AUTHOR**


::

    Nixt Niet <nixtniet@gmail.com>


**COPYRIGHT**

::

    NIXT is Public Domain.
