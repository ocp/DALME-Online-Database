from dalme_app import functions
from django.core.urlresolvers import reverse
from todo.models import Item, List, Comment
from django.contrib.auth.models import User
import json
import os



def sidebar_menu(template='sidebar_default.json'):
    """Creates the sidebar menu based on a json file describing the menu items.
    Menus are stored in the templates directory, under the menus subdirectory.

    Menu items may have the following properties:
    text: Text to be shown in menu item.
    iconClass: Class for Font Awesome icon.
    section: If the menu item is a section marker, set this property to True.
    link: Link for menu item
    counter: Add a count of some kind to menu items. The value of this key will
        be passed to the `functions.get_count()` function, and the return value
        of that function will appear as the count.
    children: Nest additional menu items as a list under this key.

    All properties default to `None`, so if you don't want to include any
    element, just leave out that key."""
    template = os.path.join('dalme','dalme_app','templates','menus',template)
    with open(template, 'r') as fp:
        menu = json.load(fp)

    _output = ''

    for item in menu:
        _output += sidebar_menu_item(_output,**item)

    return [_output]

LEVEL_LOOKUP = ['nav-second-level', 'nav-third-level', 'nav-fourth-level', 'nav-fifth-level']
def sidebar_menu_item(wholeMenu,depth=0,text=None,iconClass=None,link=None,counter=None,children=None,section=None):
    currentItem = '<li '
    if section and wholeMenu == '':
        currentItem += 'class="sidebar-section-first"'
    elif section:
        currentItem += 'class="sidebar-section"'
    currentItem += '>'
    if link:
        currentItem += '<a href="{}">'.format(link)
    if iconClass:
        currentItem += '<i class="fa {} fa-fw"></i> '.format(iconClass)
    if text:
        currentItem += text
    if counter:
        counter = functions.get_count(counter)
        currentItem += '<div class="menu-counter">{}</div>'.format(counter)
    if children:
        currentItem += '<span class="fa arrow"></span>'
    if link:
        currentItem += '</a>'
    if children:
        try:
            currentItem += '<ul class="nav {}">'.format(LEVEL_LOOKUP[depth])
        except IndexError:
            print(depth)
            currentItem += '<ul class="nav">'
        for child in children:
            currentItem += sidebar_menu_item(currentItem,depth=depth+1,**child)
        currentItem += '</ul>'
    currentItem += '</li>'

    return currentItem


def dropdowns(username):
    """ creates the top right dropdowns """
    logout = 'Logout ' + username

    dropdowns = [
        ['fa fa-tasks', 'dropdown-task-list', [
                ['1', reverse('todo-lists'), 'fa fa-plus-circle', 'Add New Task'],
                ['divider'],
                ['1', reverse('todo-lists'), 'fa fa-info-circle', 'Manage Task Lists'],
                ['1', reverse('todo-lists'), 'fa fa-check-circle', 'View Tasks Log'],
                ['divider'],
                ['0', '#', 'fa fa-star', 'My Tasks:'],
            ]

        ],
        ['fa fa-gears', 'dropdown-dev', [
                ['1', '/dashboard/list/errors', 'fa fa-medkit', 'Error codes'],
                ['divider'],
                ['0', '#', 'fa fa-list-alt', 'UI Reference:'],
                ['1', '/dashboard/UIref/dash_demo', 'fa fa-dot-circle-o', 'Dashboard Content'],
                ['1', '/dashboard/UIref/panels-wells', 'fa fa-dot-circle-o', 'Panels and Wells'],
                ['1', '/dashboard/UIref/buttons', 'fa fa-dot-circle-o', 'Buttons'],
                ['1', '/dashboard/UIref/notifications', 'fa fa-dot-circle-o', 'Notifications'],
                ['1', '/dashboard/UIref/typography', 'fa fa-dot-circle-o', 'Typography'],
                ['1', '/dashboard/UIref/icons', 'fa fa-dot-circle-o', 'Icons'],
                ['1', '/dashboard/UIref/grid', 'fa fa-dot-circle-o', 'Grid'],
                ['1', '/dashboard/UIref/tables', 'fa fa-dot-circle-o', 'Tables'],
                ['1', '/dashboard/UIref/flot', 'fa fa-dot-circle-o', 'Flot Charts'],
                ['1', '/dashboard/UIref/morris', 'fa fa-dot-circle-o', 'Morris.js Charts'],
                ['1', '/dashboard/UIref/forms', 'fa fa-dot-circle-o', 'Forms'],
            ]
        ],
        ['fa fa-user', 'dropdown-user', [
                ['1', '#', 'fa fa-user', 'Profile'],
                ['1', '#', 'fa fa-gear', 'Settings'],
                ['divider'],
                ['1', '/logout/', 'fa fa-sign-out', logout],
            ]
        ],
    ]

    user_id = User.objects.get(username=username).pk
    tasks = Item.objects.filter(assigned_to=user_id, completed=False).order_by('-created_date')[:5]
    for i in tasks:
        task_icon = functions.get_task_icon(i.list_id)
        task_url = '/dashboard/tasks/task/' + str(i.id)
        creator_id = i.created_by_id
        task_creator = User.objects.get(id=creator_id).username
        date_created = i.created_date.strftime('%a, %-d %b, %Y')
        date_due = i.due_date.strftime('%a, %-d %b, %Y')
        task_item = ['2', task_url, task_icon, i.title, str(i.id), date_created, date_due, task_creator]
        dropdowns[0][2].append(task_item)

    close_tasks = ['3', reverse('todo-mine'), 'See All']
    dropdowns[0][2].append(close_tasks)

    results = []
    _output = ''

    for item in dropdowns:
        if item[0] == 'fa-tasks':
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '"><form action="" method="POST">'

        else:
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '">'

        for menu in item[2]:
            if menu[0] == 'divider':
                _output = _output + '<li class="divider"></li>'

            elif menu[0] == '0':
                _output = _output + '<li class="dropdown-section"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</li>'

            elif menu[0] == '1':
                _output = _output + '<li><a href="' + menu[1] + '"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</a></li>'

            elif menu[0] == '2':
                _output = _output + '<li><a href="' + menu[1] + '"><div><input class="dropdown-checkbox" type="checkbox" name="mark_done" value="' + menu[4]+ '" id="mark_done_' + menu[4] + '">' + menu[3] + '<span class="pull-right text-muted"><em>Due: ' + menu[6] + '</em></span></div><div><em>Created: ' + menu[5] + ' By: ' + menu[7] + '</em></div></a></li>'

            elif menu[0] == '3':
                _output = _output + '<li class="divider"></li><li><a class="text-center" href="' + menu[1] + '"><strong>' + menu[2] + ' </strong><i class="fa fa-angle-right"></i></a></li>'


        if dropdowns[0][0] == 'fa fa-tasks':
            _output = _output + '</form></ul></li>'
        else:
            _output = _output + '</ul></li>'

        results.append(_output)

    return results
