# EAOS Enterprise AI IDE Architecture Specification

## Overview
This document specifies the multi-layer frontend composition architecture.

## Layers
1. **Presentation Layer (`.html`)**: Modular Jinja2 layouts.
2. **Runtime Engine (`.js`)**: ES6 modules and WebSockets.
3. **Configurations (`.json`)**: Declarative definitions.
4. **Android Client (`.kt` / `.xml`)**: Native Android interface.