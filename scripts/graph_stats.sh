#!/bin/bash
pip -q install py2neo && \
    python $HOME/scripts/calculate_stats.py
