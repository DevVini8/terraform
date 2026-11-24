import unittest

import pandas as pd

from dashboard import business_rules


class TestUnifiedDataset(unittest.TestCase):
    def setUp(self):
        self.sinesp = pd.DataFrame([
            dict(ano=2025, mes=3, regiao='Nordeste', uf='BA', municipio='SALVADOR',
                 evento='Feminicídio', feminino=4),
            dict(ano=2025, mes=3, regiao='Nordeste', uf='BA', municipio='SALVADOR',
                 evento='Tentativa de feminicídio', feminino=6),
        ], index=[5, 9])
        self.fc = pd.DataFrame([
            dict(ano=2025, mes=3, regiao='Nordeste', uf='BA', cidade='SALVADOR',
                 genero='Mulher cis', raca='Negra', idade=24, is_fatal=1),
            dict(ano=2025, mes=3, regiao='Nordeste', uf='BA', cidade='SALVADOR',
                 genero='Mulher trans e travesti', raca='Sem identificação', idade=36, is_fatal=0),
        ], index=[2, 8])

    def test_preserves_counts_without_join_multiplication(self):
        self.assertTrue(hasattr(business_rules, 'build_unified_dataset'))
        base = business_rules.build_unified_dataset(self.sinesp, self.fc)
        self.assertEqual(base['quantidade'].sum(), 12)
        totals = base.groupby('tipo_violencia')['quantidade'].sum().to_dict()
        self.assertEqual(totals, {'Feminicídio': 4, 'Tentativa de feminicídio': 6, 'Violência armada': 2})
        self.assertEqual(base['municipio'].unique().tolist(), ['SALVADOR'])
        self.assertEqual(base['mes'].unique().tolist(), [3])
        self.assertEqual(base.loc[base['origem'] == 'SINESP', 'quantidade'].sum(), 10)

    def test_missing_demographics_are_not_invented(self):
        self.assertTrue(hasattr(business_rules, 'build_unified_dataset'))
        base = business_rules.build_unified_dataset(self.sinesp, self.fc)
        aggregate = base[base['origem'] == 'SINESP']
        self.assertTrue(aggregate['idade'].isna().all())
        self.assertEqual(aggregate['genero'].unique().tolist(), ['Não informado'])
        self.assertEqual(aggregate['raca'].unique().tolist(), ['Não informado'])
        self.assertEqual(base.loc[base['genero'] == 'Mulher cis', 'quantidade'].sum(), 1)
        self.assertEqual(base.loc[base['raca'] != 'Não informado', 'quantidade'].sum(), 1)

    def test_empty_source_does_not_remove_the_other_source(self):
        self.assertTrue(hasattr(business_rules, 'build_unified_dataset'))
        self.assertEqual(business_rules.build_unified_dataset(self.sinesp.iloc[:0], self.fc)['quantidade'].sum(), 2)
        self.assertEqual(business_rules.build_unified_dataset(self.sinesp, self.fc.iloc[:0])['quantidade'].sum(), 10)
        base = business_rules.build_unified_dataset(self.sinesp.iloc[:0], self.fc.iloc[:0])
        self.assertTrue(base.empty)
        self.assertIn('quantidade', base.columns)
