from django.db.models.query import QuerySet


def object_to_json(model, ignore=None):
    if ignore is None:
        ignore = []
    if type(model) in [QuerySet, list]:
        json = []
        for element in model:
            json.append(_django_single_object_to_json(element, ignore))
        return json
    else:
        return _django_single_object_to_json(model, ignore)


def _django_single_object_to_json(element, ignore=None):
    return dict([(attr, getattr(element, attr)) for attr in [f.name for f in element._meta.fields if f not in ignore]])