import pytest
import logging

def test_create_slow_application():
    assert True

@pytest.mark.smoke
@pytest.mark.applications
def test_list_applications():
    print("\n11111111111")
    print("22222222222")
    print("33333333333")
    logging.info("44444444444")
    logging.warning("55555555555")
    logging.error("66666666666")
    logging.critical("77777777777")
    assert True


def test_update_application_status():
    assert True


class TestApplicationSearch:
    def test_search_applications_by_company_name(self):
        assert True

    def test_filter_applications_by_status(self):
        assert True
# python -m pytest -m smoke \
# -s -W ignore::pytest.PytestUnknownMarkWarning --log-level=DEBUG -o log_cli=true