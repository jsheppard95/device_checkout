import logging
import pytest
import time

from pcdsdevices.epics_motor import IMS

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def disconnect_component(pytestconfig):
    # Some pytest magic
    # Stops a test for user interraction
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

    capmanager.suspend_global_capture(in_=True)
    input('\nDisconnect component, then press enter\n')
    capmanager.resume_global_capture()

    yield  # At this point all the tests with this fixture are run

    capmanager.suspend_global_capture(in_=True)
    input('\nConnect component again, then press enter\n')
    capmanager.resume_global_capture()


@pytest.fixture(scope="function")
def activate_hls(pytestconfig):
    # Some pytest magic
    # Stops a test for user interraction
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

    capmanager.suspend_global_capture(in_=True)
    input('\nActivate HLS, then press enter\n')
    capmanager.resume_global_capture()

    yield  # At this point all the tests with this fixture are run


@pytest.fixture(scope="function")
def activate_lls(pytestconfig):
    # Some pytest magic
    # Stops a test for user interraction
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')

    capmanager.suspend_global_capture(in_=True)
    input('\nActivate LLS, then press enter\n')
    capmanager.resume_global_capture()

    yield  # At this point all the tests with this fixture are run


@pytest.fixture(scope='function')
def motor():
    m = IMS('XCS:USR:MMS:17', name='xcs_usr_mms_17')
    return m


#def test_that_passes(disconnect_component):
#    assert True


#def test_that_fails(disconnect_component):
#    assert False


def test_basic_motion(motor):
    m = motor
    curr_pos = m.user_readback.get()
    # Move in positive direction
    desired_pos = curr_pos + 1.0  # Not a good way to do things - units??
    m.user_setpoint.put(desired_pos)
    time.sleep(3.0)
    assert m.user_readback.get() == desired_pos
    # Move in negative direction
    curr_pos = m.user_readback.get()
    desired_pos = curr_pos - 1.0
    m.user_setpoint.put(desired_pos)
    time.sleep(3.0)
    assert m.user_readback.get() == desired_pos


def test_high_limit_switch_activation(motor, activate_hls):
    m = motor
    # have components 'm.low_limit_switch' and 'm.high_limit_switch'
    # User activates low limit switch
    assert m.high_limit_switch.get() == 1


def test_low_limit_switch_activation(motor, activate_lls):
    m = motor
    assert m.low_limit_switch.get() == 1


def test_soft_limits(motor):
    # Move motor between high and low limit switches - make sure meets
    # motion range requirements
    m = motor
    limits = m.limits  # tuple: (low_lim, high_lim)
    # NOTE: Above are soft limits - might not be set up correctly
    # Move to low limit
    m.mv(limits[0])
    time.sleep(5.0)
    assert m.user_readback.get() == limits[0]
    # Move to high limit
    m.mv(limits[1])
    time.sleep(5.0)
    assert m.user_readback.get() == limits[1]
    # NOTE: not quite the right approach, really want to jog motor until the
    # limit switch is activated, then check the position and ensure the full
    # range is accurate


def test_full_motion_range(motor):
    m = motor
