# .claude/ Folder Structure

This folder contains all project metadata, context, and definitions for structured development.

## Folder Organization

### `/context`
Centralized knowledge base for the project

- **`legal/`** - Laws, regulations, official documents
- **`data/`** - Sample data and synthetic datasets  
- **`references/`** - External resources and links
- **`hackathon/`** - Event-specific documents

### `/agents`
Agent role definitions and prompt templates

### `/instructions`
System instructions and behavior definitions per module

### `/tasks`
Feature tracking and sprint planning

### `/tools`
Tool/utility definitions and wrappers

### `/workflows`
Multi-step process orchestration

## Git Commit Strategy

Every commit references the changelog:
```
feat(module-1): add zone viability checker

See: .claude/changelog.md#[date]
```

Commits are **atomic** — one feature per commit.

---

*Project initialized: June 6, 2026*
