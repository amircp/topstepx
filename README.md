# TopStepX Python Client

📈 Unofficial Python client  [Project X](https://projectx.com) for [TopStepX](https://topstepx.com) API - Place orders, manage positions, and track trades with automatic token management.

## Installation

```bash
pip install topstepx
```

## Quick Start

```python
import asyncio
from topstepx import TopStepXAuth, TopStepXClient, OrderType, OrderSide

async def main():
    # Initialize authentication
    auth = TopStepXAuth("your_username", "your_api_key")
    client = TopStepXClient(auth)
    
    # Get active accounts
    accounts = await client.get_active_accounts()
    print(f"Found {len(accounts)} active accounts")
    
    # Get available contracts
    contracts = await client.get_available_contracts(live=True)
    print(f"Found {len(contracts)} available contracts")

asyncio.run(main())
```

## Features

- **Async/await** support using `httpx`
- **Automatic token management** with refresh before expiration
- **Type hints** throughout
- **Custom exceptions** for better error handling

## API Coverage

### Authentication
- Login with API key
- Automatic token refresh
- Token validation

### Accounts
- `get_active_accounts()` - Get list of active accounts

### Contracts
- `get_available_contracts(live=True)` - Get available contracts

### Orders
- `place_order()` - Place a new order (Market, Limit, Stop, Trailing Stop, Join Bid/Ask)
- `search_orders()` - Search orders by time range
- `get_open_orders()` - Get open orders
- `cancel_order()` - Cancel an order
- `modify_order()` - Modify an open order

### Positions
- `get_open_positions()` - Get open positions
- `close_position()` - Close entire position
- `partial_close_position()` - Partially close a position

### Trades
- `search_trades()` - Search trades by time range

## Examples

### Place a Market Order

```python
from topstepx import TopStepXAuth, TopStepXClient, OrderType, OrderSide

async def place_market_order():
    auth = TopStepXAuth("username", "api_key")
    client = TopStepXClient(auth)
    
    result = await client.place_order(
        account_id=704,
        contract_id="CON.F.US.EP.M25",
        order_type=OrderType.MARKET,
        side=OrderSide.BUY,
        size=1
    )
    print(f"Order placed: {result}")
```

### Place a Limit Order

```python
result = await client.place_order(
    account_id=704,
    contract_id="CON.F.US.EP.M25",
    order_type=OrderType.LIMIT,
    side=OrderSide.BUY,
    size=1,
    limit_price=5900.00
)
```

### Place a Stop Order

```python
result = await client.place_order(
    account_id=704,
    contract_id="CON.F.US.EP.M25",
    order_type=OrderType.STOP,
    side=OrderSide.SELL,
    size=1,
    stop_price=5850.00
)
```

### Search Orders

```python
from datetime import datetime, timedelta

orders = await client.search_orders(
    account_id=704,
    start_timestamp=datetime.now() - timedelta(days=7),
    end_timestamp=datetime.now()
)
```

### Get and Close Positions

```python
# Get open positions
positions = await client.get_open_positions(account_id=704)

# Close a position
if positions:
    await client.close_position(
        account_id=704,
        contract_id=positions[0]["contractId"]
    )

# Or partial close
await client.partial_close_position(
    account_id=704,
    contract_id="CON.F.US.EP.M25",
    size=1
)
```

### Search Trades

```python
from datetime import datetime, timedelta

trades = await client.search_trades(
    account_id=704,
    start_timestamp=datetime.now() - timedelta(days=30),
    end_timestamp=datetime.now()
)

for trade in trades:
    pnl = trade.get("profitAndLoss")
    if pnl is not None:
        print(f"Trade {trade['id']}: P&L = ${pnl}")
    else:
        print(f"Trade {trade['id']}: Opening trade (half-turn)")
```

## Error Handling

```python
from topstepx import (
    TopStepXClient, 
    AuthenticationError, 
    OrderError, 
    PositionError
)

try:
    await client.place_order(...)
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except OrderError as e:
    print(f"Order failed: {e.message} (code: {e.error_code})")
except PositionError as e:
    print(f"Position error: {e.message}")
```

## Order Types

| Type | Value | Description |
|------|-------|-------------|
| `LIMIT` | 1 | Limit order |
| `MARKET` | 2 | Market order |
| `STOP` | 4 | Stop order |
| `TRAILING_STOP` | 5 | Trailing stop order |
| `JOIN_BID` | 6 | Join bid |
| `JOIN_ASK` | 7 | Join ask |

## Order Sides

| Side | Value | Description |
|------|-------|-------------|
| `BUY` | 0 | Buy (Bid) |
| `SELL` | 1 | Sell (Ask) |

## Development

```bash
# Clone the repository
git clone https://github.com/amircp/topstepx.git
cd topstepx

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

## Author

[@bursatilboy](https://x.com/bursatilboy)

## License

MIT License - see [LICENSE](LICENSE) for details.
