evernote-utils
==============

A collection of productivity-enhancing utilities for Evernote for Windows.

Developed for and tested with Evernote 5.0 on Windows 7.

Supported Use Cases
-------------------

Disclaimer: The implementation is tightly coupled to my broader Evernote-based GTD organizational system (TODO: link to description of my system).
It is meant to enhance **my own** productivity and efficiency using my system, which means some personalized behaviours within the code.
It should quite easy to modify my scripts to suit your needs, and anyone is encouraged to do so!

### Quick creation of a new "action-note" with Launchy

A fast way to create a new Evernote "action-note", no matter what's the active application, or whether Evernote application is open.

Call Launchy (Alt+Space) and start typing the "@action-context":
![Launchy dialog](docs/action-note-1-type-on.png)

Once Launchy recognizes the context, hit "Tab" and type the note title:
![Launchy note title](docs/action-note-2-type-action.png)

Then hit "Enter" - a new note will be created in a pre-determined notebook, tagged automatically based on the chosen action context and title syntax, and opened in a separate window ready for further editing (or closing):
![Note in Evernote](docs/action-note-3-note-created.png)


#### Specifying a different notebook in the title

The quick-note-creation script supports special syntax in the title for overriding default parameters, like the destination notebook for the new note.

By prefixing the note title with `/notebook:Target Notebook Name/` or `/project:Project-specific Notebook Name/`:
![Launchy override notebook](docs/action-note-4-notebook-override.png)

The note will be created directly in the specified notebook:
![Note in Evernote](docs/action-note-5-notebook-overriden.png)

In case such a notebook does not exist, it will be created.
(note: I plan to implement a different behaviour: the script will try choosing an existing notebook that "looks like" the name specified)


#### Setting a reminder from the title

Similarly, it is also possible to prefix the note title with `/reminder:oct 3/` or `/tickle:next sunday, 10am/` in order to create a note with a reminder associated to it.

When specifying only a date:
![Launchy specify reminder date](docs/action-note-6-specify-reminder-date.png)

The note will be created with a reminder set to that date at 9am (can be modified [in the code](PyEvernote/ImportEvernoteTemplate.py#L16)):
![Note in Evernote](docs/action-note-7-reminder-date.png)
![Reminder details](docs/action-note-8-reminder-date-time.png)

When specifying also a time:
![Launchy specify reminder date & time](docs/action-note-9-specify-reminder-datetime.png)

The reminder will be set to that time as well:
![Reminder details](docs/action-note-10-reminder-date-time.png)

The script supports natural language date-time specification using [parsedatetime Python library](https://github.com/bear/parsedatetime),
so this is a dependency (install with `pip install parsedatetime`).

Note: The reminder time is calculated based on the current timezone.

In case the script was unable to parse the date, it will not set a reminder, but will prepend the note title with "FIX REMINDER" so you can see it was unable to set a reminder.


### Initialization of a new project in Evernote with Launchy or using a keyboard shortcut

Automate the process of initializing a new project in Evernote, where "project initialization" in my system includes:

1. Creating a project-specific notebook in a notebook stack.
2. Creating initial project notes in the new project notebook, based on a template.

Simply highlight in Evernote the target notebook-stack for the new project-notebook:
![Evernote notebook stack](docs/project-1-Evernote.png)

Call Launchy (Alt+Space) and start typing "enproject":
![Launchy enproject](docs/project-2-Launchy-enp.png)

Hit "Tab" and type the name of the new project (which will also be the name of the project-specific notebook):
![Launchy new project](docs/project-3-Launchy-project.png)

Hie "Enter", and behold the initialized project in the selected stack!
![Initialized Evernote project notebook and notes](docs/project-4-Evernote-Notebook.png)

Alternatively, using [AutoHotKey](http://www.autohotkey.com/), you can bind a keyboard shortcut (e.g. "Ctrl+Alt+p", or "^!p") to the ["CreateProject.exe" executable](AHK) (which is a compiled version of the [AutoHotKey script](AHK/CreateProject.ahk) to achieve something similar with AHK instead of Launchy.

Using the AHK method, you will type the project name in a popup dialog instead of the Launchy dialog:
![AHK Project name dialog](docs/project-5-AHK-Dialog.png)

This, ofcourse, requires that AutoHotKey is installed, and a keyboard shortcut is defined like this:

```AutoHotkey
#IfWinActive ahk_class ENMainFrame
	^!p::
		Run,"<package-dir>\AHK\CreateProject.exe"
#IfWinActive
```
 

Installation
------------

Requirements:

1. Windows
2. Evernote >= 5.0
3. Python 2.7
4. [parsedatetime Python library](https://github.com/bear/parsedatetime)
5. [Launchy](http://www.launchy.net/) (this probably works with other keyboard launchers, but the details will differ)

Steps:

1. [Download the package](https://github.com/itamaro/evernote-utils/archive/master.zip) (or [clone it](https://github.com/itamaro/evernote-utils.git)), and save it wherever you'd like on your computer (let's call that <package-dir>).
2. Modify the scripts to fit your workflow and system (change default notebooks, tags, action contexts, note templates).
3. Configure Launchy to index batch script files from the [QuickNotes](QuickNotes) directory under <package-dir>:
![Launchy options](docs/Launchy-configure.png)
![Configure Launchy catalog](docs/Launchy-configure-catalog.png)
4. Click "Rescan Catalog" and "OK" to finish the process

That's it!


Customization
-------------

TODO
