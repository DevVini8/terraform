import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "dashboard" / "app.py"


class TestDashboard(unittest.TestCase):
    def test_compact_single_selection_filters_and_unified_totals(self):
        app = AppTest.from_file(str(APP), default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.multiselect), 0)
        self.assertEqual(len(app.selectbox), 8)
        for widget in list(app.selectbox)[:7]:
            self.assertEqual(widget.value, "Todos")
        self.assertFalse(app.sidebar.selectbox)
        self.assertFalse(app.tabs)
        self.assertEqual(app.metric[0].value, "1.310")

    def test_type_and_profile_filters_with_empty_result(self):
        app = AppTest.from_file(str(APP), default_timeout=60).run()
        app.selectbox(key="tipo_violencia").set_value("Violência armada").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "77")
        app.selectbox(key="genero").set_value("Mulher cis").run()
        self.assertFalse(app.exception)
        self.assertLess(int(app.metric[0].value), 77)
        app.selectbox(key="tipo_violencia").set_value("Feminicídio").run()
        self.assertFalse(app.exception)
        self.assertFalse(app.metric)
        self.assertEqual(app.info[0].value, "Sem dados para os filtros selecionados.")
