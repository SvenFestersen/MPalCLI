# MPalCLI

This Python script provides a simple command-line interface to the
Freecom MusicPal Internet Radio.


## Configuration

Before you can control your MusicPal from the command-line, you have to
configure the script (set the MusicPal's ip address, your username and
password):

    mpal.py ip <musicpalIP>
    mpal.py username <username>
    mpal.py password <password>

Username and password are the same as you use for the MusicPal's web
interface.


## Usage

If invoked without parameters, mpal.py will display a short status
overview.

The following list shows the supported functions. Parameters in square
brackets \[\] are optional.
    
Turn on the MusicPal:
    mpal.py on
    
Turn off the MusicPal:
    mpal.py off
    
Play a stream given by <url>:
    mpal.py play <url>
    
Play/pause playback:
    mpal.py playpause
    
Stop playback:
    mpal.py stop
    
Set volume:
    mpal.py volume [<value>]
If &lt;value&gt; is omitted, this hows the current volume. <value> has to be
an integer in range [0, 100]. The given value is rounded to multiples
of five.
An alternative to set the volume is
    mpal.py volume set <value>
    
Play a favorite station:
    mpal.py fav [<id>]
If &lt;id&gt; is omitted, this prints a list of the favorite stations with
ids.
An alternative to play a favorite station is
    mpal.py fav play <id>
    
