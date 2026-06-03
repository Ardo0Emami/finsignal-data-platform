# FACT_BACKTEST_RESULT Contract

`fact_backtest_result` stores historical forward-return outcomes for generated asset signals.

## Grain

One row represents:

    one symbol
    one signal date
    one signal code
    one signal version

## Purpose

This table measures what happened after a signal was generated.

It is used to evaluate signal quality without changing the original signal logic.

## Look-Ahead Bias Rule

Signal features must only use data available at or before the signal timestamp.

Forward return columns are evaluation outcomes, not input features.

Do not use forward return columns to generate the signal itself.

## Horizons

Current horizons:

    1 day
    3 days
    7 days

Longer horizons can be added later when more historical data exists.
