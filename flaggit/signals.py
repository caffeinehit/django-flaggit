from django.dispatch.dispatcher import Signal

flagged = Signal(providing_args=['flag', 'created'])
review = Signal(providing_args=['flag'])
rejected = Signal(providing_args=['flag'])
approved = Signal(providing_args=['flag'])
