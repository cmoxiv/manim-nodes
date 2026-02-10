# PRD: Product Vision

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

**manim-nodes** is a self-hosted web application that provides a visual node-based interface for creating MANIM animations. It removes the programming barrier, enabling educators, content creators, and researchers to create high-quality mathematical and ML visualizations without writing code.

## Product Identity

| Attribute | Description |
|-----------|-------------|
| **Product Name** | manim-nodes |
| **Tagline** | Visual Programming for Mathematical Animations |
| **Product Type** | Full-stack web application (backend + frontend) |
| **Deployment Model** | Self-hosted (local or instructor-managed servers) |

## Problem Statement

### Pain Points Addressed

| ID | Pain Point | Description | Impact |
|----|------------|-------------|---------|
| REQ-PRD-001 | Technical Barrier | MANIM requires Python programming skills, limiting accessibility to non-coders | High - excludes many educators |
| REQ-PRD-002 | Slow Iteration | Code-compile-preview cycles are tedious and time-consuming | High - reduces productivity |
| REQ-PRD-003 | Limited Reusability | Hard to share and reuse animation patterns across projects | Medium - duplicated effort |
| REQ-PRD-004 | Live Demonstration | Instructors need to show animation construction process live in class | High - critical for teaching methodology |

## Target Users

### Primary Personas

| Persona | Description | Technical Level | Primary Use Case |
|---------|-------------|----------------|------------------|
| **Math/CS Instructor** | University or high school teacher creating course content | Low to Medium | Lecture animations, live classroom demos |
| **Content Creator** | YouTuber or online educator producing math/ML videos | Low to High | Publication-quality animations for videos |
| **Researcher** | Academic needing visualizations for papers and presentations | Medium to High | Research visualizations, conference talks |

**Target Audience:** Broad educational audience (all personas above)

## Value Proposition

### Core Value

**manim-nodes democratizes mathematical animation creation** by providing a visual, no-code interface to MANIM's powerful animation engine, enabling rapid iteration, live interaction, and community-driven extensibility.

### Key Benefits

| Benefit | Description | Target Persona |
|---------|-------------|----------------|
| **No Code Required** | Drag-and-drop node interface - zero programming needed | All users (esp. instructors) |
| **Live Preview** | See animations update in real-time as you build | All users |
| **Rapid Iteration** | Instantly test and refine animations without code cycles | Content creators, researchers |
| **Reusable Workflows** | Save and share node graphs as templates | All users |
| **Live Teaching Tool** | Demonstrate animation construction process in classroom | Instructors |
| **Extensible** | Custom nodes for specialized domains (calculus, neural networks, etc.) | Advanced users, researchers |

## Success Metrics

### Key Performance Indicators (KPIs)

| ID | Metric | Target | Priority | Measurement Method |
|----|--------|--------|----------|-------------------|
| REQ-PRD-005 | User Adoption | Growing downloads/installations month-over-month | Must | GitHub stars, download counts |
| REQ-PRD-006 | Animation Quality | User-generated outputs are publication-ready (indistinguishable from hand-coded MANIM) | Must | User feedback, showcase gallery |
| REQ-PRD-007 | Learning Curve | Non-coders create first animation in < 30 minutes | Must | User onboarding surveys, analytics |
| REQ-PRD-008 | Community Growth | Active node library contributions and template sharing | Should | Contributed nodes, shared graphs |

## Competitive Landscape

### Existing Solutions

| Solution | Approach | Limitation |
|----------|----------|------------|
| **MANIM (vanilla)** | Python library for programmatic animations | Requires coding; steep learning curve |
| **Blender Geometry Nodes** | Visual node-based 3D animation | Not specialized for math; complex UI |
| **Desmos** | Interactive math visualization | Limited to 2D graphs; not animation-focused |
| **GeoGebra** | Interactive geometry/algebra tool | Limited animation capabilities; not programmable |

### Unique Differentiators

| ID | Differentiator | Description | Competitive Advantage |
|----|----------------|-------------|----------------------|
| REQ-PRD-009 | Node-Based Visual Programming | No code required - drag-and-drop interface | Unique in MANIM ecosystem |
| REQ-PRD-010 | Live Interactive Preview | Real-time visualization as you build | Faster iteration than code-based workflows |
| REQ-PRD-011 | Educational Focus | Built for teaching - live demos, classroom use | Optimized for instructors, not just content creation |
| REQ-PRD-012 | Extensible Node Library | Domain-specific nodes (calculus, linear algebra, ML) | Specialized for math/ML education |

## Timeline

| Milestone | Target | Scope |
|-----------|--------|-------|
| **MVP Release** | 1-2 months | Basic node editor, simple animation export, core node library |
| **Community Beta** | 3-4 months | Feedback iteration, documentation, template library |
| **v1.0 Stable** | 4-6 months | Production-ready with comprehensive features |

## Assumptions

- Users have basic understanding of mathematical concepts they want to visualize
- Users have access to modern web browsers (Chrome, Firefox, Safari)
- Self-hosted deployment means users can install Python/Node.js dependencies
- MANIM library will remain stable and compatible

## Dependencies

- MANIM library (Python) for animation rendering
- Node graph visualization library (frontend)
- Python-to-MANIM code generation (backend)

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| MANIM API changes break compatibility | High | Pin to stable MANIM version; abstract via adapter layer |
| Node editor UX too complex for non-technical users | High | User testing with educators; iterative UX refinement |
| Performance issues with large graphs or complex animations | Medium | Optimize graph execution; progressive rendering |
| Limited adoption if installation is too difficult | Medium | Docker containers; one-command setup; detailed docs |
