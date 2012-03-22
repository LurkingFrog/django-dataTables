from copy import deepcopy

from django.utils.datastructures import SortedDict

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils import simplejson


__all__ = [
    'JQueryDataTable',
    'DTColumn',
    'DTButton',
]

class JQueryDataTable(forms.Form):
    table_type = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(JQueryDataTable, self).__init__(*args, **kwargs)

        # Initialize attributes needed in advance due to inheritance
        self.display_data = list()
        self.columns = list()
        self.buttons = list()

        self.columns = [
            getattr(self, x) for x in dir(self)
              if isinstance(getattr(self, x), DTColumn)
        ]

        self.buttons = [
            getattr(self, x) for x in dir(self)
              if isinstance(getattr(self, x), DTButton)
        ]

        self.load_data()

    @staticmethod
    def get_datatable_form(*args, **kwargs):
        """
        This function should be used to instantiate the subclass. It
        assumes that the table_type is defined and has been submitted
        in the post data
        """

        # Magic method for fun
        # Finds the proper class based on the table_type field
        table_type = args[0].get('table_type', 'AgentsDataTable')
        classes = filter(
            lambda x: table_type == x.__name__,
            JQueryDataTable.__subclasses__()
        )

        if len(classes) == 1:
            return classes[0](*args, **kwargs)

        elif len(classes) == 0:
            raise ValueError("'{0}' Is not a valid class".format(table_type))

        else:
            raise ValueError(
                "'{0}' matched multiple records: {1}"
                .format(table_type, classes)
            )

    def add_data_row(self):
        new_row = SortedDict()
        for column in self.columns:
            new_row[column.label] = DTCell(
                value=column.default_value,
                cell_format=deepcopy(column.format)
            )

        self.display_data.append(new_row)
        return new_row
        

    def load_data(self):
        """
        This function is made to be explicitly overridden. This function
        is expected to return a list of dictionaries.

        The convention used is a SortedDict with the keys being the
        column names you wish displayed.
        """

        raise Exception(
            'load_data must be implemented and return a list of dictionaries'
        )

    @property
    def dumps(self):
        context = {
            "aaData": list(),
            "aoColumns": list(),
            "buttons": list()
        }
        
        context['aoColumns'] = [
            {'sTitle': x.label}
            for x in self.columns
        ]
        
        # TODO: There is going to be more formatting added here, but this
        # should work for now
        context['aaData'] = list()
        for row in self.display_data:
            row_data = list()
            for cell in row.values():
                row_data.append(cell.render())
    
            context['aaData'].append(row_data)

        context['buttons'] = [x.dump for x in self.buttons]

        return simplejson.dumps(context)


class DTColumn(object):
    """
    This is a column in the data table. See the FormatWidget for additional options

    * label: The column header that is displayed. Also used as the dictionary key
      used to reference this cell's data.
    * default: The default value that should be used to initialize the cell
    * link_url: this is the url you want the cell to link to. If left as the
        default (None), there will be no link
        
    """

    def __init__(
        self,
        label,
        default='',
        link_url=None,
        custom_render_string=None,
        custom_render_type=None,
    ):
        self.label = label
        self.default_value = default

        self.format =  DTColumnFormatWidget(
            custom_render_type=custom_render_type,
            custom_render_string=custom_render_string,
        )

            
        # TODO: Add Form options
        # TODO: Add filter options
        # TODO: Add formatting options
        # TODO: Add grand totals


class DTColumnFormatWidget(object):
    """
    Used for building what is displayed on the screen. It adds in custom
    formatting so the display can automatically use:
    
    *  Links
    *  Custom Rendering
    """

    def __init__(
        self,
        custom_render_type=None,
        custom_render_string=None,
    ):
        self.custom_render_type = custom_render_type
        self.custom_render_string = custom_render_string

        
class DTCell(object):
    """
    Each one of these is the final data in a cell that needs to be
    serialized and sent to the browser.

    * value: The sortable value.
    * display: this is what is actually shown to the end user

    * _rendered_value: This should not be set by the user, as it is as done
      automatically when the JSON is calculated
    """

    def __init__(
        self,
        value,
        cell_format,
        display=None,
        link_url=None,
        custom_render_context=dict()
    ):
        self.value = value
        self.display = display
        self.format = cell_format
        self.custom_render_context = custom_render_context
        self.format.link_url = link_url

    def render(self):
        # Turn the display into a simple link
        if self.format.link_url:
            return u'<a href="{url}">{value}</a>'.format(
                url=self.format.link_url,
                value=self.value
            )
        
        return unicode(self.value)

class DTButton(object):
    """
    A button to be displayed at the battom of the data table

    label: the text shown on the button
    action_type: what kind of action is performed when clicked
        JUMP_TO_VIEW (default)
        TODO: OPEN_DIALOG
    target_view: get the url of the target using reverse()  
    use_selected: Once the check boxes go in, how many items can be selected
        IGNORE (default)
        TODO: integer greater than zero
        
    """
    def __init__(
        self, 
        label,
        target_view,
        action_type='JUMP',
        use_selected='IGNORE'
    ):
        # TODO: Add in some validation for this
        self.label = label
        self.target_view = target_view
        self.action_type = action_type
        self.use_selected = use_selected

    @property
    def dump(self):
        """
        Grab the values needed by the javascript to build a button and 
        return it in a dict
        """
        return {
            'label': self.label,
            'target': self.target_view,
            'action': self.action_type
        }



    
