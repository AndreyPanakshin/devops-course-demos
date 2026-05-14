# AI Agents Guidelines for this Project

This document outlines the basic rules and conventions for AI agents interacting with this project. Adhering to these guidelines ensures consistency, maintainability, and safe operation within the codebase.

## Core Principles

1.  **Adhere to Project Conventions:** Always prioritize and follow existing coding styles, naming conventions, and architectural patterns found in the project. Analyze surrounding code before making changes.
2.  **Safety and Security:** Never introduce vulnerabilities, expose sensitive information, or bypass security measures. Prioritize safe operations.
3.  **Clarity and Explicitness:** Make your intentions clear. If performing a significant action, briefly explain its purpose and potential impact.
4.  **Use Existing Tools and Libraries:** When possible, leverage libraries, frameworks, and tools already established in the project. Verify their usage before adoption.
5.  **Documentation:** Add documentation, including inline comments for functions, only when explicitly instructed. When instructed, ensure adequate documentation is provided for new features or significant modifications (e.g., comments for complex logic, README updates if applicable).
6.  **Testing:** When adding features or fixing bugs, include appropriate tests to ensure quality and prevent regressions.

## Change Workflow: Plan and Approve

A core principle of all modifications is that they should be as focused, small, and atomic as possible. If a change cannot be made atomically, the proposed plan must explicitly break it down into a series of distinct, sequential stages.

Before making any modifications to the project, the following iterative process must be followed:

1.  **Propose a Plan:** Prepare a detailed plan outlining the intended changes. This plan must be presented to the user for review.
2.  **Seek Approval:** Explicitly ask for the user's approval of the plan.
3.  **Incorporate Feedback:** If the user provides corrections or suggestions, create a new, updated plan that incorporates this feedback.
4.  **Re-seek Approval:** Submit the revised plan for approval again.
5.  **Repeat Until Approved:** Continue this cycle of planning, feedback, and revision until the user explicitly approves a plan. No changes may be implemented until a plan is approved.

## Interaction with the Codebase

*   **No Unapproved Commits:** Do not commit changes directly unless explicitly instructed.
*   **Temporary Files:** Utilize the project's temporary directory for any ephemeral files.
*   **Automated Tools:** Never run tests, linters, type-checkers, or any other automated quality assurance tools unless explicitly instructed to do so.

*   **No Emojis or UTF Icons:** Never use emojis, special Unicode characters, or other non-standard UTF icons in code, documentation, commit messages, or any other output.

These guidelines will evolve as the project matures.