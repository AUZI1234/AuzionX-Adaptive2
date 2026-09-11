AuzionX Adaptive v2

Adaptive market-intelligence and automated-trading research project for MetaTrader 5.

Project Status

Phase: Architecture and research

Primary instrument: XAUUSD

Platform: MetaTrader 5

Language: MQL5

Research environment: Python

Potential ML deployment: ONNX

Live trading: Not approved

---

1. Vision

AuzionX Adaptive v2 is intended to evolve beyond a setup-dependent trading robot.

The system should continuously evaluate market behaviour and determine whether current conditions provide a sufficiently strong and executable opportunity.

The system should be capable of:

- identifying market state
- detecting directional movement
- measuring momentum
- measuring acceleration
- recognizing pullbacks
- recognizing breakouts
- detecting possible exhaustion
- evaluating short-term market flow
- evaluating execution conditions
- dynamically choosing between BUY, SELL and WAIT
- managing core positions
- managing scalp positions
- managing micro-flow positions
- adapting activity to market conditions
- protecting capital through an independent risk engine

High trade frequency is a capability, not a requirement.

The system must never manufacture trades merely to increase trade count.

---

2. Primary Objective

The immediate objective is to develop and validate an adaptive XAUUSD trading engine that can make rapid local decisions when connected to the broker.

The project is also designed around limited internet availability.

Heavy research, historical analysis, model development and testing should therefore be performed locally on the development laptop whenever practical.

The live EA should perform its core decision-making locally inside MetaTrader 5.

---

3. Architecture

The intended architecture contains:

Market Perception Engine

Collects and transforms current market information.

Market State Engine

Classifies the current environment.

Possible states include:

- TREND_UP
- TREND_DOWN
- PULLBACK_UP
- PULLBACK_DOWN
- ACCELERATION_UP
- ACCELERATION_DOWN
- BREAKOUT
- COMPRESSION
- EXHAUSTION
- REVERSAL_RISK
- NO_TRADE

These names are provisional and must be validated during research.

Structure Engine

Analyzes market structure, including:

- swings
- higher highs
- higher lows
- lower highs
- lower lows
- BOS
- CHoCH
- protected structure

Flow Engine

Analyzes short-term movement, including:

- momentum
- acceleration
- tick activity
- volatility
- directional persistence
- short-term price behaviour

Probability / Scoring Engine

Combines relevant evidence into an interpretable decision score.

Core Engine

Designed to participate in larger directional movements.

Scalp Engine

Designed to participate in shorter directional movements.

Micro-Flow Engine

Designed to evaluate very short-lived market opportunities.

Risk Engine

Controls:

- position risk
- exposure
- daily loss
- drawdown
- spread
- execution conditions
- trade frequency
- emergency shutdown

Execution Engine

Handles MT5 order execution and execution-quality checks.

Telemetry Engine

Records why decisions were made and what happened afterward.

---

4. Trading Philosophy

AuzionX should not depend exclusively on:

- one indicator
- one pattern
- one order block
- one timeframe
- one entry setup

Existing price-action concepts such as market structure, BOS, CHoCH, order blocks and pullbacks may remain useful components.

However, they should become inputs to the broader market-intelligence system rather than necessarily being mandatory prerequisites for every trade.

---

5. Machine Learning

Machine learning is optional.

It must only be introduced where testing demonstrates that it adds useful predictive or decision-making value.

Potential workflow:

Historical data
→ feature generation
→ model training
→ validation
→ out-of-sample testing
→ model export
→ ONNX
→ MT5 inference

The ML model must never bypass the risk engine.

A deterministic baseline must exist so that ML performance can be compared against a non-ML system.

---

6. Research Requirements

All proposed trading logic should be investigated for:

- statistical edge
- transaction costs
- spread
- slippage
- execution limitations
- overfitting
- look-ahead bias
- survivorship bias
- regime changes
- robustness across different market conditions

No backtest result should be interpreted as proof of future profitability.

---

7. Development Rules

Never optimize for appearance.

A complicated system is not automatically a better system.

Never optimize for trade count alone.

More trades can increase costs and reduce expectancy.

Never remove risk controls to increase activity.

Never claim profitability without evidence.

Never use future information during historical simulation.

Never silently change an approved trading rule.

Never deploy untested changes to live money.

Prefer modular components.

Prefer explainable decisions.

Preserve working functionality unless there is a documented reason to change it.

---

8. Development Stages

Phase 1 — Architecture

Define the complete system before building the final EA.

Phase 2 — Market Intelligence

Build and test market-state and market-flow detection.

Phase 3 — Decision Engine

Build scoring and trade-selection logic.

Phase 4 — Risk and Execution

Build robust position and execution management.

Phase 5 — EA Integration

Integrate the components into MQL5.

Phase 6 — Historical Testing

Test against historical data.

Phase 7 — Out-of-Sample Testing

Test against data not used during development.

Phase 8 — Demo Forward Testing

Run the EA on a demo account.

Phase 9 — Controlled Live Evaluation

Only after sufficient evidence has been collected.

---

9. Initial Scope

Initial development is limited to:

XAUUSD

The system should not initially attempt to support every instrument.

Once the architecture is validated, multi-symbol support can be considered.

---

10. Current Principle

The central question for AuzionX is:

«"What is the market doing right now, is there an executable edge in that movement, and can we participate while maintaining controlled risk?"»

Not:

«"Is my favourite setup present?"»

---

11. Disclaimer

AuzionX is an experimental software and quantitative-research project.

No component of this repository guarantees profit.

All strategies and models must be validated before any real-money deployment.