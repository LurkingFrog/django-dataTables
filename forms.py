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

    def add_data(self):
        new_row = SortedDict()
        for column in self.columns:
            if hasattr(column, 'default'):
                new_row[column.label] = column.default
            else:
                new_row[column.label] = ''

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
            context['aaData'].append(
                [unicode(x) for x in row.values()]
            )

        context['buttons'] = [x.dump for x in self.buttons]

        return simplejson.dumps(context)


class DTColumn(object):
    """
    This is a column in the data table
    """

    def __init__(self, label):
        self.label = label
        
        # TODO: Add filter options
        # TODO: Add formatting options
        # TODO: Add link options


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
