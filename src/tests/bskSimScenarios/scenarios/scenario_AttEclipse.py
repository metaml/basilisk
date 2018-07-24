''' '''
'''
 ISC License

 Copyright (c) 2016-2018, Autonomous Vehicle Systems Lab, University of Colorado at Boulder

 Permission to use, copy, modify, and/or distribute this software for any
 purpose with or without fee is hereby granted, provided that the above
 copyright notice and this permission notice appear in all copies.

 THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''
## \defgroup Tutorials_6_1
## @{
# Demonstrates how to use sun safe pointing in conjunction with the Eclipse, RW, CSS Weighted Least Squares Estimator, and
# CSS modules to provide attitude guidance as the spacecraft passes through an eclipse while orbiting the Earth.
#
# Sun Safe Pointing Attitude Guidance Simulation with Eclipse Module {#scenario_AttitudeEclipse}
# ====
#
# Scenario Description
# -----
# This script sets up a 6-DOF spacecraft which is orbiting the Earth.  The goal of the scenario is to
# illustrate 1) how IMU sensors can be added to the simulation, 2) how to add the eclipse module
# to simulate shadows being cast over a CSS constellation, and 3) how to use these added modules to make use of
# sun safe pointing as a flight software algorithm to control RWs.
#
# To run the default scenario, call the python script from a Terminal window through
#
#       python scenario_AttitudeEclipse.py
#
# The simulation layout is shown in the following illustration.  Two simulation processes are created: one
# which contains dynamics modules, and one that contains the Flight Software (FSW) algorithm
# modules. Instructions on how to configure seperate processes can be found in
# [scenarioAttitudeFeedback2T.py](@ref scenarioAttitudeFeedback2T).
# ![Simulation Flow Diagram](Images/doc/scenario_AttEclipse.svg "Illustration")
#
# When the simulation completes several plots are shown for the eclipse shadow factor, the sun direction vector,
# attitude error, RW motor torque, and RW speed.
#
#
# ### Setup Changes for Spacecraft Dynamics
#
# The fundamental simulation setup is a combination of the setups used in
# [scenarioAttitudeFeedback.py](@ref scenarioAttitudeFeedback) and [scenarioCSS.py](@ref scenarioCSS).
# The dynamics simulation is setup using a SpacecraftPlus() module to which an Earth gravity
# effector is attached. In addition a CSS constellation and RW pyramid are attached.
#
# The new element is adding the IMU sensor to the spacecraft, and the eclipse module to the simulation environment.
# The specific code required to build the IMU sensor is:
# ~~~~~~~~~~~~~{.py}
#     imuObject = imu_sensor.ImuSensor()
#     imuObject.InputStateMsg = self.scObject.scStateOutMsgName
#     imuObject.OutputDataMsg = "imu_sensor_output"
# ~~~~~~~~~~~~~
# and the code required to attach it to the simulation is:
# ~~~~~~~~~~~~~{.py}
#     SimBase.AddModelToTask(self.taskName, self.imuObject, None, 205)
# ~~~~~~~~~~~~~
#
# To configure the eclipse module, use the following code:
# ~~~~~~~~~~~~~{.py}
#         self.eclipseObject.sunInMsgName = 'sun_planet_data'
#         self.eclipseObject.addPlanetName('earth')
#         self.eclipseObject.addPlanetName('moon')
#         self.eclipseObject.addPositionMsgName(self.scObject.scStateOutMsgName)
# ~~~~~~~~~~~~~
# To attach the module to the simulation use:
# ~~~~~~~~~~~~~{.py}
#     SimBase.AddModelToTask(self.taskName, self.eclipseObject, None, 204)
# ~~~~~~~~~~~~~
# The module requires spice data regarding the location of the sun, the planets to be monitored for shadow-casting
# effects, and the location of the spacecraft. In combination these inputs can produce an output that is attached to the
# CSS constellation which simulates a shadow. The eclipse object output is called using:
#
#         eclipse_data_0
#
# which gets sent to the individual CSS sensors.
#
#
# ### Flight Algorithm Changes to Configure Sun Safe Pointing Guidance
#
# The general flight algorithm setup is different than the earlier simulation scripts. Here we
# use the sunSafePoint() guidance module, the CSSWlsEst() module to evaluate the
# sun pointing vector, and the MRP_Feedback() module to provide the desired \f${\mathbf L}_r\f$
# control torque vector.
#
# The sunSafePoint() guidance module is used to steer the spacecraft to point towards the sun direction vector.
# This is used for functionality like safe mode, or a power generation mode. The inputs of the module are the
# sun direction vector (as provided by the CSSWlsEst module), as well as the body rate information (as provided by the
#  IMU). The guidance module can be configured using:
# ~~~~~~~~~~~~~{.py}
# self.sunSafePointData = sunSafePoint.sunSafePointConfig()
# self.sunSafePointWrap = SimBase.setModelDataWrap(self.sunSafePointData)
# self.sunSafePointWrap.ModelTag = "sunSafePoint"
# self.sunSafePointData.attGuidanceOutMsgName = "guidanceOut"
# self.sunSafePointData.imuInMsgName = SimBase.DynModels.imuObject.OutputDataMsg
# self.sunSafePointData.sunDirectionInMsgName = self.cssWlsEstData.navStateOutMsgName
# self.sunSafePointData.sHatBdyCmd = [1.0, 0.0, 0.0]
# ~~~~~~~~~~~~~
# The sHatBdyCmd defines the desired body pointing vector that will align with the sun direction vector.
# The sun direction vector itself is calculated through the use of a CSS constellation and the CSSWlsEst module. The
# setup for the CSS constellation can be found in the [scenarioCSS.py](@ref scenarioCSS) scenario. The CSSWlsEst module
# is a weighted least-squares minimum-norm algorithm used to estimate the body-relative sun heading using a cluster of
# coarse sun sensors. The algorithm requires a minimum of three CSS to operate correctly.
#
# To use the weighted least-squares estimator use the following code:
# ~~~~~~~~~~~~~{.py}
#         self.cssWlsEstData.cssDataInMsgName = SimBase.DynModels.CSSConstellationObject.outputConstellationMessage
#         self.cssWlsEstData.cssConfigInMsgName = "css_config_data"
#         self.cssWlsEstData.navStateOutMsgName = "sun_point_data"
# ~~~~~~~~~~~~~
# The resulting simulation illustrations are shown below.
# ![Eclipse Shadow Factor](Images/Scenarios/scenario_AttEclipse_shadowFraction.svg "Eclipse Shadow Factor")
# This plot illustrates the shadow fraction calculated by the CSS as the spacecraft orbits Earth and passes through
# the Earth's shadow. 0.0 corresponds with total eclipse and 1.0 corresponds with direct sunlight.
# ![Sun Direction Vector](Images/Scenarios/scenario_AttEclipse_sunDirectionVector.svg "Sun Direction Vector")
# The CSSWlsEst module calculates the position of the sun based on input from the CSS. The corresponding vector's three
# components are plotted. When the spacecraft passes through the eclipse, it sets the sun direction vector to
#  [0.0,0.0,0.0].
# ![Attitude Error Norm](Images/Scenarios/scenario_AttEclipse_attitudeErrorNorm.svg "Attitude Error Norm")
# The spacecraft does not change attitude if no sun direction vector is detected. Once the CSS rediscovers the sun upon
# exiting the eclipse, the spacecraft corrects and realigns with the sun direction vector.
# ![Rate Tracking Error](Images/Scenarios/scenario_AttEclipse_rateError.svg "Rate Tracking Error")
# ![RW Motor Torque](Images/Scenarios/scenario_AttEclipse_rwMotorTorque.svg "RW Motor Torque [Nm]")
# ![RW Speed](Images/Scenarios/scenario_AttEclipse_rwSpeed.svg "RW Speed [RPM]")
#
#
## @}


# Import utilities
from Basilisk.utilities import orbitalMotion, macros, unitTestSupport

# Get current file path
import sys, os, inspect
import matplotlib as plt

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

# Import master classes: simulation base class and scenario base class
sys.path.append(path + '/..')
from BSK_masters import BSKSim, BSKScenario

# Import plotting file for your scenario
sys.path.append(path + '/../plotting')
import BSK_Plotting as BSK_plt

sys.path.append(path + '/../../scenarios')

# Create your own scenario child class
class scenario_AttitudeEclipse(BSKScenario):
    def __init__(self, masterSim):
        super(scenario_AttitudeEclipse, self).__init__(masterSim)
        self.name = 'scenario_AttitudeEclipse'
        self.masterSim = masterSim

    def configure_initial_conditions(self):
        print '%s: configure_initial_conditions' % self.name
        # Configure FSW mode
        self.masterSim.modeRequest = 'sunSafePoint'

        # Configure Dynamics initial conditions

        oe = orbitalMotion.ClassicElements()
        oe.a = 7000000.0  # meters
        oe.e = 0.0
        oe.i = 33.3 * macros.D2R
        oe.Omega = 48.2 * macros.D2R
        oe.omega = 347.8 * macros.D2R
        oe.f = 85.3 * macros.D2R
        mu = self.masterSim.DynModels.gravFactory.gravBodies['earth'].mu
        rN, vN = orbitalMotion.elem2rv(mu, oe)
        orbitalMotion.rv2elem(mu, rN, vN)
        self.masterSim.DynModels.scObject.hub.r_CN_NInit = unitTestSupport.np2EigenVectorXd(rN)  # m   - r_CN_N
        self.masterSim.DynModels.scObject.hub.v_CN_NInit = unitTestSupport.np2EigenVectorXd(vN)  # m/s - v_CN_N
        self.masterSim.DynModels.scObject.hub.sigma_BNInit = [[0.1], [0.2], [-0.3]]  # sigma_BN_B
        self.masterSim.DynModels.scObject.hub.omega_BN_BInit = [[0.001], [-0.01], [0.03]]  # rad/s - omega_BN_B


    def log_outputs(self):
        print '%s: log_outputs' % self.name
        samplingTime = self.masterSim.DynModels.processTasksTimeStep

        # Dynamics process outputs: log messages below if desired.
        self.masterSim.TotalSim.logThisMessage(self.masterSim.DynModels.scObject.scStateOutMsgName, samplingTime)
        self.masterSim.TotalSim.logThisMessage("eclipse_data_0", samplingTime)

        # FSW process outputs
        self.masterSim.TotalSim.logThisMessage(self.masterSim.FSWModels.mrpFeedbackRWsData.inputRWSpeedsName, samplingTime)
        self.masterSim.TotalSim.logThisMessage(self.masterSim.FSWModels.rwMotorTorqueData.outputDataName, samplingTime)
        self.masterSim.TotalSim.logThisMessage(self.masterSim.FSWModels.trackingErrorData.outputDataName, samplingTime)
        self.masterSim.TotalSim.logThisMessage(self.masterSim.FSWModels.sunSafePointData.sunDirectionInMsgName, samplingTime)
        return

    def pull_outputs(self, showPlots):
        print '%s: pull_outputs' % self.name
        num_RW = 4 # number of wheels used in the scenario

        # Dynamics process outputs: pull log messages below if any
        r_BN_N = self.masterSim.pullMessageLogData(self.masterSim.DynModels.scObject.scStateOutMsgName + ".r_BN_N", range(3))
        shadowFactor = self.masterSim.pullMessageLogData("eclipse_data_0.shadowFactor")

        # FSW process outputs
        dataUsReq = self.masterSim.pullMessageLogData(
            self.masterSim.FSWModels.rwMotorTorqueData.outputDataName + ".motorTorque", range(num_RW))
        sigma_BR = self.masterSim.pullMessageLogData(
            self.masterSim.FSWModels.trackingErrorData.outputDataName + ".sigma_BR", range(3))
        omega_BR_B = self.masterSim.pullMessageLogData(
            self.masterSim.FSWModels.trackingErrorData.outputDataName + ".omega_BR_B", range(3))
        RW_speeds = self.masterSim.pullMessageLogData(
            self.masterSim.FSWModels.mrpFeedbackRWsData.inputRWSpeedsName + ".wheelSpeeds", range(num_RW))
        sunPoint = self.masterSim.pullMessageLogData(
            self.masterSim.FSWModels.sunSafePointData.sunDirectionInMsgName + ".vehSunPntBdy", range(3))

        # Plot results
        timeData = dataUsReq[:, 0] * macros.NANO2MIN
        BSK_plt.plot_attitude_error(timeData, sigma_BR)
        BSK_plt.plot_rw_cmd_torque(timeData, dataUsReq, num_RW)
        BSK_plt.plot_rate_error(timeData, omega_BR_B)
        BSK_plt.plot_rw_speeds(timeData, RW_speeds, num_RW)

        BSK_plt.plot_shadow_fraction(timeData, shadowFactor)
        BSK_plt.plot_sun_point(timeData, sunPoint)

        figureList = {}
        if showPlots:
            BSK_plt.show_all_plots()
        else:
            fileName = os.path.basename(os.path.splitext(__file__)[0])
            figureNames = ["attitudeErrorNorm", "rwMotorTorque", "rateError", "rwSpeed", "shadowFraction", "sunDirectionVector"]
            figureList = BSK_plt.save_all_plots(fileName, figureNames)

        return figureList



def run(showPlots):
    # Instantiate base simulation

    TheBSKSim = BSKSim()

    # Configure an scenario in the base simulation
    TheScenario = scenario_AttitudeEclipse(TheBSKSim)
    TheScenario.log_outputs()
    TheScenario.configure_initial_conditions()

    # Initialize simulation
    TheBSKSim.InitializeSimulationAndDiscover()

    # Configure run time and execute simulation
    simulationTime = macros.min2nano(60.0)
    TheBSKSim.ConfigureStopTime(simulationTime)
    print 'Starting Execution'
    TheBSKSim.ExecuteSimulation()
    print 'Finished Execution. Post-processing results'

    # Pull the results of the base simulation running the chosen scenario
    figureList = TheScenario.pull_outputs(showPlots)

    return figureList





if __name__ == "__main__":
    run(True)