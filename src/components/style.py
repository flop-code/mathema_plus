import hyperdiv as hd


def _custom_classes(component: hd.Component, *new_classes: str) -> hd.Component:
    component._classes.extend(new_classes)
    return component


def underlined(component: hd.Component) -> hd.Component:
    return _custom_classes(component, "underlined")
