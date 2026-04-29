#!/usr/bin/env python3
import csv
from datetime import datetime
def generate_csv(amount, bank):
    filename = f"payout_{bank}_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Beneficiary', 'Account', 'Amount', 'Reference'])
        writer.writerow([datetime.now().strftime('%Y-%m-%d'), 'Owner', '123456', amount, f'Kelnic Payout'])
    return filename
