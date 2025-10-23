"""
Stop-Limit Orders Module (BONUS)
Handles stop-limit order execution for Binance Futures
"""

import logging
from datetime import datetime
from typing import Dict, Any
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


class StopLimitOrderHandler:
    """
    Handles stop-limit order operations.
    
    A stop-limit order becomes a limit order when the stop price is reached.
    It combines the features of stop orders and limit orders.
    
    Use cases:
    - Stop-loss with price control
    - Take-profit with guaranteed minimum price
    - Risk management with specific exit prices
    """
    
    def __init__(self, bot):
        """
        Initialize stop-limit order handler.
        
        Args:
            bot: BasicBot instance
        """
        self.bot = bot
        self.client = bot.client
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                               stop_price: float, limit_price: float,
                               time_in_force: str = 'GTC') -> Dict[str, Any]:
        """
        Place a stop-limit order on Binance Futures.
        
        How it works:
        1. Order activates when market reaches the stop_price
        2. Once activated, becomes a limit order at limit_price
        3. Executes at limit_price or better
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Order quantity
            stop_price: Price that triggers the order
            limit_price: Limit price after trigger
            time_in_force: Order duration ('GTC', 'IOC', 'FOK')
        
        Returns:
            Dict containing order details
        
        Example - Stop Loss:
            >>> # Sell if price drops to $49,000, execute at $48,900
            >>> handler.place_stop_limit_order('BTCUSDT', 'SELL', 0.001, 49000, 48900)
        
        Example - Take Profit:
            >>> # Buy if price rises to $51,000, execute at $51,100
            >>> handler.place_stop_limit_order('BTCUSDT', 'BUY', 0.001, 51000, 51100)
        """
        try:
            # Validate basic parameters
            self.bot.validate_order_params(symbol, side, 'STOP', quantity, stop_price)
            
            # Validate stop-limit specific parameters
            if limit_price <= 0:
                raise ValueError("Limit price must be positive")
            
            if time_in_force.upper() not in ['GTC', 'IOC', 'FOK']:
                raise ValueError("time_in_force must be GTC, IOC, or FOK")
            
            # Validate price logic based on side
            if side.upper() == 'SELL' and limit_price > stop_price:
                logger.warning("For SELL: limit_price should typically be <= stop_price")
            
            if side.upper() == 'BUY' and limit_price < stop_price:
                logger.warning("For BUY: limit_price should typically be >= stop_price")
            
            logger.info(f"Placing STOP_LIMIT {side} order: {quantity} {symbol}")
            logger.info(f"Stop Price: {stop_price}, Limit Price: {limit_price}")
            
            # Place the order
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='STOP',  # STOP type creates stop-limit orders on Binance Futures
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                timeInForce=time_in_force.upper()
            )
            
            # Log success
            logger.info(f"Stop-limit order placed successfully - Order ID: {order['orderId']}")
            logger.info(f"Order details: {order}")
            
            # Format response
            result = {
                'success': True,
                'order_id': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': order['origQty'],
                'stop_price': order.get('stopPrice'),
                'limit_price': order.get('price'),
                'executed_qty': order.get('executedQty', '0'),
                'status': order['status'],
                'time_in_force': order.get('timeInForce'),
                'timestamp': datetime.fromtimestamp(order['updateTime'] / 1000).isoformat(),
                'client_order_id': order.get('clientOrderId')
            }
            
            return result
            
        except BinanceAPIException as e:
            error_msg = f"Binance API error: {e.status_code} - {e.message}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'error_code': e.code
            }
        
        except ValueError as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def place_stop_loss(self, symbol: str, quantity: float, 
                       stop_price: float, limit_offset: float = 0.001) -> Dict[str, Any]:
        """
        Convenience method to place a stop-loss order.
        Automatically calculates limit price with offset.
        
        Args:
            symbol: Trading pair
            quantity: Order quantity
            stop_price: Stop trigger price
            limit_offset: Percentage offset for limit price (default: 0.1%)
        
        Returns:
            Dict containing order details
        """
        # Calculate limit price slightly below stop price
        limit_price = stop_price * (1 - limit_offset)
        
        logger.info(f"Placing STOP LOSS: {quantity} {symbol} @ Stop: {stop_price}, Limit: {limit_price}")
        
        return self.place_stop_limit_order(symbol, 'SELL', quantity, stop_price, limit_price)
    
    def place_take_profit(self, symbol: str, quantity: float,
                         target_price: float, limit_offset: float = 0.001) -> Dict[str, Any]:
        """
        Convenience method to place a take-profit order.
        Automatically calculates limit price with offset.
        
        Args:
            symbol: Trading pair
            quantity: Order quantity
            target_price: Target trigger price
            limit_offset: Percentage offset for limit price (default: 0.1%)
        
        Returns:
            Dict containing order details
        """
        # Calculate limit price slightly above target price
        limit_price = target_price * (1 + limit_offset)
        
        logger.info(f"Placing TAKE PROFIT: {quantity} {symbol} @ Target: {target_price}, Limit: {limit_price}")
        
        return self.place_stop_limit_order(symbol, 'SELL', quantity, target_price, limit_price)