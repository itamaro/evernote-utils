import os
from string import Template
from subprocess import call
from time import strftime, sleep, gmtime, mktime

from locator import module_path
g_BaseDir = os.path.normpath(os.path.join(module_path(), '..'))
g_TmplDir = os.path.join(g_BaseDir, 'Templates')
g_QuickNoteDir = os.path.join(g_BaseDir, 'QuickNotes')
g_AhkDir = os.path.join(g_BaseDir, 'AHK')

when_mapping = ['', 'Now', 'Next', 'Soon', 'Later', 'Someday', 'WaitingFor']
action_contexts = frozenset(('@Agenda', '@Computer', '@Home', '@Office',
                             '@Online', '@Out', '@Phone', '@Wherever'))
g_FixMeTag = '~FIXME' # Tag to use in case of unmatched action context
g_DefaultReminderTime = (9, 0, 0) # 9am (H, M, S)
g_OpenNoteCmd = [os.path.join(g_AhkDir, 'OpenNote.exe')]
g_DryRun = False

# Invoke the ENScript.exe Evernote program (modify path if needed)
def call_enscript(args):
    cmd = ['ENScript.exe']
    cmd.extend(args)
    if g_DryRun:
        print cmd
    else:
        call(cmd)

# Applies template-parameters to template-file
# Creates an output file with applied template
def apply_template(template_file_path, tmpl_params,
            out_file_path=os.path.join(g_TmplDir, u'tmpENImport.enex')):
    # Read the content of the file as a template string
    with open(args.template, 'r') as tmpl_file:
        tmpl_str = Template(tmpl_file.read())
    # Apply the template and save to the output file
    out_string = tmpl_str.safe_substitute(tmpl_params)
    if g_DryRun:
        print 'Will write to file "%s"' % (out_file_path)
        print out_string
    else:
        with open(out_file_path, 'w') as f:
            f.write(out_string)
    return out_file_path

# Uses AutoHotKey (compiled script) to open the first note that matches
# the specified query in a separate window
# FIXME: Doesn't work reliably... Not sure why.
#        Sometimes the query takes too long so a wrong note is opened...
def open_first_note(query):
    call_enscript(['showNotes', '/q', query])
    sleep(0.1)
    if g_DryRun:
        print g_OpenNoteCmd
    else:
        call(g_OpenNoteCmd)

# Takes an action-context hint and returns a matching action-context tag
# Action-context tags are defined by the `action_contexts` frozenset.
# The hint is a case-insensitive partial action-context name
#  (with or without prefixing "@").
# In case of multiple matches - the first hit is returned.
def deduce_context(hint):
    # Read hint from user if not supplied.
    if not hint:
        hint = raw_input('Enter action context (@..): ').strip()
    # Ignore case.
    hint = hint.lower()
    # Add "@" if omitted.
    if not hint.startswith('@'):
        hint = '@%s' % (hint)
    for context in action_contexts:
        if context.lower().startswith(hint):
            # Match. Return tag.
            return context
    # No match. Boo. Return FIXME tag.
    print 'Invalid context :-(', 'Tagging with ~FIXME'
    return g_FixMeTag

# Support arguments-overriding based on special syntax in action title
# (see README)
def extract_args_from_title(args):
    title_args = {
        'tickle': 'reminder',
        'reminder': 'reminder',
        'notebook': 'notebook',
        'project': 'notebook',
        }
    keep_going = True
    while keep_going:
        # stop iterating after first time that no title-arg is found
        keep_going = False
        args.action_title = args.action_title.strip()
        for prefix, dest_arg in title_args.iteritems():
            arg_pref = '/%s:' % (prefix)
            if args.action_title.startswith(arg_pref):
                arg_start = len(arg_pref)
                arg_end = args.action_title.find('/', arg_start)
                # extract the content of the arg from the title
                arg_content = args.action_title[arg_start:arg_end]
                # remove entire arg-spec from the title
                args.action_title = args.action_title[arg_end+2:]
                # update argument value
                setattr(args, dest_arg, arg_content)
                # do another round
                keep_going = True
                break

# Create and import an action-note, optionally opening it in a separate window
def action_note(args):
    # Get action title (from arguments, or ask users if no argument supplied)
    args.action_title = args.action_title or    \
                        raw_input('Enter action title: ').strip()
    # Extract title-args that override command-line args
    extract_args_from_title(args)
    # Deduce when-context from title or argument (if supplied), or ask user
    if args.action_title[0] in '123456':
        when_prefix = args.action_title[0]
        # remove the prefix from the title
        args.action_title = ' '.join(args.action_title.split()[1:])
    else:
        when_prefix = args.when or raw_input(
                      'Enter action when context (single digit): ').strip()
    if args.when and when_prefix <> args.when:
        # inconsistency! Go with the title..
        print 'Detected when-context inconsistency. Choosing', when_prefix
    if not when_prefix in '123456':
        raise RuntimeError('I don\'t like you (not in range 1..6)')
    # Get action context (from arguments, or ask user if not supplied).
    context = deduce_context(args.context)
    # Process reminder, if specified
    if args.reminder:
        import parsedatetime.parsedatetime as pdt
        cal = pdt.Calendar(pdt.Constants('he_IL', True))
        res_date, res_flag = cal.parse(args.reminder)
        if 1 == res_flag:
            # parsed as date - so use 9am as default time
            res_date = res_date[:3] + g_DefaultReminderTime + res_date[6:]
        if 0 == res_flag:
            # Not parsed at all
            print 'Failed parsing reminder date/time'
            args.action_title = 'FIX REMINDER %s' % (args.action_title)
            args.reminder = None
        else:
            # Convert reminder date/time object to UTC datetime string
            args.reminder = strftime('%Y%m%dT%H%M00Z',
                                     gmtime(mktime(res_date)))
    
    # Prepare template dictionary
    tmpl_params = {
        'WhenPrefix': when_prefix,
        'ActionTitle': args.action_title,
        'WhenContext': '%s-%s' % (when_prefix, when_mapping[int(when_prefix)]),
        'ActionContext': context,
        'Reminder': args.reminder and '<note-attributes>'  \
                '<reminder-order>%s</reminder-order>'  \
                '<reminder-time>%s</reminder-time>' \
                '<reminder-done-time>00001231T000000Z</reminder-done-time>' \
                '</note-attributes>' %  \
                (strftime('%Y%m%dT%H%M%SZ', gmtime()), args.reminder) or ''
        }
    
    # Apply template
    import_file_path = apply_template(args.template, tmpl_params)
    
    timestr = strftime('%Y%m%dT%H%M00')
    # Import the note to Evernote
    # (into specific notebook if supplied, or default one otherwise)
    call_args = ['importNotes', '/s', import_file_path]
    if args.notebook:
        call_args.append('/n')
        call_args.append(args.notebook)
    call_enscript(call_args)
    
    # Open the note in a separate window after importing (if flagged to do so)
    if args.open_note:
        open_first_note('created:%s tag:.Action' % (timestr))

# Create a new project-notebook in active stack and import new-project notes
def project_notes(args):
    if not args.notebook:
        raise RuntimeError('Notebook parameter not optional for this command')
    
    # Prepare template dictionary
    tmpl_params = {
        'ProjName': args.notebook,
        }
    
    # Apply template
    import_file_path = apply_template(args.template, tmpl_params)
    
    timestr = strftime('%Y%m%dT%H%M00')
    # Import template into Evernote
    call_enscript(['importNotes', '/s', import_file_path,
                   '/n', args.notebook])
           
    # Open the first note in a separate window after importing (if flagged to)
    if args.open_note:
        open_first_note('notebook:"%s"' % (args.notebook))

# Generate batch files for quick-note creation for supported action-contexts
def batch_generation(args):
    if not args.notebook:
        raise RuntimeError('Notebook parameter not optional for this command')
    
    for context in action_contexts:
        # Prepare template dictionary
        tmpl_params = {
            'DefaultActionNotebook': args.notebook,
            'ActionContext': context,
            }
        # Apply template to create batch script in target directory
        batch_file_path = os.path.join(args.parent_dir,
                                       '%s.bat' % (context.lower()))
        apply_template(args.template, tmpl_params, batch_file_path)
    

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description='Evernote note creator.')
    parser.add_argument('-n', '--notebook',
                        help='Evernote notebook to import into')
    parser.add_argument('-o', '--open-note', action='store_true',
                        help='Open the imported note in as separate window')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Enables dry-run mode - '
                             'print the commands without executing them')
    subparsers = parser.add_subparsers()
    # Add note-action subcommand
    parser_action = subparsers.add_parser('action',
                               help='Create a new note-action')
    parser_action.add_argument('-t', '--template',
                  default=os.path.join(g_TmplDir, 'NewAction.enex.tmpl'),
                  help='Path to the new action template file')
    parser_action.add_argument('-a', '--action-title',
                               help='Action title')
    parser_action.add_argument('-w', '--when',
                               help='When context for action (single digit)')
    parser_action.add_argument('-c', '--context',
                               help='Action context for action (@...)')
    parser_action.add_argument('-r', '--reminder',
                               help='Set reminder to note-action')
    parser_action.set_defaults(func=action_note)
    # Add project-creation subcommand
    parser_project = subparsers.add_parser('project',
               help='Import project template notes to new project notebook')
    parser_project.add_argument('-t', '--template',
                      default=os.path.join(g_TmplDir, 'NewProject.enex.tmpl'),
                      help='Path to the new project template file')
    parser_project.set_defaults(func=project_notes)
    # Add quick-action batch scripts creation subcommand
    parser_batchgen = subparsers.add_parser('batch-gen',
                help='Generate batch scripts for quick-action creation')
    parser_batchgen.add_argument('-t', '--template',
                      default=os.path.join(g_TmplDir, 'QuickAction.bat.tmpl'),
                      help='Path to the quick note batch script template')
    parser_batchgen.add_argument('-p', '--parent-dir', default=g_QuickNoteDir,
                        help='Parent directory for generated batch files')
    parser_batchgen.set_defaults(func=batch_generation)
    
    args = parser.parse_args()
    g_DryRun = args.dry_run
    args.func(args)
