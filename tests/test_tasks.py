import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from datetime import datetime
from models import Task
from tasks import add_task, update_task, delete_task


class TestDisplayStatus(unittest.TestCase):
    def test_done_overrides_expired_deadline(self):
        task = Task(1, "old task", "desc", "2020-01-01T00:00:00", status="done")
        self.assertEqual(task.display_status(), "done")

    @patch("models.datetime")
    def test_pending_before_deadline(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2026, 1, 1)
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        task = Task(1, "future task", "desc", "2026-06-01T00:00:00")
        self.assertEqual(task.display_status(), "pending")

    @patch("models.datetime")
    def test_expired_past_deadline(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2026, 6, 1)
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        task = Task(1, "overdue task", "desc", "2026-01-01T00:00:00")
        self.assertEqual(task.display_status(), "expired")

    def test_invalid_deadline_string(self):
        task = Task(1, "bad deadline", "desc", "not-a-date")
        self.assertEqual(task.display_status(), "invalid deadline")


class TestAddTask(unittest.TestCase):
    def test_next_id_increments(self):
        tasks = []
        t1, next_id = add_task(tasks, 1, "first", "desc", "2026-08-01T00:00:00")
        self.assertEqual(t1.id, 1)
        self.assertEqual(next_id, 2)
        t2, next_id = add_task(tasks, next_id, "second", "desc", "2026-08-01T00:00:00")
        self.assertEqual(t2.id, 2)
        self.assertEqual(next_id, 3)

    def test_id_not_reused_after_deletion(self):
        tasks = []
        t1, next_id = add_task(tasks, 1, "first", "desc", "2026-08-01T00:00:00")
        delete_task(tasks, t1.id)
        t2, next_id = add_task(tasks, next_id, "second", "desc", "2026-08-01T00:00:00")
        self.assertEqual(t2.id, 2)  # not 1, even though ID 1 is free


class TestUpdateTask(unittest.TestCase):
    def setUp(self):
        self.tasks = []
        self.task, self.next_id = add_task(self.tasks, 1, "original", "desc", "2026-08-01T00:00:00")

    def test_partial_update_only_changes_given_field(self):
        update_task(self.tasks, self.task.id, name="renamed")
        self.assertEqual(self.task.name, "renamed")
        self.assertEqual(self.task.description, "desc")

    def test_nonexistent_id_returns_false_and_touches_nothing(self):
        result = update_task(self.tasks, 999, name="ghost")
        self.assertFalse(result)
        self.assertEqual(self.task.name, "original")

    def test_invalid_status_is_rejected(self):
        update_task(self.tasks, self.task.id, status="expired")
        self.assertEqual(self.task.status, "pending")

    def test_valid_status_is_applied(self):
        update_task(self.tasks, self.task.id, status="done")
        self.assertEqual(self.task.status, "done")


class TestDeleteTask(unittest.TestCase):
    def test_delete_existing(self):
        tasks = []
        t, _ = add_task(tasks, 1, "to delete", "desc", "2026-08-01T00:00:00")
        self.assertTrue(delete_task(tasks, t.id))
        self.assertEqual(len(tasks), 0)

    def test_delete_nonexistent_returns_false(self):
        tasks = []
        add_task(tasks, 1, "keep me", "desc", "2026-08-01T00:00:00")
        self.assertFalse(delete_task(tasks, 999))
        self.assertEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()