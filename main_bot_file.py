"""
Main Bot Class - Binance Futures Trading Bot
Core functionality and client management
"""

import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BasicBot:
    """
    Main trading bot class for Binance Futures Testnet.
    Manages API connection and provides core trading functionality.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.testnet = testnet
        
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com'
            logger.info("Initialized bot in TESTNET mode")
        else:
            logger.warning("Initialized bot in LIVE mode - USE WITH CAUTION")
        
        self._validate_connection()
    
    def _validate_connection(self) -> bool:
        """
        Validate API connection and credentials.
        
        Returns:
            bool: True if connection successful
        
        Raises:
            BinanceAPIException: If connection fails
        """
        try:
            self.client.futures_ping()
            account_info = self.client.futures_account()
            balance = account_info.get('totalWalletBalance', 'N/A')
            logger.info(f"Connection successful. Account balance: {balance} USDT")
            return True
        except BinanceAPIException as e:
            logger.error(f"API connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during connection validation: {e}")
            raise
    
    def validate_order_params(self, symbol: str, side: str, order_type: str, 
                             quantity: float, price: float = None) -> bool:
        """
        Validate order parameters before placing order.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            order_type: Order type (MARKET, LIMIT, etc.)
            quantity: Order quantity
            price: Order price (optional, required for LIMIT)
        
        Returns:
            bool: True if valid
        
        Raises:
            ValueError: If parameters are invalid
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid symbol")
        
        if side.upper() not in ['BUY', 'SELL']:
            raise ValueError("Side must be 'BUY' or 'SELL'")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if order_type.upper() == 'LIMIT' and (price is None or price <= 0):
            raise ValueError("Price must be provided and positive for LIMIT orders")
        
        logger.info(f"Order parameters validated: {symbol} {side} {order_type} {quantity}")
        return True
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get the status of an order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID
        
        Returns:
            Dict containing order status information
        """
        try:
            logger.info(f"Fetching order status: {symbol} Order ID: {order_id}")
            order = self.client.futures_get_order(symbol=symbol.upper(), orderId=order_id)
            
            result = {
                'success': True,
                'order_id': order['orderId'],
                'symbol': order['symbol'],
                'status': order['status'],
                'side': order['side'],
                'type': order['type'],
                'quantity': order['origQty'],
                'executed_qty': order['executedQty'],
                'price': order.get('price'),
                'avg_price': order.get('avgPrice')
            }
            
            logger.info(f"Order status retrieved: {order['status']}")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching order status: {e.status_code} - {e.message}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error fetching order status: {e}")
            return {'success': False, 'error': str(e)}
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an open order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID
        
        Returns:
            Dict containing cancellation result
        """
        try:
            logger.info(f"Cancelling order: {symbol} Order ID: {order_id}")
            result = self.client.futures_cancel_order(symbol=symbol.upper(), orderId=order_id)
            logger.info(f"Order {order_id} cancelled successfully")
            
            return {
                'success': True,
                'order_id': result['orderId'],
                'symbol': result['symbol'],
                'status': result['status']
            }
            
        except BinanceAPIException as e:
            logger.error(f"Error cancelling order: {e.status_code} - {e.message}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error cancelling order: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance information.
        
        Returns:
            Dict containing balance information
        """
        try:
            logger.info("Fetching account balance")
            account = self.client.futures_account()
            
            result = {
                'success': True,
                'total_balance': account['totalWalletBalance'],
                'available_balance': account['availableBalance'],
                'total_unrealized_profit': account['totalUnrealizedProfit']
            }
            
            logger.info(f"Balance retrieved: {result['total_balance']} USDT")
            return result
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching balance: {e.status_code} - {e.message}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get information about a trading symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Dict containing symbol information
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    return {
                        'success': True,
                        'symbol': s['symbol'],
                        'status': s['status'],
                        'base_asset': s['baseAsset'],
                        'quote_asset': s['quoteAsset'],
                        'price_precision': s['pricePrecision'],
                        'quantity_precision': s['quantityPrecision']
                    }
            
            return {'success': False, 'error': 'Symbol not found'}
            
        except Exception as e:
            logger.error(f"Error fetching symbol info: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Dict containing current price
        """
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol.upper())
            return {
                'success': True,
                'symbol': ticker['symbol'],
                'price': float(ticker['price'])
            }
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return {'success': False, 'error': str(e)}