# Thermodynamics SDK

A stable, minimal, correct foundation for modeling simple thermodynamic systems using the First Law of Thermodynamics, suitable for education, prototyping, and extension.

---

## Table of Contents

1.  [What this SDK is](#1-what-this-sdk-is)
2.  [What it is not](#2-what-it-is-not)
3.  [Quick Start](#3-quick-start)
4.  [Physics Conventions](#4-physics-conventions)
5.  [API Overview](#5-api-overview)
6.  [Stability Guarantees](#6-stability-guarantees)
7.  [Roadmap](#7-roadmap)

---

## 1. What this SDK is

The Thermodynamics SDK provides a basic, yet robust, framework for analyzing simple thermodynamic systems governed by the First Law of Thermodynamics. It is designed for clarity, correctness, and ease of use, making it ideal for educational purposes, rapid prototyping, and as a foundational layer for more complex thermodynamic simulations.

This SDK focuses on:
*   Modeling a single, lumped thermodynamic system.
*   Applying the First Law of Thermodynamics with a consistent sign convention.
*   Enabling persistence of system states via JSON serialization.

## 2. What it is not

To manage expectations and prevent scope creep, it's important to state what this SDK *does not* (yet) cover. These are explicit non-goals for the v1.x series:

*   ❌   **No Entropy**: Does not model entropy or the Second Law of Thermodynamics.
*   ❌   **No Temperature, Pressure, Volume**: Does not inherently deal with these properties or equations of state. All calculations are purely energy-based.
*   ❌   **No Time Evolution**: Does not simulate processes over time. It models system states and changes between them.
*   ❌   **No Multi-system Interactions**: Designed for single, isolated systems.
*   ❌   **No Carnot Cycles, PDEs, Symbolic Math**: No advanced thermodynamic cycles, partial differential equations, or symbolic computation.
*   ❌   **No Real-World Materials**: Does not include material property databases or complex substance models.
*   ❌   **No Plotting/Visualization**: Does not provide any built-in graphing or visualization tools.
*   ❌   **No Performance Optimizations**: Focus is on correctness and maintainability, not high-performance computation.
*   ❌   **No Units Abstraction**: All energy quantities are assumed to be in Joules (J). Users are responsible for external unit management.

## 3. Quick Start

### Installation

For now, you can clone the repository:

```bash
git clone https://github.com/your-org/thermodynamics-sdk.git # Replace with actual repo
cd thermodynamics-sdk