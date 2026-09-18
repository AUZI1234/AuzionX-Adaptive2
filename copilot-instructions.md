# AuzionX Adaptive v2 — Copilot Instructions

## Mission

You are contributing to AuzionX Adaptive v2, an experimental MetaTrader 5 trading system initially focused on XAUUSD. The objective is an adaptive market-intelligence engine that evaluates market movement continuously rather than relying exclusively on fixed setups.

Priorities: risk control, execution reliability, statistical evidence, adaptive market-state recognition, explainability, testability, maintainability and performance. Profit must never be assumed or guaranteed.

## Architecture

Keep these components modular: Market Perception, Market State, Structure, Momentum/Flow, Probability/Scoring, Core Position, Scalp, Micro-Flow, Risk, Exposure, Execution, Trade Management and Logging/Telemetry.

## Adaptive Philosophy

Continuously evaluate trend, pullback, momentum, acceleration, compression, breakout, exhaustion, reversal risk, changing volatility and execution conditions. BUY, SELL and WAIT are all valid decisions. WAIT is important.

## Trade Frequency

High frequency is a capability, not a mandatory target. Never manufacture trades to reach a numerical objective. Frequency must emerge from market activity, opportunity quality, expected edge, spread, commission, slippage, execution quality, exposure, account risk and market state.

## Risk

Risk controls have priority over frequency. Support maximum daily loss, maximum drawdown, maximum exposure, maximum positions, spread and execution protection, abnormal-market protection, emergency halt, consecutive-loss protection and risk reduction during unstable conditions.

## Backtesting

Avoid look-ahead bias, data leakage, overfitting, curve fitting, survivorship bias and unrealistic spreads, slippage or execution. Separate development from validation. A single backtest is not proof of profitability.

## Machine Learning

ML is optional. Do not add it merely because it sounds advanced. It must demonstrate value against a deterministic baseline, have documented features/data/validation/out-of-sample testing, be versioned and reproducible, be evaluated for overfitting and remain subordinate to risk controls. ONNX may be considered for local MT5 inference.

## MQL5

Use correct MQL5 APIs. Check return values and trade errors. Avoid unnecessary repeated calculations and blocking operations. Keep functions focused, names clear, important logic documented and parameters configurable. Separate analysis, decision, execution and management. Never assume MQL4 behaviour applies to MQL5.

## Execution

Consider spread, slippage, filling mode, trading permissions, volume limits/step, stops/freeze levels, margin and broker execution behaviour.

## Logging

Record enough to explain why an opportunity was accepted/rejected, detected market state, score, risk state, execution conditions, exit reason and outcome. Avoid excessive normal-operation logging.

## Development Process

Before a major component: understand the requirement, inspect repository code, identify dependencies, propose design, implement the smallest appropriate change, test, review and document. Do not rewrite unnecessarily.

## Live Trading

Live trading is not part of normal development. Use historical data, Strategy Tester and demo accounts. Compilation alone never justifies live deployment.

## Scope

Initial instrument: XAUUSD. Do not expand until the initial architecture is properly tested.

## User Communication

The user is the trading/product decision maker. Translate technical findings clearly. If a critical requirement is ambiguous, identify it, explain why it matters, propose options and do not silently invent the rule.
