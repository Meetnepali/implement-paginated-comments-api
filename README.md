# Guide to the Project

## Overview
You are provided with a FastAPI codebase for managing user preferences in a profile management system. This project implements in-memory CRUD REST API endpoints for preferences (such as language, notification options, and theme), enforced with validation, structured error messages, and comprehensive unit tests for the 'create' and 'read' operations. All preferences are stored in a Python dict for simplicity.

## Task Requirements
- Add or enhance the CRUD endpoints for user preference management (Create, Read, Update, Delete) in FastAPI.
- All endpoints must validate inputs using Pydantic models and return proper, structured error messages on invalid inputs, duplication, or missing users.
- Make sure that each user has at most one unique set of preferences (enforced at create time).
- Use only in-memory dict-based storage (no persistent store).
- All API responses and error responses must follow consistent models and HTTP status codes.
- Provide or improve unit test coverage (using Pytest and FastAPI’s dependency overrides) specifically for 'create' and 'read' endpoints, ensuring isolation and test reliability.

## What to Focus On
- Input validation (using Pydantic)
- Consistent FastAPI error handling (including custom error messages for all error cases)
- Unique constraint enforcement (only one preference set per user)
- Clean, maintainable organization for extensibility
- Clear, readable, and isolated unit tests (with dep overrides for in-memory state)
- Do NOT implement persistent storage, authentication, or unrelated features

## Verifying Your Solution
- Review all endpoints for the full CRUD capability and proper validation/handling.
- Ensure that unit tests for 'create' and 'read' run successfully, validate correct/incorrect data, and properly set up/tear down using dependency overrides.
- Check that error responses are always structured with the expected 'detail' field and correct HTTP status.

## Additional Guidance
- If you modify or extend the logic, keep the current structure and conventions for consistency and maintainability.
- For expected error cases (duplicate create, non-existent read, etc.), always use HTTPException with clear messages.
- Make sure all test cases are clear, concise, and representative of real use scenarios.
