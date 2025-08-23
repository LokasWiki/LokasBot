"""
Database infrastructure implementations.

This module contains concrete implementations for database operations
using various database systems like MySQL, PostgreSQL, etc.
"""

from .mysql_database import MySQLDatabase

__all__ = ["MySQLDatabase"]