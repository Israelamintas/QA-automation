def pytest_addoption(parser):
    parser.addoption(
        "--tcid",
        action="store",
        default=None,
        help="Run tests with the given tcid, can be used multiple times",
    )


def pytest_collection_modifyitems(config, items):
    selected_tcids = config.getoption("--tcid")
    if selected_tcids:
        # --tcid given in cli: do not skip tcid tests
        return
    selected_items = []
    deselected_items = []
    for item in items:
        tcid = item.iter_markers(name="tcid")
        item_tcids = [marker.args[0] for marker in tcid]
        if any(tcid in selected_tcids for tcid in item_tcids):
            selected_items.append(item)
        else:
            deselected_items.append(item)
    items[:] = selected_items
    config.hook.pytest_deselected(items=deselected_items)
