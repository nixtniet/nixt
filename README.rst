**NAME**


::

    nixt - write your own commands


**SYNOPSIS**


::

    nixt [cmd] [arg=val] [arg==val]


**DESCRIPTION**


::

    nixt has it's modules in the ~/.nixt/mods directory so for a
    hello world command you would  edit a file in ~/.nixt/mods/hello.py
    and add the following


    def hello(event):
        event.reply("hello world !!")


    typing the hello command would result into a nice hello world !!


    $ nixt hello
    hello world !!


**FILES**

::

    ~/.nixt
    ~/.local/bin/nixt
    ~/.local/share/pipx/venvs/nixt/*


**AUTHOR**


::

    Nixt Niet <``nixtniet@gmail.com``>


**COPYRIGHT**

::

    nixt is Public Domain.
