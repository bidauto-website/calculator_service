import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text

# Ensure project root is on sys.path so that 'app' package can be imported
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.logger import logger
from app.database.db.session import engine


def _coerce_bool_series(series: pd.Series) -> pd.Series:
    """Coerce a pandas Series with values like 0/1, "0"/"1", "true"/"false" to booleans."""
    true_vals = {"1", "true", "t", "yes", "y"}
    false_vals = {"0", "false", "f", "no", "n"}

    def to_bool(x):
        if isinstance(x, bool):
            return x
        if pd.isna(x):
            return False
        s = str(x).strip().lower()
        if s in true_vals:
            return True
        if s in false_vals:
            return False
        # Fallback: non-empty/non-zero truthiness
        try:
            return bool(int(s))
        except Exception:
            return s not in ("", "0", "false", "none", "nan")

    return series.map(to_bool)


async def seed_fees(engine: Engine):
    src_dir = CURRENT_FILE.parent / 'src'

    # Map CSV paths
    tables = {
        'destination': src_dir / 'destination.csv',
        'location': src_dir / 'location.csv',
        'terminal': src_dir / 'terminal.csv',
        'vehicle_type': src_dir / 'vehicle_type.csv',
        'fee_type': src_dir / 'fee_type.csv',
        'fee': src_dir / 'fee.csv',
        'additional_fee': src_dir / 'additional_fee.csv',
        'additional_special_fee': src_dir / 'additional_special_fee.csv',
        'delivery_price': src_dir / 'delivery_price.csv',
        'shipping_price': src_dir / 'shipping_price.csv',
    }

    # Deletion order: children first, then parents (to satisfy FKs)
    delete_order = [
        'shipping_price',
        'delivery_price',
        'fee',
        'additional_special_fee',
        'additional_fee',
        'fee_type',
        'vehicle_type',
        'terminal',
        'location',
        'destination',
    ]

    # Insertion order: parents first, then children
    insert_order = [
        'destination',
        'location',
        'terminal',
        'vehicle_type',
        'fee_type',
        'additional_fee',
        'additional_special_fee',
        'fee',
        'delivery_price',
        'shipping_price',
    ]

    # Phase 1: delete existing data without dropping tables (preserve schema & FKs)
    with engine.begin() as conn:
        for table in delete_order:
            logger.info(f'Clearing table {table}')
            try:
                conn.execute(text(f'DELETE FROM "{table}"'))
            except Exception as e:
                logger.warning(f'Failed to delete from {table}: {e}')

    # Phase 2: insert data
    for table in insert_order:
        path = tables[table]
        logger.info(f'Seeding table {table} from {path}')
        df = pd.read_csv(path)
        if table == 'destination' and 'is_default' in df.columns:
            df['is_default'] = _coerce_bool_series(df['is_default'])
        df.to_sql(table, engine, if_exists='append', index=False)


if __name__ == '__main__':
    import asyncio

    asyncio.run(seed_fees(engine))




