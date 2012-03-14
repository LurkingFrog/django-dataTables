from django import template

register = template.Library()

class DataTableNode(template.Node):
    def __init__(self, form_class):
        self.form_class = form_class

    def render(self, context):
        t = template.loader.get_template('datatables/dataTable.html')
        context.update({'table_name': self.form_class})
        return t.render(context)


@register.tag
def add_datatable(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, form_class = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError(
            '{0} tag requires a single argument'
            .format(token.contents.split()[0])
        )

    try:
        return DataTableNode(form_class)

    except Exception as ex:
        raise template.TemplateSyntaxError(
            '{0} did not render properly'
            .format(token.contents.split()[0])
        )



