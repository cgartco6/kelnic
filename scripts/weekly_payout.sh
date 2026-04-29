#!/bin/bash
echo "Triggering weekly payout"
python /opt/kelnic/scripts/generate_bank_file.py
