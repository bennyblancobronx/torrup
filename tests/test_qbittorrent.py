"""Tests for qBitTorrent integration."""

import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

from src.utils.qbittorrent import (
    add_to_qbt,
    get_qbt_client,
)

class TestQBitTorrentUtils(unittest.TestCase):

    @patch("src.utils.qbittorrent.get_setting")
    @patch("src.utils.qbittorrent.qbittorrentapi.Client")
    def test_get_qbt_client_returns_client_when_enabled(self, mock_client_cls, mock_get_setting):
        """Test that client is created and logged in when enabled."""
        # Setup settings
        settings = {
            "qbt_enabled": "1",
            "qbt_url": "localhost:8080",
            "qbt_user": "admin",
            "qbt_pass": "adminadmin"
        }
        mock_get_setting.side_effect = lambda conn, key: settings.get(key)

        # Setup mock client
        mock_instance = MagicMock()
        mock_client_cls.return_value = mock_instance

        # Execute
        client = get_qbt_client()

        # Verify
        self.assertIsNotNone(client)
        mock_client_cls.assert_called_with(
            host="http://localhost:8080",
            username="admin",
            password="adminadmin",
            REQUESTS_ARGS={'timeout': (3.1, 10)}
        )
        mock_instance.auth_log_in.assert_called_once()

    @patch("src.utils.qbittorrent.get_setting")
    def test_get_qbt_client_returns_none_when_disabled(self, mock_get_setting):
        """Test that None is returned when qbt is disabled."""
        mock_get_setting.side_effect = lambda conn, key: "0" if key == "qbt_enabled" else ""

        client = get_qbt_client()

        self.assertIsNone(client)

    @patch("src.utils.qbittorrent.get_setting")
    @patch("src.utils.qbittorrent.qbittorrentapi.Client")
    def test_get_qbt_client_handles_exception(self, mock_client_cls, mock_get_setting):
        """Test that None is returned on connection error."""
        settings = {"qbt_enabled": "1"}
        mock_get_setting.side_effect = lambda conn, key: settings.get(key)

        # Mock exception
        mock_client_cls.side_effect = Exception("Connection failed")

        client = get_qbt_client()

        self.assertIsNone(client)

    @patch("src.utils.qbittorrent.get_qbt_client")
    @patch("builtins.open", new_callable=mock_open, read_data=b"torrent_data")
    @patch("src.utils.qbittorrent.Path")
    def test_add_to_qbt_success(self, mock_path, mock_file, mock_get_client):
        """Test successful torrent addition."""
        # Setup mocks
        mock_client = MagicMock()
        mock_client.torrents_add.return_value = "Ok."
        mock_get_client.return_value = mock_client

        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = True
        mock_path_obj.name = "test.torrent"
        mock_path_obj.parent = Path("/downloads")
        mock_path.return_value = mock_path_obj

        # Execute
        result = add_to_qbt("/tmp/test.torrent", "/downloads/movie.mkv", category="movies")

        # Verify
        self.assertTrue(result)
        mock_client.torrents_add.assert_called()
        args, kwargs = mock_client.torrents_add.call_args
        self.assertEqual(kwargs['category'], "movies")
        self.assertEqual(kwargs['tags'], "torrup")

    @patch("src.utils.qbittorrent.get_qbt_client")
    def test_add_to_qbt_no_client(self, mock_get_client):
        """Test add_to_qbt fails gracefully if client is None."""
        mock_get_client.return_value = None
        result = add_to_qbt("path", "path")
        self.assertFalse(result)

    @patch("src.utils.qbittorrent.get_qbt_client")
    @patch("src.utils.qbittorrent.Path")
    def test_add_to_qbt_file_not_found(self, mock_path, mock_get_client):
        """Test add_to_qbt fails if torrent file is missing."""
        mock_get_client.return_value = MagicMock()
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False
        mock_path.return_value = mock_path_obj

        result = add_to_qbt("missing.torrent", "savepath")
        self.assertFalse(result)
