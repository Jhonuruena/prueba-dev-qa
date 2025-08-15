import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from e2e_tests.the_internet.utils.driver import get_driver
from e2e_tests.the_internet.pages.drag_and_drop_page import DragAndDropPage

class TestDragAndDrop:
    def setup_method(self):
        self.driver = get_driver()
        self.page = DragAndDropPage(self.driver)

    def test_drag_and_drop(self):
        self.page.open()
        assert self.page.get_header_a() == "A"
        assert self.page.get_header_b() == "B"
        self.page.drag_a_to_b()
        import time
        time.sleep(1)

    def teardown_method(self):
        self.driver.quit()