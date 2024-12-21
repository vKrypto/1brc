const fs = require('fs');
const faker = require('@faker-js/faker');

// Configuration
const OUTPUT_FILE = 'transactions.csv';
const TOTAL_ROWS = 1_000_000_000;
const CHUNK_SIZE = 50_000;

async function generateData() {
  // Write CSV Header
  fs.writeFileSync(OUTPUT_FILE, "timestamp,txn_amount,small_description,accountid,status,market_type,symbol,quantity,symbol_price,txn_fee,trade_type,exchangeid\n");

  for (let i = 0; i < TOTAL_ROWS; i += CHUNK_SIZE) {
    let chunk = '';
    for (let j = 0; j < CHUNK_SIZE; j++) {
      const timestamp = new Date().toISOString();
      const txnAmount = faker.datatype.float({ min: -10000, max: 10000, precision: 0.00000001 });
      const description = faker.lorem.sentence(5);
      const accountId = faker.datatype.number({ min: 1000000000, max: 9999999999 });
      const status = faker.helpers.randomize(["failed", "success", "pending"]);
      const marketType = faker.helpers.randomize(["SPOT", "FUTURES", "MARGIN"]);
      const symbol = faker.helpers.randomize(["BTC", "ETH", "ADA"]);
      const quantity = faker.datatype.float({ min: 0.01, max: 1000, precision: 0.00000001 });
      const symbolPrice = faker.datatype.float({ min: 0.01, max: 100000, precision: 0.00000001 });
      const txnFee = faker.datatype.float({ min: 0.01, max: 50, precision: 0.00000001 });
      const tradeType = faker.helpers.randomize(["BUY", "SELL"]);
      const exchangeId = faker.datatype.number({ min: 1, max: 100 });

      chunk += `${timestamp},${txnAmount},${description},${accountId},${status},${marketType},${symbol},${quantity},${symbolPrice},${txnFee},${tradeType},${exchangeId}\n`;
    }

    // Append chunk to file
    fs.appendFileSync(OUTPUT_FILE, chunk);
    console.log(`Generated ${(i + CHUNK_SIZE) / TOTAL_ROWS * 100}%`);
  }
}

generateData().then(() => console.log("Data generation complete!"));
