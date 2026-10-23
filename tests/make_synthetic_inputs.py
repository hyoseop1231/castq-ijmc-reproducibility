#!/usr/bin/env python3
"""Create explicitly synthetic schema fixtures; never read research data.

This fixture is for execution smoke tests, not manuscript-result reproduction.
Only Python standard-library modules are used. No input data are accepted/read.
"""

import argparse
import csv
from datetime import date, timedelta
import os
from pathlib import Path
import random
import sqlite3

SEED = 20261023
N_DAYS = 198
START_DATE = date(2000, 1, 1)
TARGET_COLUMNS = [
    'defect_' + name
    for name in ['사혼입', 'gh', '누탕', '파손', '크랙', '블로우',
                 '수축', '중파손', '과절삭', '기타']
]


def create_new_output(path):
    """Reject existing targets and symlinks, including existing ancestor links.

    The caller must choose a trusted parent directory. This simple check is not
    a defense against a hostile concurrent process replacing path components.
    """
    output = Path(os.path.abspath(os.path.expanduser(os.fspath(path))))
    for component in [output, *output.parents]:
        if component.is_symlink():
            raise ValueError('Output path and ancestors must not be symlinks.')
    if os.path.lexists(output):
        raise ValueError('Output already exists; choose a new directory.')
    if not output.parent.is_dir():
        raise ValueError('Output parent must already exist as a directory.')
    # Exclusive creation also rejects a target created after the checks above.
    os.mkdir(output, mode=0o700)
    return output


def generate(output):
    """Write only new synthetic files inside a newly created output folder."""
    rng = random.Random(SEED)
    raw = output / 'raw_db'
    raw.mkdir(mode=0o700)
    process = sqlite3.connect(raw / 'process.db')
    observations = None
    try:
        observations = sqlite3.connect(raw / 'observations.db')
        process.execute('CREATE TABLE tbDissolution '
                        '(d_DL_Date TEXT, n_DL_Temperture REAL)')
        process.execute('CREATE TABLE tbModeling '
                        '(d_ML_Date TEXT, n_ML_Count INTEGER, '
                        'n_ML_ITEM_ID INTEGER)')
        observation_columns = ', '.join(
            'value_{} REAL'.format(i) for i in range(1, 9)
        )
        observations.execute('CREATE TABLE spectro_analysis_records '
                             '(analysis_date TEXT, ' + observation_columns + ')')
        fields = ['dissolution_date', 'defect_date', 'has_defect'] + TARGET_COLUMNS
        # Exclusive file mode protects against accidental overwriting.
        with (output / 'archive.csv').open('x', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for day_index in range(N_DAYS):
                day = (START_DATE + timedelta(days=day_index)).isoformat()
                # Explicit alternation ensures both classes in each fixed split;
                # this label pattern is arbitrary, not an industrial mechanism.
                positive = day_index % 2
                counts = [0] * len(TARGET_COLUMNS)
                if positive:
                    counts[rng.randrange(len(counts))] = rng.randint(1, 4)
                row = dict(zip(TARGET_COLUMNS, counts))
                row.update(dissolution_date=day,
                           defect_date='' if day_index >= N_DAYS - 2 else day,
                           has_defect=positive)
                writer.writerow(row)
                # All values below are arbitrary seeded random draws, unrelated
                # to any real plant, author data, or intended physical model.
                for _ in range(rng.randint(2, 5)):
                    process.execute('INSERT INTO tbDissolution VALUES (?, ?)',
                                    (day, round(rng.uniform(500.0, 900.0), 4)))
                for _ in range(rng.randint(1, 4)):
                    process.execute('INSERT INTO tbModeling VALUES (?, ?, ?)',
                                    (day, rng.randint(10, 80), rng.randint(1, 6)))
                for _ in range(rng.randint(1, 3)):
                    channels = [round(rng.uniform(0.01, 5.0), 6)
                                for _ in range(8)]
                    observations.execute(
                        'INSERT INTO spectro_analysis_records '
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (day, *channels),
                    )
        process.commit()
        observations.commit()
    finally:
        process.close()
        if observations is not None:
            observations.close()
    # Labels and dates here are simulation metadata, not a captured source log.
    with (output / 'SYNTHETIC_FIXTURE.txt').open('x', encoding='utf-8') as f:
        f.write('EXPLICITLY SYNTHETIC: no author or industrial data.\n'
                'Purpose: schema/execution smoke test only; not paper results.\n'
                'Seed: 20261023. Simulated start: 2000-01-01. Days: 198.\n'
                'One archive row per simulated day. Alternating arbitrary labels.\n'
                'Chronological pre-exclusion split sizes: 115/32/51.\n'
                'Last two simulated outcome dates missing; eligible: 115/32/49.\n'
                'No scientific or physical interpretation of simulated values.\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True,
                        help='New output directory; existing paths are refused.')
    args = parser.parse_args()
    try:
        output = create_new_output(args.out)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    try:
        generate(output)
    except Exception:
        # Do not delete a partial folder or retry into it automatically.
        print('Synthetic generation failed; partial output is retained. '
              'Inspect it and choose another NEW output directory for retry.')
        raise
    print('Created EXPLICITLY SYNTHETIC schema fixture: '
          '198 simulated days, eligible split sizes 115/32/49; seed 20261023. '
          'No analysis pipeline was run.')


if __name__ == '__main__':
    main()
