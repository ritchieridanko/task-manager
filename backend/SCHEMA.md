# Task Manager Database Schema

## 1. `boards` Table:

- **id**: UUID (Primary Key, Default: `GEN_RANDOM_UUID()`)
- **name**: VARCHAR (Not Null)
- **created_at**: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- **updated_at**: TIMESTAMPTZ (Not Null, Default: `NOW()`)

## 2. `tasks` Table:

- **id**: UUID (Primary Key, Default: `GEN_RANDOM_UUID()`)
- **board_id**: UUID (Not Null, FK: `boards(id)` with `ON DELETE RESTRICT`)
- **title**: VARCHAR (Not Null)
- **description**: VARCHAR (Nullable)
- **status**: VARCHAR (Not Null, Default: `TODO`)
- **created_at**: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- **updated_at**: TIMESTAMPTZ (Not Null, Default: `NOW()`)

## 3. Indexes:

- **idx_tasks_board_id**: Added on `tasks(board_id)` to optimize filtering and querying tasks belonging to a specific board.
