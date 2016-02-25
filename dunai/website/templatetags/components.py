from django.template import Library, Context, loader
from django.shortcuts import render
from django.template import TemplateDoesNotExist
# from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe

register = Library()

WRAP = u'<!-- COMPONENT {name} -->\n{content}\n<!-- END COMPONENT {name} -->\n'


class ComponentError(Exception):
    pass


def get_component(name):
    try:
        tpl = loader.get_template('dunai/parts/{}.jade'.format(name))
    except TemplateDoesNotExist, e:
        raise ComponentError('Component "{}" not found.'.format(name))
    return tpl


@register.simple_tag(takes_context=False)
def component(name, **kwargs):
    # if name == 'button':
    #     context = dict(
    #         href='#',
    #         onclick=None,
    #         content='Button'
    #     )
    #     context.update(kwargs)
    #
    #     if not context.get('onclick') and context.get('href') == '#':
    #         context['onclick'] = 'return false;'
    # else:
    context = dict(kwargs)

    # Expose some settings
    # context.update(expose_settings(None))
    context['component_name'] = name

    return mark_safe(WRAP.format(
        name=name,
        content=get_component(name).render(Context(context))
    ))


@register.simple_tag(takes_context=True)
def param(context, name, **kwargs):
    component_name = context['component_name']

    if name not in context:
        raise ComponentError('Component "{}": missing argument "{}".'.format(component_name, name))

    value = context[name]

    if 'type' in kwargs:
        type_name = type(value).__name__
        if type_name.lower() != kwargs['type']:
            raise ComponentError('Component "{}": argument "{}" must be of type "{}", got "{}".'.format(
                component_name, name, kwargs['type'], type_name
            ))

    return ''
