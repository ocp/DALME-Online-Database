"""Interface for the public.wagtail_hooks module."""

from wagtail import hooks

from .admin_extra_css_js import extra_admin_css, extra_admin_js
from .extra_icons import register_extra_icons
from .hide_users_menu import hide_users_menu
from .redirects_before_serving import add_redirects_before_serving_pages
from .rich_text_features import enable_rich_text_features

hooks.register('construct_settings_menu', hide_users_menu)
hooks.register('insert_global_admin_css', extra_admin_css, order=0)
hooks.register('insert_global_admin_js', extra_admin_js)
hooks.register('before_serve_page', add_redirects_before_serving_pages)
hooks.register('register_rich_text_features', enable_rich_text_features)
hooks.register('register_icons', register_extra_icons)
