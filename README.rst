**NAME**

| ``nixt`` - NIXT
|


**SYNOPSIS**

| ``nixt [-c|d|h|s] [-a] [-v] [-u] [-x] [-l level] [-m m1,m2] [-w wdr]``
| ``nixt [cmd] [arg=val] [arg==val]``
|

**DESCRIPTION**

``NIXT`` has all you need to program a unix cli program, such as disk
perisistence for configuration files, event handler to handle the
client/server connection, bork on exit for have an early exit, etc.

``NIXT`` contains python3 code to program objects in a functional way.
it provides an "clean namespace" Base class that only has dunder
methods, so the namespace is not cluttered with method names. This
makes storing and reading to/from json possible.

``NIXT`` is a python3 IRC bot, it can connect to IRC, fetch and
display RSS feeds, take todo notes, keep a shopping list and log
text. You can run it under systemd for 24/7 presence in a IRC channel.

``NIXT`` is Public Domain.


**INSTALL**


installation is done with pipx

| ``$ pipx install nixt``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ nixt -x srv > nixt.service``
| ``$ sudo mv nixt.service /etc/systemd/system/``
| ``$ sudo systemctl enable nixt --now``
|
| joins ``#nixt`` on localhost
|


**USAGE**


use ``nixt`` to control the program, default it does nothing

| ``$ nixt``
| ``$``
|

the -h option will show you possible options

| ``$ nixt -h``
| usage: nixt [-c|d|h|s] [-a] [-v] [-u] [-x] [-l level] [-m m1,m2] [-w wdr]
|        nixt [cmd] [arg=val] [arg==val]
|
| NIXT
|
| options:
|   -h, --help         show this help message and exit
|   -c, --console      run as console.
|   -d, --daemon       run as background daemon.
|   -s, --service      run as service.
|
|   -a, --all          load all modules.
|   -l, --level level  set loglevel.
|   -m, --mods m1,m2   modules to load.
|   -v, --verbose      enable verbose.
|   -w, --wait         wait for services to start.
|   -u, --user         use local mods directory.
|   -x, --admin        enable admin mode.
|   --wdr wdr          set working directory.
|
| use "nixt cmd" for a list of commands.
|

see list of commands

| ``$ nixt cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,log,mod,mre,nme,``
| ``pwd,rem,req,res,rss,srv,syn,tdo,thr,upt``
|

start console

| ``$ nixt -c``
|

start console and run irc and rss clients

| ``$ nixt -c mods=irc,rss``
|

list available modules

| ``$ nixt mod``
| ``err,flt,fnd,irc,llm,log,mbx,mdl,mod,req,rss,``
| ``rst,slg,tdo,thr,tmr,udp,upt``
|

start daemon

| ``$ nixt -d``
| ``$``
|

start service

| ``$ nixt -s``
| ``<runs until ctrl-c>``
|


**COMMANDS**


here is a list of available commands

| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``log`` - log text
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``tdo`` - add todo item
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**CONFIGURATION**


irc

| ``$ nixt cfg irc server=<server>``
| ``$ nixt cfg irc hannel=<channel>``
| ``$ nixt cfg irc nick=<nick>``
|

sasl

| ``$ nixt pwd <nsnick> <nspass>``
| ``$ nixt cfg irc password=<frompwd>``
|

rss

| ``$ nixt rss <url>``
| ``$ nixt dpl <url> <item1,item2>``
| ``$ nixt rem <url>``
| ``$ nixt nme <url> <name>``
|

opml

| ``$ nixt exp``
| ``$ nixt imp <filename>``
|


**PROGRAMMING**

| nixt has it's user modules in the ~/.nixt/mods directory so for a
| hello world command you would  edit a file in ~/.nixt/mods/hello.py
| and add the following
|

::

    def hello(event):
        event.reply("hello world !!")


|
| typing the hello command would result into a nice hello world !!
|

::

    $ nixt hello
    hello world !!


|
| commands run in their own thread and the program borks on exit to enable a
| short debug cycle, output gets flushed on print so exceptions appear in the
| systemd logs. modules can contain your own written python3 code.
|


**FILES**

|
| ``~/.nixt``
| ``~/.local/bin/nixt``
| ``~/.local/share/pipx/venvs/nixt/*``
|

**AUTHOR**

|
| ``Nixt Niet`` <``nietniet@gmail.com``>
|

**COPYRIGHT**

|
| ``NIXT`` is Public Domain.
|
