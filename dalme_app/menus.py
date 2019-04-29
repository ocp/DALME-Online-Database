from django.urls import reverse
import json, os
from . import functions
from dalme_app.models import *

def menu_constructor(request, item_constructor, template, state):
    """
    Builds menus based on an item_constructor and a json file describing the menu items.
    Menus are stored in the templates directory, under the menus subdirectory.
    """
    user_id = request.user.id
    _output = ''
    template = os.path.join('dalme_app','templates','menus',template)
    with open(template, 'r') as fp:
        menu = json.load(fp)
    for item in menu:
        if 'permissions' in item:
            if functions.check_group(request, item['permissions']):
                _output += eval(item_constructor + '(_output,state,**item)')
        else:
            _output += eval(item_constructor + '(_output,state,**item)')
    if item_constructor == 'dropdown_item':
        _output = dropdown_tasks(_output, user_id)
    return [_output]

def sidebar_item(wholeMenu,state,depth=0,text=None,iconClass=None,link=None,counter=None,section=None,children=None,divider=None, itemClass=None, blank=None, permissions=None):
    """ creates menu items for the sidebar """
    if section:
        currentItem = '<div class="sidebar-heading">{}</div><hr class="sidebar-divider">'.format(text)
    elif divider:
        currentItem = '<hr class="sidebar-divider">'
    else:
        if text in state['breadcrumb']:
            currentItem = '<li class="nav-item active">'
        else:
            currentItem = '<li class="nav-item">'
        if children:
            currentItem += '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" aria-controls="collapse{}">'.format(itemClass, itemClass)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a>'.format(text)
            if text in state['breadcrumb'] and state['sidebar'] != 'toggled':
                currentItem += '<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            else:
                currentItem += '<div id="collapse{}" class="collapse" aria-labelledby="heading{}" data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            currentItem += '<div class="bg-white py-2 collapse-inner rounded">'
            for child in children:
                if 'section' in child:
                    currentItem += '<div class="sidebar-menu-heading">{}</div>'.format(child['text'])
                else:
                    currentItem += '<a class="collapse-item'
                    if child['text'] in state['breadcrumb']:
                        currentItem += ' active'
                    currentItem += '" href="{}"'.format(child['link'])
                    if 'blank' in child:
                        currentItem += ' target="_blank"'
                    currentItem += '><i class="fas fa-fw {}"></i> {}</a>'.format(child['iconClass'], child['text'])
            currentItem += '</div></div></li>'
        else:
            currentItem += '<a class="nav-link" href="{}">'.format(link)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a></li>'.format(text)
    return currentItem

def tile_item(wholeMenu,state,colourClass=None,iconClass=None,counter=None,counterTitle=None,linkTarget=None,linkTitle=None, permissions=None):
    """ creates tiles for the dashboard homepage """
    try:
        counter = functions.get_count(counter)
    except:
        counter = 'n/a'
    currentItem = '<div class="col-xl-3 col-sm-6 mb-3">'
    currentItem += '<div class="card shadow text-dark-grey bg-{}-soft o-hidden h-100"><div class="card-body">'.format(colourClass)
    currentItem += '<div class="card-body-icon"><i class="fas {} fa-comments"></i></div>'.format(iconClass)
    currentItem += '<div class="mr-5"><b>{}</b> {}</div></div>'.format(counter, counterTitle)
    currentItem += '<a class="card-footer text-dark-grey clearfix small z-1" href="{}">'.format(linkTarget)
    currentItem += '<span class="float-left">{}</span>'.format(linkTitle)
    currentItem += '<span class="float-right"><i class="fas fa-angle-right"></i></span></a></div></div>'
    return currentItem

def dropdown_item(wholeMenu,state,topMenu=None,infoPanel=None,title=None,itemClass=None,iconClass=None,childrenIconClass=None,children=None,text=None,link=None,divider=None,section=None,counter=None,circleColour=None,moreText=None,moreLink=None,permissions=None, tooltip=None):
    """ creates items for the top right dropdowns """
    if link:
        currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left">'
        currentItem += '<a class="nav-link dropdown-toggle" href="{}" id="{}button" role="button" data-toggle="tooltip" data-placement="bottom" title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(link, itemClass, tooltip)
        currentItem += '<i class="fas {} fa-g"></i></a>'.format(iconClass)
    else:
        currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(tooltip)
        currentItem += '<a class="nav-link dropdown-toggle" href="#" id="{}Dropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'.format(itemClass)
        currentItem += '<i class="fas {} fa-g"></i>'.format(iconClass)
        currentItem += '</a><div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="{}Dropdown">'.format(itemClass)
        for child in children:
            if divider:
                currentItem += '<div class="dropdown-divider"></div>'
            else:
                currentItem += '<a class="dropdown-item" href="{}">'.format(child['link'])
                if 'iconClass' in child:
                    currentItem += '<i class="fas {} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(child['iconClass'], child['text'])
                else:
                    currentItem += '<i class="fas {} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(childrenIconClass, child['text'])
        currentItem += '</div></li> '
    return currentItem

def dropdown_tasks(wholeMenu, user_id):
    button = ''
    dropmenu = ''
    overdue = False
    counter = False
    try:
        tasks = Task.objects.filter(assigned_to=user_id, completed=0)
        counter = tasks.count()
        tasks = tasks[:5]
        for task in tasks:
            dropmenu += '<div class="dropdown-tasks-item d-flex"><div class="dropdown-tasks-info"><a href="/tasks/{}">'.format(task.id)
            dropmenu += '<div class="mb-1">{}</div><div class="d-flex"><div class="dropdown-tasks-list float-left">{}</div>'.format(task.title, task.task_list)
            if task.due_date:
                if task.overdue_status():
                    overdue = True
                    dropmenu += '<div class="dropdown-tasks-overdue float-right">Due: {}</div>'.format(task.due_date)
                else:
                    dropmenu += '<div class="dropdown-tasks-due float-right">Due: {}</div>'.format(task.due_date)
            dropmenu += '</div></div></a><div class="dropdown-tasks-buttons"><a class="btn dropdown-tasks-btn dropdown-tasks-btn-bb" href=""><i class="fa fa-pen fa-fw"></i></a><a class="btn dropdown-tasks-btn" href="{% url "todo:task_toggle_done" task.id %}"><i class="fa fa-check fa-fw"></i></a></div></div>'
    except:
        dropmenu += '<div class="dropdown-tasks-empty">No tasks are currently assigned to you.</div>'
    dropmenu += '<a class="dropdown-tasks-action dropdown-tasks-action-rb" href="{}">{}</a>'.format('/tasks/mine', 'Show all my tasks')
    dropmenu += '<a class="dropdown-tasks-action" href="#" onclick="{}">{}</a></div></li>'.format('createTask()', 'Add new task')
    button = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" title="Your task list" data-delay=\'{"show":"1000", "hide":"0"}\'>'
    button += '<a class="nav-link dropdown-toggle" href="#" id="tasksDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    button += '<i class="fas fa-tasks fa-fw"></i>'
    if counter:
        if overdue:
            button += '<span class="badge topbar-badge-alert">{}</span>'.format(counter)
        else:
            button += '<span class="badge topbar-badge">{}</span>'.format(counter)
    button += '</a><div class="dropdown-tasks dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="tasksDropdown">'
    button += '<div class="dropdown-tasks-header">Your Tasks</div>'
    wholeMenu += button
    wholeMenu += dropmenu
    return wholeMenu
