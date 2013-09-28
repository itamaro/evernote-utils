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
