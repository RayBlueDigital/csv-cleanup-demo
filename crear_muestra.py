"""Demostración original de limpieza CSV. Todos los datos son ficticios."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime
import csv
import json
import re
import unittest

ROOT = Path(__file__).parent / 'muestra_csv'
HEADERS = ['pedido', 'cliente', 'fecha', 'importe_USD', 'estado']


def clean(row):
    result = {k: ' '.join(row[k].split()) for k in HEADERS}
    if not result['pedido'] or not result['cliente']:
        raise ValueError('Pedido o cliente vacío')
    result['fecha'] = datetime.strptime(result['fecha'].replace('/', '-'), '%Y-%m-%d').date().isoformat()
    raw = result['importe_USD'].removeprefix('$').strip()
    if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d{1,2})?', raw):
        raise ValueError('Importe vacío o formato no admitido; no se adivina el separador decimal')
    result['importe_USD'] = str(Decimal(raw.replace(',', '')).quantize(Decimal('0.01')))
    result['estado'] = result['estado'].lower()
    if result['estado'] not in {'pagado', 'pendiente', 'cancelado'}:
        raise ValueError('Estado desconocido')
    for key in ('pedido', 'cliente', 'estado'):
        if result[key].startswith(('=', '+', '-', '@')):
            result[key] = "'" + result[key]
    return result


class Checks(unittest.TestCase):
    def base(self):
        return dict(zip(HEADERS, ['A001', ' Ana   Demo ', '2026/10/01', '$1,250.00', ' PAGADO ']))

    def test_normalization(self):
        row = clean(self.base())
        self.assertEqual(row['cliente'], 'Ana Demo')
        self.assertEqual(row['importe_USD'], '1250.00')
        self.assertEqual(row['fecha'], '2026-10-01')
        self.assertEqual(row['estado'], 'pagado')

    def test_missing_amount(self):
        row = self.base(); row['importe_USD'] = ''
        with self.assertRaises(ValueError): clean(row)

    def test_ambiguous_decimal(self):
        row = self.base(); row['importe_USD'] = '12,50'
        with self.assertRaises(ValueError): clean(row)

    def test_invalid_date(self):
        row = self.base(); row['fecha'] = '2026-02-30'
        with self.assertRaises(ValueError): clean(row)

    def test_csv_formula(self):
        row = self.base(); row['cliente'] = '=HYPERLINK("https://example.invalid")'
        self.assertTrue(clean(row)['cliente'].startswith("'="))


def main():
    tests = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
    if not tests.wasSuccessful(): raise SystemExit(1)
    ROOT.mkdir(parents=True, exist_ok=True)
    source = [
        ['A001', ' Ana   Demo ', '2026/10/01', '$1,250.00', ' PAGADO '],
        ['A002', 'Tienda Ejemplo', '2026-10-02', '80.5', 'pendiente'],
        ['A003', 'Estudio Ficticio', '2026/10/03', '149.99', 'Pagado'],
        ['A002', 'Tienda Ejemplo', '2026-10-02', '80.50', ' PENDIENTE '],
        ['A004', 'Cliente Muestra', '2026-10-04', '$600.00', 'pagado'],
        ['A005', ' Negocio   Demo ', '2026-10-05', '200', 'cancelado'],
        ['A006', 'Dato Incompleto', '2026-10-06', '', 'pagado'],
        ['A007', 'Fecha Incorrecta', '2026-02-30', '90', 'pendiente'],
    ]
    with (ROOT / 'antes.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(HEADERS); w.writerows(source)
    accepted, seen, issues, duplicates = [], {}, [], []
    with (ROOT / 'antes.csv').open(encoding='utf-8-sig', newline='') as f:
        for number, row in enumerate(csv.DictReader(f), 2):
            try:
                result = clean(row)
            except ValueError as exc:
                issues.append({'fila_origen': number, 'motivo': str(exc), 'datos_originales': row})
                continue
            key = result['pedido']
            if key in seen:
                if seen[key] == result:
                    duplicates.append({'fila_origen': number, 'pedido': key, 'motivo': 'Duplicado exacto después de normalizar'})
                    continue
                raise ValueError(f'Conflicto de pedido {key}: requiere revisión; no se sobrescribe')
            seen[key] = result
            accepted.append(result)
    with (ROOT / 'despues.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, HEADERS); w.writeheader(); w.writerows(accepted)
    report = {
        'demostracion': 'Datos ficticios, no pertenecen a clientes ni representan ventas reales',
        'filas_originales': len(source), 'filas_validas': len(accepted),
        'duplicados_exactos': duplicates, 'incidencias_sin_inventar_datos': issues,
        'total_importes_validos_USD_incluyendo_cancelados': str(sum((Decimal(r['importe_USD']) for r in accepted), Decimal('0.00'))),
        'tests_aprobados': tests.testsRun,
    }
    (ROOT / 'informe.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    with (ROOT / 'despues.csv').open(encoding='utf-8-sig', newline='') as f:
        loaded = list(csv.DictReader(f))
    assert loaded == accepted
    assert len(source) == len(accepted) + len(duplicates) + len(issues)
    assert (len(loaded), len(duplicates), len(issues)) == (5, 1, 2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
