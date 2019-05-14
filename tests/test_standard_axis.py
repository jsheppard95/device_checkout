import logging
import pytest
import time

from pcdsdevices.epics_motor import EpicsMotor

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
    m = EpicsMotor('XCS:USR:MMS:17', name='xcs_usr_mms_17')
    return m


#def test_that_passes(disconnect_component):
#    assert True


#def test_that_fails(disconnect_component):
#    assert False


# Current issue:
# Using EpicsMotor can read/write to each of the components but cannot use
# basic functions available in xcspython

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


def test_full_range_of_motion(motor):
    # Move motor between high and low limit switches - make sure meets
    # motion range requirements
    pass
