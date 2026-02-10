# TODO

## Completed
- [x] Ignore nodes that have no input (do not fail when they exist) [added: 2026-02-07, completed: 2026-02-08] - Already working in validator
- [x] Allow drag and drop of json files on canvas to load a new graph. [added: 2026-02-08, completed: 2026-02-08]
- [x] Complete export dialog UI with quality and FPS selection [completed: 2026-02-08]
- [x] Highlight selected edges in blue [completed: 2026-02-08]
- [x] Fix parameter placeholder replacement (pivot, target, angle_rad) [completed: 2026-02-08]

## Future Enhancements
- [ ] Expose node parameters as optional input connectors (e.g., Circle radius, MoveTo target position) [added: 2026-02-08]
- [ ] Add keyboard shortcuts (Ctrl+S, Delete, Esc)
- [ ] Visual error highlighting on nodes when validation fails
- [ ] Undo/Redo functionality
- [ ] Node search/filter in palette
- [ ] Copy/Paste nodes
- [ ] Multi-node selection and group operations
- [ ] Security review before production deployment - address critical vulnerabilities (code injection, CORS, rate limiting, timeouts) [added: 2026-02-09]
