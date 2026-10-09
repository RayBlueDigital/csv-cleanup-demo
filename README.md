# Ray Blue Digital — reproducible CSV cleanup demo

An original, AI-assisted Python demonstration. **All data are fictional. This is not a client case, a sales record, or proof of earnings.**

## Reproduce it

Python 3.9 or newer; standard library only. Run:

```sh
python3 crear_muestra.py
```

The script first runs five regression tests, then creates `muestra_csv/antes.csv`, `muestra_csv/despues.csv`, and `muestra_csv/informe.json`. It writes only those demonstration outputs, relative to the script. Do not place real client data at those paths.

Verified locally on October 8, 2026: five tests passed; the script exited with status 0. This is a local execution result, not a claim about a GitHub Actions run.

## What the example demonstrates

- Eight input records become five accepted records.
- One duplicate is identified after normalization.
- Two invalid records are reported with their original values instead of inventing replacements.
- Whitespace, case, dates, and dollar amounts are normalized using explicit sample rules.
- Ambiguous decimal formatting and impossible dates are rejected.
- An illustrative formula-prefix safeguard is tested. This is not a universal spreadsheet-security guarantee.
- Conflicting records sharing an order ID stop processing rather than silently overwriting data.

The displayed monetary totals are computed **only from fictional sample rows**, including a cancelled order. They are not business revenue or payments received.

## Limits

This is a fixed-schema example using Spanish column names and status values, not a general-purpose production cleaner. A real job requires agreed rules, a non-sensitive sample, and written acceptance criteria. Locale assumptions and spreadsheet behavior need review for the target application. Client data must not be uploaded to this public repository.

## Services

Ray Blue Digital is a human-owned service based in Mexico, using AI-assisted implementation and reproducible verification. We offer small, fixed-scope CSV cleanup and Python automation jobs. No fabricated employment history, client testimonials, or paid-work claims.

A **USD60 CSV pilot** covers one non-sensitive file of up to 10,000 rows, agreed normalization/deduplication rules, cleaned output, an issue report, and one agreed revision. The scope and delivery deadline must be confirmed after reviewing the sample; availability is not an unconditional delivery promise. Payment method: PayPal in USD, by prior agreement.

Portfolio: https://ray-blue-digital.deserted-porter.workers.dev

Contact: ray.blue.digital@gmail.com

To discuss a job, describe the intended output, row count, deadline, and acceptance checks. Do not include credentials, financial-account access, confidential records, or personal customer data in a public issue.
