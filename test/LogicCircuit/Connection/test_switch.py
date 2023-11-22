from unittest import mock

import pytest

from Computer.LogicCircuit.Connection import (Connection, ConnectionError,
                                              Switch, SwitchError)


@pytest.fixture
def sample_switch():
    switch = Switch()
    switch._input_connections = [Connection(), Connection()]
    switch._output_connection = Connection()
    return switch


def test_switch_init():
    switch = Switch()
    assert len(switch._input_connections) == 2
    assert all(conn is None for conn in switch._input_connections)
    assert switch._output_connection is None


def test_switch_feed_error_inputs_not_set():
    switch = Switch()
    with pytest.raises(SwitchError) as exc:
        switch.feed()

    assert exc.value.args[0] == "The input connections have not all been set!"


@mock.patch.object(Connection, "feed")
def test_switch_feed_error_bad_connections(mock_feed, sample_switch):
    mock_feed.side_effect = ConnectionError()
    with pytest.raises(SwitchError) as exc:
        sample_switch.feed()

    assert exc.value.args[0] == "It looks like nothing is connected!"


@mock.patch.object(Connection, "feed")
def test_switch_feed_get_first(mock_feed, sample_switch):
    mock_feed.side_effect = [0, ConnectionError()]
    assert sample_switch.feed() == 0


@mock.patch.object(Connection, "feed")
def test_switch_feed_get_second(mock_feed, sample_switch):
    mock_feed.side_effect = [ConnectionError(), 1]
    assert sample_switch.feed() == 1


def test_switch_has_input_connection_set_error_bad_index(sample_switch):
    with pytest.raises(SwitchError) as exc:
        sample_switch.has_input_connection_set(index=3)

    assert exc.value.args[0] == "You entered an unknown connection: 3!"


def test_switch_has_input_connection(sample_switch):
    empty_switch = Switch()
    for conn in range(2):
        assert not empty_switch.has_input_connection_set(index=conn)
        assert sample_switch.has_input_connection_set(index=conn)


def test_switch_has_output_connection(sample_switch):
    empty_switch = Switch()
    assert not empty_switch.has_output_connection_set()
    assert sample_switch.has_output_connection_set()


def test_switch_reset(sample_switch):
    assert all(conn is not None for conn in sample_switch._input_connections)
    assert sample_switch._output_connection is not None
    sample_switch.reset()
    assert all(conn is None for conn in sample_switch._input_connections)
    assert sample_switch._output_connection is None


def test_switch_set_input_connection_error_already_connected(sample_switch):
    with pytest.raises(SwitchError) as exc:
        sample_switch.set_input_connection(conn=Connection(), index=0)

    assert exc.value.args[0] == "Input connection 0 has already been connected!"


def test_switch_set_input_connection():
    switch = Switch()
    switch.set_input_connection(conn=Connection(), index=0)
    assert switch._input_connections[0] is not None


def test_switch_set_output_connection_error_already_connected(sample_switch):
    with pytest.raises(SwitchError) as exc:
        sample_switch.set_output_connection(conn=Connection())

    assert exc.value.args[0] == "The output connection has already been connected!"


def test_switch_set_output_connection():
    switch = Switch()
    switch.set_output_connection(conn=Connection())
    assert switch._output_connection is not None
