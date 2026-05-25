# KILO_TODO - Disagreements between README, docs, and code

## Critical Bugs

### 1. Missing comma in README decorator example
**Location:** README.md:48
```python
@sparkle_log.monitor_metrics_on_call(("cpu", "memory" "drive"), 60)
```
**Issue:** Missing comma between `"memory"` and `"drive"`. This should be:
```python
@sparkle_log.monitor_metrics_on_call(("cpu", "memory", "drive"), 60)
```

## Inconsistencies

### 2. Default style mismatch between decorator and context manager
- **Decorator** (`as_decorator.py:116`): default style is `"bar"`
- **Context manager** (`as_context_manager.py:41`): default style is `"faces"`

The README doesn't specify a style in either example, so users get different defaults depending on which approach they use. Should be aligned.

### 3. Scheduler parameter name mismatch
**Location:** `scheduler.py:478` defines `seconds` but `as_decorator.py:135` and `as_context_manager.py:65` pass `interval` as the 4th positional argument.

This works due to positional args but is confusing. Consider renaming to `interval` for clarity.

### 4. Missing `CustomMetricsCallBacks` export in `__init__.py`
The README shows using `custom_metrics={"dodgy": dodgy_metric}` but `CustomMetricsCallBacks` type is not exported from `__init__.py`. Users who want type hints cannot import it.

## Documentation Issues

### 5. docs/TODO.md is stale/outdated
The TODO file has incomplete items marked with `***` that appear to be done (support for various sparkline styles exists in `ui.py`). The file should be cleaned up or removed.

### 6. Missing documentation for `log_system_metrics` function
The README shows `sparkline` and `GraphStyle` as public API but `log_system_metrics` (exported in `__init__.py`) is not documented. This is a stateful alternative to the decorator/context manager.

### 7. README says "up to log entries" but doesn't specify number
**Location:** README.md:34
> "This will write up to log entries to your AWS Lambda log"

The sentence is incomplete - "up to **X** log entries" should specify the number (which is 30 based on `log_writer.py`).

### 8. No documentation for CLI options
The `__main__.py` has several CLI options (`--metrics`, `--interval`, `--duration`, `--style`, `--version`) that are not documented in README.md.

### 9. Source.md duplicates information
SOURCE.md is auto-generated source code documentation that duplicates what's in the code. It doesn't add value as "documentation" and may cause confusion about what users should read.
