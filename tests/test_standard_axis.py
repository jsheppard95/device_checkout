import logging
import pytest
import time

from pcdsdevices.epics_motor import IMS

logger = logging.getLogger(__name__)

###########################################################################
# Example fixture to stop for user interaction
#@pytest.fixture(scope="function")
#def disconnect_component(pytestconfig):
#    # Some pytest magic
#    # Stops a test for user interraction
#    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')
#
#    capmanager.suspend_global_capture(in_=True)
#    input('\nDisconnect component, then press enter\n')
#    capmanager.resume_global_capture()
#
#    yield  # At this point all the tests with this fixture are run
#
#    capmanager.suspend_global_capture(in_=True)
#    input('\nConnect component again, then press enter\n')
#    capmanager.resume_global_capture()
###########################################################################


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

#def capture(pytestconfig, msg)

@pytest.fixture(scope='function')
def motor():
    m = IMS('XCS:USR:MMS:17', name='xcs_usr_mms_17')
    return m


def test_that_passes():
    assert True


def test_that_fails():
    assert False


def test_basic_motion(motor):
    m = motor
    curr_pos = m.user_readback.get()
    start_time = m.user_readback.timestamp
    # Move in positive direction
    desired_pos = curr_pos + 1.0  # Not a good way to do things - units??
    m.mvr(1.0, wait=True)
    end_time = m.user_readback.timestamp
    assert m.user_readback.get() == desired_pos
    dt_pos_move = end_time - start_time
    logger.debug('Time for +1 mm move: %s' % dt_pos_move)
    # Move in negative direction
    curr_pos = m.user_readback.get()
    start_time = m.user_readback.timestamp
    desired_pos = curr_pos - 1.0
    m.mvr(-1.0, wait=True)
    end_time = m.user_readback.get()
    assert m.user_readback.get() == desired_pos
    dt_neg_move = end_time - start_time
    logger.debug('Time for -1 mm move: %s' % dt_neg_move)


def test_high_limit_switch_activation(motor, activate_hls):
    m = motor
    # have components 'm.low_limit_switch' and 'm.high_limit_switch'
    # User activates low limit switch
    assert m.high_limit_switch.get() == 1


def test_low_limit_switch_activation(motor, activate_lls):
    m = motor
    assert m.low_limit_switch.get() == 1


#def test_soft_limits(motor):
#    # Move motor between high and low limit switches - make sure meets
#    # motion range requirements
#    m = motor
#    limits = m.limits  # tuple: (low_lim, high_lim)
#    # NOTE: Above are soft limits - might not be set up correctly
#    # Move to low limit
#    m.mv(limits[0])
#    time.sleep(5.0)
#    assert m.user_readback.get() == limits[0]
#    # Move to high limit
#    m.mv(limits[1])
#    time.sleep(5.0)
#    assert m.user_readback.get() == limits[1]
    # NOTE: not quite the right approach, really want to jog motor until the
    # limit switch is activated, then check the position and ensure the full
    # range is accurate


def test_full_motion_range(motor):
    # Here we want to move the motor from low limit to high limit and
    # record the position of each, then compare to specified full motion
    # range
    time.sleep(1.0)
    m = motor
    # Move to low limit switch, record position:
    lls_activated = m.low_limit_switch.get()
    try:
        while not lls_activated:
            m.mvr(-0.5, wait=True)
            lls_activated = m.low_limit_switch.get()
    except:
        lls_pos = m.user_readback.get()
    logger.debug('LLS value: %s' % lls_pos)
    # Now do same for high limit switch:
    hls_activated = m.high_limit_switch.get()
    try:
        while not hls_activated:
            m.mvr(0.5, wait=True)
            hls_activated = m.high_limit_switch.get()
    except:
        hls_pos = m.user_readback.get()
    logger.debug('HLS value: %s' % hls_pos)
    full_range = hls_pos - lls_pos
    logger.debug('Full range of motion: %s' % full_range)
    return full_range




