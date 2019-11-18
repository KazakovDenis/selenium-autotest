# use: $ pytest -vv test_tensor.py
from tensor import *


class TestTensorTask:

    def setup_class(self):
        logging.info(' =========== Test suite started ===========')
        self.tensor = TensorTask()

    def teardown_class(self):
        self.tensor.driver.quit()
        logging.info(' =========== Test suite finished ===========')

    def setup(self):
        logging.info(' ----------- Test started -----------')

    def teardown(self):
        logging.info(' ----------- Test finished -----------')

    def test_get_links(self):
        """ Testing get_links """
        task1 = self.tensor.get_links()
        assert task1_expected == task1

    def test_get_pictures(self):
        """ Testing get_pictures """
        task2 = self.tensor.get_pictures()
        assert task2_expected == task2
