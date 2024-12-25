#!/bin/bash

OUTPUT_FILE="transactions.csv"
ROWS=50000
CHUNK_SIZE=50000

generate_chunk() {
  for i in $(seq 1 $CHUNK_SIZE); do
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    TXN_AMOUNT=$(awk -v min=-10000 -v max=10000 'BEGIN{srand(); printf "%.8f\n", min+rand()*(max-min)}')
    DESC="Description $(shuf -i 1-10000 -n 1)"
    ACCOUNTID=$(shuf -i 1000000000-9999999999 -n 1)
    STATUS=$(shuf -e failed success pending -n 1)
    MARKET_TYPE=$(shuf -e SPOT FUTURES MARGIN -n 1)
    SYMBOL=$(cat /dev/urandom | tr -dc 'A-Z' | head -c 3)
    QUANTITY=$(awk -v min=0.01 -v max=1000 'BEGIN{srand(); printf "%.8f\n", min+rand()*(max-min)}')
    SYMBOL_PRICE=$(awk -v min=0.01 -v max=100000 'BEGIN{srand(); printf "%.8f\n", min+rand()*(max-min)}')
    TXN_FEE=$(awk -v min=0.01 -v max=50 'BEGIN{srand(); printf "%.8f\n", min+rand()*(max-min)}')
    TRADE_TYPE=$(shuf -e BUY SELL -n 1)
    EXCHANGEID=$(shuf -i 1-100 -n 1)

    echo "$TIMESTAMP,$TXN_AMOUNT,$DESC,$ACCOUNTID,$STATUS,$MARKET_TYPE,$SYMBOL,$QUANTITY,$SYMBOL_PRICE,$TXN_FEE,$TRADE_TYPE,$EXCHANGEID"
  done
}

# Write header
echo "timestamp,txn_amount,small_description,accountid,status,market_type,symbol,quantity,symbol_price,txn_fee,trade_type,exchangeid" > $OUTPUT_FILE

# Progress tracking
TOTAL_CHUNKS=$((ROWS / CHUNK_SIZE))
CURRENT_CHUNK=0

# Generate in chunks
for ((i=1; i<=$ROWS; i+=$CHUNK_SIZE)); do
  generate_chunk >> $OUTPUT_FILE
  CURRENT_CHUNK=$((CURRENT_CHUNK + 1))
  PERCENT=$((CURRENT_CHUNK * 100 / TOTAL_CHUNKS))
  echo "Progress: $PERCENT% ($CURRENT_CHUNK/$TOTAL_CHUNKS chunks completed)"
done

echo "Data generation complete!"
