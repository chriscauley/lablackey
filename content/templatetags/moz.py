from django import template

register = template.Library()

@register.filter(name='m')
def m(value):
    return "%s\n    %s"%(value,value.replace("-webkit-","-moz-"))

@register.tag(name='moz')
def moz(parser, token):
    nodelist = parser.parse(('endmoz',))
    parser.delete_first_token()
    return MozNode(nodelist)

class MozNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        return output+"\n"+output.replace("-webkit-","-moz-")
